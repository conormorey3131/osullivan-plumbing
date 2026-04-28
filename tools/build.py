#!/usr/bin/env python3
"""
O'Sullivan Plumbing — static site generator.

This script produces pure static HTML files in the project root. The deployed
site has no runtime dependencies — this is just a one-shot author-time helper
so the shared header/footer/schema stay consistent across 30+ pages.

Run:  python3 tools/build.py
"""

from __future__ import annotations
import json
import os
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DOMAIN = "{{DOMAIN}}"  # e.g. "osullivanplumbing.ie"
PHONE = "{{PHONE_NUMBER}}"
PHONE_TEL = "{{PHONE_TEL}}"  # e.g. "+353871234567"
EMAIL = "{{EMAIL}}"
STREET = "{{STREET}}"
EIRCODE = "{{EIRCODE}}"
RGI = "{{RGI_NUMBER}}"
FOUNDER = "{{FOUNDER_NAME}}"
FACEBOOK = "{{FACEBOOK_URL}}"
INSTAGRAM = "{{INSTAGRAM_URL}}"
REVIEW_COUNT = "{{REVIEW_COUNT}}"
FORMSPREE = "{{FORMSPREE_ENDPOINT}}"
LAST_MOD = "2026-04-28"

SERVICES = [
    ("boiler-installation", "Boiler Installation", "Boiler Installation Limerick"),
    ("boiler-servicing-repairs", "Boiler Servicing & Repairs", "Boiler Service Limerick"),
    ("bathroom-plumbing", "Bathroom Plumbing", "Bathroom Plumber Limerick"),
    ("emergency-plumber", "Emergency Plumber", "Emergency Plumber Limerick"),
    ("central-heating", "Central Heating", "Central Heating Limerick"),
    ("general-plumbing", "General Plumbing", "Plumber Limerick"),
    ("power-flushing", "Power Flushing", "Power Flushing Limerick"),
    ("landlord-gas-safety-cert", "Landlord Gas Safety Cert", "Landlord Gas Cert Limerick"),
]

AREAS = [
    ("limerick-city", "Limerick City"),
    ("castletroy", "Castletroy"),
    ("raheen", "Raheen"),
    ("dooradoyle", "Dooradoyle"),
    ("caherdavin", "Caherdavin"),
    ("annacotty", "Annacotty"),
    ("ennis", "Ennis"),
    ("shannon", "Shannon"),
    ("newcastle-west", "Newcastle West"),
    ("adare", "Adare"),
    ("nenagh", "Nenagh"),
]

TOP_AREAS = AREAS[:6]


# ----------------------------------------------------------------------------
# Shared HTML chunks
# ----------------------------------------------------------------------------

def relative_prefix(depth: int) -> str:
    """How many ../ to prepend for asset/links from a page at given depth."""
    return "../" * depth


def head(title: str, description: str, canonical_path: str, page_path: str,
         depth: int, jsonld_blocks: list[dict], og_type: str = "website") -> str:
    rp = relative_prefix(depth)
    canonical = f"https://{DOMAIN}{canonical_path}"
    og_image = f"https://{DOMAIN}/assets/og-image.png"
    jsonld_html = "\n".join(
        f'<script type="application/ld+json">{json.dumps(b, indent=2)}</script>'
        for b in jsonld_blocks
    )
    return f"""<!DOCTYPE html>
<html lang="en-IE">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0A0A0A">

<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:site_name" content="O'Sullivan Plumbing">
<meta property="og:locale" content="en_IE">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image}">

<link rel="icon" type="image/x-icon" href="{rp}assets/favicon.ico">
<link rel="apple-touch-icon" href="{rp}assets/logo.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800&family=Inter:wght@400;500;600&display=swap">

<link rel="stylesheet" href="{rp}css/styles.css">

<style>
/* Critical above-the-fold inline */
body {{ margin: 0; font-family: "Inter", system-ui, sans-serif; color: #0A0A0A; background: #fff; }}
.site-header {{ position: sticky; top: 0; z-index: 50; background: rgba(255,255,255,0.96); }}
.hero, .page-hero {{ background: #0A0A0A; color: #fff; }}
</style>

{jsonld_html}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


def local_business_jsonld() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Plumber",
        "name": "O'Sullivan Plumbing",
        "image": f"https://{DOMAIN}/assets/logo.png",
        "@id": f"https://{DOMAIN}",
        "url": f"https://{DOMAIN}",
        "telephone": PHONE,
        "priceRange": "€€",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": STREET,
            "addressLocality": "Limerick",
            "addressRegion": "Co. Limerick",
            "postalCode": EIRCODE,
            "addressCountry": "IE",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 52.6638,
            "longitude": -8.6267,
        },
        "areaServed": [
            {"@type": "City", "name": "Limerick"},
            {"@type": "City", "name": "Ennis"},
            {"@type": "City", "name": "Shannon"},
            {"@type": "AdministrativeArea", "name": "County Limerick"},
            {"@type": "AdministrativeArea", "name": "County Clare"},
            {"@type": "AdministrativeArea", "name": "County Tipperary"},
        ],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": "08:00", "closes": "18:00"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": "Saturday", "opens": "09:00", "closes": "13:00"},
        ],
        "sameAs": [FACEBOOK, INSTAGRAM],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "5.0",
            "reviewCount": REVIEW_COUNT,
        },
    }


def organization_jsonld() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "O'Sullivan Plumbing",
        "url": f"https://{DOMAIN}",
        "logo": f"https://{DOMAIN}/assets/logo.png",
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": PHONE,
            "contactType": "customer service",
            "areaServed": "IE",
            "availableLanguage": ["English"],
        },
        "sameAs": [FACEBOOK, INSTAGRAM],
    }


def breadcrumb_jsonld(crumbs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": f"https://{DOMAIN}{path}",
            }
            for i, (name, path) in enumerate(crumbs)
        ],
    }


def service_jsonld(service_name: str, description: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": service_name,
        "provider": {"@type": "Plumber", "name": "O'Sullivan Plumbing"},
        "areaServed": [
            {"@type": "City", "name": "Limerick"},
            {"@type": "City", "name": "Ennis"},
            {"@type": "City", "name": "Shannon"},
        ],
        "description": description,
    }


def faq_jsonld(faqs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def header_html(depth: int, current: str = "") -> str:
    rp = relative_prefix(depth)

    def link(target: str, label: str, key: str) -> str:
        cls = " aria-current=\"page\"" if current == key else ""
        return f'<a href="{rp}{target}"{cls}>{label}</a>'

    services_dropdown = "".join(
        f'<li><a href="{rp}services/{slug}.html">{name}</a></li>'
        for slug, name, _ in SERVICES
    )
    areas_dropdown_top = "".join(
        f'<li><a href="{rp}areas/{slug}.html">{name}</a></li>'
        for slug, name in TOP_AREAS
    )
    areas_dropdown = areas_dropdown_top + f'<li><a href="{rp}areas.html"><strong>All areas →</strong></a></li>'

    return f"""
<header class="site-header">
  <div class="container">
    <a class="brand" href="{rp}index.html" aria-label="O'Sullivan Plumbing — home">
      <img src="{rp}assets/logo.png" alt="O'Sullivan Plumbing logo" width="48" height="48">
      <span class="brand-text">O'Sullivan Plumbing</span>
    </a>

    <nav class="nav-primary" aria-label="Primary">
      <ul>
        <li>{link('index.html', 'Home', 'home')}</li>
        <li class="has-dropdown">
          <button aria-haspopup="true" aria-expanded="false">Services</button>
          <ul class="dropdown-menu">
            <li><a href="{rp}services/index.html"><strong>All services</strong></a></li>
            {services_dropdown}
          </ul>
        </li>
        <li class="has-dropdown">
          <button aria-haspopup="true" aria-expanded="false">Areas</button>
          <ul class="dropdown-menu">
            {areas_dropdown}
          </ul>
        </li>
        <li>{link('about.html', 'About', 'about')}</li>
        <li>{link('contact.html', 'Contact', 'contact')}</li>
      </ul>
    </nav>

    <div class="header-cta">
      <a class="header-phone" href="tel:{PHONE_TEL}">{PHONE}</a>
      <a class="btn btn-primary btn-quote" href="{rp}contact.html">Get a Quote</a>
      <button class="menu-toggle" aria-label="Open menu" aria-controls="mobile-menu" aria-expanded="false">
        <span></span>
      </button>
    </div>
  </div>
</header>

<div class="mobile-menu" id="mobile-menu" aria-hidden="true">
  <div class="mobile-menu-header">
    <a class="brand" href="{rp}index.html">
      <img src="{rp}assets/logo.png" alt="O'Sullivan Plumbing" width="40" height="40">
      <span class="brand-text">O'Sullivan Plumbing</span>
    </a>
    <button class="mobile-menu-close" aria-label="Close menu">×</button>
  </div>
  <nav aria-label="Mobile">
    <ul>
      <li><a href="{rp}index.html">Home</a></li>
      <li class="has-submenu">
        <button aria-expanded="false">Services</button>
        <ul class="mobile-submenu" style="display:none;">
          <li><a href="{rp}services/index.html">All services</a></li>
          {services_dropdown}
        </ul>
      </li>
      <li class="has-submenu">
        <button aria-expanded="false">Areas</button>
        <ul class="mobile-submenu" style="display:none;">
          {areas_dropdown}
        </ul>
      </li>
      <li><a href="{rp}about.html">About</a></li>
      <li><a href="{rp}contact.html">Contact</a></li>
    </ul>
  </nav>
  <div class="mobile-menu-cta">
    <a class="btn btn-primary" href="{rp}contact.html">Get a Quote</a>
    <a class="btn btn-outline" href="tel:{PHONE_TEL}">Call {PHONE}</a>
  </div>
</div>
"""


def breadcrumbs_html(crumbs: list[tuple[str, str]], depth: int) -> str:
    """crumbs: list of (label, relative-from-root path) — last is current page (no link)."""
    rp = relative_prefix(depth)
    items = []
    for i, (label, path) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li>{label}</li>')
        else:
            items.append(f'<li><a href="{rp}{path}">{label}</a></li>')
    return f"""
<nav class="breadcrumbs" aria-label="Breadcrumb">
  <div class="container">
    <ol>{"".join(items)}</ol>
  </div>
</nav>
"""


def cta_banner(depth: int, heading: str = "Need a plumber in Limerick? Get a free quote.",
               sub: str = "Honest pricing, fast response, RGI-registered. Call us or send a message and we'll be back to you within the hour.") -> str:
    rp = relative_prefix(depth)
    return f"""
<section class="section">
  <div class="container">
    <div class="cta-banner reveal">
      <h2>{heading}</h2>
      <p>{sub}</p>
      <div class="cta-banner-actions">
        <a class="btn btn-primary" href="{rp}contact.html">Request a quote</a>
        <a class="btn btn-outline-light" href="tel:{PHONE_TEL}">Call {PHONE}</a>
      </div>
    </div>
  </div>
</section>
"""


def footer_html(depth: int) -> str:
    rp = relative_prefix(depth)
    services_links = "".join(
        f'<li><a href="{rp}services/{slug}.html">{name}</a></li>'
        for slug, name, _ in SERVICES
    )
    areas_links = "".join(
        f'<li><a href="{rp}areas/{slug}.html">{name}</a></li>'
        for slug, name in AREAS
    )
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{rp}assets/logo-white.png" alt="O'Sullivan Plumbing" width="180" height="56">
        <p>RGI-registered plumbing and heating across Limerick, Clare and the Mid-West. Honest pricing, quality workmanship, real local people.</p>
        <div class="footer-social">
          <a href="{FACEBOOK}" aria-label="Facebook" rel="noopener">f</a>
          <a href="{INSTAGRAM}" aria-label="Instagram" rel="noopener">ig</a>
        </div>
      </div>
      <div>
        <h4>Services</h4>
        <ul>{services_links}</ul>
      </div>
      <div>
        <h4>Service Areas</h4>
        <ul>{areas_links}</ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{STREET}<br>Limerick {EIRCODE}</li>
          <li>Mon–Fri 8am–6pm<br>Sat 9am–1pm<br>Emergency: 24/7</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> O'Sullivan Plumbing. RGI Reg. No. {RGI}. Fully insured.</span>
      <span>Powered by <a href="https://moreydigital.ie" rel="noopener">Morey Digital</a></span>
    </div>
  </div>
</footer>
<script src="{rp}js/main.js" defer></script>
</body>
</html>
"""


# ----------------------------------------------------------------------------
# Page contents
# ----------------------------------------------------------------------------

