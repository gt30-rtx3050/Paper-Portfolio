"""
Content for the Paper Portfolio build.

Everything in this file is original placeholder material written for
this project. Swap the values here and re-run `python3 tools/build.py`
to re-issue every page. The layout, class names, design tokens and
interaction layer come from portfolio/styles.css and portfolio/app.js
and are shared by all pages.
"""
from __future__ import annotations

# --- brand -----------------------------------------------------------------
BRAND = {
    "name": "Folio Studio",
    "wordmark": "Folio",
    "location": "Rotterdam, NL",
    "email": "hello@folio-studio.example",
    "tagline": "Interactive designer &amp; creative developer",
    "since": "2019",
    "description": (
        "Folio is an independent design and development studio crafting "
        "iconic digital experiences through motion, typography and creative "
        "coding for brands and agencies around the world."
    ),
    "socials": [
        ("twitter", "https://twitter.com/", "Twitter"),
        ("instagram", "https://instagram.com/", "Instagram"),
        ("dribbble", "https://dribbble.com/", "Dribbble"),
        ("behance", "https://www.behance.net/", "Behance"),
    ],
}

# --- services --------------------------------------------------------------
SERVICES = [
    ("01", "Visual Direction", "Positioning, art direction and the system that holds a brand together."),
    ("02", "Interface Design", "Layout, typography and motion built for real reading behaviour."),
    ("03", "Creative Development", "WebGL, shaders, scroll choreography and interaction engineering."),
    ("04", "Design & Build", "Design systems handed over clean, documented and ready to ship."),
]

