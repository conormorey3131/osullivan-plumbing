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

The following `{PLACEHOLDER}` tags appear throughout the generated HTML and
in the JSON-LD blocks. Replace each by editing `tools/build.py` (and
re-running it) **or** by find-and-replacing across the HTML files directly.

| Placeholder | Where it appears | Replace with |
|---|---|---|
| `{{DOMAIN}}` | Canonical URLs, JSON-LD, sitemap, robots.txt | `osullivanplumbing.ie` |
| `{{PHONE_NUMBER}}` | Header, footer, CTAs, JSON-LD | e.g. `087 123 4567` |
| `{{PHONE_TEL}}` | All `tel:` href links | e.g. `+353871234567` |
| `{{EMAIL}}` | Footer, contact page | e.g. `hello@osullivanplumbing.ie` |
| `{{STREET}}` | Footer, JSON-LD address | e.g. `12 Main Street` |
| `{{EIRCODE}}` | Footer, JSON-LD | e.g. `V94 ABC1` |
| `{{RGI_NUMBER}}` | Footer, about page, JSON-LD | RGI registration number |
| `{{FOUNDER_NAME}}` | About page, testimonials | e.g. `Sean O'Sullivan` |
| `{{FACEBOOK_URL}}` | Footer, JSON-LD `sameAs` | Full Facebook page URL |
| `{{INSTAGRAM_URL}}` | Footer, JSON-LD `sameAs` | Full Instagram URL |
| `{{REVIEW_COUNT}}` | JSON-LD aggregateRating | e.g. `47` |
| `{{FORMSPREE_ENDPOINT}}` | Contact form `action` | Your Formspree endpoint, e.g. `https://formspree.io/f/abcdwxyz` |

## Setting up the form

The contact form is wired to Formspree (no backend needed):

1. Sign up at https://formspree.io (free tier covers 50 submissions/month).
2. Create a form, copy the endpoint URL (e.g. `https://formspree.io/f/abc123`).
3. Replace `{{FORMSPREE_ENDPOINT}}` everywhere it appears.
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
