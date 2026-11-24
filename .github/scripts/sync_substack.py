#!/usr/bin/env python3
"""Refresh the Writing cards in index.html from the Substack RSS feed.

Runs on a schedule in GitHub Actions (.github/workflows/substack-sync.yml).
Shows the newest posts first; empty slots keep the placeholder cards.
Only the block between the SUBSTACK:START / SUBSTACK:END markers is touched.

Usage: sync_substack.py [path/to/feed.xml]   (a local file is for testing)
"""
import html
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEED_URL = "https://jacobzhang.substack.com/feed"
INDEX = Path(__file__).resolve().parents[2] / "index.html"
CARDS = 3
PLACEHOLDERS = [
    ("Idea 1", "I have something to say"),
    ("Idea 2", "I have more things to say"),
    ("Idea 3", "I have even more things to say"),
]
START, END = "<!-- SUBSTACK:START -->", "<!-- SUBSTACK:END -->"
INDENT = "        "


def fetch_feed(source):
    if source:
        return Path(source).read_bytes()
    req = urllib.request.Request(FEED_URL, headers={
        "User-Agent": "Mozilla/5.0 (compatible; jacobzhang.me-substack-sync/1.0)",
        "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def clean(text, limit=None):
    text = re.sub(r"<[^>]+>", " ", html.unescape(text or ""))
    text = re.sub(r"\s+", " ", text).strip()
    if limit and len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:|-") + "…"
    return text


def posts_from(xml_bytes):
    root = ET.fromstring(xml_bytes)
    posts = []
    for item in root.iter("item"):
        title = clean(item.findtext("title"))
        link = (item.findtext("link") or "").strip().split("?")[0]
        if title and link.startswith("https://"):
            posts.append((title, clean(item.findtext("description"), 160), link))
    return posts


def card(i, title, text, link=None):
    e = html.escape
    href = f'"{e(link)}" target="_blank" rel="noopener"' if link else '"#"'
    return "\n".join([
        f"{INDENT}<a class=\"card\" href={href} data-substack>",
        f"{INDENT}  <span class=\"num\">{i:02d}</span>",
        f"{INDENT}  <h3>{e(title)}</h3>",
        f"{INDENT}  <p>{e(text)}</p>",
        f"{INDENT}  <span class=\"go\">Read on Substack <i>→</i></span>",
        f"{INDENT}</a>",
    ])


def main():
    posts = posts_from(fetch_feed(sys.argv[1] if len(sys.argv) > 1 else None))
    if not posts:
        sys.exit("Feed had no posts; leaving the page unchanged.")
    cards = [card(i + 1, *p) for i, p in enumerate(posts[:CARDS])]
    cards += [card(i + 1, *PLACEHOLDERS[i]) for i in range(len(cards), CARDS)]
    block = f"{START}\n" + "\n".join(cards) + f"\n{INDENT}{END}"

    page = INDEX.read_text(encoding="utf-8")
    if page.count(START) != 1 or page.count(END) != 1:
        sys.exit("Couldn't find the SUBSTACK markers in index.html.")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, page, flags=re.S)
    if new == page:
        print(f"Up to date ({len(posts)} post(s) in feed).")
        return
    INDEX.write_text(new, encoding="utf-8")
    print("Updated Writing cards:", "; ".join(p[0] for p in posts[:CARDS]))


if __name__ == "__main__":
    main()
