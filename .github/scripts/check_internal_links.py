#!/usr/bin/env python3
"""Check internal links in a built Jekyll site (stdlib only).

The html-proofer equivalent asked for in issue #1 with external checks
disabled: verifies that every internal link/asset reference in the built
site resolves to a real file (or a directory index), and that #fragments
match an id/name anchor in the target page. Catches broken liquid, nav,
and asset paths — deliberately not the state of the outside web.

Usage: check_internal_links.py --root _site --origin https://example.org
Exit codes: 0 all good, 1 broken references found, 2 usage/system error.
"""

from __future__ import annotations

import argparse
import os
import sys
import urllib.parse
from html.parser import HTMLParser

# (tag, attribute) pairs that reference a URL.
URL_ATTRS = {
    ("a", "href"),
    ("link", "href"),
    ("img", "src"),
    ("img", "srcset"),
    ("source", "src"),
    ("source", "srcset"),
    ("script", "src"),
    ("use", "href"),
    ("form", "action"),
    ("iframe", "src"),
}

SKIP_SCHEMES = ("mailto:", "tel:", "feed:", "data:", "javascript:", "sms:")


class RefCollector(HTMLParser):
    """Collect URL references and anchor ids from one HTML file."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []  # (line, url)
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        for attr_name, value in attrs:
            if attr_name == "id" and value:
                self.anchors.add(value)
            if (tag, attr_name) in URL_ATTRS and value:
                self.refs.append((line, value.strip()))
            # Legacy anchor names (<a name="...">).
            if tag == "a" and attr_name == "name" and value:
                self.anchors.add(value)

    # Self-closing forms of the tags above (e.g. <img/> after html5lib-ish output).
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def parse_html(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        parser = RefCollector()
        parser.feed(fh.read())
        parser.close()
        return parser


def split_srcset(value):
    for candidate in value.split(","):
        url = candidate.strip().split(" ")[0]
        if url:
            yield url


def resolve(root, current_rel, url, origin):
    """Return (kind, resolved_abs_path, fragment) or (None, url, None) to skip.

    kind is "file" | "anchor" (fragment-only link) | "skip".
    """
    url = url.strip()
    # Peel off the fragment first (fragments may sit on any reference type).
    fragment = None
    if "#" in url:
        url, fragment = url.split("#", 1)
        fragment = fragment.strip() or None

    if not url:  # "#" or "#section" — fragment-only link
        return ("anchor", None, fragment) if fragment else (None, url, None)

    low = url.lower()
    if low.startswith(SKIP_SCHEMES):
        return None, url, None
    if low.startswith("//"):  # protocol-relative → external
        return None, url, None
    if low.startswith(("http://", "https://")):
        if origin and low.startswith(origin.lower().rstrip("/") + "/"):
            url = urllib.parse.urlparse(url).path or "/"
        else:
            return None, url, None

    url = urllib.parse.unquote(url.split("?", 1)[0].split(";", 1)[0])

    if url.startswith("/"):
        target = os.path.normpath(os.path.join(root, url.lstrip("/")))
    else:
        base = os.path.dirname(os.path.join(root, current_rel))
        target = os.path.normpath(os.path.join(base, url))
    return "file", target, fragment


def check_site(root, origin):
    html_files = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.endswith((".html", ".htm")):
                html_files.append(os.path.join(dirpath, name))

    parsed = {p: parse_html(p) for p in html_files}
    errors = []
    checked = 0

    for page, collector in sorted(parsed.items()):
        rel = os.path.relpath(page, root)
        for line, raw in collector.refs:
            for url in split_srcset(raw) if is_srcset(raw) else [raw]:
                kind, target, fragment = resolve(root, rel, url, origin)
                if kind is None:
                    continue
                checked += 1

                if kind == "anchor":
                    target_page, anchors = page, collector.anchors
                else:
                    target_page = None
                    for candidate in (
                        target,
                        os.path.join(target, "index.html"),
                        os.path.join(target, "index.htm"),
                        target + ".html",
                    ):
                        if os.path.isfile(candidate):
                            target_page = candidate
                            break
                    if target_page is None:
                        errors.append(f"{rel}:{line}: broken link {raw!r} -> no file at {target}")
                        continue
                    anchors = parsed[target_page].anchors if target_page in parsed else parse_html(target_page).anchors

                if fragment and fragment not in anchors:
                    errors.append(
                        f"{rel}:{line}: broken fragment {raw!r} -> #{fragment} not found in "
                        f"{os.path.relpath(target_page, root)}"
                    )

    return sorted(set(errors)), len(parsed), checked


def is_srcset(raw):
    # srcset lists look like "img.png 1x, img@2x.png 2x"; a plain URL with a
    # comma in a query string would be unusual on this site.
    return " " in raw and ", " in raw


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default="_site", help="built site directory (default: _site)")
    ap.add_argument("--origin", default="", help="site origin whose absolute URLs count as internal")
    args = ap.parse_args()

    root = args.root.rstrip("/")
    if not os.path.isdir(root):
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    errors, pages, checked = check_site(root, args.origin)
    print(f"checked {checked} internal references across {pages} HTML pages")

    if errors:
        for err in errors:
            print(f"  {err}")
        print(f"FAIL: {len(errors)} broken internal reference(s)")
        return 1
    print("OK: no broken internal links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