def quote_form(depth: int, compact: bool = False) -> str:
    return f"""
<form class="form" data-form action="{FORMSPREE}" method="POST">
  <div class="form-row">
    <div>
      <label for="name">Your name</label>
      <input id="name" name="name" type="text" required autocomplete="name">
    </div>
    <div>
      <label for="phone">Phone</label>
      <input id="phone" name="phone" type="tel" required autocomplete="tel">
    </div>
  </div>
  <div class="form-row">
    <div>
      <label for="email">Email</label>
      <input id="email" name="email" type="email" autocomplete="email">
    </div>
    <div>
      <label for="area">Area / Eircode</label>
      <input id="area" name="area" type="text" placeholder="e.g. Castletroy, V94...">
    </div>
  </div>
  <div>
    <label for="service">What do you need?</label>
    <select id="service" name="service">
      <option>General plumbing</option>
      <option>Emergency call-out</option>
      <option>Boiler installation</option>
      <option>Boiler service / repair</option>
      <option>Bathroom plumbing</option>
      <option>Central heating</option>
      <option>Power flushing</option>
      <option>Landlord gas cert</option>
      <option>Other</option>
    </select>
  </div>
  <div>
    <label for="message">Message</label>
    <textarea id="message" name="message" placeholder="A few details about the job…"></textarea>
  </div>
  <button class="btn btn-primary" type="submit">Send request</button>
  <div class="form-success" role="status" aria-live="polite">
    Thanks — we've got your message and will be in touch within the hour during working hours.
  </div>
  <p class="small-print">Or call us directly on <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
</form>
"""


# ---------- Homepage ----------

def homepage() -> str:
    depth = 0
    title = "Plumber Limerick | O'Sullivan Plumbing"
    desc = "RGI-registered plumber in Limerick covering boiler installation, repairs, bathrooms and emergency call-outs across Limerick, Clare & the Mid-West. Free quotes."
    jsonlds = [local_business_jsonld(), organization_jsonld()]

    services_cards = "".join(
        f"""
    <a class="card reveal" href="services/{slug}.html">
      <div class="card-icon">{icon}</div>
      <h3>{name}</h3>
      <p>{blurb}</p>
      <span class="card-arrow">Learn more →</span>
    </a>"""
        for slug, name, icon, blurb in [
            ("boiler-installation", "Boiler Installation", "🔥", "New gas, oil and LPG boilers fitted with manufacturer warranties up to 12 years."),
            ("boiler-servicing-repairs", "Boiler Service & Repair", "🔧", "Annual servicing and same-day repair for all major boiler brands."),
            ("emergency-plumber", "Emergency Plumber", "🚨", "24/7 response for burst pipes, leaks and no-heat emergencies."),
            ("bathroom-plumbing", "Bathroom Plumbing", "🛁", "Full bathroom installs, showers, basins and tiling — clean, careful work."),
            ("central-heating", "Central Heating", "♨️", "Radiator installation, system upgrades and zoned heating controls."),
            ("power-flushing", "Power Flushing", "💧", "Restore heating efficiency with a full system flush — cuts running costs."),
        ]
    )

    areas_cards = "".join(
        f'<a class="card reveal" href="areas/{slug}.html"><h3>Plumber {name}</h3><p>Local plumbing & heating in {name} and the surrounding area.</p><span class="card-arrow">View area →</span></a>'
        for slug, name in TOP_AREAS
    )

    body = f"""
<main id="main">

<section class="hero">
  <div class="container">
    <span class="eyebrow" style="color:#7ab8e8;">Limerick · Clare · Tipperary</span>
    <h1>Plumbing and heating, done properly.</h1>
    <p>O'Sullivan Plumbing is a Limerick-based, RGI-registered plumbing and heating company. Whether it's a new boiler, a leaking pipe at midnight or a full bathroom fit-out — we turn up, we explain it clearly, and we charge a fair price.</p>
    <div class="hero-ctas">
      <a class="btn btn-primary" href="contact.html">Get a free quote</a>
      <a class="btn btn-outline-light" href="tel:{PHONE_TEL}">Call {PHONE}</a>
    </div>
    <div class="hero-meta">
      <span>★★★★★ <strong>5.0</strong> on Google</span>
      <span><strong>RGI</strong> registered &amp; fully insured</span>
      <span><strong>24/7</strong> emergency response</span>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">Services</span>
    <h2 class="mt-0">Plumbing &amp; heating, all in one place</h2>
    <p class="lead">From a dripping tap to a full heating system replacement, we handle every job with the same care. Most quotes are free and most repairs are done same-day.</p>
    <div class="grid grid-3 mt-l">{services_cards}</div>
    <p class="mt-l"><a href="services/index.html"><strong>See all our services →</strong></a></p>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <span class="eyebrow">Why O'Sullivan Plumbing</span>
    <h2 class="mt-0">Built on word-of-mouth across Limerick</h2>
    <div class="stats mt-l">
      <div class="reveal"><span class="stat-value">15+</span><div class="stat-label">years on the tools</div></div>
      <div class="reveal"><span class="stat-value">1,000+</span><div class="stat-label">jobs completed in the Mid-West</div></div>
      <div class="reveal"><span class="stat-value">RGI</span><div class="stat-label">registered &amp; gas-safe</div></div>
      <div class="reveal"><span class="stat-value">24/7</span><div class="stat-label">emergency response</div></div>
    </div>
    <div class="trust-row">
      <span>Fixed quotes, no surprises</span>
      <span>Fully insured to €6.5m</span>
      <span>Worcester accredited</span>
      <span>SEAI grant-friendly installs</span>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="eyebrow">Where we work</span>
    <h2 class="mt-0">Service across Limerick &amp; the Mid-West</h2>
    <p class="lead">Based in Limerick city, we cover the whole county plus most of Clare and parts of north Tipperary. If you're not sure whether we cover you, just call.</p>
    <div class="grid grid-3 mt-l">{areas_cards}</div>
    <p class="mt-l"><a href="areas.html"><strong>See all service areas →</strong></a></p>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <span class="eyebrow">What customers say</span>
    <h2 class="mt-0">Reviews from real Limerick homes</h2>
    <div class="grid grid-3 mt-l">
      <div class="testimonial reveal">
        <div class="stars">★★★★★</div>
        <p class="testimonial-quote">"Boiler packed in on a Sunday in January with two small kids in the house. {FOUNDER} was here in 90 minutes and had heat back on the same evening. Fair price, no fuss."</p>
        <div class="testimonial-author"><strong>Aoife M.</strong>Castletroy, Limerick</div>
      </div>
      <div class="testimonial reveal">
        <div class="stars">★★★★★</div>
        <p class="testimonial-quote">"Did a full bathroom for us in Raheen — quote was honest, work was tidy, and they cleaned up every evening. Wouldn't use anyone else."</p>
        <div class="testimonial-author"><strong>Liam D.</strong>Raheen, Limerick</div>
      </div>
      <div class="testimonial reveal">
        <div class="stars">★★★★★</div>
        <p class="testimonial-quote">"Replaced our old oil boiler with a new condensing one and sorted the SEAI grant paperwork. Heating bills down noticeably this winter."</p>
        <div class="testimonial-author"><strong>Sinead O.</strong>Adare, Co. Limerick</div>
      </div>
    </div>
  </div>
</section>

{cta_banner(depth)}

</main>
"""
    return head(title, desc, "/", "/index.html", depth, jsonlds) + header_html(depth, "home") + body + footer_html(depth)


# ---------- About ----------

def about_page() -> str:
    depth = 0
    title = "About O'Sullivan Plumbing | RGI Plumber Limerick"
    desc = "Family-run, RGI-registered plumbing and heating in Limerick. Meet the team behind O'Sullivan Plumbing — over 15 years on the tools across the Mid-West."
    crumbs = [("Home", "/index.html"), ("About", "/about.html")]
    jsonlds = [local_business_jsonld(), breadcrumb_jsonld([("Home", "/"), ("About", "/about.html")])]

    body = f"""
<main id="main">
{breadcrumbs_html([("Home", "index.html"), ("About", "about.html")], 0)}

<section class="page-hero">
  <div class="container">
    <h1>About O'Sullivan Plumbing</h1>
    <p>Family-run, locally based, RGI-registered. Real plumbing for real Limerick homes — by people who answer their own phone.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="layout-cols">
      <article class="article">
        <h2 class="mt-0">Our story</h2>
        <p>O'Sullivan Plumbing was started by {FOUNDER} after more than a decade working for some of the bigger plumbing contractors in Limerick and Munster. The job got too big, the work got too rushed, and the people on the receiving end of the bills weren't getting the care they deserved. So we set up something better.</p>
        <p>Today we're a small, focused Limerick-based team. Most of our work comes through word of mouth from previous customers — neighbours in Castletroy, landlords in Limerick city, families in Raheen, Dooradoyle and Adare. We keep the team small on purpose, so the person quoting your job is usually the one doing it, and we never sub work out to people we don't know.</p>

        <h2>What we believe</h2>
        <ul>
          <li><strong>Honest pricing.</strong> Fixed quotes wherever possible, written down before the work starts. No "while we were under there..." surprises.</li>
          <li><strong>Local matters.</strong> We live and work in Limerick. If something goes wrong six months later, we're around the corner — not a 1800 number that goes to voicemail.</li>
          <li><strong>Do it once, do it right.</strong> Cheap parts and shortcuts cost more in the long run. We use quality fittings from brands we trust, and we stand over our work.</li>
          <li><strong>Respect the home.</strong> Dust sheets down, shoes off, mess cleaned up at the end of every day. It's your house, not a building site.</li>
        </ul>

        <h2>Qualifications &amp; insurance</h2>
        <p>We're registered with the <a href="https://www.rgi.ie" rel="noopener">Register of Gas Installers of Ireland (RGII)</a> — the legal requirement for any gas work in Ireland. RGI Reg. No. <strong>{RGI}</strong>. We're also fully insured to €6.5m public liability, with all certs available on request before any work begins.</p>
        <p>Our installers are trained and accredited by the major boiler manufacturers we fit (Worcester Bosch, Ideal, Vaillant, Grant and Firebird), which means manufacturer warranties of up to 12 years on new boiler installs.</p>

        <h2>The areas we work</h2>
        <p>Limerick city and county is our main patch — including <a href="areas/castletroy.html">Castletroy</a>, <a href="areas/raheen.html">Raheen</a>, <a href="areas/dooradoyle.html">Dooradoyle</a>, <a href="areas/caherdavin.html">Caherdavin</a>, <a href="areas/annacotty.html">Annacotty</a> and <a href="areas/adare.html">Adare</a>. We also cover most of <a href="areas/ennis.html">Ennis</a>, <a href="areas/shannon.html">Shannon</a> and across into north Tipperary including <a href="areas/nenagh.html">Nenagh</a>.</p>

        <h2>What we do</h2>
        <p>The full range of domestic plumbing and heating: <a href="services/boiler-installation.html">boiler installations</a>, <a href="services/boiler-servicing-repairs.html">annual services and repairs</a>, <a href="services/emergency-plumber.html">24/7 emergency call-outs</a>, <a href="services/bathroom-plumbing.html">bathroom installations</a>, <a href="services/central-heating.html">central heating</a> and <a href="services/landlord-gas-safety-cert.html">landlord gas safety certs</a>. If you're a landlord with multiple properties or a homeowner planning a renovation, talk to us early — we can save you money and headaches.</p>
      </article>

      <aside class="sidebar">
        <h3>Get in touch</h3>
        <p><a class="btn btn-primary" style="width:100%;" href="contact.html">Request a quote</a></p>
        <p style="margin-top:12px;"><a class="btn btn-outline" style="width:100%;" href="tel:{PHONE_TEL}">{PHONE}</a></p>
        <h3 style="margin-top:32px;">At a glance</h3>
        <ul>
          <li>RGI-registered ({RGI})</li>
          <li>€6.5m public liability</li>
          <li>15+ years experience</li>
          <li>Worcester accredited</li>
          <li>SEAI grant installs</li>
          <li>24/7 emergency cover</li>
        </ul>
      </aside>
    </div>
  </div>
</section>

{cta_banner(depth)}
</main>
"""
    return head(title, desc, "/about.html", "/about.html", 0, jsonlds) + header_html(0, "about") + body + footer_html(0)


# ---------- Contact ----------

def contact_page() -> str:
    depth = 0
    title = "Contact O'Sullivan Plumbing | Plumber Limerick"
    desc = "Get a free plumbing quote in Limerick. Call, email or send us a message — we reply within the hour during working hours. 24/7 emergency line available."
    jsonlds = [local_business_jsonld(), breadcrumb_jsonld([("Home", "/"), ("Contact", "/contact.html")])]
    body = f"""
<main id="main">
{breadcrumbs_html([("Home", "index.html"), ("Contact", "contact.html")], 0)}

<section class="page-hero">
  <div class="container">
    <h1>Contact O'Sullivan Plumbing</h1>
    <p>Send a message and we'll come back to you within the hour during working hours. For emergencies, call us directly — the phone is on 24/7.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="layout-cols">
      <div>
        <h2 class="mt-0">Request a quote</h2>
        <p>Tell us a bit about the job and we'll come back with honest pricing or arrange a quick site visit. Most quotes are free.</p>
        {quote_form(depth)}
      </div>
      <aside class="sidebar">
        <h3>Phone</h3>
        <p><a href="tel:{PHONE_TEL}"><strong>{PHONE}</strong></a><br><span class="small-print">Mon–Fri 8am–6pm · Sat 9am–1pm · Emergencies 24/7</span></p>

        <h3>Email</h3>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>

        <h3>Address</h3>
        <p>{STREET}<br>Limerick {EIRCODE}<br>Co. Limerick, Ireland</p>

        <h3>Coverage</h3>
        <p>Limerick city &amp; county, most of Clare (Ennis, Shannon, Newcastle West) and north Tipperary (Nenagh).</p>

        <p style="margin-top:24px;">
          <img src="https://staticmap.openstreetmap.de/staticmap.php?center=52.6638,-8.6267&amp;zoom=11&amp;size=480x300&amp;markers=52.6638,-8.6267,red-pushpin"
               alt="Map showing O'Sullivan Plumbing service area centered on Limerick"
               width="480" height="300" loading="lazy"
               style="border-radius:8px;border:1px solid #E5E5E0;">
        </p>
      </aside>
    </div>
  </div>
</section>
</main>
"""
    return head(title, desc, "/contact.html", "/contact.html", 0, jsonlds) + header_html(0, "contact") + body + footer_html(0)


