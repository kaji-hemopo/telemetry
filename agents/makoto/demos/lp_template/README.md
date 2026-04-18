# Demo 3: Landing Page Template

**Purpose:** Proves capability to build LP制作 jobs (highest volume JP pattern, ¥50-100k on Lancers).

**What it is:** A bilingual JP/EN service landing page template — clean, conversion-focused, works for any service business.

**Stack:** Pure HTML + CSS (no framework) · ~350 lines · deploy anywhere (Neocities, GitHub Pages, Netlify)

---

## Features

- **Bilingual JP/EN toggle** — one button switches the entire page language
- **4-service grid** — landing pages, LINE Bot, FastAPI backends, web scraping
- **Pain-point hero** — addresses common client frustrations
- **Contact form** — with JS form submission (no backend needed, replace action with Formspree)
- **Mobile responsive** — works on all screen sizes
- **No dependencies** — single HTML file, no build step

---

## Customizing for Client Work

```html
<!-- Change hero text -->
<h1><span class="accent">Web</span> & IT solutions<br>built for your business</h1>

<!-- Change services -->
<div class="service">
    <h3>Your Service Name</h3>
    <p>Description in JP or EN</p>
</div>

<!-- Change price -->
<div class="price">¥XXX,000 <span>starting from</span></div>

<!-- Wire up contact form -->
<!-- Replace <form> action with your Formspree endpoint -->
```

---

## Live Example

- This template is the basis for `jackson_gbp_landing.html` (GBP management service) in `workspace_makoto/outputs/`
- The LP template strips GBP-specific content to create a generic service template

---

## Deployment (30 seconds)

```bash
# Neocities (free)
# 1. Upload index.html to Neocities dashboard
# 2. Your-site.neocities.org/lp_template/

# GitHub Pages
# 1. Push to a GitHub repo
# 2. Enable GitHub Pages → published at your-repo.github.io/
```

---

## Gig Fit

| Pattern | Rate | Evidence |
|---------|------|----------|
| LP制作 (landing page) | ¥50-100k | Top of Lancers domestic opps |
| WordPress LP | ¥80-150k | 9+ LP jobs in intel, all ¥80k+ |
| Bilingual LP | ¥100-200k | Few competitors do JP+EN |

Use this template as the demo link in Lancers proposals — "Here's an example LP I built: [URL]"

---

## Files

```
lp_template/
├── index.html    ← Complete landing page template (this file)
└── README.md     ← This file
```