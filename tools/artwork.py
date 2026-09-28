"""
Generative artwork for the Paper Portfolio pages.

Every image is produced from scratch here — layered geometric
compositions seeded deterministically from the project slug, so the
work has its own visual identity instead of borrowing anyone else's
photography. Output is SVG written to portfolio/img/.
"""
from __future__ import annotations

import hashlib
import os

INK = "#1D1D1B"
PAPER = "#E8E3DA"
BEIGE = "#CDC6BE"


def _rng(seed: str):
    """Small deterministic PRNG so builds are reproducible."""
    h = int(hashlib.sha256(seed.encode()).hexdigest()[:16], 16)
    state = h

    def nxt(lo: float, hi: float) -> float:
        nonlocal state
        state = (state * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        return lo + ((state >> 11) / float(1 << 53)) * (hi - lo)

    return nxt


# --- composition families -------------------------------------------------

def _arcs(r, w, h):
    els = []
    # A couple of solid forms first, to anchor the composition...
    for i in range(3):
        cx = r(0.15 * w, 0.85 * w)
        cy = r(0.15 * h, 0.85 * h)
        rad = r(0.06 * w, 0.16 * w)
        els.append(
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rad:.0f}" fill="{INK}" opacity="{r(0.75, 1):.2f}"/>'
        )
    # ...then the drawn arcs sweeping across the plate.
    for i in range(9):
        cx = r(-0.1 * w, 1.1 * w)
        cy = r(-0.1 * h, 1.1 * h)
        rad = r(0.14 * w, 0.7 * w)
        sw = r(1.2, 6.0)
        col = INK if i % 3 else BEIGE
        op = r(0.4, 1)
        dash = f' stroke-dasharray="{r(2, 26):.0f} {r(6, 40):.0f}"' if i % 4 == 2 else ""
        els.append(
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rad:.0f}" fill="none" '
            f'stroke="{col}" stroke-width="{sw:.1f}" opacity="{op:.2f}"{dash}/>'
        )
    return els


def _bars(r, w, h):
    els = []
    n = int(r(9, 18))
    bw = w / n
    for i in range(n):
        bh = r(0.08 * h, 0.92 * h)
        y = h - bh if i % 2 else 0
        col = INK if i % 4 else BEIGE
        els.append(
            f'<rect x="{i * bw:.1f}" y="{y:.1f}" width="{bw * 0.72:.1f}" height="{bh:.1f}" '
            f'fill="{col}" opacity="{r(0.45, 1):.2f}"/>'
        )
    return els


def _grid(r, w, h):
    els = []
    step = r(0.06 * w, 0.13 * w)
    x = step
    while x < w:
        els.append(f'<line x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{h}" stroke="{INK}" stroke-width="0.7" opacity="0.28"/>')
        x += step
    y = step
    while y < h:
        els.append(f'<line x1="0" y1="{y:.0f}" x2="{w}" y2="{y:.0f}" stroke="{INK}" stroke-width="0.7" opacity="0.28"/>')
        y += step
    for _ in range(int(r(3, 7))):
        cx, cy = r(0, w), r(0, h)
        rad = r(0.08 * w, 0.3 * w)
        els.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rad:.0f}" fill="none" stroke="{INK}" stroke-width="{r(1, 3):.1f}"/>')
    return els


def _waves(r, w, h):
    els = []
    for i in range(int(r(5, 10))):
        amp = r(0.03 * h, 0.13 * h)
        base = h * (i + 0.5) / int(r(5, 10))
        d = [f"M0 {base:.0f}"]
        step = w / 8
        for s in range(1, 9):
            d.append(f"Q {s * step - step / 2:.0f} {base + (amp if s % 2 else -amp):.0f} {s * step:.0f} {base:.0f}")
        els.append(
            f'<path d="{" ".join(d)}" fill="none" stroke="{INK if i % 2 else BEIGE}" '
            f'stroke-width="{r(1, 3.4):.1f}" opacity="{r(0.4, 0.9):.2f}"/>'
        )
    return els


def _blocks(r, w, h):
    els = []
    for _ in range(int(r(6, 13))):
        bw, bh = r(0.08 * w, 0.36 * w), r(0.06 * h, 0.34 * h)
        x, y = r(0, w - bw), r(0, h - bh)
        if r(0, 1) > 0.55:
            els.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{INK}" opacity="{r(0.6, 1):.2f}"/>')
        else:
            els.append(
                f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="none" '
                f'stroke="{INK}" stroke-width="{r(1, 3):.1f}" opacity="{r(0.4, 0.9):.2f}" '
                f'transform="rotate({r(-14, 14):.1f} {x + bw / 2:.0f} {y + bh / 2:.0f})"/>'
            )
    return els


