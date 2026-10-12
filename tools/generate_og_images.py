#!/usr/bin/env python3
"""Generate the static OG images (1200x630) for the site and every blog post.

Re-establishes the SVG -> rsvg-convert pipeline used for the site banner
(run 4, issue #3) as a committed, re-runnable script (issue #8). The SVG
sources are kept under tools/og-svg/ for reference; the PNGs that actually
ship are written to assets/og/ (per-post) and assets/og-image.png (site).

Design mirrors the homepage hero: dark surface, violet/cyan/amber aurora
blobs, and the signature white-to-violet gradient heading. No plane — the
flight-path motif was removed from the site in run 8.

Usage:
    python3 tools/generate_og_images.py            # SVGs + PNGs (needs rsvg-convert)
    python3 tools/generate_og_images.py --svg-only # SVGs only

After adding a new post, re-run this script and add its og_image front matter:
    og_image: /assets/og/<slug>.png
Posts without og_image fall back to the site banner in _layouts/default.html.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "_posts"
SVG_DIR = ROOT / "tools" / "og-svg"
OG_DIR = ROOT / "assets" / "og"
SITE_BANNER = ROOT / "assets" / "og-image.png"

W, H = 1200, 630

# Site tokens (assets/css/style.css :root, dark palette — OG images are dark-first).
BG = "#0b0d12"
TEXT = "#e7eaf1"
MUTED = "#9aa4b5"
ACCENT = "#9c6cf7"
ACCENT_2 = "#22d3ee"
AMBER = "#fbbf24"
FONT = "Liberation Sans, sans-serif"

# Approximate bold-glyph advance as a fraction of font size; used only for
# wrapping. Real rendering is done by rsvg-convert/pango.
CHAR_W = 0.56
MAX_TEXT_W = W - 2 * 90
TITLE_SIZES = (64, 58, 52, 46)


def parse_front_matter(path: pathlib.Path) -> dict:
    """Minimal front-matter reader for the flat keys posts use."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path.name}: no front matter")
    _, fm, _ = text.split("---", 2)
    data = {}
    for line in fm.splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key.strip()] = [v.strip() for v in inner.split(",")] if inner else []
        else:
            data[key.strip()] = value.strip("\"'")
    return data


def slug_of(path: pathlib.Path) -> str:
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)


