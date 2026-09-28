#!/usr/bin/env python3
"""
build.py — generates every page of the Paper Portfolio site.

    python3 tools/build.py

Reads the design system from portfolio/styles.css, the interaction layer
from portfolio/app.js, the copy from tools/content.py, and writes static
HTML to the repository root at the paths the navigation links to:

    /index.html                (home — hand-authored, see portfolio/paper.html)
    /work/index.html
    /about/index.html
    /legal/index.html
    /work/<slug>/index.html
    portfolio/img/*.svg
"""
from __future__ import annotations

import base64
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import artwork as art  # noqa: E402
from content import (  # noqa: E402
    AWARDS,
    EXPERIENCES,
    BRAND,
    LEGAL,
    PROJECTS,
    PUBLICATIONS,
    SERVICES,
    SKILLS,
    TESTIMONIALS,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "portfolio", "img")

INK = "#1D1D1B"
BEIGE = "#CDC6BE"

ASSETS: dict = {}


# --- small helpers ---------------------------------------------------------

def e(text: str) -> str:
    """Escape text for HTML, preserving intentional &amp; entities."""
    return html.escape(str(text), quote=True).replace("&amp;amp;", "&amp;")


def data_uri(svg: str) -> str:
    raw = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return "data:image/svg+xml;base64," + raw


def slug_path(slug: str) -> str:
    return f"/work/{slug}/"


# --- brand mark ------------------------------------------------------------

def monogram(dark: bool = True) -> str:
    """Original two-letter wordmark used in the navigation bar."""
    fg = "#1D1D1B" if dark else BEIGE
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 272 41">'
        f'<g fill="none" stroke="{fg}" stroke-width="3">'
        f'<path d="M6 34V7h7l10 17 10-17h7v27h-6V16L25 33h-4L12 16v18z"/>'
        f'<path d="M54 7h24v6H61v7h15v6H61v8h18v6H54z"/>'
        f'<path d="M90 7h7l12 18V7h6v27h-7L96 16v18h-6z"/>'
        f'<path d="M128 7h20a8 8 0 0 1 0 16h-2l9 11h-8l-8-10h-5v10h-6zm6 6v5h13a2.5 2.5 0 0 0 0-5z"/>'
        f'<path d="M170 7h6v21h16v6h-22z"/>'
        f'<path d="M204 7h6v27h-6z"/>'
        f'<path d="M222 7h20a8 8 0 0 1 0 16h-2l9 11h-8l-8-10h-5v10h-6zm6 6v5h13a2.5 2.5 0 0 0 0-5z"/>'
        f"</g></svg>"
    )


MONO_DARK = data_uri(monogram(True))
MONO_LIGHT = data_uri(monogram(False))


# --- shared components -----------------------------------------------------

HEAD_SCRIPTS = (
    '<script defer src="https://cdn.jsdelivr.net/npm/locomotive-scroll@4.1.3/dist/locomotive-scroll.min.js"></script>\n'
    '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.7.1/gsap.min.js"></script>\n'
    '<script defer src="https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js"></script>\n'
    '<script defer src="https://cdn.prod.website-files.com/5f2429f172d117fcee10e819/js/webflow.07467efa9.js"></script>\n'
    '<script defer src="https://unpkg.com/butter-slider"></script>\n'
    '<script defer src="/portfolio/app.js"></script>'
)


def head(title: str, desc: str, depth: int = 0) -> str:
    p = "/portfolio" + "/.." * depth if depth else "/portfolio"
    return f"""<!DOCTYPE html>
<html lang="en" class="w-mod-js w-mod-ix has-scroll-init has-scroll-smooth">
<head>
<meta charset="utf-8">
<title>{e(title)} — Paper Portfolio</title>
<meta name="description" content="{e(desc)}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://uploads-ssl.webflow.com" rel="preconnect" crossorigin="anonymous">
<link href="https://cdn.prod.website-files.com" rel="preconnect" crossorigin="anonymous">
<link href="{p}/styles.css" rel="stylesheet" type="text/css">
<link href="{p}/site.css" rel="stylesheet" type="text/css">
{HEAD_SCRIPTS}
</head>"""


