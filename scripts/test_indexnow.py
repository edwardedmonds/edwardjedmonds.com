import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from indexnow import (build_manifest, changed_urls, confirm_deployment, fingerprint,
                      prepare, request, submit, validate_manifest)

SITE = 'https://edwardjedmonds.com/'
CONFIG = {'site': SITE, 'key': '12345678abcdef12'}


def html(text='An essay', robots='index, follow', css='one.css'):
    return (f'<html><head><title>Essay</title><meta name="robots" content="{robots}">'
            f'<meta name="description" content="Evidence"><link rel="canonical" href="{SITE}">'
            f'<link rel="stylesheet" href="/{css}"></head><body><main><h1>{text}</h1></main>'
            '<footer>2026</footer></body></html>')


class IndexNowTests(unittest.TestCase):
    def test_new_updated_deleted_and_unchanged_pages(self):
        old = {'pages': {SITE+'old/': 'a', SITE+'same/': 'b', SITE+'edit/': 'c'}}
        new = {'pages': {SITE+'new/': 'd', SITE+'same/': 'b', SITE+'edit/': 'e'}}
        self.assertEqual(changed_urls(old, new), [SITE+'edit/', SITE+'new/', SITE+'old/'])
        self.assertEqual(changed_urls(new, new), [])

    def test_content_and_metadata_count_but_css_and_footer_do_not(self):
        initial = fingerprint(html())
        self.assertNotEqual(initial, fingerprint(html('New evidence')))
        self.assertNotEqual(initial, fingerprint(html().replace('content="Evidence"', 'content="Revised"')))
        self.assertEqual(initial, fingerprint(html(css='two.css')))
        self.assertEqual(initial, fingerprint(html().replace('2026', '2027')))

    def test_only_sitemap_pages_are_selected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'sitemap.xml').write_text(f'<urlset><url><loc>{SITE}</loc></url></urlset>')
            (root/'index.html').write_text(html())
            (root/'private.html').write_text('not for submission')
            self.assertEqual(list(build_manifest(root, SITE)['pages']), [SITE])
            (root/'index.html').write_text(html(robots='noindex, follow'))
            with self.assertRaises(ValueError):
                build_manifest(root, SITE)

    def test_reject_foreign_and_traversal_urls(self):
        for url in ['https://elsewhere.example/', SITE+'%2e%2e/private/', SITE+'?draft=true']:
            with self.assertRaises(ValueError):
                validate_manifest({'version': 1, 'pages': {url: 'a'*64}}, SITE)

    def test_first_deployment_bootstrap_and_next_unchanged_plan(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'sitemap.xml').write_text(f'<urlset><url><loc>{SITE}</loc></url></urlset>')
            (root/'index.html').write_text(html())
            (root/(CONFIG['key']+'.txt')).write_text(CONFIG['key'])
            plan = root/'plan.json'
            missing = HTTPError(SITE, 404, 'Not found', {}, None)
            with patch('indexnow.request', side_effect=missing):
                prepare(root, plan, CONFIG)
            self.assertEqual(json.loads(plan.read_text())['urls'], [SITE])
            previous = (root/'indexnow-manifest.json').read_bytes()
            with patch('indexnow.request', return_value=(200, previous)):
                prepare(root, plan, CONFIG)
            self.assertEqual(json.loads(plan.read_text())['urls'], [])

    def test_unchanged_plan_never_calls_the_network(self):
        with tempfile.TemporaryDirectory() as temp:
            plan = Path(temp)/'plan.json'
            plan.write_text(json.dumps({'manifest': {'version': 1, 'pages': {}}, 'urls': []}))
            with patch('indexnow.confirm_deployment') as confirm, patch('indexnow.request') as send:
                submit(plan, CONFIG)
                confirm.assert_not_called()
                send.assert_not_called()

    def test_failed_deployment_blocks_submission(self):
        with tempfile.TemporaryDirectory() as temp:
            plan = Path(temp)/'plan.json'
            plan.write_text(json.dumps({'manifest': {'version': 1, 'pages': {SITE: 'a'*64}}, 'urls': [SITE]}))
            with patch('indexnow.confirm_deployment', side_effect=RuntimeError('not live')), patch('indexnow.request') as send:
                with self.assertRaises(RuntimeError):
                    submit(plan, CONFIG)
                send.assert_not_called()

    def test_success_and_pending_validation_are_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            plan = Path(temp)/'plan.json'
            plan.write_text(json.dumps({'manifest': {'version': 1, 'pages': {}}, 'urls': [SITE+'removed/']}))
            for status in [200, 202]:
                with patch('indexnow.confirm_deployment'), patch('indexnow.request', return_value=(status, b'')) as send:
                    submit(plan, CONFIG)
                    payload = json.loads(send.call_args.args[1])
                    self.assertEqual(payload['urlList'], [SITE+'removed/'])
                    self.assertEqual(payload['keyLocation'], SITE+CONFIG['key']+'.txt')

    def test_key_and_manifest_must_both_be_live(self):
        expected = {'version': 1, 'pages': {}}
        with patch('indexnow.request', side_effect=[(200, json.dumps(expected).encode()), (200, CONFIG['key'].encode())]):
            confirm_deployment(CONFIG, expected)
        with patch('indexnow.request', return_value=(200, b'{}')), patch('indexnow.time.sleep'):
            with self.assertRaises(RuntimeError):
                confirm_deployment(CONFIG, expected)

    def test_transient_errors_retry_but_invalid_key_does_not(self):
        for code, calls in [(429, 3), (503, 3), (403, 1)]:
            with patch('indexnow.urlopen', side_effect=HTTPError(SITE, code, 'error', {}, None)) as fetch, patch('indexnow.time.sleep'):
                with self.assertRaises(HTTPError):
                    request(SITE)
                self.assertEqual(fetch.call_count, calls)


if __name__ == '__main__':
    unittest.main()