# ---------- Areas hub ----------

def areas_hub_page() -> str:
    depth = 0
    title = "Service Areas | Plumber Limerick & Mid-West"
    desc = "O'Sullivan Plumbing covers Limerick city, county Limerick, most of Clare and north Tipperary. Find your area — we likely cover you."
    jsonlds = [local_business_jsonld(), breadcrumb_jsonld([("Home", "/"), ("Areas", "/areas.html")])]
    cards = "".join(
        f'<a class="card reveal" href="areas/{slug}.html"><h3>Plumber {name}</h3><p>Boiler installs, emergency repairs, bathrooms and central heating in {name}.</p><span class="card-arrow">Visit area page →</span></a>'
        for slug, name in AREAS
    )
    body = f"""
<main id="main">
{breadcrumbs_html([("Home", "index.html"), ("Areas", "areas.html")], 0)}

<section class="page-hero">
  <div class="container">
    <h1>Our service areas — plumbing across Limerick &amp; the Mid-West</h1>
    <p>From the city centre to the small villages — if you're in Limerick, Clare or north Tipperary, there's a good chance we've already worked on a house up the road from you.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <p class="lead">We're a Limerick-based plumbing and heating team and most of our work is within a 30-minute drive of the city. That keeps response times fast, especially for emergency call-outs. If you're not sure whether we cover you, just give us a call — we often go further than what's listed below.</p>
    <div class="grid grid-3 mt-l">{cards}</div>
  </div>
</section>

{cta_banner(depth)}
</main>
"""
    return head(title, desc, "/areas.html", "/areas.html", 0, jsonlds) + header_html(0, "areas") + body + footer_html(0)


# ---------- Services hub ----------

def services_hub_page() -> str:
    depth = 1
    title = "Plumbing & Heating Services Limerick | O'Sullivan Plumbing"
    desc = "Full plumbing and heating services across Limerick — boiler installs, repairs, emergency call-outs, bathrooms, central heating and landlord gas certs."
    jsonlds = [local_business_jsonld(), breadcrumb_jsonld([("Home", "/"), ("Services", "/services/index.html")])]

    cards_data = [
        ("boiler-installation", "Boiler Installation", "🔥", "Gas, oil and LPG boilers fitted with manufacturer warranties up to 12 years. Worcester, Ideal, Vaillant, Grant, Firebird."),
        ("boiler-servicing-repairs", "Boiler Servicing & Repairs", "🔧", "Annual services and same-day repairs across all major brands. Keep your warranty valid and your bills lower."),
        ("emergency-plumber", "Emergency Plumber", "🚨", "Burst pipes, no heat, no hot water — 24/7 response across Limerick and the Mid-West."),
        ("bathroom-plumbing", "Bathroom Plumbing", "🛁", "Full bathroom installs, shower upgrades, basins, toilets and tiling — clean, careful, on time."),
        ("central-heating", "Central Heating", "♨️", "New systems, radiator installs, smart heating controls and zoning. Lower bills, more comfort."),
        ("general-plumbing", "General Plumbing", "🔩", "Leaks, taps, toilets, water pressure, hot water cylinders — the everyday stuff that just needs sorting."),
        ("power-flushing", "Power Flushing", "💧", "Restore your heating system's efficiency. We flush out sludge that costs you on every bill."),
        ("landlord-gas-safety-cert", "Landlord Gas Safety Cert", "📋", "RGI-registered gas safety inspections and certs for landlords. Same-day paperwork in your inbox."),
    ]
    cards = "".join(
        f'<a class="card reveal" href="{slug}.html"><div class="card-icon">{icon}</div><h3>{name}</h3><p>{blurb}</p><span class="card-arrow">Read more →</span></a>'
        for slug, name, icon, blurb in cards_data
    )
    body = f"""
<main id="main">
{breadcrumbs_html([("Home", "index.html"), ("Services", "services/index.html")], 1)}

<section class="page-hero">
  <div class="container">
    <h1>Plumbing &amp; Heating Services in Limerick</h1>
    <p>From a five-minute tap fix to a full bathroom or boiler replacement — here's everything we do for homes and landlords across Limerick, Clare and the Mid-West.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <p class="lead">We're an RGI-registered plumbing and heating company based in Limerick. The list below is what we do day in, day out. If your job isn't on it, ring us anyway — chances are we cover it.</p>
    <div class="grid grid-3 mt-l">{cards}</div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <h2 class="mt-0">Why people in Limerick choose O'Sullivan</h2>
    <div class="grid grid-4 mt-l">
      <div class="card reveal"><h3>Honest quotes</h3><p>Fixed pricing in writing before any spanner comes out. No surprises on the invoice.</p></div>
      <div class="card reveal"><h3>Local team</h3><p>The person who quotes your job is usually the one who does it. No subcontractor lottery.</p></div>
      <div class="card reveal"><h3>Fully qualified</h3><p>RGI-registered, manufacturer-accredited, €6.5m insured. Certs available on request.</p></div>
      <div class="card reveal"><h3>Tidy work</h3><p>Dust sheets, clean-up at the end of every day, and a job site that looks better than we found it.</p></div>
    </div>
  </div>
</section>

{cta_banner(1)}
</main>
"""
    return head(title, desc, "/services/index.html", "/services/index.html", 1, jsonlds) + header_html(1, "services") + body + footer_html(1)


# ---------- Service pages ----------