def _orbit(r, w, h):
    els = []
    cx, cy = r(0.3 * w, 0.7 * w), r(0.35 * h, 0.65 * h)
    for i in range(int(r(8, 16))):
        rad = r(0.05 * w, 0.46 * w)
        els.append(
            f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rad:.0f}" ry="{rad * r(0.12, 0.6):.0f}" '
            f'fill="none" stroke="{INK if i % 3 else BEIGE}" stroke-width="{r(0.8, 2.6):.1f}" '
            f'opacity="{r(0.35, 0.95):.2f}" transform="rotate({r(0, 180):.0f} {cx:.0f} {cy:.0f})"/>'
        )
    els.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r(4, 16):.0f}" fill="{INK}"/>')
    return els


FAMILIES = [_arcs, _bars, _grid, _waves, _blocks, _orbit]


def artwork(seed: str, w: int = 1600, h: int = 1100, variant: int = 0) -> str:
    """Return a standalone SVG string for the given seed."""
    r = _rng(f"{seed}:{variant}")
    fam = FAMILIES[variant % len(FAMILIES)]
    body = fam(r, w, h)

    # Halftone-ish dot field for texture.
    dots = []
    for _ in range(90):
        dots.append(
            f'<circle cx="{r(0, w):.0f}" cy="{r(0, h):.0f}" r="{r(1.0, 3.4):.1f}" fill="{INK}" opacity="{r(0.08, 0.3):.2f}"/>'
        )

    bg = [BEIGE, PAPER, INK, "#DCD5C9"][variant % 4]
    fg_alt = PAPER if bg == INK else INK

    # Repaint the family colours if the plate is dark.
    if bg == INK:
        body = [e.replace(INK, PAPER).replace(BEIGE, BEIGE) for e in body]
        dots = [d.replace(INK, PAPER) for d in dots]

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        f'<rect width="{w}" height="{h}" fill="{bg}"/>'
        f'<g>{"".join(dots)}</g>'
        f'<g>{"".join(body)}</g>'
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="none" stroke="{fg_alt}" stroke-width="2" opacity="0.5"/>'
        f'</svg>'
    )


def mark(seed: str, w: int = 600, h: int = 420) -> str:
    """A smaller 'title plate' used as the project wordmark stand-in."""
    r = _rng(f"mark:{seed}")
    pts = []
    for i in range(int(r(3, 6))):
        pts.append((r(0.1 * w, 0.9 * w), r(0.15 * h, 0.85 * h), r(0.03 * w, 0.11 * w)))
    shapes = "".join(
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad:.0f}" fill="{INK}" opacity="{r(0.5, 1):.2f}"/>'
        for x, y, rad in pts
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        f'<rect width="{w}" height="{h}" fill="{PAPER}"/>{shapes}'
        f'<line x1="0" y1="{h - 1}" x2="{w}" y2="{h - 1}" stroke="{INK}" stroke-width="3"/>'
        f'</svg>'
    )


def portrait(seed: str, w: int = 700, h: int = 700) -> str:
    """Abstract stand-in portrait plate for the press / testimonial slots."""
    r = _rng(f"portrait:{seed}")
    cx, cy = w * 0.5, h * 0.42
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        f'<rect width="{w}" height="{h}" fill="{BEIGE}"/>'
        f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{w * 0.27:.0f}" fill="{INK}" opacity="0.9"/>'
        f'<path d="M{w * 0.16:.0f} {h} Q {w * 0.5:.0f} {h * 0.52:.0f} {w * 0.84:.0f} {h} Z" fill="{INK}" opacity="0.9"/>'
        + "".join(
            f'<line x1="0" y1="{h * (i + 1) / 14:.0f}" x2="{w}" y2="{h * (i + 1) / 14:.0f}" '
            f'stroke="{PAPER}" stroke-width="1" opacity="{r(0.1, 0.3):.2f}"/>'
            for i in range(13)
        )
        + '</svg>'
    )


def write_assets(out_dir: str, projects) -> dict:
    """Render every plate for every project; return a slug -> paths map."""
    os.makedirs(out_dir, exist_ok=True)
    paths: dict = {}
    for p in projects:
        slug = p["slug"]
        entry = {"thumb": None, "mark": None, "gallery": [], "portrait": None}
        # Thumb and mark are always required by the templates.
        name = f"{slug}-thumb.svg"
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
            fh.write(artwork(slug, 1200, 840, variant=p.get("variant", 0)))
        entry["thumb"] = f"/portfolio/img/{name}"

        name = f"{slug}-mark.svg"
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
            fh.write(mark(slug))
        entry["mark"] = f"/portfolio/img/{name}"

        for i, _ in enumerate(p.get("gallery", [])):
            name = f"{slug}-g{i}.svg"
            with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
                fh.write(artwork(slug, 1800, 1200, variant=p.get("variant", 0) + i + 1))
            entry["gallery"].append(f"/portfolio/img/{name}")

        if p.get("portrait"):
            name = f"{slug}-portrait.svg"
            with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
                fh.write(portrait(slug))
            entry["portrait"] = f"/portfolio/img/{name}"
        paths[slug] = entry
    return paths
