// Citation popovers: author–year citations, evidence-note markers, and Markdown footnotes.
// Progressive enhancement: without JS every marker is a plain in-page anchor.
(() => {
  const SELECTOR = "a.cite, a.evidence-ref, a.footnote-ref";
  if (!document.querySelector(SELECTOR)) return;

  // Reference entries gain "cited in text" back-links (1 2 3 …).
  document.querySelectorAll(".reference[id^='ref-']").forEach(entry => {
    const key = entry.id.slice(4);
    const cites = document.querySelectorAll(`a.cite[data-ref="${CSS.escape(key)}"]`);
    if (!cites.length) return;
    const wrap = document.createElement("span");
    wrap.className = "ref-backlinks";
    wrap.append("Cited ↑ ");
    cites.forEach((cite, i) => {
      if (!cite.id) cite.id = `cite-${key}-${i + 1}`;
      const a = document.createElement("a");
      a.href = `#${cite.id}`;
      a.textContent = String(i + 1);
      a.setAttribute("aria-label", `Back to citation ${i + 1} in the text`);
      wrap.append(a, i < cites.length - 1 ? " " : "");
    });
    entry.append(wrap);
  });

  const canHover = matchMedia("(hover: hover) and (pointer: fine)");
  const narrow = matchMedia("(max-width: 34rem)");
  const pop = document.createElement("div");
  pop.className = "cite-popover";
  pop.setAttribute("role", "dialog");
  pop.setAttribute("aria-label", "Citation details");
  pop.tabIndex = -1;
  pop.hidden = true;
  document.body.appendChild(pop);

  let current = null;
  let timer = null;

  const targetOf = link => {
    let id = "";
    try { id = decodeURIComponent((link.getAttribute("href") || "").slice(1)); } catch { return null; }
    return id ? document.getElementById(id) : null;
  };

  function build(link) {
    const target = targetOf(link);
    if (!target) return null;
    const frag = document.createElement("div");
    let more = "Go to reference ↓";
    if (link.classList.contains("evidence-ref")) {
      const title = target.querySelector(".evidence-title");
      const body = target.querySelector(".evidence-content");
      if (!body) return null;
      if (title) {
        const h = document.createElement("p");
        h.className = "pop-title";
        h.textContent = title.textContent;
        frag.append(h);
      }
      frag.append(body.cloneNode(true));
      more = "Go to note ↓";
    } else {
      frag.append(...Array.from(target.cloneNode(true).childNodes));
      if (link.classList.contains("footnote-ref")) more = "Go to footnote ↓";
    }
    frag.querySelectorAll("[id]").forEach(el => el.removeAttribute("id"));
    frag.querySelectorAll(".ref-backlinks, .evidence-back, .footnote-backref, [role='doc-backlink']").forEach(el => el.remove());
    const foot = document.createElement("p");
    foot.className = "pop-more";
    const a = document.createElement("a");
    a.href = link.getAttribute("href");
    a.textContent = more;
    foot.append(a);
    frag.append(foot);
    return frag;
  }

  function place(link) {
    pop.removeAttribute("style");
    pop.classList.toggle("is-sheet", narrow.matches);
    if (narrow.matches) return;
    pop.style.visibility = "hidden";
    pop.style.left = "0";
    pop.style.top = "0";
    const r = link.getBoundingClientRect();
    const w = pop.offsetWidth;
    const h = pop.offsetHeight;
    const left = Math.min(Math.max(r.left + r.width / 2 - w / 2, 8), window.innerWidth - w - 8);
    const below = r.bottom + 8;
    const above = r.top - h - 8;
    const top = below + h > window.innerHeight && above > 8 ? above : below;
    pop.style.left = `${left + window.scrollX}px`;
    pop.style.top = `${top + window.scrollY}px`;
    pop.style.visibility = "";
  }

  function show(link, focus) {
    clearTimeout(timer);
    const content = build(link);
    if (!content) return;
    if (current) current.removeAttribute("aria-expanded");
    pop.replaceChildren(content);
    pop.hidden = false;
    current = link;
    link.setAttribute("aria-expanded", "true");
    place(link);
    if (focus) pop.focus({ preventScroll: true });
  }

  function hide(restoreFocus) {
    clearTimeout(timer);
    pop.hidden = true;
    if (current) {
      current.removeAttribute("aria-expanded");
      if (restoreFocus) current.focus({ preventScroll: true });
      current = null;
    }
  }

  document.querySelectorAll(SELECTOR).forEach(link => {
    if (targetOf(link)) link.setAttribute("aria-haspopup", "dialog");
  });

  // Capture phase so we run before evidence.js's own click handler.
  document.addEventListener("click", event => {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest(SELECTOR);
    if (link && !pop.contains(link) && targetOf(link)) {
      const open = !pop.hidden && current === link;
      // Mouse users who already see the hover preview: a second click follows the link.
      if (open && canHover.matches) return;
      event.preventDefault();
      event.stopPropagation();
      if (open) hide(); else show(link, event.detail === 0);
      return;
    }
    if (!pop.contains(event.target)) hide();
  }, true);

  document.addEventListener("mouseover", event => {
    if (!canHover.matches) return;
    const link = event.target.closest(SELECTOR);
    if (link && !pop.contains(link) && targetOf(link)) {
      clearTimeout(timer);
      timer = setTimeout(() => show(link, false), 150);
    } else if (pop.contains(event.target)) {
      clearTimeout(timer);
    }
  });

  document.addEventListener("mouseout", event => {
    if (!canHover.matches) return;
    const link = event.target.closest(SELECTOR);
    if ((link && !pop.contains(link)) || pop.contains(event.target)) {
      clearTimeout(timer);
      timer = setTimeout(() => hide(false), 250);
    }
  });

  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && !pop.hidden) hide(true);
  });
  window.addEventListener("hashchange", () => hide(false));
  window.addEventListener("resize", () => hide(false));
})();