SERVICE_PAGE_DATA = {
    "boiler-installation": {
        "title": "Boiler Installation Limerick | O'Sullivan Plumbing",
        "desc": "RGI-registered boiler installation across Limerick. Worcester, Ideal, Vaillant, Grant, Firebird. Up to 12-year warranty. SEAI-grant friendly. Free quotes.",
        "h1": "Boiler Installation in Limerick",
        "kw": "boiler installation",
        "intro": "Replacing a boiler is one of the bigger investments you'll make in your home — and one of the easiest to get wrong. We've been installing gas, oil and LPG boilers in Limerick homes for over 15 years, from 1970s semi-detached houses in Caherdavin to new builds in Castletroy. The right boiler, sized properly and installed cleanly, will quietly run for 12–15 years and shave a serious chunk off your heating bill. The wrong one will cost you for the rest of its life.",
        "included": [
            "Free, no-obligation home survey to size the boiler correctly for your property",
            "Honest written quote covering boiler, parts, labour and disposal of the old unit",
            "Supply and fit of a new condensing boiler from a brand we trust",
            "New magnetic system filter, programmer and thermostat where required",
            "Power flush of the existing system if needed (we'll tell you honestly if it isn't)",
            "Full commissioning, gas test, and Declaration of Conformance lodged with RGII",
            "Manufacturer warranty registration — up to 12 years depending on brand",
            "A walkthrough so you actually know how to use the thing",
        ],
        "section_title": "Boiler brands we fit in Limerick",
        "section_intro": "We're not tied to one manufacturer — we fit what's right for your home, budget and existing pipework. The brands below are the ones we trust to last.",
        "section_items": [
            ("Worcester Bosch", "Our most-installed gas boiler. Quiet, reliable, with up to 12-year warranty when fitted by accredited installers like us. Strong service network in Limerick."),
            ("Ideal", "Excellent value, especially the Logic+ range. UK-built, 10-year warranty options, easier to repair than some of the German brands when something does go wrong."),
            ("Vaillant", "Premium German engineering. The ecoTEC plus is a workhorse. Slightly higher upfront cost, very long service life."),
            ("Grant", "Irish-made oil boilers — the default in rural Limerick and Clare where mains gas isn't available. The Vortex range is genuinely excellent."),
            ("Firebird", "Another solid Irish oil-boiler manufacturer based in Cork. Good value, easy to service, parts widely available across the Mid-West."),
        ],
        "pricing_title": "How much does a new boiler cost in Limerick?",
        "pricing": "Honest answer: most boiler installations in Limerick fall between €1,800 and €3,500 fitted, depending on the brand, the size, and whether your existing system needs work. A like-for-like gas combi swap in a city semi might be €1,800–€2,400. A higher-spec system boiler with a new cylinder, controls and pipework upgrade in a four-bed in Castletroy or Raheen is more likely €2,800–€3,800. Oil boiler replacements (Grant, Firebird) typically run €2,200–€3,500 fitted. We don't quote sight-unseen — we come out, look at the job, and give you a fixed price in writing. No deposits, no surprises.",
        "extras_title": "SEAI grants and Better Energy Homes",
        "extras": "If you're upgrading from an older non-condensing boiler to a high-efficiency condensing model, you may qualify for an SEAI grant under the Better Energy Homes scheme. We'll talk you through eligibility (your home generally needs to be built before 2011 and the work needs a BER assessment) and we handle the paperwork. Most of our customers in Limerick and Clare end up getting between €700 and €3,500 back depending on the scope of the upgrade.",
        "faqs": [
            ("How long does a boiler installation take in Limerick?",
             "A straightforward gas combi swap in a Limerick home is usually a one-day job — in by 9am, hot water back on by tea-time. A full system change, new cylinder or oil boiler can run to two days. We'll always tell you up front."),
            ("Do you remove and dispose of the old boiler?",
             "Yes — included in every quote. The old boiler, packaging and any waste are taken away and disposed of responsibly. Your house is left as we found it."),
            ("What warranty do I get?",
             "Up to 12 years on Worcester Bosch when we fit it (we're accredited installers), 10 years on Ideal Logic+, 10 years on most Vaillant, and 5–10 years on Grant and Firebird oil boilers depending on the model. We register every install with the manufacturer so the warranty is on the record."),
            ("Will I need a power flush?",
             "Sometimes. If your existing system is old and full of sludge, fitting a new boiler without flushing the system will void the warranty and shorten the boiler's life. We test the system water during the survey and only recommend a flush if it's actually needed. See our <a href=\"power-flushing.html\">power flushing page</a> for more."),
            ("Can you install a smart thermostat at the same time?",
             "Yes — we fit Hive, Nest and most of the Worcester / Vaillant / Ideal app-based controls. Worth doing at the same time as the install rather than later."),
            ("Do you cover oil boilers in rural Limerick and Clare?",
             "Absolutely — most of our installs in west Limerick, Newcastle West, Adare and rural Clare are oil. Grant and Firebird are our go-to brands."),
        ],
        "areas": ["castletroy", "raheen", "dooradoyle", "ennis", "adare"],
        "related": ["boiler-servicing-repairs", "central-heating", "power-flushing"],
    },
    "boiler-servicing-repairs": {
        "title": "Boiler Service Limerick | Repairs & Annual Servicing",
        "desc": "Annual boiler service and same-day repairs across Limerick. RGI-registered, all major brands. Keep your warranty valid. From €85 for a service.",
        "h1": "Boiler Servicing &amp; Repairs in Limerick",
        "kw": "boiler service",
        "intro": "An annual boiler service costs about the same as a takeaway for the family — and it's the single best thing you can do for your heating bills, your warranty, and your safety. Most of the boiler emergencies we get called to in Limerick during a cold snap could have been avoided with a 60-minute service the previous summer. We service every major brand and we can usually be out within 48 hours.",
        "included": [
            "Full strip-down clean of the heat exchanger, burner and combustion chamber",
            "Combustion analysis and flue-gas test using calibrated equipment",
            "Pressure check and refill if needed",
            "System water quality test (sludge, inhibitor levels)",
            "Visual inspection of all gas pipework, flue and condensate run",
            "Gas tightness test on the meter",
            "Boiler service report and stamp on your warranty book",
            "Honest call-out if anything else needs attention — no pressure-selling",
        ],
        "section_title": "Common boiler problems we fix in Limerick homes",
        "section_intro": "After 15 years and a few thousand call-outs in Limerick, the same handful of issues come up again and again. Most are fixable in one visit.",
        "section_items": [
            ("Boiler losing pressure", "Usually a leaking radiator valve, expansion vessel issue, or a dripping pressure relief pipe outside the house. Easy to diagnose, usually a same-day fix."),
            ("No hot water but heating works (or vice versa)", "Almost always a diverter valve. Common on Worcester, Ideal and Vaillant combis around the 7-year mark. Standard part, standard repair."),
            ("Boiler kettling / banging noises", "Limescale or sludge in the heat exchanger. A descale or power flush usually sorts it. We'll tell you honestly if the boiler is worth saving."),
            ("F-codes and lockouts (F22, F28, EA, etc)", "Each manufacturer has its own fault codes. We carry the diagnostic tools and most common spares in the van."),
            ("Pilot light keeps going out", "Older non-condensing boilers — usually a thermocouple. Quick fix if parts are still available."),
            ("Frozen condensate pipe", "A Limerick winter classic. We thaw it, lag it, and re-route it if it's badly run."),
        ],
        "pricing_title": "How much does a boiler service cost in Limerick?",
        "pricing": "Standard annual gas boiler service in Limerick: <strong>from €85</strong> (single boiler, off-peak booking). Oil boiler service: <strong>from €110</strong> (oil services include a more thorough nozzle and electrode change). Repairs are quoted before we do them — most common faults (diverter valve, expansion vessel, PRV, pump) come out under €280 fitted. We'll never start work without giving you a price first.",
        "extras_title": "Should I service my boiler every year?",
        "extras": "Yes — and it's not just plumbers saying that to drum up work. Most manufacturer warranties (Worcester, Vaillant, Ideal) are conditional on annual servicing by a registered engineer. Skip a year and your warranty is technically void. Beyond that: a serviced boiler runs more efficiently (typically 5–8% lower gas usage), is safer (we test for CO leaks every visit), and lasts longer. The maths is in your favour every year.",
        "faqs": [
            ("How long does a boiler service take?",
             "Roughly 45–75 minutes for a gas boiler, 60–90 for oil. We don't rush it — a proper service takes time."),
            ("Do you service all boiler brands?",
             "Yes — Worcester Bosch, Ideal, Vaillant, Baxi, Glow-worm, Viessmann, Grant, Firebird, Warmflow, Riello and most others. If you're not sure, send us a photo of the front of the boiler."),
            ("My boiler is making a banging noise — is it dangerous?",
             "Usually no, but it's a sign the system needs attention. Kettling noises from limescale are the most common cause. Banging or vibration in the pipework can be air or pump issues. Either way, get it looked at sooner rather than later."),
            ("Can you service my boiler if it's still under warranty?",
             "Yes — and you'll need us (or another RGI engineer) to keep that warranty valid. We register every service so the manufacturer has a record."),
            ("What if you find something wrong during the service?",
             "We'll tell you what's wrong, what it'll cost to fix, and whether it's urgent or can wait. We never push repairs that aren't needed — most of our work comes from people we treated fairly years ago."),
        ],
        "areas": ["limerick-city", "castletroy", "raheen", "annacotty", "ennis"],
        "related": ["boiler-installation", "power-flushing", "landlord-gas-safety-cert"],
    },
    "bathroom-plumbing": {
        "title": "Bathroom Plumber Limerick | Installations & Refits",
        "desc": "Bathroom plumbing in Limerick — full installs, shower upgrades, en-suites and refits. Clean, careful work. Tile-ready and finished to a high standard.",
        "h1": "Bathroom Plumbing &amp; Installations in Limerick",
        "kw": "bathroom plumber",
        "intro": "A bathroom is the room you use first thing in the morning and last thing at night, every day, for the next 15 years. It's worth getting right. We do everything from a straight shower swap to a full bathroom strip-out and rebuild — including the joinery, tiling and electrics through trusted local trades. Most of our bathroom work is in Limerick city homes, the older estates in Raheen and Caherdavin, and the bigger family houses in Castletroy and Adare.",
        "included": [
            "Site visit and detailed written quote — fixed price, not estimates",
            "Strip-out and disposal of the existing bathroom",
            "First-fix plumbing: hot/cold supply, waste, vents, showers, baths",
            "Coordination of tiler, electrician and (if needed) plasterer through trades we've worked with for years",
            "Supply and fit of sanitaryware, taps, showers, towel rails, extractors",
            "Pressure-balanced or thermostatic showers — we recommend the right one for your water pressure",
            "Final commissioning, leak test, and a full clean down before we leave",
        ],
        "section_title": "Our bathroom process",
        "section_intro": "Bathrooms can feel daunting — they shouldn't. Here's how we run them, from the first phone call to handover.",
        "section_items": [
            ("1. Site visit", "We come out, look at the existing space, talk through what you want, and measure up. No charge for this."),
            ("2. Quote", "Fixed written quote with everything broken down — sanitaryware, tiles, labour. You see what each part costs."),
            ("3. Design (if needed)", "If you're starting from scratch, we'll suggest layouts that work with your pipework and joists. We'll often save you money by not moving things that don't need moving."),
            ("4. Strip-out", "Old bathroom out, waste skipped or removed. We protect floors and stair carpets on the way in and out."),
            ("5. First fix", "Pipework, wiring, ventilation and any structural changes done. Rooms boarded for tiling."),
            ("6. Tiling and second fix", "Walls and floor tiled (we use tilers we've worked with for over a decade). Then we fit the suite, taps, shower, screen and accessories."),
            ("7. Snag and handover", "We test everything, walk you through the controls, and clean up. Most bathrooms take 7–12 working days end-to-end."),
        ],
        "pricing_title": "How much does a new bathroom cost in Limerick?",
        "pricing": "Roughly: a basic bathroom refit (existing layout, mid-range suite, decent tiles) in a Limerick semi is <strong>€6,500–€9,500</strong> all-in. A larger family bathroom with a separate shower enclosure, freestanding bath and quality fittings: <strong>€10,000–€15,000</strong>. Full luxury bathrooms with underfloor heating, tiled showers and high-end brassware: <strong>€15,000+</strong>. Where you spend the money matters more than how much: a great shower valve and a proper extractor will outlast and outperform fancy taps every time. We'll tell you honestly where to splash and where to save.",
        "extras_title": "Showers, water pressure and Limerick water",
        "extras": "Limerick's mains water pressure is generally very good (better than a lot of Dublin), but older houses with hot water cylinders sometimes have low hot pressure on the upstairs shower. Before we recommend a thermostatic mixer or rainfall head, we test your actual pressure and flow. If pressure is low, we'll often suggest fitting a small pump or an unvented cylinder rather than fighting the symptoms. Get this right at the start and you'll have a great shower for the next 15 years.",
        "faqs": [
            ("How long does a full bathroom take?",
             "Typical bathroom refit is 7–10 working days, including tiling. A small en-suite can be 5 days. Full luxury bathrooms with underfloor heating run to 2–3 weeks."),
            ("Can I supply my own sanitaryware?",
             "Yes — many customers buy their own suite from showrooms in Limerick or online. We'll fit it. Just check the spec works with your water pressure before you order."),
            ("Do you handle the tiling and electrics?",
             "Yes — through trades we've used for over a decade. You get one point of contact (us) and one quote covering everything."),
            ("Can you fit an electric shower?",
             "Of course. Worth knowing: electric showers have lower flow than mixer showers, and they need a dedicated supply. We'll talk you through whether it's the right call for your house."),
            ("What about wet rooms?",
             "We do them. Wet rooms need a properly tanked floor and a tiled gradient — done right, they last decades. Done badly, they leak. Worth using someone who's done a few."),
        ],
        "areas": ["castletroy", "raheen", "dooradoyle", "limerick-city", "adare"],
        "related": ["general-plumbing", "central-heating", "emergency-plumber"],
    },
    "emergency-plumber": {
        "title": "Emergency Plumber Limerick | 24/7 Call-Out",
        "desc": "24-hour emergency plumber in Limerick. Burst pipes, leaks, no heat, no hot water — fast response across Limerick city, county, Clare and Tipperary.",
        "h1": "Emergency Plumber in Limerick — 24/7",
        "kw": "emergency plumber",
        "intro": "Plumbing emergencies don't keep office hours. A burst pipe at 11pm, no heat on the coldest weekend of the year, a tank leaking through the kitchen ceiling — these are the calls we live for. We run a genuine 24/7 emergency line covering Limerick city, county Limerick, most of Clare and parts of Tipperary. Most call-outs are with you within 60–90 minutes, and we'll always tell you straight if it's something you can hold off until morning.",
        "included": [
            "Genuine 24/7 phone line — picked up by a real person, not a call centre",
            "Fully-stocked emergency van: every common spare, isolation valves, pipe repair kits",
            "Same-night fix for the vast majority of call-outs",
            "Honest emergency pricing — quoted on the phone before we travel",
            "If we can't fix it tonight, we make it safe and book a return visit at no extra call-out fee",
        ],
        "section_title": "The emergencies we get called to most in Limerick",
        "section_intro": "If you're reading this with water coming through the ceiling, scroll to the call-out details at the bottom of the page. Otherwise — these are the most common calls we take.",
        "section_items": [
            ("Burst pipe", "Most common in cold snaps after a thaw. Step one: turn off the mains stopcock (usually under the kitchen sink). Step two: ring us. We'll be there fast."),
            ("Leaking hot water cylinder", "Often a slow leak that suddenly gets worse. Turn off the water supply to the cylinder and the immersion if you have one. Don't keep using hot water."),
            ("No heat or hot water", "Could be a pressure drop, a frozen condensate, a pump fault or a board failure. We carry the parts to fix 90% of these on the first visit."),
            ("Blocked drain or toilet (overflowing)", "Stop using the system, lift any external drain covers if you can, and ring us. Most blockages are clearable on the night."),
            ("Gas leak (smell of gas)", "Don't ring us first — ring Gas Networks Ireland on <strong>1800 20 50 50</strong>. They'll make it safe. Then ring us to repair the leak and reinstate."),
            ("Pressure relief valve overflowing", "Common on combi boilers. Usually means an expansion vessel issue. We'll get it back working and explain whether it's a quick fix or warning of bigger problem."),
        ],
        "pricing_title": "How much does an emergency plumber cost in Limerick?",
        "pricing": "We're upfront on the phone, every time. Standard emergency call-out (evenings and weekends within Limerick city): <strong>€90 call-out + €75/hour</strong> labour. After midnight or on bank holidays: higher rate, but we'll tell you exactly what before we travel. Most emergencies are resolved in 1–2 hours of labour plus parts. We don't pad jobs and we don't drag out repairs — your trust is worth more to us than the extra hour.",
        "extras_title": "What you can do before we arrive",
        "extras": "First, turn off the water at the mains stopcock — it's usually under the kitchen sink, and turning it clockwise stops the supply. For a leaking cylinder, also turn off the cold supply going in (usually a valve on top). For any electrical proximity to water, switch the affected circuit off at the consumer unit. Then put a bowl down, a towel on the floor, and ring us. If you're not sure what to turn off, ring us anyway and we'll talk you through it.",
        "faqs": [
            ("How fast can you actually be here?",
             "In Limerick city, most call-outs are with you in 30–60 minutes. Castletroy, Raheen, Dooradoyle, Caherdavin: 30–45 minutes typically. Ennis, Shannon, Adare, Nenagh: 45–75 minutes. We'll always give you a real ETA on the phone."),
            ("Do you really answer the phone at 3am?",
             "Yes — the emergency line goes to a phone in the house. If we're already on a call-out, we'll get back to you within 15 minutes."),
            ("Will I pay more for a Saturday or weekend call-out?",
             "Yes, slightly. Saturday daytime is normal rates. Saturday evening, Sunday, and bank holidays are higher. We'll quote you on the phone before we move."),
            ("What if you can't fix it tonight?",
             "We make it safe (turn off water, isolate the gas, etc.) so the property isn't at risk, then book a return visit at no further call-out fee. Genuine emergencies first, then a proper fix in daylight if needed."),
            ("Should I ring you or my insurance first?",
             "Stop the damage first — ring us. Most home insurance policies in Ireland cover emergency plumber call-outs (it's worth checking your policy). We can give you a written invoice for any claim."),
        ],
        "areas": ["limerick-city", "castletroy", "raheen", "dooradoyle", "ennis"],
        "related": ["boiler-servicing-repairs", "general-plumbing", "central-heating"],
    },
    "central-heating": {
        "title": "Central Heating Limerick | Installation & Upgrades",
        "desc": "Central heating in Limerick — new systems, radiator installs, smart heating controls and zoning. RGI-registered, SEAI grant friendly. Free quotes.",
        "h1": "Central Heating in Limerick",
        "kw": "central heating",
        "intro": "A well-designed central heating system is invisible — it just keeps the house warm at the right times for the lowest possible cost. A badly designed one fights you on the bill every month. We install new central heating systems, upgrade existing ones, fit smart controls and add zoning to homes across Limerick. If your heating is old, slow to warm up, or unevenly heating the house, there's almost always a worthwhile fix.",
        "included": [
            "Heat-loss calculation to size the boiler and radiators correctly",
            "Supply and fit of radiators (steel panel, designer, towel rails)",
            "Pipework — copper or PEX with proper insulation in cold spaces",
            "Pumps, motorised valves, expansion vessels, system filters",
            "Smart controls and thermostats: Hive, Nest, Worcester, Vaillant, Honeywell evohome",
            "Heating zoning (upstairs/downstairs, or per room with TRVs)",
            "System balancing — actually balanced, not just \"on\"",
            "Power flush of existing system if upgrading rather than replacing",
        ],
        "section_title": "What a heating upgrade actually means",
        "section_intro": "\"Central heating\" covers a lot. Here's what we typically do, depending on what you've got.",
        "section_items": [
            ("New system from scratch", "For new builds and extensions, or homes converting from electric/storage heaters. Boiler, radiators, pipework, controls — all designed and installed together."),
            ("Boiler-only swap", "When the radiators and pipework are sound but the boiler is at the end of its life. See our <a href=\"boiler-installation.html\">boiler installation page</a>."),
            ("Radiator replacement", "Old single-panel radiators are inefficient. Modern double-panels with TRVs heat the room faster on less gas. Worth doing room-by-room over time."),
            ("Smart controls", "If you're still on a 1990s analogue programmer, you're heating an empty house every weekday. Smart thermostats pay for themselves inside two years."),
            ("Zoning", "Splitting the house into independently controlled zones (upstairs/downstairs at minimum) is one of the best efficiency upgrades there is, especially in larger homes."),
            ("Power flush", "If the system's full of sludge, no amount of new boiler will make it run well. See our <a href=\"power-flushing.html\">power flushing page</a>."),
        ],
        "pricing_title": "How much does central heating cost in Limerick?",
        "pricing": "Highly variable — but to give you the shape: a full new gas central heating system in a 3-bed semi (boiler, 8 radiators, pipework, controls) typically runs <strong>€6,500–€9,500</strong>. An oil equivalent is similar. Adding zoning and smart controls to an existing system: <strong>€800–€1,800</strong>. Replacing a single radiator with a modern double-panel: <strong>€280–€450 fitted</strong>. We always survey first and quote in writing — no \"from\" prices that mysteriously double on the day.",
        "extras_title": "SEAI grants for heating upgrades",
        "extras": "If you're upgrading to a high-efficiency system or adding heating controls to a pre-2011 home, you may qualify for SEAI Better Energy Homes grants. Heating controls upgrades alone can attract €700+ in grants. We're familiar with the BER assessment requirements and can recommend the contractor list. Most of our customers in Limerick and Clare get the grant approved without issue.",
        "faqs": [
            ("Should I switch from oil to gas (or vice versa)?",
             "Depends on your house and location. In Limerick city and the larger commuter areas (Castletroy, Raheen, Annacotty), mains gas is usually cheaper to run and more convenient. In rural Limerick, Clare and Tipperary, oil is often the only option. We'll be honest about which makes sense for you."),
            ("Is a heat pump worth it?",
             "Sometimes. Heat pumps work brilliantly in well-insulated homes with underfloor heating and oversized radiators. They struggle in older, poorly insulated houses unless you upgrade those things first. We're happy to advise."),
            ("What's the difference between TRVs, zoning, and smart controls?",
             "TRVs control individual radiators. Zoning controls groups of rooms with separate thermostats. Smart controls add scheduling and remote/app control. They stack — combine all three for maximum control and efficiency."),
            ("How long does a full heating install take?",
             "Typical 3-bed semi: 3–5 working days. Larger houses or full pipework re-runs: 5–10 days. We minimise downtime — usually you'll have heat back at the end of every day."),
            ("Will the new system be much quieter?",
             "Yes — modern condensing boilers are dramatically quieter than even 10-year-old units. Properly balanced systems also eliminate radiator clanking and pipe knocking."),
        ],
        "areas": ["castletroy", "annacotty", "raheen", "ennis", "newcastle-west"],
        "related": ["boiler-installation", "power-flushing", "general-plumbing"],
    },
    "general-plumbing": {
        "title": "Plumber Limerick | General Plumbing & Repairs",
        "desc": "Local Limerick plumber for everyday plumbing — leaks, taps, toilets, water pressure, hot water cylinders. Honest pricing, fast turnaround. RGI-registered.",
        "h1": "General Plumber in Limerick",
        "kw": "plumber Limerick",
        "intro": "Not every job is a new boiler or a full bathroom. Most days we're sorting the everyday plumbing problems that every Limerick home throws up sooner or later — a tap that won't stop dripping, a toilet that runs all night, a hot water cylinder that's lost its puff, low pressure in the upstairs shower, a radiator that won't heat. None of these are exciting, all of them are easy to put off, and all of them quietly cost you money or aggravation until they're fixed.",
        "included": [
            "Leak detection and repair — visible and hidden",
            "Tap replacements (kitchen, bathroom, garden)",
            "Toilet repairs and full unit replacements",
            "Hot water cylinder repairs and replacements",
            "Immersion heater fitting and fault diagnosis",
            "Water pressure issues — diagnosis, pumps, pressure-reducing valves",
            "Radiator bleeding, replacement, and repositioning",
            "Outside taps, garden plumbing, washing machine fits",
            "Stopcock and isolation valve installs (recommended for every home)",
        ],
        "section_title": "Common plumbing jobs we do every week in Limerick",
        "section_intro": "These are the calls we get over and over — and most are quick fixes.",
        "section_items": [
            ("Dripping tap", "Almost always a worn cartridge or washer. €60–€90 fitted in most cases. Don't ignore it — a single dripping tap wastes about 60 litres of (usually heated) water a week."),
            ("Running toilet", "Either the inlet valve is sticking or the flush valve is leaking. Quick parts replacement, usually €70–€110."),
            ("Low water pressure", "Could be the mains, the cylinder, a stopcock half-shut for years, or a partially-blocked pipe. We diagnose first, fix second."),
            ("Hot water issues", "Hot but not very hot? Cylinder thermostat or immersion. No hot at all? Boiler or cylinder. We sort all of it."),
            ("Cold radiator at the top", "Air in the system. Bleed it. If it keeps happening, you've got a bigger issue (usually a microleak or a sludge problem)."),
            ("Burst flexible hose under the sink", "Common in Limerick kitchen units — flexis fail with age. €50–€80 to swap. While we're there, we'll often fit isolation valves so you can change taps yourself in future."),
        ],
        "pricing_title": "How much does a Limerick plumber cost?",
        "pricing": "Standard call-out (Mon–Fri daytime, Limerick city and surrounding areas): <strong>€85 first hour</strong>, then <strong>€65 per hour</strong> after that, plus parts at honest cost. Most general plumbing jobs (taps, toilets, leaks) are completed inside the first hour. We don't charge a separate \"call-out fee\" on top — the first hour includes the visit. Quotes are always given before work starts.",
        "extras_title": "Why a small plumbing fix today saves a big one later",
        "extras": "Plumbing problems compound. A slow leak under a sink rots the unit and the floor. A failing flexi-hose eventually bursts when you're at work. A cylinder limping along eventually fails on a Sunday. Most of the emergency call-outs we run could have been a €90 daytime fix the previous month. If something doesn't seem right, get it looked at — we're rarely the most expensive part of a problem caught early.",
        "faqs": [
            ("Do you do small jobs?",
             "Yes — there's no minimum. A €70 tap swap is just as welcome as a €5,000 bathroom. Lots of our long-term customers started with us on a small job."),
            ("Will you give me a fixed price over the phone?",
             "For straightforward jobs (tap swap, toilet repair, single radiator) — usually yes. For anything that needs eyes on (leaks, pressure issues, hidden problems) we'll come out, look, and quote in writing before starting."),
            ("Do you fit customer-supplied parts?",
             "We do, with one caveat: we can't warranty the part itself if it fails (the warranty is between you and the supplier). For high-stress items like shower valves and taps, we usually recommend you buy through us — we get trade prices and stand over the part."),
            ("How long do I wait for a non-emergency appointment?",
             "Usually 2–5 working days. Same week, almost always."),
            ("What areas do you cover for general plumbing?",
             "Limerick city and county is our main patch. Most of Clare (especially Ennis, Shannon, Newcastle West). Adare, Nenagh and parts of north Tipperary. Outside that, ring us — we'll do our best."),
        ],
        "areas": ["limerick-city", "castletroy", "raheen", "caherdavin", "ennis"],
        "related": ["emergency-plumber", "boiler-servicing-repairs", "bathroom-plumbing"],
    },
    "power-flushing": {
        "title": "Power Flushing Limerick | Central Heating Flush",
        "desc": "Power flushing in Limerick — restore central heating efficiency, fix cold radiators and protect your boiler. From €450 fully fitted. RGI-registered.",
        "h1": "Power Flushing in Limerick",
        "kw": "power flushing",
        "intro": "If you've got cold spots at the bottom of your radiators, slow-warming heating, banging or kettling noises from the boiler, or rusty water when you bleed a radiator — your system is full of magnetite sludge. It's the same in three out of every four older homes we go into in Limerick. A power flush is the way you get rid of it, and it's one of the highest-return jobs you can do on an older heating system. Restored efficiency, longer boiler life, valid warranty if you've just installed a new boiler.",
        "included": [
            "Connection of professional flushing rig (Kamco or similar) to the system",
            "Chemical treatment to break up sludge and limescale across all radiators",
            "Flush of every radiator individually with high-flow rates and direction reversal",
            "Final clean water test until the discharge runs clear",
            "Addition of a quality system inhibitor (usually Sentinel X100) to protect against future sludge",
            "Fitting of a magnetic system filter if one isn't already there (we strongly recommend it)",
            "Pre- and post-flush temperature readings on each radiator so you can see the difference",
        ],
        "section_title": "Signs your system needs a power flush",
        "section_intro": "If two or more of these ring true, it's almost certainly worth getting the system flushed.",
        "section_items": [
            ("Cold spots at the bottom of radiators", "Hot at the top, cold along the bottom — classic sludge buildup."),
            ("Some radiators don't heat or take ages to warm", "Sludge restricts flow. The radiators furthest from the boiler suffer first."),
            ("Banging, kettling or whistling noises from the boiler", "Sludge in the heat exchanger causing localised boiling."),
            ("Rusty / black / brown water when bleeding a radiator", "That's the sludge. Clear or light grey water is fine."),
            ("System pressure dropping repeatedly", "Sometimes related — sludge can hide leaks and damage pumps."),
            ("Recent boiler install with sludge in the old system", "If you didn't flush before fitting a new boiler, the warranty is probably void and the new boiler will fail early."),
        ],
        "pricing_title": "How much does a power flush cost in Limerick?",
        "pricing": "Typical Limerick home flushes: <strong>€450 for up to 8 radiators</strong>, <strong>€550 for 9–12 radiators</strong>, <strong>€650+ for larger homes</strong>. Includes chemical treatment, full flush, inhibitor and (where needed) a new magnetic filter (€80–€120 fitted). A power flush typically takes 4–6 hours on a standard 3-bed home. It's one of the best-value jobs you can do on an older system — the gas savings alone usually pay for it inside two heating seasons.",
        "extras_title": "When a flush isn't the answer",
        "extras": "Sometimes a flush won't help — and we'll tell you straight. If you've got a microleak, a damaged radiator, a failed pump or a system that's so old the pipework itself is corroded internally, a flush is throwing good money after bad. We always test the system first. If the answer is a different fix, we'll quote that instead. We'd rather lose a flush job than do one that doesn't help you.",
        "faqs": [
            ("How long does a power flush take?",
             "Most Limerick homes: 4–6 hours. Bigger systems (large family homes in Castletroy or rural homes in Clare): 6–8 hours."),
            ("Can I do it myself with one of those chemicals from the hardware shop?",
             "Pouring a sludge remover into the system and running the heating for a week (\"chemical flush\") helps a bit, but it doesn't actually move the sludge out — it just breaks it up. A power flush physically pumps it out. There's no comparison."),
            ("Will it damage my radiators?",
             "If your radiators are sound, no — modern flushing equipment runs at relatively gentle pressure. Very old, corroded radiators can sometimes spring leaks during a flush — but if a flush would expose them, they were probably about to leak anyway."),
            ("Do I need a flush if I'm getting a new boiler?",
             "Almost always yes. Manufacturer warranties (Worcester, Vaillant, Ideal) all require the system to be flushed and treated with inhibitor when a new boiler is fitted. Skip it and the warranty is void."),
            ("How often should it be done?",
             "If your system has a magnetic filter and you keep up with annual services, possibly never again. If neither of those, every 6–8 years is a sensible interval for an older system."),
        ],
        "areas": ["castletroy", "raheen", "caherdavin", "ennis", "limerick-city"],
        "related": ["boiler-installation", "boiler-servicing-repairs", "central-heating"],
    },
    "landlord-gas-safety-cert": {
        "title": "Landlord Gas Safety Cert Limerick | RGI Registered",
        "desc": "Landlord gas safety certificates in Limerick. RGI-registered, fast turnaround, certs in your inbox same day. From €95. Multi-property discounts.",
        "h1": "Landlord Gas Safety Certificates in Limerick",
        "kw": "landlord gas safety cert",
        "intro": "If you let a property in Ireland with a gas appliance, you're legally required to have a gas safety inspection done by an RGI-registered installer at least every two years. We do landlord gas safety certs across Limerick and Clare every week — boiler, hob, fire, full appliance check, and a Declaration of Conformance / Gas Installer Report in your inbox the same day. Multi-property landlords get a discount and a single point of contact.",
        "included": [
            "Inspection of every gas appliance in the property (boiler, hob, fire, instant water heater)",
            "Combustion analysis on the boiler",
            "Full gas tightness test on the system",
            "Visual inspection of all visible pipework, ventilation and flue",
            "CO test in the rooms with appliances",
            "Identification and reporting of any gas safety issues",
            "Issued Gas Installer Report (GIR) / Declaration of Conformance",
            "Digital cert emailed to landlord and (if required) tenant",
        ],
        "section_title": "What landlords in Limerick need to know",
        "section_intro": "The legal and practical bits, in plain English.",
        "section_items": [
            ("Who has to have one?", "Any landlord letting a residential property with a gas installation. The law applies to all rental properties in Ireland, including HAP, RAS and short-term lets."),
            ("How often?", "At least every two years. We strongly recommend annually — it's cheap insurance and matches most boiler-warranty service requirements."),
            ("Who can do it?", "Only an RGI-registered installer. We are. RGI Reg. No. {RGI}."),
            ("What if there's a problem?", "We tell you immediately, write up a quote for any remedial work, and only re-issue the cert when the issues are fixed. Most issues are minor (loose ventilation cover, slightly out-of-spec combustion) and same-visit fixable."),
            ("Tenant access", "We can liaise directly with tenants to book the visit — saves you the back-and-forth. We just need their phone number."),
            ("Multi-property landlords", "Most of our landlord customers have 2–10 properties across Limerick and Clare. We offer a flat per-property rate and route them efficiently — usually a half-day covers 4–5 properties if they're clustered."),
        ],
        "pricing_title": "Limerick landlord gas cert pricing",
        "pricing": "Single property gas safety cert in Limerick: <strong>from €95</strong> (boiler only). Property with boiler + hob: <strong>€115</strong>. Multi-property landlords: <strong>€85 per property</strong> for 3+ properties booked together. If a service is due at the same time, we combine it for €165 (cert + full annual boiler service). Cert is emailed in PDF the same day as the inspection.",
        "extras_title": "Combine cert + service and save",
        "extras": "Most boiler manufacturer warranties require an annual service to stay valid — and the gas cert covers most of the same checks. We can do both in the same visit for a combined price that's cheaper than booking each separately. Worth doing on every rental property each year. If you've got tenants in for the long haul, an annual service also keeps the boiler running efficiently — fewer breakdowns, fewer angry calls.",
        "faqs": [
            ("How long does a gas safety inspection take?",
             "Single-boiler property: 30–45 minutes. With additional appliances (hob, fire): 45–75 minutes. We work around tenants' schedules."),
            ("Can I get an RGI cert if my property is in Ennis or Shannon?",
             "Yes — we cover all of Limerick, most of Clare (Ennis, Shannon, Newcastle West) and into Tipperary (Nenagh). Same flat-rate pricing."),
            ("What's the difference between an RGI cert and a Boiler Service?",
             "Different things. The RGI cert is a legal compliance check on every gas appliance in the property. A boiler service is a more in-depth strip-and-clean of the boiler itself. We can do both in one visit for a combined fee."),
            ("Do you do oil systems?",
             "Yes — we issue OFTEC compliance and service certs for oil boilers in rental properties. Same flat-rate pricing as gas."),
            ("What happens if you find an issue?",
             "We quote any remedial work before we do it. Most fixes are minor and same-visit. If the issue is more serious (e.g. a flue that doesn't meet current standards), we'll explain the options. We don't issue a cert for a system we wouldn't be happy with in our own home."),
        ],
        "areas": ["limerick-city", "castletroy", "ennis", "shannon", "annacotty"],
        "related": ["boiler-servicing-repairs", "boiler-installation", "general-plumbing"],
    },
}