def top_overlay() -> str:
    return """<div class="gl-canvas below w-embed"><canvas id="below-canvas"></canvas></div>
<div class="rotate"><div class="rotate-desc">Please rotate your device<br>to ensure a better experience.</div></div>"""


def grid_overlay() -> str:
    cols = "".join('<div class="grid-col"></div>' for _ in range(20))
    return f'<div class="grid">{cols}<div class="hide-grid w-embed"></div></div>'


def nav(active: str) -> str:
    """active: one of 'index' | 'work' | 'about'."""
    def menu_link(key: str, label_html: str, href: str) -> str:
        cur = " w--current" if key == active else ""
        aria = ' aria-current="page"' if key == active else ""
        return (
            f'<a draggable="false" aria-label="{e(BRAND["name"])} – {"Experience" if key == "work" else key.title()}" '
            f'data-color="{BEIGE}" rel="noopener" href="{href}"{aria} '
            f'class="menu-link {key} w-inline-block{cur}">'
            f'<h1 class="menu-title {key}">{label_html}</h1>'
            f'<div class="m-active {key}"></div>'
            f"</a>"
        )

    links = "".join(
        [
            f'<a draggable="false" aria-label="{e(BRAND["name"])} – Twitter" rel="noopener" '
            f'target="_blank" href="{BRAND["socials"][0][1]}" class="f-li new-tab w">twitter</a>'
            '<div class="f-li ci w">·</div>'
            f'<a draggable="false" aria-label="{e(BRAND["name"])} – Instagram" rel="noopener" '
            f'target="_blank" href="{BRAND["socials"][1][1]}" class="f-li new-tab w">insta<span class="f-span">g</span>ram</a>'
            '<div class="f-li ci w">·</div>'
            f'<a draggable="false" aria-label="{e(BRAND["name"])} – Dribbble" rel="noopener" '
            f'target="_blank" href="{BRAND["socials"][2][1]}" class="f-li new-tab w">dribbble</a>'
            '<div class="f-li ci w">·</div>'
            f'<a draggable="false" aria-label="{e(BRAND["name"])} – Behance" rel="noopener" '
            f'target="_blank" href="{BRAND["socials"][3][1]}" class="f-li new-tab w">behan<span class="f-span">c</span>e</a>'
        ]
    )

    cur_head = " w--current" if active == "index" else ""
    return f"""<nav data-scroll-target="#app" data-scroll="true" data-scroll-sticky="true" class="nav default is-inview">
<div class="gl-canvas w-embed"><canvas id="above-canvas"></canvas></div>
<div class="nav-inner">
<div class="paper-background work"><div class="paper-mode w-embed"></div></div>
<div aria-label="nav-link" rel="noopener" class="nav-block l"><div class="n-text">{e(BRAND["location"])}</div></div>
<a data-color="{INK}" aria-label="brand" rel="noopener" href="/" class="nav-head w-inline-block{cur_head}">
<img src="{MONO_DARK}" alt="{e(BRAND["name"])}" draggable="false" class="nav-img dark">
<img src="{MONO_LIGHT}" alt="" loading="eager" class="nav-img light" style="opacity:0;display:none">
</a>
<div class="nav-block r"><div class="nav-link"><div class="nav-lines">
<div class="nav-line up"></div><div class="nav-line bottom"></div>
</div></div></div>
<div class="menu" style="display:none">
<div class="menu-w">
{menu_link("index", "Index", "/")}
{menu_link("work", 'Experience', "/work/")}
{menu_link("about", 'Ab<span class="f-span space">o</span>ut', "/about/")}
<div class="f-block li w-clearfix">{links}</div>
</div>
<div class="menu-line"><div class="menu-face"></div><div class="menu-side" style="display:none"></div></div>
</div>
</div>
</nav>"""


def work_item(p: dict, variant: str = "") -> str:
    a = ASSETS[p["slug"]]
    new = (
        f'<div class="new-w-2 sp"><div class="new-2">New</div></div>'
        if p.get("isNew")
        else '<div class="new-w-2 sp w-condition-invisible"><div class="new-2">New</div></div>'
    )
    return f"""<div role="listitem" class="item l w-dyn-item {variant}">
<a draggable="false" aria-label="{e(p["title"])}" rel="noopener" href="{slug_path(p["slug"])}" class="item-link w-inline-block">
<div class="item-img-w"><div class="item-img w-embed">
<img src="{a["thumb"]}" alt="{e(p["desc"])}" draggable="false" loading="lazy">
</div></div>
<div class="item-block">
<div class="item-tw">
<img loading="lazy" draggable="false" src="{a["mark"]}" alt="{e(p["title"])}" class="item-t">
{new}
</div>
<div class="item-desc">{e(p["desc"])}</div>
</div>
</a>
</div>"""


