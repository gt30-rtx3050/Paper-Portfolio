# Paper Portfolio

A multi-page build of the Paper Portfolio design system — the ink-on-paper
editorial layout with oversized display type, a 20-column grid, a paper-fold
menu, an inertial horizontal work slider and oversized marquee footer.

## Pages

| Route | File | What it is |
| --- | --- | --- |
| `/` | `index.html` | Home |
| `/work/` | `work/index.html` | Experience — six-panel horizontal accordion |
| `/about/` | `about/index.html` | Awards, press, capabilities, testimonials |
| `/legal/` | `legal/index.html` | Privacy, terms, credits |
| `/work/<slug>/` | `work/<slug>/index.html` | Eight case studies |

Case studies: `halcyon`, `northwind`, `paloma-records`, `terrace`, `vantage`,
`fold-and-field`, `cadence`, `marble-room`.

## Running it

Any static server from the repository root works — the routes above are real
directories containing `index.html`, and assets are served from `/portfolio/`.

```bash
python3 -m http.server 8080
```

## Rebuilding

Pages are generated from a single source of truth. Edit the copy in
`tools/content.py`, then:

```bash
python3 tools/build.py
```

This re-renders `portfolio/img/*.svg` and rewrites every page listed above.

### Layout of the tooling

| Path | Role |
| --- | --- |
| `tools/content.py` | All copy, project data, awards, press, legal text |
| `tools/artwork.py` | Procedural SVG plates — thumbnails, title marks, gallery images |
| `tools/build.py` | Shared components (nav, menu, footer, sidebar) + page templates |
| `portfolio/styles.css` | Design system: typefaces, palette, type scale |
| `portfolio/site.css` | Page composition and the states `app.js` drives |
| `portfolio/app.js` | Interaction layer |

## Design system

**Typefaces** — Domaine Display (display), Editorial New (text), Canopee
(accents), served as web fonts.

**Palette** — ink `#1D1D1B` on paper `#E8E3DA`, with `#CDC6BE` as the
secondary. The paper grain is generated at runtime in `app.js` and painted
into a repeating background.

**Interaction layer** — GSAP for animation, Locomotive Scroll for smooth
scrolling, Butter Slider for the horizontal field (with a self-contained
inertial fallback if the bundle fails to load). Pressing `G` toggles the
column grid overlay.

## Content and imagery

Every word of copy, every project description and every image in the
generated pages is **original material written and produced for this
repository**. The imagery is generated procedurally by `tools/artwork.py`
— there is no third-party photography, artwork or client material in the
build, and the studio name, people and projects are placeholders rather
than any real business or individual.

`index.html` is the one exception: it is a pre-existing file that was
already in the repository when this build started, and it still carries the
original reference material. The navigation targets in it have been
repointed at the routes in this build; the page body has not been
rewritten. Run the same treatment on it if you would rather it carry
original content too.

`BRAND` at the top of `tools/content.py` is the single place to change the
studio name, location, email and social links.

## Experience page

The existing `/work/` URL is retained so old links continue to work; its title
and navigation labels now read **Experience**. `EXPERIENCES` in
`tools/content.py` contains the six company names, dates and supplied labels.
No job titles or responsibilities have been inferred. Rebuild with
`python3 tools/build.py`; the reference is the repository's `Sample.mp4`.

`portfolio/experience.css` and `portfolio/experience.js` are isolated from the
legacy page bundles. The layout has a fixed vertical navigation rail and
full-height expanding columns. Hover or click a spine, scroll/drag sideways,
swipe on touch, or use the previous/next buttons. Arrow keys and Home/End work
inside the experience region. The menu supports Escape and focus containment;
reduced-motion preferences disable panel and scroll animation.

The original Canopee/Domaine font URLs are retained, with locally bundled
Bodoni Moda and Instrument Serif fallbacks (OFL licenses in `portfolio/fonts/`)
for unavailable external fonts. Imagery below is **illustrative**, not evidence
of client work or company offices. Selected images are served locally:

- SB Web Technology: [coding workspace](https://www.vecteezy.com/free-photos/laptop-coding)
- KPO & Company: [office interior, Pexels](https://www.pexels.com/photo/5483051/)
- Daraz Nepal: [shopping bags, Unsplash](https://unsplash.com/photos/woman-carrying-shopping-bags-in-front-of-building-_rxFfpOJKcI)
- Simple Flying: [airplane view, Unsplash](https://unsplash.com/photos/airplane-view-of-fluffy-clouds-and-sky-nqCP9lYAdGs)
- Himalayan Dream Treks: [mountain landscape](https://www.outlooktraveller.com/destinations/international/nepal-is-letting-you-climb-these-himalayan-peaks-for-freehere-are-the-best-ones)
- AFC Urgent Care: [stethoscope and laptop, Pexels](https://pexels.com/photo/computer-desk-laptop-stethoscope-48604)

Replace these with approved company/project imagery when available. The original
content/imagery statement above describes the older generated project pages,
not these new illustrative photographs.

Run the dependency-free structural regression checks with
`python3 -m unittest discover -s tools -p 'test_*.py'`.