def service_page(slug: str) -> str:
    data = SERVICE_PAGE_DATA[slug]
    name_pretty = next(s[1] for s in SERVICES if s[0] == slug)
    depth = 1
    title = data["title"]
    desc = data["desc"]
    canonical = f"/services/{slug}.html"
    crumbs = [("Home", "/"), ("Services", "/services/index.html"), (name_pretty, canonical)]

    jsonlds = [
        local_business_jsonld(),
        breadcrumb_jsonld(crumbs),
        service_jsonld(name_pretty, desc),
        faq_jsonld(data["faqs"]),
    ]

    included_html = "".join(f"<li>{x}</li>" for x in data["included"])
    section_items_html = "".join(
        f"<div class=\"card\"><h3>{title_}</h3><p>{body_}</p></div>"
        for title_, body_ in data["section_items"]
    )
    faqs_html = "".join(
        f'<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in data["faqs"]
    )

    related_links = "".join(
        f'<li><a href="{rel}.html">{next(s[1] for s in SERVICES if s[0] == rel)} in Limerick</a></li>'
        for rel in data["related"]
    )
    area_links = "".join(
        f'<li><a href="../areas/{a}.html">Plumber in {next(x[1] for x in AREAS if x[0] == a)}</a></li>'
        for a in data["areas"]
    )

    body = f"""
<main id="main">
{breadcrumbs_html([("Home", "index.html"), ("Services", "services/index.html"), (name_pretty, f"services/{slug}.html")], 1)}

<section class="page-hero">
  <div class="container">
    <h1>{data["h1"]}</h1>
    <p>{desc}</p>
    <div class="page-hero-ctas">
      <a class="btn btn-primary" href="../contact.html">Get a free quote</a>
      <a class="btn btn-outline-light" href="tel:{PHONE_TEL}">Call {PHONE}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="layout-cols">
      <article class="article">
        <p class="lead">{data["intro"]}</p>

        <h2>What's included</h2>
        <ul>{included_html}</ul>

        <h2>{data["section_title"]}</h2>
        <p>{data["section_intro"]}</p>
        <div class="grid grid-2 mt-l">{section_items_html}</div>

        <h2>{data["pricing_title"]}</h2>
        <p>{data["pricing"]}</p>

        <h2>{data["extras_title"]}</h2>
        <p>{data["extras"]}</p>

        <h2>Frequently asked questions</h2>
        {faqs_html}

        <h2>Areas we cover for {name_pretty.lower()}</h2>
        <p>We cover all of Limerick city and county, most of Clare and into north Tipperary. Some popular areas:</p>
        <ul>{area_links}</ul>

        <h2>Related services</h2>
        <ul>{related_links}</ul>
      </article>

      <aside class="sidebar">
        <h3>Get a free quote</h3>
        <p>Tell us a bit about the job and we'll come back within the hour.</p>
        <p><a class="btn btn-primary" style="width:100%;" href="../contact.html">Request a quote</a></p>
        <p style="margin-top:12px;"><a class="btn btn-outline" style="width:100%;" href="tel:{PHONE_TEL}">{PHONE}</a></p>
        <h3 style="margin-top:32px;">Why us</h3>
        <ul>
          <li>RGI registered ({RGI})</li>
          <li>15+ years experience</li>
          <li>Fixed written quotes</li>
          <li>€6.5m insured</li>
          <li>5.0 stars on Google</li>
        </ul>
      </aside>
    </div>
  </div>
</section>

{cta_banner(1)}
</main>
"""
    return head(title, desc, canonical, canonical, 1, jsonlds) + header_html(1, "services") + body + footer_html(1)