def sidebar(active: str | None = None, limit: int = 6) -> str:
    items = "".join(
        work_item(p) for p in PROJECTS[:limit]
    )
    init = " init" if active is None else ""
    return f"""<header class="sidebar{init}">
<div data-butter-butter-options="smoothAmount:0.15,dragSpeed:2.5,hasTouchEvent:true" data-butter-container="Butter" class="s-container">
<div data-butter-slidable="Butter" class="s-inner">
<div class="s-grid w-dyn-list"><div role="list" class="s-block w-dyn-items">{items}</div></div>
</div></div>
</header>"""


def marquee() -> str:
    unit = (
        f'<div class="marquee-content">'
        f'<h4 class="f-news">Let&rsquo;s create something together</h4>'
        f'<a target="_blank" aria-label="{e(BRAND["name"])} – Project Request" rel="noopener" '
        f'draggable="false" href="mailto:{BRAND["email"]}?subject=Project%20Request" class="marquee-link w-inline-block">'
        f'<div class="marquee-text">Email Me</div></a></div>'
    )
    return f'<div class="marquee"><div class="marquee--inner">{unit * 3}</div></div>'


def footer() -> str:
    stamp = data_uri(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'
        f'<circle cx="100" cy="100" r="86" fill="none" stroke="{INK}" stroke-width="2"/>'
        f'<circle cx="100" cy="100" r="70" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="4 6"/>'
        f'<path d="M60 120V80h9l13 22 13-22h9v40h-8V96l-12 20h-4L68 96v24z" fill="{INK}"/>'
        f"</svg>"
    )
    socials = "".join(
        f'<a target="_blank" rel="noopener" href="{url}" class="f-link new-tab w">{e(name)}</a>'
        for _, url, name in BRAND["socials"]
    )
    return f"""<div class="footer">
{marquee()}
<div class="f-info">
<div class="f-col left">
<div class="f-title">{e(BRAND["wordmark"])}&copy;</div>
<div class="f-year">{e(BRAND["since"])}</div>
<img src="{stamp}" alt="" class="f-stamp" loading="lazy">
</div>
<div class="f-col right">
<a href="/legal/" class="f-link w">Legal</a>
{socials}
</div>
</div>
</div>"""


def gallery_overlay() -> str:
    return """<div class="gallery-overlay">
<div class="gallery-container">
<img src="" alt="">
<div class="gallery-cap"></div>
</div>
<button class="gallery-close" type="button" aria-label="Close gallery">Close</button>
</div>"""


def shell(*, title: str, desc: str, body_class: str, active: str, main: str, depth: int = 0) -> str:
    return "\n".join(
        [
            head(title, desc, depth),
            f'<body class="body {body_class}">',
            top_overlay(),
            f'<main id="app" data-scroll-container="null" data-scroll="true" class="app">',
            grid_overlay(),
            nav(active),
            main,
            footer(),
            gallery_overlay(),
            "</main>",
            "</body>",
            "</html>",
            "",
        ]
    )


def write(path: str, content: str) -> None:
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  {path}  ({len(content) / 1024:.1f} KB)")


# --- pages -----------------------------------------------------------------