# --- projects --------------------------------------------------------------
# `desc` is the one-line card copy; `body` is the long case-study narrative.
PROJECTS = [
    {
        "slug": "halcyon",
        "title": "Halcyon",
        "client": "Halcyon Parfums",
        "year": "2023",
        "variant": 0,
        "tags": ["eCommerce", "Fashion"],
        "isNew": True,
        "desc": "Halcyon is an independent fragrance house where each scent is released as a numbered edition.",
        "body": (
            "A fragrance house that releases in small numbered editions needed a storefront that could "
            "make scarcity feel considered rather than commercial. We built the catalogue around a single "
            "horizontal axis: every bottle sits on the same line, and the page itself behaves like a "
            "shelf you move through."
        ),
        "role": "Art Direction, Interface Design, Creative Development",
        "year_line": "2023 — 2024",
        "scope": ["Art Direction", "Interface Design", "WebGL", "Headless Commerce", "Motion System"],
        "stack": "WebGL · GSAP · Three.js · Headless Commerce",
        "gallery": [
            "The shelf: a single continuous axis holding every edition in release order.",
            "Bottle plates rendered live so the glass reads differently under each light.",
            "Checkout reduced to three fields and one decision.",
            "The archive wall, twelve years of editions in one uninterrupted scroll.",
        ],
        "awards": [("Site of the Day", "2024"), ("Special Kudos", "2023"), ("Editorial Pick", "2023")],
    },
    {
        "slug": "northwind",
        "title": "Northwind",
        "client": "Northwind Labs",
        "year": "2023",
        "variant": 1,
        "tags": ["Portfolio", "Digital"],
        "isNew": True,
        "desc": "Northwind turns forty years of climate observation into an open dataset anyone can query.",
        "body": (
            "Forty years of climate observation is a lot of data and a very short attention span. The "
            "brief was to make a research archive feel like something you could touch. We built a single "
            "continuous canvas where every dataset is a surface you can push, pull and cross-reference."
        ),
        "role": "Design System, Data Visualisation, Front-end Architecture",
        "year_line": "2023",
        "scope": ["Design System", "Data Visualisation", "Web Workers", "Documentation"],
        "stack": "Canvas · D3 · Web Workers · Static Generation",
        "gallery": [
            "The landing surface: forty years of records rendered as one continuous field.",
            "A single station pulled out of the field and expanded to full screen.",
            "Comparison mode, two regions overlaid on one projection.",
            "Every chart exports to a static image with its provenance attached.",
        ],
        "awards": [("Site of the Month", "2023"), ("Developer Award", "2023")],
    },
    {
        "slug": "paloma-records",
        "title": "Paloma",
        "client": "Paloma Records",
        "year": "2022",
        "variant": 2,
        "tags": ["Digital", "Music"],
        "isNew": True,
        "desc": "Paloma is an independent label whose catalogue is organised by texture rather than genre.",
        "body": (
            "An independent label that files its catalogue by texture instead of genre asked for a site "
            "with no genre filter at all. We built one instead: a field of covers you move through, and a "
            "set of dials that narrow the field by mood, tempo and instrumentation."
        ),
        "role": "Interaction Design, Creative Development, Sound Design",
        "year_line": "2022 — 2023",
        "scope": ["Interaction Design", "Creative Development", "Audio Engine", "Art Direction"],
        "stack": "Web Audio · Canvas · GSAP · Headless CMS",
        "gallery": [
            "The catalogue field, sortable only by feel.",
            "A release opened up: sleeve, credits, and the room it was recorded in.",
            "The dial panel, four parameters and no labels.",
            "Live session cuts, streamed with a scrubbable waveform.",
        ],
        "awards": [("Honourable Mention", "2023"), ("Site of the Day", "2022")],
    },
    {
        "slug": "terrace",
        "title": "Terrace",
        "client": "Terrace Hotels",
        "year": "2022",
        "variant": 3,
        "tags": ["Portfolio", "Architecture"],
        "isNew": True,
        "desc": "Terrace runs eleven small hotels and needed one site that could hold all of them.",
        "body": (
            "Eleven small hotels, eleven very different rooms, one site. Rather than a template with a "
            "photo slot, we built a layout engine: each property supplies a set of measurements and the "
            "page composes itself around them."
        ),
        "role": "Art Direction, Design System, Template Architecture",
        "year_line": "2021 — 2022",
        "scope": ["Art Direction", "Design System", "CMS Modelling", "Photography Direction"],
        "stack": "Static Generation · Sanity · GSAP",
        "gallery": [
            "The index, eleven properties held in a single column of type.",
            "A room page composed from measurements rather than a fixed template.",
            "Booking flow, three steps and no account required.",
            "The print booklet, generated from the same CMS as the site.",
        ],
        "awards": [("Jury Mention", "2022")],
    },
    {
        "slug": "vantage",
        "title": "Vantage",
        "client": "Vantage Optics",
        "year": "2022",
        "variant": 4,
        "tags": ["eCommerce", "Fashion"],
        "isNew": False,
        "desc": "Vantage makes eyewear to prescription, and the site had to make that feel effortless.",
        "body": (
            "Prescription eyewear is a considered purchase, but most stores make it feel like a form. "
            "We moved the fitting conversation to the front: pick a frame, adjust the lenses in a live "
            "preview, and only then ask for anything."
        ),
        "role": "Interface Design, E-commerce, Creative Development",
        "year_line": "2022",
        "scope": ["Interface Design", "E-commerce", "Live Preview", "Accessibility"],
        "stack": "Three.js · WebGL · Stripe · Vue",
        "gallery": [
            "Frame selection with a live lens preview.",
            "The fitting guide, six questions and a recommendation.",
            "Colourway switching without a page load.",
            "Checkout, reduced to a single scrollable column.",
        ],
        "awards": [("Conversion Award", "2022")],
    },
    {
        "slug": "fold-and-field",
        "title": "Fold &amp; Field",
        "client": "Fold &amp; Field",
        "year": "2021",
        "variant": 5,
        "tags": ["eCommerce", "Fashion"],
        "isNew": False,
        "desc": "A technical apparel label whose garments are built to be repaired rather than replaced.",
        "body": (
            "A label built around repairability has an obvious problem: nothing about a jacket page tells "
            "you it will still be here in fifteen years. We put the repair programme at the centre of the "
            "site — every product carries its full service history and a parts list."
        ),
        "role": "Design Direction, E-commerce, Content Design",
        "year_line": "2021",
        "scope": ["Design Direction", "E-commerce", "Content Design", "Design System"],
        "stack": "Static Generation · Shopify · GSAP",
        "gallery": [
            "The garment page leads with its repair record, not its price.",
            "An exploded diagram, every part individually orderable.",
            "The service timeline for a ten-year-old jacket.",
            "The full parts catalogue, searchable by component.",
        ],
        "awards": [("Site of the Day", "2021"), ("Sustainability Commendation", "2021")],
    },
    {
        "slug": "cadence",
        "title": "Cadence",
        "client": "Cadence",
        "year": "2021",
        "variant": 0,
        "tags": ["Digital", "Corporate"],
        "isNew": False,
        "desc": "Cadence is a streaming service built by musicians who were tired of opaque royalty maths.",
        "body": (
            "The pitch was radical for a streaming service: publish the royalty maths. We designed a "
            "player where every stream is a data point, and where an artist can watch their own earnings "
            "resolve in real time."
        ),
        "role": "Product Design, Data Visualisation, Front-end",
        "year_line": "2020 — 2021",
        "scope": ["Product Design", "Data Visualisation", "Front-end", "Design System"],
        "stack": "React · D3 · Web Audio · Node",
        "gallery": [
            "The player, with the royalty line drawn live under the waveform.",
            "An artist dashboard resolving a single stream in real time.",
            "The public royalty model, opened up and explorable.",
            "Discovery, rebuilt around tempo rather than genre.",
        ],
        "awards": [("Product Award", "2021"), ("Editorial Pick", "2021")],
    },
    {
        "slug": "marble-room",
        "title": "Marble Room",
        "client": "Marble Room Biennale",
        "year": "2020",
        "variant": 2,
        "tags": ["Portfolio", "Culture"],
        "isNew": False,
        "desc": "A design biennale that wanted its archive to be browsable without a single index page.",
        "body": (
            "Four editions, three hundred works, no index. The archive was structured as a set of rooms "
            "you move between, each holding one edition, with the wall text kept exactly where a gallery "
            "wall would put it."
        ),
        "role": "Art Direction, Design, Front-end",
        "year_line": "2020",
        "scope": ["Art Direction", "Design", "Front-end", "Archive Tooling"],
        "stack": "Vue · GSAP · Static Generation",
        "gallery": [
            "The entrance: four doors, one per edition.",
            "A room, hung to the wall text of a real gallery.",
            "Work detail, with the catalogue notes kept in the margin.",
            "The archive tool used by the curatorial team to hang each room.",
        ],
        "awards": [("Cultural Site of the Year", "2020")],
    },
]