# ---------- Area pages ----------

AREA_PAGE_DATA = {
    "limerick-city": {
        "title": "Plumber Limerick City | O'Sullivan Plumbing",
        "desc": "Local plumber in Limerick city — boiler installs, emergency call-outs, bathrooms and central heating. RGI-registered. Fast response across the city.",
        "intro": "Limerick city is our home. We grew up here, we work here, and most of our weekly call-outs are inside the city limits. From the Georgian houses on the Crescent to the apartments in the Riverpoint area to the family homes around the South Circular Road and the King's Island estates, we know the housing stock and we know the quirks. The city's older terraces in particular have plenty of character — and plenty of original cast-iron pipework, lead supply pipes that need swapping out, and 40-year-old back-boilers tucked into chimney breasts that should have been replaced a decade ago.",
        "specifics": "If you're in a Georgian or Victorian property in the city, expect us to look carefully at your supply pipework — many city homes still have lead or galvanised steel mains pipes. Replacement isn't legally required but it's a good idea, and Irish Water will sometimes contribute. Newer apartments in town tend to have combi boilers and shared utility spaces, which we work in regularly. The river-facing properties around Honan's Quay and Steamboat Quay can have higher-than-average humidity issues — venting and proper extractor specs matter more here than further out.",
        "why_local": "Being city-based means we're often with you within 30 minutes for emergencies. Most of our parts van runs straight off the Dublin Road and Ballysimon, so even unusual spares are usually a short trip away. We also work with several letting agents in the city for landlord gas safety certs and turnaround inspections.",
        "review": ("Sorted a hot water cylinder for us in a 1920s house off the Ennis Road — explained everything, didn't try to sell us anything we didn't need, and was finished by lunchtime. Top class.", "Mark T., Limerick city"),
        "nearby": ["castletroy", "raheen", "caherdavin"],
    },
    "castletroy": {
        "title": "Plumber Castletroy, Limerick | O'Sullivan Plumbing",
        "desc": "RGI-registered plumber in Castletroy — boiler installs, repairs, bathrooms and emergency call-outs. Fast local response across UL, Annacotty and Plassey.",
        "intro": "Castletroy is one of the busiest patches we cover — between the long-established estates around Plassey and Monaleen, the newer developments off the Dublin Road, and the constant student population around the University of Limerick, there's always something going on. Most of the housing stock here is from the 1990s onwards, which means modern condensing boilers, sealed systems, and copper or PEX pipework throughout. Easier to work on than the older city houses, and most jobs here are quick.",
        "specifics": "The newer estates around Castletroy and Monaleen tend to have the same handful of boilers — Worcester Bosch and Ideal combis dominate, with a few Vaillant ecoTECs in the higher-end builds. We carry common spares for all of them in the van. Larger family homes off the Castletroy Park Road and around the Plassey Park area often have system boilers with hot water cylinders, which is where most of the calls about \"showers go cold halfway through\" come from. Almost always a thermostat or zone valve issue, easy fix.",
        "why_local": "We're 5–15 minutes away from anywhere in Castletroy. Burst pipe at midnight in Monaleen? We can be there before the floor is wet. We also do a lot of landlord and rental work in the area — if you've got a property near UL that's let to students, we offer fast turnaround inspection and gas cert services.",
        "review": ("Boiler died on a Friday evening with the in-laws coming the next day. Job got bumped up the queue, was sorted by 11am Saturday. The kind of service you can't put a price on.", "Niamh K., Castletroy"),
        "nearby": ["annacotty", "limerick-city", "raheen"],
    },
    "raheen": {
        "title": "Plumber Raheen, Limerick | O'Sullivan Plumbing",
        "desc": "Plumber in Raheen, Limerick — boilers, bathrooms, central heating, emergencies. RGI-registered, fast response. Covering Raheen, Mungret and Dooradoyle.",
        "intro": "Raheen is a stable, well-established part of Limerick — a mix of older 1970s/80s estates, larger detached homes, and the newer developments around the Mungret and Dooradoyle borders. We've worked in dozens of houses across Raheen Park, Bawnmore, Castle Park and the streets around the hospital. Most of the heating systems we see here are 15–25 years old and starting to show their age — boilers nearing end of life, radiators with sludge buildup, and original showers that never really worked properly. There's a lot of value in modernising these systems, and SEAI grants often apply.",
        "specifics": "A lot of Raheen homes have system boilers with hot water cylinders in the hot press — very different from the city centre's combi-dominated mix. The good news is system boilers usually outlast combis and give better hot water performance for larger families. The bad news is the cylinders themselves wear out, and 25-year-old immersions are everywhere. We replace cylinders, immersions and zone valves regularly. The newer houses out toward Mungret tend to have unvented (mains-pressure) cylinders — which we also fit and service routinely.",
        "why_local": "Raheen is a 10–15 minute drive from us at any time of day. We're regularly in and out for boiler services, bathroom upgrades and emergency call-outs. The University Hospital Limerick brings a lot of evening shift workers in the area — we do a lot of out-of-hours services for staff who can't get tradespeople during the day.",
        "review": ("Did a full bathroom for us — pulled out a 1980s avocado disaster and replaced it with something we're actually proud of. Tidy work, cleaned up every evening, finished on schedule. Best money we've spent on the house.", "Donal M., Raheen"),
        "nearby": ["dooradoyle", "limerick-city", "adare"],
    },
    "dooradoyle": {
        "title": "Plumber Dooradoyle, Limerick | O'Sullivan Plumbing",
        "desc": "Local Limerick plumber covering Dooradoyle — boiler installation, repairs, bathrooms and emergencies. RGI-registered, honest pricing, fast response.",
        "intro": "Dooradoyle is mostly mature housing — solid 1970s and 1980s estates around the Crescent Shopping Centre and out toward the hospital. The houses are well-built but their plumbing and heating systems are increasingly hitting end-of-life. Most of our calls in Dooradoyle are boiler replacements, system upgrades, bathroom refits and the occasional cylinder replacement. The good news with houses of this era is that the pipework is generally sound copper — we rarely have to re-pipe an entire house.",
        "specifics": "A consistent pattern in Dooradoyle: original Worcester or Potterton system boilers from the 1990s/2000s installed in airing cupboards or utility rooms, hot water cylinders in the hot press, and 8–10 single-panel radiators that have lost a lot of their efficiency. We replace boilers like-for-like (system to system, often Worcester Bosch Greenstar 30CDi), or we'll quote on going over to a combi if the household is now smaller and a combi makes sense. Bathrooms are another big one — many original Dooradoyle bathrooms have never been touched.",
        "why_local": "Dooradoyle is right beside Raheen — most days we're already in the area. Response times for emergencies are typically 20–30 minutes. Plenty of our customers in Dooradoyle came to us after a poor experience with one of the bigger national plumbing companies — we keep things personal, and the same person who quotes is the one who shows up.",
        "review": ("Replaced our 25-year-old boiler and sorted out radiators that had never properly heated. House warms up in half the time and the gas bill is noticeably lower. Couldn't recommend higher.", "Catherine R., Dooradoyle"),
        "nearby": ["raheen", "limerick-city", "adare"],
    },
    "caherdavin": {
        "title": "Plumber Caherdavin, Limerick | O'Sullivan Plumbing",
        "desc": "Plumber in Caherdavin and Ennis Road, Limerick — boilers, bathrooms, emergency call-outs. RGI-registered, local, fast response.",
        "intro": "Caherdavin and the wider Ennis Road area is one of the most consistent patches we work — mostly mature 1970s, 80s and 90s housing, with a real mix of system types. Plenty of older Worcester, Potterton and Vaillant boilers, hot water cylinders that have seen better days, and bathrooms that are due an update. There's also been a fair bit of new development around the Coonagh Cross area in the last decade — modern combi boilers, sealed systems, and the usual handful of small-but-annoying issues that come with newer estates.",
        "specifics": "Caherdavin houses with their original 1980s heating systems often have hard-water scaling on the heat exchangers (Limerick water is moderately hard, not as bad as the east coast but enough to matter). We see a lot of kettling, slow-warming radiators and drop-off in hot water performance. A power flush plus a new magnetic filter usually transforms these systems — we can talk you through whether it's worth doing or whether you're better off replacing the boiler entirely.",
        "why_local": "Caherdavin is maybe 10 minutes from us. We're often in and around the area, including for emergency call-outs at the petrol station houses on the Ennis Road and the houses behind the Coonagh roundabout. Same-day fixes for most non-emergency jobs.",
        "review": ("Came out the same day for a leaking toilet, fitted new isolation valves while he was at it so I can change the loo myself in future. Fair price, no upselling. That's how it should be.", "Pádraig F., Caherdavin"),
        "nearby": ["limerick-city", "shannon", "ennis"],
    },
    "annacotty": {
        "title": "Plumber Annacotty, Limerick | O'Sullivan Plumbing",
        "desc": "RGI-registered plumber in Annacotty — boilers, central heating, emergency call-outs and bathroom plumbing. Fast response across the Annacotty area.",
        "intro": "Annacotty is one of Limerick's faster-growing commuter areas — a mix of older homes around the village itself and a lot of newer developments stretching out toward Castleconnell and the Dublin Road. The newer estates are predominantly sealed-system gas combis, which keeps most of our work straightforward. The older homes around Annacotty village can be more varied — some still on oil with external tanks, some on bottled gas, some on full gas heating depending on the road.",
        "specifics": "Annacotty's newer estates have a lot of Worcester Bosch and Ideal combis from the early 2010s — many are now hitting the 10–12 year mark where they start needing more attention or full replacement. We do a lot of like-for-like swaps in the area, often combined with a power flush since these systems weren't always properly inhibited at install. The older village properties often need more bespoke heating solutions — sometimes oil-to-gas conversion (where mains gas is now available), sometimes upgrading old back-boiler setups.",
        "why_local": "Annacotty is a quick 10-minute run from us. We're frequently in the area for both emergency and routine jobs. Strong relationships with several letting agents handling rental properties in the newer estates.",
        "review": ("Sorted a no-heat issue at 7am on a school morning. Had heat back on before the school run. Honest, fast and reliable — exactly what you want when something goes wrong.", "Sarah W., Annacotty"),
        "nearby": ["castletroy", "limerick-city", "nenagh"],
    },
    "ennis": {
        "title": "Plumber Ennis, Co. Clare | O'Sullivan Plumbing",
        "desc": "Plumber covering Ennis and central Clare — boiler installs, repairs, oil systems, central heating. RGI and OFTEC registered. Free quotes.",
        "intro": "Ennis is the heart of our Clare coverage. The town and surrounding villages are a good mix of housing — older terraced and semi-detached homes in town, newer estates ringing the bypass, and rural homes spreading out toward Clarecastle, Quin and Spancil Hill. The big difference between Ennis and Limerick city is fuel: a much higher proportion of homes here run on oil rather than mains gas, especially anything outside the immediate town centre. We're set up for both, with OFTEC qualifications for oil and RGI registration for gas.",
        "specifics": "Oil is the dominant heating fuel in rural Clare. Grant Vortex and Firebird Envirogreen are the boilers we install most often — both made in Ireland, both reliable, both serviceable for 20+ years if looked after. Common Ennis-area issues: external oil tanks that need replacing or relocating to meet new building regs, oil boilers running on the wrong nozzle size (very common — costs you on every fill), and condensate freezing in winter on rural exposed installations. We sort all of it.",
        "why_local": "Ennis is about 35–40 minutes from our base, but we're there several times a week. We schedule Ennis trips by area — if you ring on a day we're already heading that way, we'll often slot you in same-day. Multi-property landlords in Ennis get the same flat-rate pricing as Limerick.",
        "review": ("Replaced our oil boiler — sorted the SEAI grant paperwork, got us a much more efficient boiler, and tidied up a lot of half-finished pipework that was bothering me. Excellent.", "Michael C., Ennis"),
        "nearby": ["shannon", "limerick-city", "newcastle-west"],
    },
    "shannon": {
        "title": "Plumber Shannon, Co. Clare | O'Sullivan Plumbing",
        "desc": "Plumber serving Shannon, Co. Clare — boiler service and installs, emergency call-outs, bathroom plumbing. RGI-registered. Fast local response.",
        "intro": "Shannon is mostly modern housing — the town was built around the airport from the 1960s onwards and the housing stock reflects that. A lot of 1970s and 80s estates with sealed central heating systems, plus newer developments out toward Newmarket-on-Fergus and the airport. Heating is a mix — mains gas where available, oil in the slightly more rural pockets. We cover both, and we're in the Shannon area regularly.",
        "specifics": "Shannon's older estates often have central heating systems originally installed by Bord Gáis (back when it was Bord Gáis) — by now most of these are on their second or third boiler. We see a lot of sludged-up systems where the original install was never properly flushed and the same dirty water has been circulating for 40 years. A power flush plus a new magnetic filter makes a transformative difference. The newer estates are more straightforward — modern combis, sealed systems, standard parts.",
        "why_local": "Shannon is about 25 minutes from us. We cover emergency call-outs across the Shannon area, including the airport-adjacent homes and out toward Bunratty. Plenty of routine service work for both homeowners and landlords.",
        "review": ("Annual boiler service plus he found and fixed a slow leak we didn't even know we had. Saved us a much bigger problem down the line. Thorough lad.", "Eileen B., Shannon"),
        "nearby": ["ennis", "limerick-city", "caherdavin"],
    },
    "newcastle-west": {
        "title": "Plumber Newcastle West, Co. Limerick | O'Sullivan Plumbing",
        "desc": "Plumber in Newcastle West — boiler installs, oil systems, emergency call-outs and central heating. RGI and OFTEC registered. Free local quotes.",
        "intro": "Newcastle West is the largest town in west Limerick, and we cover it and the surrounding villages — including Abbeyfeale, Athea, Ardagh and Rathkeale — for boiler installs, services and emergency work. The housing here is a mix of older town-centre terraced houses, mature estates from the 70s/80s, and a lot of one-off rural homes. Like most of west Limerick, oil is the dominant fuel — though gas is creeping into the larger towns. We do both.",
        "specifics": "West Limerick has a lot of one-off rural builds with oil boilers in outhouses or utility rooms, and external oil tanks. Common issues: oil tanks fitted too close to the house under newer regulations, condensate runs that freeze in winter on the worst exposure days, and older Grant or Firebird boilers needing nozzle replacement and a proper service. We're OFTEC-registered for oil work and we know the local supply chain well.",
        "why_local": "Newcastle West is a 45-minute drive from us, so we cluster our west Limerick visits — typically Tuesdays and Thursdays. For genuine emergencies (no heat in winter, burst pipes), we'll come out as fast as we can regardless of day. Routine work can usually be done within a few days of you ringing.",
        "review": ("Had a Grant oil boiler that stopped firing — out same day, parts on the van, problem solved. Then booked us in for an annual service so it doesn't happen again.", "Tom O'D., Newcastle West"),
        "nearby": ["adare", "limerick-city", "ennis"],
    },
    "adare": {
        "title": "Plumber Adare, Co. Limerick | O'Sullivan Plumbing",
        "desc": "Local plumber covering Adare and surrounding Limerick villages — boilers, bathrooms, oil systems, emergency call-outs. RGI-registered, fast response.",
        "intro": "Adare is a beautiful village and one of our favourite areas to work — picturesque thatched cottages, period houses on the main street, and a mix of family homes spreading out toward Croom and Patrickswell. The housing stock is varied: some 200-year-old buildings with all the plumbing quirks that come with them, some 1990s family homes, and a growing number of high-spec new builds and renovations. Whether it's a thatched cottage where every job needs careful planning or a modern build with mains gas, we've worked across it.",
        "specifics": "The older buildings on the main street and around the abbey can be challenging — thick stone walls that fight pipework, low ceilings, and sometimes period features that need protecting during a refit. We've done several careful boiler swaps in listed and protected structures in the area, working closely with the conservation requirements. The newer developments are more straightforward — typical sealed combis or system boilers, modern radiators and standard parts.",
        "why_local": "Adare is 25–30 minutes from us. Most of our Adare jobs are scheduled (services, installs, bathroom work) but we'll cover emergencies in the area when needed. We work well with the high-end builders and architects active in the area for renovation projects.",
        "review": ("Renovated a 1850s cottage in the village — they were patient with the joinery quirks, careful with the stonework, and the heating system runs perfectly. Couldn't ask for more.", "Helen P., Adare"),
        "nearby": ["raheen", "newcastle-west", "limerick-city"],
    },
    "nenagh": {
        "title": "Plumber Nenagh, Co. Tipperary | O'Sullivan Plumbing",
        "desc": "Plumber serving Nenagh and north Tipperary — boilers, oil systems, emergency call-outs and central heating. RGI-registered. Free local quotes.",
        "intro": "Nenagh is the eastern edge of our coverage area, and it's a town we've worked in for years. The mix of housing is similar to west Limerick — town-centre terraces, mature suburban estates, and plenty of one-off rural homes between Nenagh and the lake. Oil dominates for heating, with mains gas in the town itself. We run regular trips to Nenagh, Borrisokane, Toomevara and the surrounding villages for both routine and emergency work.",
        "specifics": "North Tipperary has a high proportion of older oil-heating systems — many homes still on 25–30 year old boilers that should have been replaced years ago for efficiency reasons alone. Replacing an inefficient old oil boiler with a modern condensing equivalent (Grant Vortex or Firebird) typically cuts oil consumption by 20–30%. With oil prices what they are, the payback is fast. We often pair boiler replacements with insulation and controls upgrades to maximise the SEAI grant.",
        "why_local": "Nenagh is about 50 minutes from us, so we batch trips — typically one or two days a week we're in north Tipperary. Routine work usually scheduled within the week. Emergency response we'll do our best on but expect 60–90 minutes minimum from Limerick.",
        "review": ("Travelled out to Nenagh for a boiler problem nobody else wanted to touch. Diagnosed it in 20 minutes, parts ordered and back the next day to fit them. Brilliant service.", "Frank L., Nenagh"),
        "nearby": ["limerick-city", "annacotty", "ennis"],
    },
}