def page_work() -> str:
    """Full-height horizontal experience accordion, based on Sample.mp4."""
    cards = []
    for i, job in enumerate(EXPERIENCES):
        slug = job["slug"]
        opened = i == 0
        cards.append(f'''<article class="experience-card{' is-active' if opened else ''}">
<button class="experience-spine" id="tab-{slug}" aria-expanded="{str(opened).lower()}" aria-controls="panel-{slug}">
<span class="spine-name">{e(job["name"])}</span>
<span class="spine-year">{e(job["years"])}</span>
</button>
<section class="experience-panel" id="panel-{slug}" aria-labelledby="tab-{slug}" {'inert' if not opened else ''}>
<div class="panel-inner">
<div class="panel-copy">
<div class="panel-tags"><span>{e(job["label"])}</span></div>
<h2>{e(job["name"])}</h2>
<p>{e(job["name"])}<br>{e(job["years"])}{'<br>' + e(job["label"]) if job["label"] != 'Experience' else ''}</p>
</div>
<img class="panel-image" src="/portfolio/img/experience/{slug}.jpg" alt="{e(job["image_alt"])}" draggable="false" {'fetchpriority="high"' if opened else 'loading="lazy"'}>
</div>
</section>
</article>''')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Experience — Paper Portfolio</title>
<meta name="description" content="Six chapters of professional experience, 2018–2026.">
<link rel="stylesheet" href="/portfolio/experience.css">
<script defer src="/portfolio/experience.js"></script>
</head>
<body class="experience-page">
<a class="skip-link" href="#experience">Skip to experience</a>
<header class="experience-rail">
<button class="rail-menu" aria-label="Open navigation" aria-expanded="false" aria-controls="experience-menu"><span></span><span></span></button>
<a class="rail-brand" href="/">The Paper Portfolio</a>
<h1 class="rail-label">Experience</h1>
</header>
<nav id="experience-menu" class="experience-menu" aria-label="Main navigation" inert hidden>
<a href="/">Index</a><a href="/work/" aria-current="page">Experience</a><a href="/about/">About</a>
<span class="menu-caption">The Paper Portfolio · 2018–2026</span>
</nav>
<main id="experience" class="experience-viewport" tabindex="0" aria-label="Experience. Scroll horizontally or use arrow keys to explore.">
<div class="experience-track">{''.join(cards)}</div>
</main>
<div class="experience-controls" aria-label="Browse experience">
<button type="button" data-step="-1" aria-label="Previous experience">←</button>
<span class="experience-count" aria-live="polite">01 / 06</span>
<button type="button" data-step="1" aria-label="Next experience">→</button>
</div>
</body>
</html>
'''


def page_about() -> str:
    """Awards, press, capabilities and testimonials."""
    award_rows = "".join(
        f"""<div class="aw1-item">
<div class="aw1-title"><span class="text bold">{e(name)}</span></div>
<div class="aw1-title"><span class="text">{e(project)}</span></div>
<div class="aw1-title"><span class="text small">{e(year)}</span></div>
</div>"""
        for name, project, year in AWARDS
    )

    award_counts = [
        ("Site of the Day", "Awards", sum(1 for n, _, _ in AWARDS if n == "Site of the Day")),
        ("Site of the Month", "Winners", sum(1 for n, _, _ in AWARDS if n == "Site of the Month")),
        ("Honourable Mention", "Awards", sum(1 for n, _, _ in AWARDS if n == "Honourable Mention")),
        ("Jury Mention", "Mentions", sum(1 for n, _, _ in AWARDS if n == "Jury Mention")),
    ]
    m_rows = "".join(
        f"""<a href="/work/" class="m-row w-inline-block">
<div class="m-col">
<div class="m-wrap w-clearfix"><div class="m-inner">
<h3 class="m-init">{e(name)}</h3>
<h3 class="m-title">{e(kind)}</h3>
</div><div class="m-numb">{count}</div></div>
</div>
</a>"""
        for name, kind, count in award_counts
    )

    pub_rows = "".join(
        f"""<div class="article-item">
<div class="article-header">
<div class="pub-numb__wrap"><span class="numb">{i + 1:02d}</span></div>
<div class="article-block" style="margin-left:2vw"><span class="pub-source">{e(outlet)}</span></div>
<div class="article-block" style="margin-left:auto"><span class="pub-source">{e(year)}</span></div>
</div>
<div class="article-grid">
<div class="article-block"><h3 class="article-title">{e(title)}</h3></div>
<div class="article-block"><div class="item-desc">{e(issue)}</div></div>
<div class="article-block"><div class="pub-link"><span class="text small">Read more</span></div></div>
</div>
</div>"""
        for i, (outlet, issue, title, year) in enumerate(PUBLICATIONS)
    )

    skill_rows = "".join(
        f"""<div class="aw-skill__item">
<img src="{ASSETS[PROJECTS[i % len(PROJECTS)]["slug"]]["mark"]}" alt="" class="aw-skill-img" loading="lazy">
<div class="aw-skill__text"><span class="text bold">{e(name)}</span>
<div><span class="text small aw">{e(desc)}</span></div></div>
</div>"""
        for i, (name, desc) in enumerate(SKILLS)
    )

    quotes = "".join(
        f"""<div class="aw-block s-{(i % 4) + 1}" style="background-color:{BEIGE}">
<div class="aw-content">
<div class="aw-desc s-{(i % 4) + 1}">
<div class="aw-infos center h"><div class="aw-box">
<div class="aw-info">
<h3 class="aw-name">{e(role)}</h3>
<div class="aw-role">{e(org)}</div>
</div>
</div></div>
<div class="aw-text" style="margin-top:2vw">
<span class="text">&ldquo;{e(quote)}&rdquo;</span>
</div>
</div>
<div class="aw-inner w-embed"><div class="dash"></div></div>
</div>
</div>"""
        for i, (quote, role, org) in enumerate(TESTIMONIALS)
    )

    services = "".join(
        f"""<div class="aw1-item">
<div class="aw1-title" style="height:6vw">
<span class="text bold">{e(num)}</span>
<span class="text big" style="font-size:3.2vw">{e(name)}</span>
</div>
<div class="aw1-desc"><span class="text small">{e(desc)}</span></div>
</div>"""
        for num, name, desc in SERVICES
    )

    main = f"""<div class="main h">
<header class="aw-1">
<div class="aw1-outer">
<h1 class="head ab" data-words>{e(BRAND["wordmark"])}</h1>
<div class="aw1-b">
<div class="aw1-col le">
<h5 class="has-dropcap">{BRAND["description"]}</h5>
</div>
<div class="aw1-col ri">
<div class="h-info-col">
<div class="aw-3">
<div class="aw3-wrap">
<div class="aw3-head">Awards</div>
</div>
</div>
<div class="aw-before s1"><div class="aw-line"></div></div>
<div class="aw-content">
{award_rows}
</div>
</div>
</div>
</div>
</div>
</header>

<section class="h-item awards" data-reveal>
<div class="aw-block-w">{m_rows}</div>
</section>

<section class="aw-3" data-reveal>
<div class="aw-3-inner">
<div class="aw3-head">Capabilities</div>
<div class="aw3-wrap" style="display:block">
<div class="aw-slider__content">
<div class="aw-skill__wrap">{skill_rows}</div>
</div>
</div>
<div class="aw3-client__wrap"><span class="aw3-client"><span class="aw3-line">Services</span></span></div>
</div>
<div class="aw1-b"><div class="aw1-col le">{services}</div></div>
</section>

<section class="aw-2" data-reveal>
<div class="aw2-head">Press</div>
<div class="publications" style="padding-left:2vw;padding-right:2vw">{pub_rows}</div>
</section>

<section class="h-item r" data-reveal>
<div class="aw-block-w">{quotes}</div>
</section>
</div>"""
    return shell(
        title="About",
        desc=f"Awards, press and capabilities for {BRAND['name']}.",
        body_class="about",
        active="about",
        main=main,
    )


def page_legal() -> str:
    blocks = []
    for title, rows in LEGAL:
        items = "".join(
            f"""<div class="aw1-item">
<div class="aw1-title"><span class="text bold">{e(name)}</span></div>
<div class="aw1-desc" style="width:60%"><span class="text small">{e(text)}</span></div>
</div>"""
            for name, text in rows
        )
        blocks.append(
            f"""<section data-reveal>
<div class="aw2-head" style="padding-top:4vw">{e(title)}</div>
<div class="aw-1"><div class="aw1-b"><div class="aw1-col le">{items}</div></div></div>
</section>"""
        )

    main = f"""<div class="main h">
<header class="aw-1">
<div class="aw1-outer">
<h1 class="head ab" data-words>Legal</h1>
<div class="aw1-b"><div class="aw1-col le">
<p class="text">This build ships with placeholder legal copy. Replace it with a policy you have
actually had reviewed before putting it in front of visitors.</p>
</div></div>
</div>
</header>
<div class="legal-w" data-reveal>{"".join(blocks)}</div>
</div>"""
    return shell(
        title="Legal",
        desc=f"Privacy, terms and credits for {BRAND['name']}.",
        body_class="legal",
        active="index",
        main=main,
    )


def page_case(idx: int) -> str:
    p = PROJECTS[idx]
    a = ASSETS[p["slug"]]
    nxt = PROJECTS[(idx + 1) % len(PROJECTS)]

    awards = "".join(
        f"""<div class="aw1-item">
<div class="aw1-title"><span class="text bold">{e(name)}</span></div>
<div class="aw1-title"><span class="text small">{e(year)}</span></div>
</div>"""
        for name, year in p["awards"]
    )

    scope = "".join(
        f'<div class="tag tag-w">{e(s)}</div>' for s in p["scope"]
    )

    plates = "".join(
        f"""<a href="#" data-gallery-item="{a["gallery"][i]}" data-gallery-caption="{e(cap)}"
   class="l-way gl-{(i % 5) + 1} w-inline-block" style="border:1px solid {INK}">
<img src="{a["gallery"][i]}" alt="{e(cap)}" loading="lazy"
     style="width:100%;height:100%;object-fit:cover" data-drift="6">
</a>"""
        for i, cap in enumerate(p["gallery"])
    )

    main = f"""<div class="main work-case">
<header class="aw-1" data-reveal>
<div class="aw1-outer">
<div class="bar-wrap left">
<a href="/work/" class="button-text back w-inline-block">
<span class="button-ico">&larr;</span>All Work
</a>
</div>
<h1 class="aw1-head" data-words>{e(p["title"])}</h1>
<div class="aw1-b">
<div class="aw1-col le">
<div class="case-info">
<div class="case-block">
<div class="case"><span class="text small aw">Client</span></div>
<div class="case"><span class="text">{e(p["client"])}</span></div>
<div class="case" style="margin-top:1.5vw"><span class="text small aw">Year</span></div>
<div class="case"><span class="text">{e(p["year_line"])}</span></div>
<div class="case" style="margin-top:1.5vw"><span class="text small aw">Role</span></div>
<div class="case"><span class="text">{e(p["role"])}</span></div>
<div class="case" style="margin-top:1.5vw"><span class="text small aw">Stack</span></div>
<div class="case"><span class="text">{e(p["stack"])}</span></div>
</div>
<div class="case-block" style="text-align:right">
<img src="{a["mark"]}" alt="{e(p["title"])}" style="width:16vw" loading="lazy">
</div>
</div>
</div>
<div class="aw1-col ri">
<div class="pub-link" style="flex-direction:column;gap:.6vw">{scope}</div>
</div>
</div>
</div>
</header>

<section class="case-desc wrap" data-reveal>
<div class="l-grid">
<h2 class="l-h2 p1" data-words>{e(p["title"])}</h2>
<div class="l-block gl-1">
<p class="p-text">{e(p["body"])}</p>
</div>
</div>
</section>

<section class="l-way-list" style="display:flex;gap:1vw;padding:0 2vw 4vw" data-reveal>
{plates}
</section>

<section class="aw-3" data-reveal>
<div class="aw3-head">Recognition</div>
<div class="aw-1"><div class="aw1-b"><div class="aw1-col le">{awards}</div></div></div>
</section>

<section class="case-extra" data-reveal>
<a href="{slug_path(nxt["slug"])}" data-next class="cta-h home w-inline-block">
<div class="cta-text work">
<span class="f-span space">Next</span>
</div>
<div class="h-item stamp" style="background:transparent">
<span class="text">{e(nxt["title"])} &rarr;</span>
</div>
</a>
</section>
</div>"""
    return shell(
        title=p["title"],
        desc=p["desc"],
        body_class="work case",
        active="work",
        main=main,
    )


# --- run -------------------------------------------------------------------

def main() -> None:
    print("Rendering artwork…")
    global ASSETS
    ASSETS = art.write_assets(IMG_DIR, PROJECTS)

    print("Writing pages…")
    write("/work/index.html", page_work())
    write("/about/index.html", page_about())
    write("/legal/index.html", page_legal())
    for i, _ in enumerate(PROJECTS):
        write(f"/work/{PROJECTS[i]['slug']}/index.html", page_case(i))

    print(f"\nDone — {len(PROJECTS) + 3} pages, {len(ASSETS)} artwork sets.")


if __name__ == "__main__":
    main()