# --- awards (about page) ---------------------------------------------------
AWARDS = [
    ("Site of the Day", "Halcyon", "2024"),
    ("Developer Award", "Northwind", "2023"),
    ("Site of the Month", "Northwind", "2023"),
    ("Honourable Mention", "Paloma Records", "2023"),
    ("Special Kudos", "Halcyon", "2023"),
    ("Jury Mention", "Terrace Hotels", "2022"),
    ("Site of the Day", "Fold &amp; Field", "2021"),
    ("Product Award", "Cadence", "2021"),
    ("Site of the Day", "Marble Room", "2020"),
    ("Cultural Site of the Year", "Marble Room", "2020"),
]

# --- press / publications (about page) -------------------------------------
PUBLICATIONS = [
    ("Interface Annual", "Issue 14", "The case for one continuous axis", "2024"),
    ("Form Quarterly", "No. 88", "Interview: motion as documentation", "2023"),
    ("Journal of Interface", "Vol. 31", "Repairable interfaces", "2023"),
    ("Motion Review", "Issue 07", "Ten years of scroll choreography", "2022"),
    ("Grid &amp; Gutter", "No. 41", "Building a layout engine, not a template", "2022"),
    ("Type Review", "Issue 19", "Oversized type as a wayfinding device", "2021"),
]

# --- capabilities (about page) --------------------------------------------
SKILLS = [
    ("Art Direction", "Brand systems, editorial voice, campaign language."),
    ("Interface Design", "Layout, type systems, motion specification."),
    ("Creative Development", "WebGL, shaders, scroll engines, interaction."),
    ("Design Systems", "Tokens, documentation, handover, governance."),
]

# --- testimonials (about page) ---------------------------------------------
# Placeholder quotes written for this build — not attributed to real people.
TESTIMONIALS = [
    (
        "Studio Folio rebuilt our archive in six weeks and it has been the single biggest "
        "improvement to how people find our work since we launched.",
        "Editorial Lead",
        "Terrace Hotels",
    ),
    (
        "They treat detail as a structural question rather than a finishing pass. Everything "
        "they hand over is documented, and everything actually works.",
        "Head of Product",
        "Cadence",
    ),
    (
        "The clearest process we have worked with. A weekly demo, no surprises, and a build "
        "that shipped on the day it was promised.",
        "Managing Partner",
        "Northwind Labs",
    ),
    (
        "Our conversion went up and our support tickets went down, which we did not think was "
        "possible to do at the same time.",
        "Founder",
        "Halcyon Parfums",
    ),
]

# --- legal -----------------------------------------------------------------
LEGAL = [
    (
        "Privacy",
        [
            ("What we collect", "This site is a static build. It sets no cookies, runs no analytics and sends nothing to a server of ours. Your browser may keep ordinary cache entries."),
            ("Third-party assets", "Typefaces are fetched from a font CDN. Loading a page therefore discloses your IP address to that provider. Self-host the font files if you would rather avoid it."),
            ("Contact details", "The contact address in the footer is a placeholder. Replace it with a real inbox before deploying, and it should be covered by whatever policy you then publish."),
            ("Your rights", "Because nothing is stored, there is nothing for us to export or delete. If the site is later connected to a form or a CMS, this section needs rewriting to match."),
        ],
    ),
    (
        "Terms",
        [
            ("Use of this site", "The layout, typography and interaction system are reproduced as a front-end reference. Do not use it to publish material you do not have the right to publish."),
            ("Content and imagery", "All copy, project descriptions and imagery in this build are original placeholders generated for this repository. Replace them with your own work."),
            ("Availability", "No warranty is given. The site is provided as-is, without any commitment to uptime or fitness for a particular purpose."),
            ("Liability", " To the fullest extent permitted by law, no liability is accepted for loss arising from use of this site."),
        ],
    ),
    (
        "Credits",
        [
            ("Typefaces", "Domaine Display, Editorial New and Canopee, served as web fonts."),
            ("Libraries", "GSAP for animation, Locomotive Scroll for smooth scrolling."),
            ("Build", "Pages are generated by tools/build.py and styled by portfolio/styles.css."),
            ("Artwork", "Every image is produced procedurally by tools/artwork.py. No third-party imagery is included."),
        ],
    ),
]