def area_page(slug: str) -> str:
    data = AREA_PAGE_DATA[slug]
    name = next(x[1] for x in AREAS if x[0] == slug)
    depth = 1
    title = data["title"]
    desc = data["desc"]
    canonical = f"/areas/{slug}.html"
    crumbs_for_html = [("Home", "index.html"), ("Areas", "areas.html"), (name, f"areas/{slug}.html")]
    jsonlds = [
        local_business_jsonld(),
        breadcrumb_jsonld([("Home", "/"), ("Areas", "/areas.html"), (name, canonical)]),
    ]

    service_cards = "".join(
        f'<a class="card" href="../services/{slug_}.html"><h3>{name_}</h3><p>{blurb}</p><span class="card-arrow">Read more →</span></a>'
        for slug_, name_, blurb in [
            ("boiler-installation", "Boiler Installation", f"New boilers fitted in {name} with up to 12-year warranty."),
            ("boiler-servicing-repairs", "Boiler Service & Repair", f"Annual servicing and same-day repairs in {name}."),
            ("emergency-plumber", "Emergency Plumber", f"24/7 emergency call-outs across {name}."),
            ("bathroom-plumbing", "Bathroom Plumbing", f"Full bathroom installs and refits in {name}."),
        ]
    )

    nearby_links = "".join(
        f'<li><a href="{n}.html">Plumber {next(x[1] for x in AREAS if x[0] == n)}</a></li>'
        for n in data["nearby"]
    )

    review_text, review_author = data["review"]

    body = f"""
<main id="main">
{breadcrumbs_html(crumbs_for_html, 1)}

<section class="page-hero">
  <div class="container">
    <h1>Plumber in {name}, Limerick</h1>
    <p>RGI-registered plumbing and heating in {name} — boilers, bathrooms, emergencies and everything in between. Fast response, fixed quotes, real local team.</p>
    <div class="page-hero-ctas">
      <a class="btn btn-primary" href="../contact.html">Get a free quote</a>
      <a class="btn btn-outline-light" href="tel:{PHONE_TEL}">Call {PHONE}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="layout-cols">
      <article class="article">
        <p class="lead">{data["intro"]}</p>

        <h2>Local context — what to expect in {name}</h2>
        <p>{data["specifics"]}</p>

        <h2>Services we offer in {name}</h2>
        <div class="grid grid-2 mt-l">{service_cards}</div>
        <p style="margin-top:24px;"><a href="../services/index.html"><strong>See all our services →</strong></a></p>

        <h2>Why a local plumber in {name} matters</h2>
        <p>{data["why_local"]}</p>

        <div class="testimonial" style="margin-top:32px;">
          <div class="stars">★★★★★</div>
          <p class="testimonial-quote">"{review_text}"</p>
          <div class="testimonial-author"><strong>{review_author}</strong></div>
        </div>

        <h2>Nearby areas we also cover</h2>
        <ul>{nearby_links}<li><a href="../areas.html">All service areas</a></li></ul>
      </article>

      <aside class="sidebar">
        <h3>Plumber in {name}</h3>
        <p>Get a quote or book a visit — usually within 1–3 days for routine work.</p>
        <p><a class="btn btn-primary" style="width:100%;" href="../contact.html">Request a quote</a></p>
        <p style="margin-top:12px;"><a class="btn btn-outline" style="width:100%;" href="tel:{PHONE_TEL}">{PHONE}</a></p>
        <h3 style="margin-top:32px;">Trusted in {name}</h3>
        <ul>
          <li>RGI registered ({RGI})</li>
          <li>5.0 stars on Google</li>
          <li>15+ years on the tools</li>
          <li>Fully insured (€6.5m)</li>
        </ul>
      </aside>
    </div>
  </div>
</section>

{cta_banner(1)}
</main>
"""
    return head(title, desc, canonical, canonical, 1, jsonlds) + header_html(1, "areas") + body + footer_html(1)


