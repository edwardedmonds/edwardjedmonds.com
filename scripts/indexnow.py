#!/usr/bin/env python3
"""Prepare an IndexNow change list before deployment; submit it after deployment."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

from check_metadata import Page

ENDPOINT = "https://api.indexnow.org/indexnow"
MANIFEST = "indexnow-manifest.json"
USER_AGENT = "EdwardEdmonds-IndexNow/1.0 (+https://edwardjedmonds.com/)"


def read_config(path):
    config = json.loads(path.read_text())
    origin = urlsplit(config["site"])
    if origin.scheme != "https" or origin.path != "/" or origin.query or origin.fragment:
        raise ValueError("Site must be an HTTPS root URL")
    if not re.fullmatch(r"[A-Za-z0-9-]{8,128}", config["key"]):
        raise ValueError("Invalid IndexNow key")
    return config


def validate_url(url, site):
    parts = urlsplit(url)
    if (parts.scheme, parts.netloc) != ("https", urlsplit(site).netloc):
        raise ValueError(f"URL outside the configured site: {url}")
    if parts.query or parts.fragment or ".." in unquote(parts.path).split("/"):
        raise ValueError(f"Not a canonical page URL: {url}")
    return parts


def fingerprint(html):
    page = Page(html)
    if "noindex" in page.value("robots") or "refresh" in page.meta:
        raise ValueError("Sitemap contains an excluded page")
    main = re.search(r"<main\b[^>]*>(.*?)</main>", html, re.S)
    if not main:
        raise ValueError("Missing main content")
    # Exclude stylesheet/script fingerprints and the site's annual footer date.
    metadata = {key: value for key, value in page.meta.items()
                if key in ("description", "author", "robots")
                or key.startswith(("og:", "twitter:", "article:"))}
    data = {"title": page.title, "meta": metadata, "schema": page.schema,
            "main": re.sub(r"\s+", " ", main[1]).strip()}
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def build_manifest(root, site):
    pages = {}
    for node in ET.parse(root / "sitemap.xml").getroot():
        url = node.findtext("{*}loc")
        parts = validate_url(url, site)
        path = root / unquote(parts.path).lstrip("/")
        if parts.path.endswith("/"):
            path /= "index.html"
        html = path.read_text()
        canonical = [x.get("href") for x in Page(html).links if x.get("rel") == "canonical"]
        if canonical != [url]:
            raise ValueError(f"Sitemap and canonical disagree: {url}")
        pages[url] = fingerprint(html)
    if not pages:
        raise ValueError("Refusing to prepare an empty site")
    return {"version": 1, "pages": pages}


def validate_manifest(manifest, site):
    if manifest.get("version") != 1 or not isinstance(manifest.get("pages"), dict):
        raise ValueError("Unsupported deployment manifest")
    for url, digest in manifest["pages"].items():
        validate_url(url, site)
        if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
            raise ValueError("Invalid page fingerprint")
    return manifest


def changed_urls(previous, current):
    old, new = previous["pages"], current["pages"]
    return sorted(url for url in old.keys() | new.keys() if old.get(url) != new.get(url))


def request(url, data=None):
    headers = {"User-Agent": USER_AGENT, "Cache-Control": "no-cache"}
    if data is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
    req = Request(url, data=data, headers=headers)
    for attempt in range(3):
        try:
            with urlopen(req, timeout=20) as response:
                return response.status, response.read()
        except HTTPError as exc:
            exc.close()
            if (exc.code != 429 and exc.code < 500) or attempt == 2:
                raise
        except (URLError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(5 * (attempt + 1))


def prepare(root, plan_path, config):
    current = build_manifest(root, config["site"])
    key_path = root / (config["key"] + ".txt")
    if key_path.read_text().strip() != config["key"]:
        raise ValueError("Published key file does not match configuration")
    try:
        _, body = request(config["site"] + MANIFEST)
        previous = validate_manifest(json.loads(body), config["site"])
    except HTTPError as exc:
        exc.close()
        if exc.code != 404:
            raise
        previous = {"version": 1, "pages": {}}
        print("First IndexNow deployment: submitting the public sitemap pages.")
    urls = changed_urls(previous, current)
    (root / MANIFEST).write_text(json.dumps(current, sort_keys=True, indent=2) + "\n")
    plan_path.write_text(json.dumps({"manifest": current, "urls": urls}, indent=2) + "\n")
    print(f"IndexNow prepared {len(urls)} added, changed, or removed URLs.")


def confirm_deployment(config, expected):
    # The new manifest and key must be live before any change is announced.
    for attempt in range(6):
        try:
            _, body = request(config["site"] + MANIFEST)
            _, key = request(config["site"] + config["key"] + ".txt")
            if json.loads(body) == expected and key.decode().strip() == config["key"]:
                return
        except (HTTPError, URLError, TimeoutError, ValueError):
            pass
        if attempt < 5:
            time.sleep(10)
    raise RuntimeError("Live site does not yet match this deployment; no URLs submitted")


def submit(plan_path, config):
    plan = json.loads(plan_path.read_text())
    validate_manifest(plan["manifest"], config["site"])
    urls = sorted(set(plan["urls"]))
    for url in urls:
        validate_url(url, config["site"])
    if not urls:
        print("IndexNow: no changed public pages; nothing submitted.")
        return
    confirm_deployment(config, plan["manifest"])
    for offset in range(0, len(urls), 10000):
        batch = urls[offset:offset + 10000]
        payload = {"host": urlsplit(config["site"]).netloc, "key": config["key"],
                   "keyLocation": config["site"] + config["key"] + ".txt", "urlList": batch}
        status, _ = request(ENDPOINT, json.dumps(payload).encode())
        if status not in (200, 202):
            raise RuntimeError(f"Unexpected IndexNow response: HTTP {status}")
        note = "accepted" if status == 200 else "received; key validation pending"
        print(f"IndexNow: {len(batch)} URLs {note} (HTTP {status}). This does not confirm indexing.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "submit"))
    parser.add_argument("--site-dir", type=Path, default=Path("public"))
    parser.add_argument("--plan", type=Path, default=Path("indexnow-plan.json"))
    parser.add_argument("--config", type=Path, default=Path("indexnow.json"))
    args = parser.parse_args()
    config = read_config(args.config)
    if args.command == "prepare":
        prepare(args.site_dir, args.plan, config)
    else:
        submit(args.plan, config)
