# acre&key — Property Intelligence & Blog System

A minimalist, high-performance property intelligence blog engineered strictly according to the **[acre&key Design System v2.1](https://acrenkey.com/style-guide/)** and inspired by the layout mechanics of the **Self Storage India blog**.

---

## 🏛️ Design System Compliance

### 1. The Strict 6-Token WCAG AAA Palette
- **Titanium Frost (`#FAFAFA`)**: Base positive-space canvas that eliminates harsh pure-white glare.
- **Obsidian Black (`#2B2D31`)**: Primary editorial ink, display headings, and dark breakout surfaces (`13.22:1` AAA).
- **Text Copper AAA (`#804526`)**: Section kickers, inline links, active filter pills, and valuation metrics (`7.19:1` AAA).
- **Primary Copper CTA (`linear-gradient(135deg, #E88D67 0%, #9E3F23 100%)`)**: Primary conversion buttons with subtle optical text shadow.
- **Muted Slate (`#55555A`)**: Long-form analytical copy and secondary labels (`7.10:1` AAA).
- **Highlight Peach (`#E88D67`)**: Accents and focus rings on dark surfaces.

### 2. Typography
- **Headlines & Editorial Titles**: `'Cormorant Garamond', serif` (font-weight: 400/500, letter-spacing: -0.02em, `text-wrap: balance`).
- **Body, UI & Numerals**: `'Manrope', sans-serif` (tabular numbers, line-height: 1.65–1.8, `text-wrap: pretty`).

### 3. Geometry & Physics
- **Strict 4px Geometry**: `border-radius: 4px` across cards, buttons, search inputs, and image frames.
- **Hairline Dividers**: `0.5px solid rgba(85, 85, 90, 0.15)`.
- **Art Direction Photo Filter**: `filter: saturate(0.85) contrast(1.05)`.
- **Cinematic Flat Interaction**: Smooth background and border transitions without heavy drop-shadow lifts.

---

## ✨ Features & Layout Mechanics

### Home Page (`index.html`)
- **Minimalist Hero with Live Search**: Real-time client-side search filtering dossiers by keyword, topic, or location.
- **Category Filter Strip**: Instant filtering by `Micro-Markets`, `Valuation`, `Asset Fundamentals`, and `Regulatory & Tax`.
- **3-Column Responsive Cards Grid**: Featuring architectural thumbnail banners, category badges, dates, read times, and clear action links.

### Article Detail Page (`posts/hello-world.html`)
- **Reading Scroll Progress Bar**: Sticky top progress indicator in metallic copper gradient tracking scroll completion.
- **Breadcrumb Navigation**: Clear hierarchical navigation paths.
- **Author & Verification Row**: Author avatar, title, publication date, reading time, and official **Fact-Checked** badge.
- **Social Sharing Strip**: Direct one-click share to WhatsApp, LinkedIn, X, and native clipboard link copying.
- **Key Takeaways & Executive Summary Box**: Scannable summary of core findings.
- **Table of Contents Box**: Anchor links for smooth in-page jumping.
- **Analytical Data Matrix Table**: Structured comparison of micro-market yields and pricing.
- **In-Article Advisory Banner**: High-impact mid-article conversion callout.
- **Interactive FAQ Accordion**: Expandable investor Q&As with smooth CSS transitions.
- **Author Bio Card**: Founder profile with credentials and LinkedIn link.
- **Sticky Advisory Sidebar**:
  - Private advisory consultation booking card.
  - Valuation matrix calculator tool CTA.
  - Related intelligence dossiers.
  - Verified client review with 5-star rating.

---

## 📁 Project Structure

```
blogs/
├── index.html            # Minimalist blog home with live search & category filters
├── style.css             # Complete acre&key v2.1 design system stylesheet
├── posts/
│   └── hello-world.html  # Full property intelligence dossier & detail page
└── README.md             # Project documentation
```

---

## 🚀 Local Preview & Deployment

### View Locally
Open `index.html` directly in your browser, or launch a local server:

```bash
# Python
python3 -m http.server 8000

# or npx serve
npx serve .
```

### GitHub Pages Deployment
1. Go to repository **Settings** &gt; **Pages** on [grvmon/blogs](https://github.com/grvmon/blogs).
2. Set Source to **Deploy from a branch**, Branch to **`main`**, and folder to **`/(root)`**.
3. Your site will be published at `https://grvmon.github.io/blogs/`.

---

## 📄 License
MIT &copy; 2026 acre&amp;key. All rights reserved.