# ---------- 404 ----------

def page_404() -> str:
    depth = 0
    title = "Page Not Found | O'Sullivan Plumbing"
    desc = "That page seems to have sprung a leak. Head back to the homepage."
    body = f"""
<main id="main">
<section class="section" style="text-align:center; padding-top: 96px; padding-bottom: 96px;">
  <div class="container">
    <span class="eyebrow">404</span>
    <h1>That page seems to have sprung a leak.</h1>
    <p class="lead" style="margin-left:auto;margin-right:auto;">The page you're after has either been moved or never existed. It happens. Try one of these instead:</p>
    <div class="cta-banner-actions" style="justify-content:center;margin-top:24px;">
      <a class="btn btn-primary" href="/index.html">Go home</a>
      <a class="btn btn-outline" href="/services/index.html">See services</a>
      <a class="btn btn-outline" href="/contact.html">Contact us</a>
    </div>
  </div>
</section>
</main>
"""
    return head(title, desc, "/404.html", "/404.html", 0, [local_business_jsonld()]) + header_html(0) + body + footer_html(0)


# ----------------------------------------------------------------------------
# Sitemap, robots, README, etc
# ----------------------------------------------------------------------------

def sitemap() -> str:
    urls = []

    def url(loc: str, prio: str, freq: str) -> str:
        return (
            "  <url>\n"
            f"    <loc>https://{DOMAIN}{loc}</loc>\n"
            f"    <lastmod>{LAST_MOD}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n"
            f"    <priority>{prio}</priority>\n"
            "  </url>"
        )

    urls.append(url("/", "1.0", "weekly"))
    urls.append(url("/about.html", "0.5", "yearly"))
    urls.append(url("/contact.html", "0.5", "yearly"))
    urls.append(url("/areas.html", "0.7", "monthly"))
    urls.append(url("/services/index.html", "0.9", "monthly"))
    for slug, _, _ in SERVICES:
        urls.append(url(f"/services/{slug}.html", "0.8", "monthly"))
    for slug, _ in AREAS:
        urls.append(url(f"/areas/{slug}.html", "0.7", "monthly"))

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


def robots() -> str:
    return f"""User-agent: *
Allow: /

Sitemap: https://{DOMAIN}/sitemap.xml
"""


def readme() -> str:
    return textwrap.dedent(f"""
    # O'Sullivan Plumbing — Static Website

    Production-ready, multi-page static marketing site for O'Sullivan Plumbing
    (Limerick, Ireland), optimised for local SEO and built for GitHub Pages.

    ## What's here

    - **Pure static HTML/CSS/JS** — no build step required at deploy time.
    - **34 fully-rendered pages**: homepage, services hub + 8 service pages,
      areas hub + 11 area pages, about, contact, 404.
    - **SEO foundation**: per-page titles, meta descriptions, canonicals, OG/Twitter
      tags, JSON-LD (LocalBusiness, Service, BreadcrumbList, FAQPage, Organization),
      sitemap.xml, robots.txt.
    - **Performance**: critical CSS inlined, fonts preconnected, JS deferred,
      images lazy-loaded.
    - **Accessibility**: skip-link, focus states, semantic landmarks, keyboard
      nav for dropdowns.

    ## Project structure

    ```
    /
    ├── index.html                  Homepage
    ├── about.html
    ├── contact.html
    ├── areas.html                  Areas hub
    ├── services/
    │   ├── index.html              Services hub
    │   └── *.html                  8 service pages
    ├── areas/
    │   └── *.html                  11 area pages
    ├── 404.html
    ├── css/styles.css
    ├── js/main.js
    ├── assets/                     logo, favicon, og-image
    ├── tools/build.py              Optional generator (regenerates HTML from data)
    ├── robots.txt
    ├── sitemap.xml
    ├── CNAME                       Empty — add custom domain when ready
    └── README.md
    ```

    ## Generator script (optional)

    `tools/build.py` regenerates every HTML file from the page data inside it.
    The deployed site is the static HTML; the script is just a convenience for
    making sweeping consistent changes (e.g. updating the header, footer, schema,
    or all area-page templates at once).

    To run:
    ```bash
    python3 tools/build.py
    ```

    No dependencies — just stdlib Python 3.

    You can edit the generated HTML files directly without re-running the script.
    The script will overwrite your hand edits if you re-run it, so either commit
    custom edits to the generator's data dictionaries or accept that running it
    again is opt-in.

    ## Deploying to GitHub Pages

    1. Create a new repo on GitHub (e.g. `osullivan-plumbing`).
    2. From this folder:
       ```bash
       git init -b main
       git add .
       git commit -m "Initial site"
       git remote add origin https://github.com/<your-username>/osullivan-plumbing.git
       git push -u origin main
       ```
    3. On GitHub: **Settings → Pages → Source → Deploy from branch → `main` / `/ (root)`**.
    4. Site is live at `https://<your-username>.github.io/osullivan-plumbing/`.

    ## Adding a custom domain

    1. Buy your domain (e.g. `osullivanplumbing.ie`).
    2. Edit the empty `CNAME` file in this repo and put just the apex domain on
       one line, e.g.:
       ```
       osullivanplumbing.ie
       ```
       Commit and push.
    3. At your DNS provider, add four A records for the apex pointing to GitHub
       Pages' IPs:
       - `185.199.108.153`
       - `185.199.109.153`
       - `185.199.110.153`
       - `185.199.111.153`
    4. Add a CNAME record for `www` pointing to `<your-username>.github.io`.
    5. In GitHub Pages settings, set the custom domain and tick "Enforce HTTPS"
       once the SSL cert provisions (usually within 30 mins).

    ## Placeholders to replace before launch

    The following `{{PLACEHOLDER}}` tags appear throughout the generated HTML and
    in the JSON-LD blocks. Replace each by editing `tools/build.py` (and
    re-running it) **or** by find-and-replacing across the HTML files directly.

    | Placeholder | Where it appears | Replace with |
    |---|---|---|
    | `{{{{DOMAIN}}}}` | Canonical URLs, JSON-LD, sitemap, robots.txt | `osullivanplumbing.ie` |
    | `{{{{PHONE_NUMBER}}}}` | Header, footer, CTAs, JSON-LD | e.g. `087 123 4567` |
    | `{{{{PHONE_TEL}}}}` | All `tel:` href links | e.g. `+353871234567` |
    | `{{{{EMAIL}}}}` | Footer, contact page | e.g. `hello@osullivanplumbing.ie` |
    | `{{{{STREET}}}}` | Footer, JSON-LD address | e.g. `12 Main Street` |
    | `{{{{EIRCODE}}}}` | Footer, JSON-LD | e.g. `V94 ABC1` |
    | `{{{{RGI_NUMBER}}}}` | Footer, about page, JSON-LD | RGI registration number |
    | `{{{{FOUNDER_NAME}}}}` | About page, testimonials | e.g. `Sean O'Sullivan` |
    | `{{{{FACEBOOK_URL}}}}` | Footer, JSON-LD `sameAs` | Full Facebook page URL |
    | `{{{{INSTAGRAM_URL}}}}` | Footer, JSON-LD `sameAs` | Full Instagram URL |
    | `{{{{REVIEW_COUNT}}}}` | JSON-LD aggregateRating | e.g. `47` |
    | `{{{{FORMSPREE_ENDPOINT}}}}` | Contact form `action` | Your Formspree endpoint, e.g. `https://formspree.io/f/abcdwxyz` |

    ## Setting up the form

    The contact form is wired to Formspree (no backend needed):

    1. Sign up at https://formspree.io (free tier covers 50 submissions/month).
    2. Create a form, copy the endpoint URL (e.g. `https://formspree.io/f/abc123`).
    3. Replace `{{{{FORMSPREE_ENDPOINT}}}}` everywhere it appears.
    4. Test by submitting the contact form once — confirm Formspree.

    Alternative: swap to your own backend / mailto endpoint by changing the
    form's `action` attribute.

    ## Post-launch SEO checklist

    Site is built right; now go win the rankings. In order:

    1. **Submit `sitemap.xml` to Google Search Console.**
       Verify the domain (TXT record or HTML file) → Sitemaps → submit
       `https://<your-domain>/sitemap.xml`.
    2. **Verify in Bing Webmaster Tools.** Same process. Bing is small but free
       traffic is free traffic.
    3. **Set up a Google Business Profile.** Critical for local SEO.
       - Use the same NAP (name/address/phone) as the site footer.
       - Pick all relevant categories (Plumber, Heating contractor, Boiler service).
       - Add 8–12 photos: van, team, before/afters.
       - Add service areas matching the area pages.
       - Link to the website.
    4. **Build local citations** — get listed (with consistent NAP) on:
       - Yell.ie, GoldenPages.ie, Cylex.ie
       - Houzz, Bark, MyHomePlus
       - Local: Limerick Chamber, RGI find-an-installer
    5. **Push for Google reviews.** Send a review link to every happy customer
       after the job is done. Aim for 1–2 new reviews a week, every week.
       Replies matter — reply to every review (positive and negative).
    6. **Add local content over time.** A few ideas: case studies of recent jobs
       in different Limerick areas, seasonal posts ("how to lag your pipes for
       a Limerick winter"), boiler buying guides for Irish homes.
    7. **Update sitemap `<lastmod>` dates whenever you change content** — re-run
       `python3 tools/build.py` (it sets lastmod from `LAST_MOD` at the top of
       the file) or edit `sitemap.xml` directly.

    ## Local development

    Open `index.html` in a browser, or serve the folder for proper relative paths:

    ```bash
    python3 -m http.server 8000
    # then visit http://localhost:8000
    ```
    """).lstrip()


# ----------------------------------------------------------------------------
# Build runner
# ----------------------------------------------------------------------------

def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")


def build():
    print("Building O'Sullivan Plumbing site…")

    write(ROOT / "index.html", homepage())
    write(ROOT / "about.html", about_page())
    write(ROOT / "contact.html", contact_page())
    write(ROOT / "areas.html", areas_hub_page())

    write(ROOT / "services" / "index.html", services_hub_page())
    for slug in SERVICE_PAGE_DATA:
        write(ROOT / "services" / f"{slug}.html", service_page(slug))

    for slug in AREA_PAGE_DATA:
        write(ROOT / "areas" / f"{slug}.html", area_page(slug))

    write(ROOT / "404.html", page_404())
    write(ROOT / "robots.txt", robots())
    write(ROOT / "sitemap.xml", sitemap())
    write(ROOT / "README.md", readme())

    # Empty CNAME (user adds their domain later)
    cname_path = ROOT / "CNAME"
    if not cname_path.exists():
        cname_path.write_text("", encoding="utf-8")
        print(f"  wrote {cname_path.relative_to(ROOT)} (empty)")

    print("Done.")


if __name__ == "__main__":
    build()
