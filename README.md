# Gaurav's Blogs

A minimalist, high-performance personal blog built with pure semantic HTML5, modern CSS, and zero build dependencies.

## ✨ Features

- **Zero Build Step:** Native web primitives. No bundlers, transpilers, or `node_modules` required.
- **Modern Typography:**
  - `text-wrap: balance` for symmetrical, balanced headlines.
  - `text-wrap: pretty` for orphan-free body copy.
  - Fluid sizing with CSS `clamp()`.
  - Line-length capped to 72 characters (`72ch`) for optimal reading ergonomics.
- **Light & Dark Mode:** Auto-detects system color preference (`prefers-color-scheme: dark`) with an interactive toggle that persists your preference in `localStorage`.
- **Fully Responsive & Accessible:**
  - Semantic landmark elements (`<header>`, `<nav>`, `<main>`, `<article>`, `<footer>`).
  - Screen reader friendly with skip-to-content links and ARIA labels.
  - Fast Core Web Vitals (sub-50ms load times).

---

## 📁 Project Structure

```
blogs/
├── index.html            # Blog homepage with article cards feed
├── style.css             # Main stylesheet with CSS custom properties & theme tokens
├── posts/
│   └── hello-world.html  # Full article template
└── README.md             # Project documentation
```

---

## 🚀 Getting Started

### 1. View Locally
Simply double-click `index.html` to open it in any browser, or run a local server:

```bash
# Python
python3 -m http.server 8000

# or Node / npx
npx serve .
```
Then visit `http://localhost:8000`.

### 2. Adding a New Blog Post
1. Duplicate `posts/hello-world.html` and rename it (e.g., `posts/my-new-post.html`).
2. Update the `<title>`, metadata (`<time>`, tags), and content inside `<article>`.
3. Add a new card entry to the `<div class="posts-grid">` in `index.html`.

### 3. Deploying with GitHub Pages
This repository is pre-configured to deploy on GitHub Pages for free:
1. Go to your repository on GitHub: [grvmon/blogs](https://github.com/grvmon/blogs).
2. Click **Settings** > **Pages** in the left sidebar.
3. Under **Build and deployment**:
   - Source: **Deploy from a branch**
   - Branch: **main** / **/(root)**
4. Click **Save**. Your site will be live at `https://grvmon.github.io/blogs/`.

---

## 📄 License
MIT © Gaurav Mongia