def wrap_title(title: str) -> tuple[str, list[str]]:
    """Pick the largest title size that fits in <= 3 lines, then wrap."""
    for size in TITLE_SIZES:
        char_limit = int(MAX_TEXT_W // (CHAR_W * size))
        lines, current = [], ""
        for word in title.split():
            candidate = f"{current} {word}".strip()
            if len(candidate) <= char_limit:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        if len(lines) <= 3 and all(len(line) <= char_limit for line in lines):
            return size, lines
    return TITLE_SIZES[-1], lines[:3]


def defs() -> str:
    return f"""  <defs>
    <radialGradient id="aurora-violet" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.34"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="aurora-cyan" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{ACCENT_2}" stop-opacity="0.26"/>
      <stop offset="1" stop-color="{ACCENT_2}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="aurora-amber" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{AMBER}" stop-opacity="0.16"/>
      <stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="title-grad" x1="0" y1="0" x2="1" y2="0.35">
      <stop offset="0.45" stop-color="{TEXT}"/>
      <stop offset="1" stop-color="{ACCENT}"/>
    </linearGradient>
    <linearGradient id="bar-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ACCENT}"/>
      <stop offset="1" stop-color="{ACCENT_2}"/>
    </linearGradient>
  </defs>"""


def aurora() -> str:
    # Echoes the hero blob placement: violet top-left, cyan top-right,
    # amber peeking from the bottom centre.
    return f"""  <rect width="{W}" height="{H}" fill="{BG}"/>
  <ellipse cx="170" cy="-40" rx="560" ry="480" fill="url(#aurora-violet)"/>
  <ellipse cx="1060" cy="30" rx="520" ry="440" fill="url(#aurora-cyan)"/>
  <ellipse cx="640" cy="700" rx="520" ry="380" fill="url(#aurora-amber)"/>"""


def header_footer(left_meta: str) -> str:
    esc = html.escape
    return f"""  <text x="90" y="94" font-family="{FONT}" font-size="24" font-weight="bold"
        letter-spacing="3" fill="{MUTED}">NAYIB MARTIN GOUSHESH</text>
  <text x="{W - 90}" y="94" font-family="{FONT}" font-size="24"
        text-anchor="end" fill="{MUTED}">n-cryptd.github.io</text>
  <text x="90" y="{H - 62}" font-family="{FONT}" font-size="26" fill="{MUTED}">{esc(left_meta)}</text>"""


def post_svg(title: str, left_meta: str) -> str:
    size, lines = wrap_title(title)
    line_h = round(size * 1.22)
    block_h = line_h * len(lines)
    # Anchor the title block to the accent bar; nudge 1-2 line titles toward centre.
    block_top = 186 + (3 - len(lines)) * (line_h // 2)
    esc = html.escape
    title_text = "\n".join(
        f'  <text x="90" y="{block_top + i * line_h + round(size * 0.82)}" font-family="{FONT}" '
        f'font-size="{size}" font-weight="bold" fill="url(#title-grad)">{esc(line)}</text>'
        for i, line in enumerate(lines)
    )
    bar_y = block_top + block_h + 40
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{defs()}
{aurora()}
{header_footer(left_meta)}
{title_text}
  <rect x="90" y="{bar_y}" width="150" height="10" rx="5" fill="url(#bar-grad)"/>
</svg>
"""


def site_svg() -> str:
    name_size = 82
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{defs()}
{aurora()}
  <text x="90" y="94" font-family="{FONT}" font-size="24" font-weight="bold"
        letter-spacing="3" fill="{MUTED}">n-cryptd.github.io</text>
  <text x="90" y="330" font-family="{FONT}" font-size="{name_size}" font-weight="bold"
        fill="url(#title-grad)">Nayib Martin Goushesh</text>
  <rect x="90" y="380" width="150" height="10" rx="5" fill="url(#bar-grad)"/>
  <text x="90" y="462" font-family="{FONT}" font-size="40" fill="{MUTED}">Aerospace Engineer &amp; AI Specialist</text>
  <text x="90" y="{H - 62}" font-family="{FONT}" font-size="26" fill="{MUTED}">Barcelona, Spain</text>
</svg>
"""


def render(svg_path: pathlib.Path, png_path: pathlib.Path) -> None:
    subprocess.run(
        ["rsvg-convert", "--width", str(W), "--height", str(H),
         "--format", "png", "--output", str(png_path), str(svg_path)],
        check=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--svg-only", action="store_true", help="write SVG sources without rendering PNGs")
    args = ap.parse_args()

    SVG_DIR.mkdir(parents=True, exist_ok=True)
    OG_DIR.mkdir(parents=True, exist_ok=True)

    posts = sorted(POSTS_DIR.glob("*.md"))
    if not posts:
        print("no posts found", file=sys.stderr)
        return 1

    for post in posts:
        fm = parse_front_matter(post)
        title = fm.get("title", "")
        date = fm.get("date", "")
        tags = fm.get("tags", [])
        try:
            date_str = dt.date.fromisoformat(str(date)).strftime("%b %-d, %Y")
        except ValueError:
            date_str = str(date)
        left_meta = " · ".join([date_str] + list(tags))
        svg_path = SVG_DIR / f"{slug_of(post)}.svg"
        svg_path.write_text(post_svg(title, left_meta), encoding="utf-8")
        print(f"wrote {svg_path.relative_to(ROOT)}")
        if not args.svg_only:
            png_path = OG_DIR / f"{slug_of(post)}.png"
            render(svg_path, png_path)
            print(f"rendered {png_path.relative_to(ROOT)}")

    site = SVG_DIR / "site-banner.svg"
    site.write_text(site_svg(), encoding="utf-8")
    print(f"wrote {site.relative_to(ROOT)}")
    if not args.svg_only:
        render(site, SITE_BANNER)
        print(f"rendered {SITE_BANNER.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
