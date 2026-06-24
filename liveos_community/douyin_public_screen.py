"""Browser research snippet for public-screen events."""

from __future__ import annotations


PUBLIC_SCREEN_OBSERVER_JS = r"""
(() => {
  const selectors = [
    '.webcast-chatroom___list',
    '[class*="webcast-chatroom"][class*="list"]',
    '[class*="chatroom"]'
  ];
  const list = selectors.map(s => document.querySelector(s)).find(Boolean);
  if (!list) {
    console.warn('LiveOS Community: chat list not found');
    return;
  }
  const seen = new Set();
  const emit = (node) => {
    const text = (node.innerText || node.textContent || '').replace(/\s+/g, ' ').trim();
    if (!text || seen.has(text)) return;
    seen.add(text);
    console.log(JSON.stringify({ ts: new Date().toISOString(), text }));
  };
  list.querySelectorAll('[class*="webcast-chatroom___item"], [class*="chatroom"][class*="item"]').forEach(emit);
  new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      for (const node of mutation.addedNodes) {
        if (node.nodeType === 1) emit(node);
      }
    }
  }).observe(list, { childList: true, subtree: true });
  console.log('LiveOS Community observer attached');
})();
"""


def browser_snippet() -> str:
    return PUBLIC_SCREEN_OBSERVER_JS.strip()

