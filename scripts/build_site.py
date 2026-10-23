#!/usr/bin/env python3
"""Build the acre&key static blog from content/posts and site.config.json.

Change the public address in site.config.json (baseUrl), then run:

    python3 scripts/build_site.py
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import os
import re
import shutil
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.stderr.write("Missing dependency. Install it with: pip install markdown\n")
    raise

from link_plan import (  # noqa: E402
    HUBS,
    STATIC_POSTS,
    TOPIC_SLUG,
    ZONE_LINKS,
    apply_link_plan,
    classify_index_links,
    context_sentences,
    inject_static_html,
    related_block_html,
    short_anchor,
    sibling_sentence,
    weave_sentences,
    load_plan,
    load_topic_map,
    plan_by_source,
    sibling_hubs,
    static_by_slug,
    write_decisions,
)

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
POSTS_DIR = CONTENT / "posts"
CONFIG_PATH = ROOT / "site.config.json"
SECTIONS = ("blog", "insights", "areas")
SECTION_LABEL = {"blog": "Blog", "insights": "Insights", "areas": "Areas"}
UNPUBLISHED_RE = re.compile(
    r"^https://acrenkey\.com/(?:blogs|insights)/([a-z0-9-]+)/?$"
)

BANNED = [
    (re.compile(r"\bindependent\b", re.I), "independent"),
    (re.compile(r"\bobjective\b", re.I), "objective"),
    (re.compile(r"\bunbiased\b", re.I), "unbiased"),
    (re.compile(r"\bbest\b", re.I), "best"),
    (re.compile(r"\bguaranteed\b", re.I), "guaranteed"),
    (re.compile(r"No\.1", re.I), "No.1"),
    (re.compile(r"\bluxury\b", re.I), "luxury"),
    (re.compile(r"\bpremium\b", re.I), "premium"),
    (re.compile(r"dream home", re.I), "dream home"),
    (re.compile(r"100%"), "100%"),
]

SHARE_WA = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>'
)
SHARE_LI = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>'
    '<rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>'
)
SHARE_X = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M4 4l11.733 16h4.267l-11.733 -16z"></path>'
    '<path d="M4 20l6.768 -6.768m2.46 -2.46l6.772 -6.772"></path></svg>'
)
SHARE_COPY = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>'
    '<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>'
)
FAQ_CHEVRON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<polyline points="6 9 12 15 18 9"></polyline></svg>'
)
CTA_ARROW = (
    '<svg class="cta-arrow" viewBox="0 0 16 16" fill="none" stroke="currentColor" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<line x1="4.5" y1="11.5" x2="11.5" y2="4.5"></line>'
    '<polyline points="6.5 4.5 11.5 4.5 11.5 9.5"></polyline></svg>'
)
TOC_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;" aria-hidden="true">'
    '<line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line>'
    '<line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line>'
    '<line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>'
)

MD = markdown.Markdown(extensions=["tables", "sane_lists", "fenced_code"], output_format="html")


AUTHORS = ("Gaurav", "Nitin", "Arvind")
AUTHOR_PROFILES = {
    "Gaurav": {
        "name": "Gaurav Mongia",
        "role": "Market Strategy · Product · Tech",
        "jobTitle": "Co-founder & Head of Product & Strategy",
        "avatar": "https://acrenkey.com/style-guide/assets/gaurav-mongia-founder-acre-key.webp",
        "thumb": "https://acrenkey.com/style-guide/assets/gaurav-mongia-founder-acre-key-96.webp",
        "linkedin": "https://www.linkedin.com/in/gaurav-a-mongia/",
        "description": "Building data-driven evaluation models and micro-market frameworks to give buyers absolute clarity.",
    },
    "Nitin": {
        "name": "Nitin Gupta",
        "role": "Investments · Decision Framework",
        "jobTitle": "Co-founder & Head of Investments",
        "avatar": "https://acrenkey.com/style-guide/assets/nitin-gupta-founder-acre-key.webp",
        "thumb": "https://acrenkey.com/style-guide/assets/nitin-gupta-founder-acre-key-96.webp",
        "linkedin": "https://www.linkedin.com/in/nitin-gupta-7446864/",
        "description": "Former corporate finance leader applying institutional diligence and quantitative risk models to home buying in Bengaluru.",
    },
    "Arvind": {
        "name": "Arvind Patidar",
        "role": "Advisory · Execution",
        "jobTitle": "Co-founder & Head of Operations",
        "avatar": "https://acrenkey.com/style-guide/assets/arvind-patidar-founder-acre-key.webp",
        "thumb": "https://acrenkey.com/style-guide/assets/arvind-patidar-founder-acre-key-96.webp",
        "linkedin": "https://www.linkedin.com/in/arvind-patidar/",
        "description": "Operations and engineering leader ensuring flawless execution, civic compliance, and zero-compromise due diligence.",
    },
}
IMAGE_W, IMAGE_H = 1200, 675


def img_tag(root: str, post: dict, cls: str, hero: bool = False) -> str:
    loading = 'loading="eager" fetchpriority="high"' if hero else 'loading="lazy"'
    src = f'{root}{esc(post["image"])}'
    small = src[:-5] + "-800.webp" if src.endswith(".webp") else ""
    sizes = "(max-width: 767px) calc(100vw - 32px), 1232px" if hero else "(max-width: 767px) calc(100vw - 32px), 400px"
    srcset = f' srcset="{small} 800w, {src} {IMAGE_W}w" sizes="{sizes}"' if small and (ROOT / post["image"].replace(".webp", "-800.webp")).exists() else ""
    return (
        f'<img src="{src}"{srcset} width="{IMAGE_W}" height="{IMAGE_H}" '
        f'alt="{esc(post["image_alt"])}" class="{cls}" {loading} decoding="async">'
    )


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def load_config() -> dict:
    config = json.loads(CONFIG_PATH.read_text())
    base = config["baseUrl"]
    if not base.startswith("https://") or not base.endswith("/"):
        raise SystemExit("site.config.json baseUrl must be an https URL ending with /")
    return config


def abs_url(base: str, path: str = "") -> str:
    root = base.rstrip("/") + "/"
    if not path:
        return root
    return root + path.lstrip("/")


def public_path(section: str, slug: str) -> str:
    """Path under the site root. Blog guides sit directly under baseUrl, so the
    canonical is /blogs/{slug}/ rather than /blogs/blog/{slug}/."""
    if section == "blog":
        return f"{slug}/"
    return f"{section}/{slug}/"


def site_prefix(public: str) -> str:
    depth = len([part for part in public.split("/") if part])
    return "../" * depth


def relative_href(from_public: str, to_public: str) -> str:
    rel = os.path.relpath(to_public.strip("/"), start=from_public.strip("/") or ".")
    if not rel.endswith("/"):
        rel += "/"
    return rel


def section_crumb(post: dict, base: str) -> tuple[str, str] | None:
    """Middle breadcrumb: Area guides, Data insights, or the post's topic hub."""
    if post.get("section") == "areas":
        return "Area guides", abs_url(base, "areas/")
    if post.get("section") == "insights":
        return "Data insights", abs_url(base, "insights/")
    slug = TOPIC_SLUG.get(post.get("topic") or "")
    if slug:
        return post["topic"], abs_url(base, f"topic/{slug}/")
    return None


def nav_current(post: dict) -> str:
    if post.get("section") in {"areas", "insights"}:
        return post["section"]
    return TOPIC_SLUG.get(post.get("topic") or "", "")


def static_posts() -> list[dict]:
    rows = []
    for item in STATIC_POSTS:
        rows.append({**item, "image": f"assets/img/{item['slug']}.webp"})
    return rows


def section_siblings(post: dict, ordered: list[dict]) -> list[dict]:
    """The next guides in the same section that have a 2–5 word name."""
    group = sorted(
        [item for item in ordered if item.get("section") == post.get("section")],
        key=lambda item: (item["rank"], item["slug"]),
    )
    if len(group) < 2:
        return []
    index = next(i for i, item in enumerate(group) if item["slug"] == post["slug"])
    picked = []
    step = 1
    while len(picked) < 3 and step < len(group):
        candidate = group[(index + step) % len(group)]
        if candidate["slug"] != post["slug"] and short_anchor(candidate["h1"]):
            picked.append(candidate)
        step += 1
    return picked


def html_oxford(pairs: list[tuple[str, str]]) -> str:
    bits = [f'<a href="{esc(href)}">{esc(label)}</a>' for label, href in pairs]
    if not bits:
        return ""
    if len(bits) == 1:
        return bits[0]
    if len(bits) == 2:
        return f"{bits[0]} and {bits[1]}"
    return ", ".join(bits[:-1]) + " and " + bits[-1]


def is_hub_page(path: Path) -> bool:
    if path.name != "index.html":
        return False
    if path.parent in {ROOT / "areas", ROOT / "insights"}:
        return True
    return path.parent.parent == ROOT / "topic"


def quoted_field(front_matter: str, key: str) -> str:
    match = re.search(rf'^{re.escape(key)}:\s*"(.*)"\s*$', front_matter, re.M)
    if not match:
        raise ValueError(f"Missing front matter field {key}")
    return match.group(1)


def optional_field(front_matter: str, key: str) -> str:
    match = re.search(rf'^{re.escape(key)}:\s*"(.*)"\s*$', front_matter, re.M)
    return match.group(1) if match else ""


def render_markdown(text: str) -> str:
    MD.reset()
    return MD.convert(text.strip()) if text.strip() else ""


def transform_inline(text: str, on_link) -> str:
    """Walk inline links and images. on_link(label, url, is_image) returns replacement or None to keep."""
    out = []
    i = 0
    n = len(text)
    while i < n:
        is_image = text.startswith("![", i)
        is_link = text.startswith("[", i)
        if not is_image and not is_link:
            out.append(text[i])
            i += 1
            continue
        start = i
        label_at = i + (2 if is_image else 1)
        close = text.find("](", label_at)
        if close == -1 or "\n\n" in text[label_at:close]:
            out.append(text[i])
            i += 1
            continue
        label = text[label_at:close]
        k = close + 2
        depth = 1
        while k < n and depth:
            if text[k] == "(":
                depth += 1
            elif text[k] == ")":
                depth -= 1
            k += 1
        if depth != 0:
            out.append(text[i])
            i += 1
            continue
        url = text[close + 2 : k - 1].strip()
        replacement = on_link(label, url, is_image)
        out.append(text[start:k] if replacement is None else replacement)
        i = k
    return "".join(out)


def linkify_bare_urls(text: str) -> str:
    def repl(match: re.Match) -> str:
        raw = match.group(1)
        url = raw.rstrip(".,;:")
        trail = raw[len(url) :]
        if not url:
            return raw
        return f"[{url}]({url}){trail}"

    return re.sub(r"(?<!\()(?<!\[)(https?://[^\s<>\[\]]+)", repl, text)


def plain_markdown(text: str) -> str:
    def keep_label(label: str, url: str, is_image: bool) -> str:
        return "" if is_image else label

    text = transform_inline(text, keep_label)
    text = text.replace("**", "").replace("`", "")
    text = re.sub(r"(?<!\*)\*(?!\*)", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def html_to_text(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def slugify(text: str) -> str:
    text = html_to_text(text).lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "section"


class IdFactory:
    def __init__(self) -> None:
        self.used: dict[str, int] = {}

    def make(self, text: str) -> str:
        base = slugify(text)
        count = self.used.get(base, 0)
        self.used[base] = count + 1
        return base if count == 0 else f"{base}-{count + 1}"

    def stamp(self, fragment: str) -> str:
        def repl(match: re.Match) -> str:
            tag = match.group(1)
            inner = match.group(2)
            heading_id = self.make(inner)
            return f'<{tag} id="{heading_id}">{inner}</{tag}>'

        return re.sub(r"<(h[23])>(.*?)</\1>", repl, fragment, flags=re.S)


def wrap_tables(fragment: str) -> str:
    fragment = fragment.replace(
        "<table>",
        '<div class="data-matrix-table-wrap"><table class="data-matrix-table">',
    )
    return fragment.replace("</table>", "</table></div>")


def heading_entries(fragment: str) -> list[tuple[str, str]]:
    entries = []
    for heading_id, inner in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', fragment, flags=re.S):
        entries.append((heading_id, html_to_text(inner)))
    return entries


def format_date(iso: str) -> str:
    year, month, day = iso.split("-")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{int(day)} {months[int(month) - 1]} {year}"


def read_time(text: str) -> int:
    words = re.findall(r"[A-Za-z0-9']+", text)
    return max(1, round(len(words) / 200))


def split_sections(body: str) -> tuple[str, list[tuple[str, str]]]:
    parts = re.split(r"(?=^## )", body, flags=re.M)
    intro = parts[0]
    sections = []
    for part in parts[1:]:
        lines = part.splitlines()
        title = lines[0][3:].strip()
        rest = "\n".join(lines[1:]).strip()
        sections.append((title, rest))
    return intro, sections


def parse_intro(intro: str) -> tuple[str, str, str]:
    short = ""
    quote_lines = []
    rest_lines = []
    for line in intro.splitlines():
        if line.startswith("# "):
            continue
        if line.startswith(">"):
            quote_lines.append(re.sub(r"^>\s?", "", line))
            continue
        if line.startswith("**Short answer:**"):
            short = line
            continue
        rest_lines.append(line)
    return short.strip(), "\n".join(quote_lines).strip(), "\n".join(rest_lines).strip()


def load_posts(config: dict) -> tuple[list[dict], list[dict]]:
    manifest_path = CONTENT / "manifest.csv"
    rows = list(csv.DictReader(manifest_path.open()))
    by_file = {}
    for path in sorted(POSTS_DIR.glob("*.md")):
        raw = path.read_text()
        match = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not match:
            raise SystemExit(f"No front matter: {path.name}")
        front, body = match.group(1), match.group(2)
        by_file[path.name] = {
            "file": path.name,
            "seo_title": quoted_field(front, "title"),
            "meta": quoted_field(front, "meta_description"),
            "slug": quoted_field(front, "slug"),
            "date_modified": quoted_field(front, "date_modified"),
            "date_published": optional_field(front, "date_published"),
            "dataset_name": optional_field(front, "dataset_name"),
            "dataset_description": optional_field(front, "dataset_description"),
            "dataset_distribution": optional_field(front, "dataset_distribution"),
            "dataset_csv": optional_field(front, "dataset_csv"),
            "dataset_csv_2": optional_field(front, "dataset_csv_2"),
            "include_howto": optional_field(front, "include_howto"),
            "body": body,
        }

    if len(rows) != len(by_file):
        raise SystemExit(f"Manifest has {len(rows)} rows, content has {len(by_file)} files")

    posts = []
    for row in rows:
        item = by_file.get(row["file"])
        if item is None:
            raise SystemExit(f"Manifest file missing: {row['file']}")
        section = row["section"].strip()
        if section not in SECTIONS:
            raise SystemExit(f"Unknown section {section} for {row['file']}")
        slug = row["slug"].strip() or item["slug"]
        if slug != item["slug"]:
            raise SystemExit(f"Slug mismatch for {row['file']}: {slug} vs {item['slug']}")
        h1_match = re.search(r"^# (.+)$", item["body"], re.M)
        if not h1_match:
            raise SystemExit(f"Missing H1: {row['file']}")
        posts.append(
            {
                **item,
                "rank": int(row["rank"]),
                "section": section,
                "h1": h1_match.group(1).strip(),
                "path": public_path(section, slug),
                "author": (row.get("author") or "").strip(),
                "image_alt": (row.get("image_alt") or "").strip(),
                "image": f"assets/img/{slug}.webp",
                "published": (item.get("date_published") or "").strip() or config["datePublished"],
            }
        )

    posts.sort(key=lambda post: post["rank"])
    for post in posts:
        if post["author"] not in AUTHORS:
            raise SystemExit(f"Unknown or missing author for {post['file']}: {post['author']!r}")
        if not post["image_alt"]:
            raise SystemExit(f"Missing image_alt for {post['file']}")
    slugs = [post["slug"] for post in posts]
    if len(slugs) != len(set(slugs)):
        raise SystemExit("Duplicate slugs")
    return posts, []


def prepare_body(
    post: dict,
    slug_section: dict[str, str],
    unlinked: list[dict],
    base_url: str,
    links: list | None = None,
    sentences: list[str] | None = None,
) -> dict:
    body = post["body"].split("\n## Suggested images", 1)[0].rstrip() + "\n"
    if links:
        body = apply_link_plan(body, links, post)
    elif "_decisions" not in post:
        post["_decisions"] = []
        post["_related_block"] = {"title": "", "items": []}
    extra = list(context_sentences(post))
    extra.extend(sentences or [])
    if extra:
        body = weave_sentences(body, extra)
    dropped_images = {"count": 0}

    def on_image_or_later(label: str, url: str, is_image: bool):
        return None

    def drop_images(label: str, url: str, is_image: bool):
        if is_image:
            dropped_images["count"] += 1
            return ""
        return None

    body = transform_inline(body, drop_images)
    body = linkify_bare_urls(body)

    def rewrite(label: str, url: str, is_image: bool):
        if is_image:
            return None
        target = url.strip()
        fragment = ""
        if "#" in target:
            target, fragment = target.split("#", 1)
            fragment = "#" + fragment
        query = ""
        if "?" in target:
            target, query = target.split("?", 1)
            query = "?" + query
        match = UNPUBLISHED_RE.match(target)
        if match:
            slug = match.group(1)
            if slug in {"areas", "insights"} and re.fullmatch(
                r"https://acrenkey\.com/blogs/(?:areas|insights)/?", target
            ):
                href = relative_href(post["path"], f"{slug}/") + fragment
                return f"[{label}]({href})"
            if static_by_slug(slug):
                href = relative_href(post["path"], f"{slug}/") + fragment
                visible = label
                if label.strip().rstrip("/") == target.rstrip("/"):
                    visible = abs_url(base_url, f"{slug}/")
                return f"[{visible}]({href})"
            section = slug_section.get(slug)
            if section:
                href = relative_href(post["path"], public_path(section, slug)) + fragment
                visible = label
                if label.strip().rstrip("/") == target.rstrip("/"):
                    visible = abs_url(base_url, public_path(section, slug))
                return f"[{visible}]({href})"
            unlinked.append(
                {
                    "from": post["slug"],
                    "slug": slug,
                    "label": plain_markdown(label),
                    "url": url,
                    "kind": "unpublished-post",
                }
            )
            return label
        if target.startswith("/") and not target.startswith("//"):
            unlinked.append(
                {
                    "from": post["slug"],
                    "slug": target,
                    "label": plain_markdown(label),
                    "url": url,
                    "kind": "missing-file",
                }
            )
            return label
        return None

    body = transform_inline(body, rewrite)
    intro, sections = split_sections(body)
    short, takeaways, intro_rest = parse_intro(intro)
    named = {title: rest for title, rest in sections}
    for required in (
        "Frequently asked questions",
        "Talk it through with acre&key",
        "Sources",
    ):
        if required not in named:
            raise SystemExit(f"{post['file']} missing section: {required}")

    content_parts = []
    if intro_rest.strip():
        content_parts.append(intro_rest.strip())
    for title, rest in sections:
        if title in {
            "Frequently asked questions",
            "Talk it through with acre&key",
            "Sources",
        }:
            continue
        content_parts.append(f"## {title}\n\n{rest}".strip())

    howto = None
    if (post.get("include_howto") or "").lower() == "yes":
        for title, rest in sections:
            if not title.lower().startswith("how to"):
                continue
            parts = re.split(r"^### (.+)$", rest, flags=re.M)
            chunks = parts[1:]
            steps = []
            if chunks and len(chunks) % 2 == 0:
                for index in range(0, len(chunks), 2):
                    steps.append((chunks[index].strip(), chunks[index + 1].strip()))
            if len(steps) >= 2:
                howto = {"name": title, "steps": steps}
            break

    faqs = []
    faq_parts = re.split(r"^### (.+)$", named["Frequently asked questions"], flags=re.M)
    # [preamble, q1, a1, q2, a2, ...]
    chunks = faq_parts[1:]
    if len(chunks) % 2 != 0:
        raise SystemExit(f"Broken FAQ in {post['file']}")
    for index in range(0, len(chunks), 2):
        faqs.append((chunks[index].strip(), chunks[index + 1].strip()))
    if not faqs:
        raise SystemExit(f"No FAQs in {post['file']}")

    talk = named["Talk it through with acre&key"].strip()
    talk_paras = [part.strip() for part in re.split(r"\n\s*\n", talk) if part.strip()]
    published_text = "\n".join(
        [
            post["h1"],
            short,
            takeaways,
            "\n\n".join(content_parts),
            named["Frequently asked questions"],
            talk,
            named["Sources"],
        ]
    )
    return {
        "short": short,
        "short_plain": plain_markdown(short.removeprefix("**Short answer:**").strip()),
        "takeaways": takeaways,
        "content_md": "\n\n".join(content_parts).strip(),
        "faqs": faqs,
        "talk_first": talk_paras[0] if talk_paras else "",
        "talk_rest": "\n\n".join(talk_paras[1:]).strip(),
        "sources_md": "## Sources\n\n" + named["Sources"].strip(),
        "dropped_images": dropped_images["count"],
        "words": published_text,
        "howto": howto,
    }


def json_ld(config: dict, post: dict, canonical: str, faqs: list[tuple[str, str]], answer_html: list[str], howto: dict | None = None) -> str:
    org = config["organization"]
    author_key = post["author"]
    profile = AUTHOR_PROFILES[author_key]
    author_id_slug = slugify(profile["name"])
    organization = {
        "@type": "Organization",
        "@id": "https://acrenkey.com/#organization",
        "name": org["brand"],
        "alternateName": "acreNkey",
        "legalName": org["name"],
        "url": org["url"],
        "logo": {
            "@type": "ImageObject",
            "@id": "https://acrenkey.com/#logo",
            "url": "https://acrenkey.com/style-guide/assets/logo.jpg",
            "contentUrl": "https://acrenkey.com/style-guide/assets/logo.jpg",
        },
        "identifier": {
            "@type": "PropertyValue",
            "propertyID": "Karnataka RERA Agent Registration",
            "value": "PRM/KA/RERA/1251/446/AG/260814/007659",
        },
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "8th floor, Summit A, Brigade Metropolis, Brigade Metro Rd, Garudachar Palya, Mahadevapura",
            "addressLocality": "Bengaluru",
            "addressRegion": "Karnataka",
            "postalCode": "560048",
            "addressCountry": "IN",
        },
        "sameAs": [
            "https://www.linkedin.com/company/acrenkey/",
            "https://www.instagram.com/acrenkey/",
            "https://www.youtube.com/channel/UC-6WtLxFOaR_X2y7FQTBcHw",
            "https://x.com/acreNkey",
            "https://www.facebook.com/profile.php?id=61589792184848",
        ],
        "telephone": "+91-9071693393",
    }
    author_entity = {
        "@type": "Person",
        "@id": f"https://acrenkey.com/#{author_id_slug}",
        "name": profile["name"],
        "jobTitle": profile.get("jobTitle") or profile["role"],
        "image": profile["avatar"],
        "description": profile.get("description", ""),
        "worksFor": {"@id": "https://acrenkey.com/#organization"},
        "url": "https://acrenkey.com/",
        "sameAs": [profile["linkedin"]],
    }
    crumb = section_crumb(post, config["baseUrl"])
    breadcrumb_items = [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": org["url"]},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": abs_url(config["baseUrl"])},
    ]
    if crumb:
        breadcrumb_items.append(
            {"@type": "ListItem", "position": 3, "name": crumb[0], "item": crumb[1]}
        )
    breadcrumb_items.append(
        {
            "@type": "ListItem",
            "position": len(breadcrumb_items) + 1,
            "name": post["h1"],
            "item": canonical,
        }
    )
    graph = [
        {
            "@type": "BlogPosting",
            "headline": post["h1"],
            "description": post["meta"],
            "datePublished": post.get("published") or config["datePublished"],
            "dateModified": post["date_modified"] or post.get("published") or config["datePublished"],
            "inLanguage": "en-IN",
            "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
            "url": canonical,
            "image": abs_url(config["baseUrl"], post["image"]),
            "author": author_entity,
            "publisher": organization,
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": [".article-title", ".short-answer"],
            },
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {"@type": "Answer", "text": html_to_text(answer)},
                }
                for (question, _), answer in zip(faqs, answer_html)
            ],
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": breadcrumb_items,
        },
    ]
    if post.get("dataset_name"):
        distribution = []
        for rel in (
            post.get("dataset_distribution") or "",
            post.get("dataset_csv") or "",
            post.get("dataset_csv_2") or "",
        ):
            rel = rel.strip()
            if not rel:
                continue
            distribution.append(
                {
                    "@type": "DataDownload",
                    "encodingFormat": "application/geo+json" if rel.endswith(".geojson") else "text/csv",
                    "contentUrl": abs_url(config["baseUrl"], rel),
                }
            )
        graph.append(
            {
                "@type": "Dataset",
                "name": post["dataset_name"],
                "description": post.get("dataset_description") or post["meta"],
                "url": canonical,
                "creator": organization,
                "spatialCoverage": {"@type": "Place", "name": "Bengaluru"},
                "distribution": distribution,
            }
        )
    if howto and howto.get("steps"):
        graph.append(
            {
                "@type": "HowTo",
                "name": howto["name"],
                "step": [
                    {
                        "@type": "HowToStep",
                        "position": index,
                        "name": plain_markdown(name),
                        "text": plain_markdown(body),
                    }
                    for index, (name, body) in enumerate(howto["steps"], start=1)
                ],
            }
        )
    payload = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return payload.replace("<", "\\u003c")


def json_ld_index(config: dict, posts: list[dict]) -> str:
    org = config["organization"]
    canonical = abs_url(config["baseUrl"])
    organization = {
        "@type": ["RealEstateAgent", "Organization"],
        "@id": "https://acrenkey.com/#organization",
        "name": org["brand"],
        "alternateName": "acreNkey",
        "legalName": org["name"],
        "url": org["url"],
        "logo": {
            "@type": "ImageObject",
            "@id": "https://acrenkey.com/#logo",
            "url": "https://acrenkey.com/style-guide/assets/logo.jpg",
            "contentUrl": "https://acrenkey.com/style-guide/assets/logo.jpg",
        },
        "identifier": {
            "@type": "PropertyValue",
            "propertyID": "Karnataka RERA Agent Registration",
            "value": "PRM/KA/RERA/1251/446/AG/260814/007659",
        },
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "8th floor, Summit A, Brigade Metropolis, Brigade Metro Rd, Garudachar Palya, Mahadevapura",
            "addressLocality": "Bengaluru",
            "addressRegion": "Karnataka",
            "postalCode": "560048",
            "addressCountry": "IN",
        },
        "sameAs": [
            "https://www.linkedin.com/company/acrenkey/",
            "https://www.instagram.com/acrenkey/",
            "https://www.youtube.com/channel/UC-6WtLxFOaR_X2y7FQTBcHw",
            "https://x.com/acreNkey",
            "https://www.facebook.com/profile.php?id=61589792184848",
        ],
        "telephone": "+91-9071693393",
    }
    graph = [
        organization,
        {
            "@type": "WebSite",
            "@id": f"{canonical}#website",
            "url": canonical,
            "name": "acre&key Bengaluru Home Buying Guides",
            "description": (
                "Plain-language guides for people buying a home in Bengaluru: costs, loans, "
                "legal checks, and how neighbourhoods differ."
            ),
            "publisher": {"@id": "https://acrenkey.com/#organization"},
            "inLanguage": "en-IN",
            "potentialAction": {
                "@type": "SearchAction",
                "target": {
                    "@type": "EntryPoint",
                    "urlTemplate": f"{canonical}?q={{search_term_string}}",
                },
                "query-input": "required name=search_term_string",
            },
        },
        {
            "@type": "Blog",
            "@id": f"{canonical}#blog",
            "url": canonical,
            "name": "Bengaluru Home Buying Guides",
            "description": (
                "Plain-language guides for people buying a home in Bengaluru: costs, loans, "
                "legal checks, and how neighbourhoods differ."
            ),
            "publisher": {"@id": "https://acrenkey.com/#organization"},
            "inLanguage": "en-IN",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": org["url"]},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": canonical},
            ],
        },
    ]
    payload = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return payload.replace("<", "\\u003c")


def head_tags(title: str, description: str, canonical: str, root: str, og_type: str, published: str | None, jsonld: str | None, image: str | None = None, author: str | None = None) -> str:
    brand = "acre&amp;key"
    lines = [
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<meta name="theme-color" content="#2B2D31">',
        f"<title>{esc(title)} | {brand}</title>",
        f'<meta name="description" content="{esc(description)}">',
        f'<meta name="author" content="{esc(author or "Acrenkey Realty LLP")}">',
        f'<link rel="canonical" href="{esc(canonical)}">',
        f'<link rel="preload" href="{root}assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>',
        f'<link rel="preload" href="{root}assets/fonts/cormorant-garamond-latin.woff2" as="font" type="font/woff2" crossorigin>',
        f'<link rel="icon" type="image/svg+xml" sizes="any" href="{root}{asset("favicon.svg")}">',
        f'<link rel="icon" type="image/png" sizes="48x48" href="{root}{asset("favicon-48x48.png")}">',
        f'<link rel="icon" type="image/png" sizes="32x32" href="{root}{asset("favicon-32x32.png")}">',
        f'<link rel="icon" type="image/png" sizes="16x16" href="{root}{asset("favicon-16x16.png")}">',
        f'<link rel="apple-touch-icon" sizes="180x180" href="{root}{asset("apple-touch-icon.png")}">',
        f'<link rel="shortcut icon" href="{root}{asset("favicon.ico")}">',
        f'<link rel="manifest" href="{root}{asset("site.webmanifest")}">',
        f'<link rel="stylesheet" href="{root}{asset("style.css")}">',
        f'<link rel="stylesheet" href="{root}{asset("assets/ak-chrome.css")}">',
        f'<link rel="stylesheet" href="{root}{asset("assets/ak-lead-form.css")}">',
        f'<script src="{root}{asset("assets/ak-chrome.js")}" defer></script>',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(description)}">',
        f'<meta property="og:url" content="{esc(canonical)}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:site_name" content="{brand}">',
        '<meta property="og:locale" content="en_IN">',
        f'<meta name="twitter:card" content="{"summary_large_image" if image else "summary"}">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(description)}">',
    ]
    if image:
        lines += [
            f'<meta property="og:image" content="{esc(image)}">',
            f'<meta property="og:image:width" content="{IMAGE_W}">',
            f'<meta property="og:image:height" content="{IMAGE_H}">',
            f'<meta name="twitter:image" content="{esc(image)}">',
        ]
    if published:
        lines.append(f'<meta property="article:published_time" content="{esc(published)}">')
    if jsonld:
        lines.append(f'<script type="application/ld+json">{jsonld}</script>')
    return "\n  ".join(lines)


PARTIALS = Path(__file__).resolve().parent / "partials"


def asset(rel: str) -> str:
    """Asset path with a content-hash query so edge caches (Cloudflare, max-age 7d) pick up new CSS/JS on deploy."""
    digest = hashlib.sha1((ROOT / rel).read_bytes()).hexdigest()[:10]
    return f"{rel}?v={digest}"


def consult_modal(root: str) -> str:
    """acrenkey.com "Start Consultation" pop-up: markup from grvmon/a-K index.html (scripts/partials/lead-form-modal.html)
    plus its script (assets/ak-lead-form.js = a-K lead-form.min.js, which defines window.openModal and posts to HubSpot)."""
    markup = (PARTIALS / "lead-form-modal.html").read_text().strip()
    return f'<script src="{root}{asset("assets/ak-lead-form.js")}" defer></script>{markup}'


def blog_subnav(current: str = "", base: str = "https://acrenkey.com/blogs/") -> str:
    """Blog section nav. Sits in normal flow under the fixed site header."""
    items = [
        ("properties", "Properties", "https://acrenkey.com/property/"),
        ("calculators", "Calculators", "https://acrenkey.com/calculators/"),
        ("index", "Blog", abs_url(base)),
    ]
    for hub in HUBS:
        items.append((hub["key"], hub["name"], abs_url(base, hub["path"])))
    items.append(("answers", "Answers", "https://answers.acrenkey.com/"))
    links = []
    for key, label, href in items:
        current_attr = ' aria-current="page"' if key == current else ""
        links.append(f'<a href="{esc(href)}"{current_attr}>{esc(label)}</a>')
    return (
        '<nav class="blog-subnav" aria-label="Blog">'
        f'<div class="blog-subnav-inner">{"".join(links)}</div></nav>'
    )


def header(root: str, current: str = "", base: str = "https://acrenkey.com/blogs/") -> str:
    """acrenkey.com header, copied from grvmon/a-K index.html (scripts/partials/header.html)."""
    return (
        '<a href="#main-content" class="skip-link">Skip to main content</a>\n  '
        + (PARTIALS / "header.html").read_text().strip()
    )


def browse_row(base: str, current: str = "") -> str:
    links = []
    for hub in HUBS:
        if hub.get("section"):
            continue
        current_attr = ' aria-current="page"' if hub["key"] == current else ""
        href = abs_url(base, hub["path"])
        links.append(
            f'<a class="browse-link" href="{esc(href)}"{current_attr}>{esc(hub["name"])}</a>'
        )
    return '<nav class="browse-row" aria-label="Browse by">' + "".join(links) + "</nav>"


def hub_prose(hub: dict) -> str:
    """In-sentence name. Nav chips keep the short hub label."""
    return hub.get("prose") or hub["name"]


def hub_intro(hub: dict, base: str) -> str:
    """One link per sentence. Each hub points at the full guide index and two neighbours."""
    first, second = sibling_hubs(hub["key"])[:2]
    paragraphs = [
        f'<p class="hub-intro">These notes are part of the <a href="{esc(abs_url(base))}">full set of guides</a>.</p>',
        (
            f'<p class="hub-intro">The collection beside this one is '
            f'<a href="{esc(abs_url(base, first["path"]))}">{esc(hub_prose(first))}</a>.</p>'
        ),
        (
            f'<p class="hub-intro">Another grouping is '
            f'<a href="{esc(abs_url(base, second["path"]))}">{esc(hub_prose(second))}</a>.</p>'
        ),
    ]
    if hub["key"] == "areas":
        paragraphs.append(
            '<p class="hub-intro">Reviewed projects are listed on the '
            '<a href="https://acrenkey.com/property/">Properties page</a>.</p>'
        )
    return "\n    ".join(paragraphs)


def footer(root: str) -> str:
    """acrenkey.com homepage footer, copied from grvmon/a-K index.html (scripts/partials/footer.html)."""
    return (PARTIALS / "footer.html").read_text().strip()


def cta_link(extra_class: str = "") -> str:
    classes = "primary-cta-btn" + (f" {extra_class}" if extra_class else "")
    return f"""<a href="https://acrenkey.com/" class="{classes}">
              <span>Request Advisory Call</span>
              <span class="cta-arrow-badge" aria-hidden="true">{CTA_ARROW}</span>
            </a>"""


def takeaway_html(source: str) -> str:
    list_md = "\n".join(line for line in source.splitlines() if line.startswith("- "))
    fragment = render_markdown(list_md)
    match = re.search(r"<ul>.*</ul>", fragment, re.S)
    if not match:
        raise SystemExit("Key takeaways did not render as a list")
    listing = match.group(0).replace("<ul>", '<ul class="summary-list">', 1)
    return f"""<div class="executive-summary-box">
          <div class="summary-heading">
            {TOC_ICON}
            <span>Key takeaways</span>
          </div>
          {listing}
        </div>"""


def toc_html(entries: list[tuple[str, str]]) -> str:
    items = "\n".join(
        f'            <li><a href="#{esc(heading_id)}">{esc(title)}</a></li>'
        for heading_id, title in entries
    )
    return f"""<div class="toc-box">
          <div class="toc-title">
            {TOC_ICON}
            <span>Table of contents</span>
          </div>
          <ol class="toc-list">
{items}
          </ol>
        </div>"""


def faq_html(faqs: list[tuple[str, str]]) -> str:
    blocks = []
    for question, answer_md in faqs:
        answer = wrap_tables(render_markdown(answer_md))
        blocks.append(
            f"""<div class="faq-item">
              <button type="button" class="faq-trigger" aria-expanded="false">
                <span>{esc(question)}</span>
                {FAQ_CHEVRON}
              </button>
              <div class="faq-body">
                {answer}
              </div>
            </div>"""
        )
    inner = "\n            ".join(blocks)
    return f"""<section class="faq-section" aria-labelledby="frequently-asked-questions">
          <h2 id="frequently-asked-questions" class="faq-title">Frequently asked questions</h2>
          <div class="faq-accordion-group">
            {inner}
          </div>
        </section>""", [wrap_tables(render_markdown(answer)) for _, answer in faqs]


def banner_html(first_md: str, heading_id: str) -> str:
    paragraph = render_markdown(first_md)
    return f"""<div class="in-article-advisory-banner">
            <span class="banner-kicker">acre&amp;key</span>
            <h2 id="{esc(heading_id)}">Talk it through with acre&amp;key</h2>
            {paragraph}
            {cta_link()}
          </div>"""


def related_sidebar(post: dict, posts: list[dict]) -> str:
    same = [item for item in posts if item["section"] == post["section"] and item["slug"] != post["slug"]]
    same.sort(key=lambda item: abs(item["rank"] - post["rank"]))
    picked = same[:4]
    if len(picked) < 4:
        others = [item for item in posts if item["slug"] != post["slug"] and item not in picked]
        others.sort(key=lambda item: abs(item["rank"] - post["rank"]))
        picked.extend(others[: 4 - len(picked)])
    items = []
    for item in picked:
        href = relative_href(post["path"], item["path"])
        items.append(
            f"""<li>
              <a href="{esc(href)}" class="widget-link-thumb">
                {img_tag(site_prefix(post['path']), item, 'widget-thumb')}
                <span>{esc(item['h1'])}</span>
              </a>
            </li>"""
        )
    return "\n            ".join(items)


def prev_next(post: dict, posts: list[dict]) -> str:
    index = next(i for i, item in enumerate(posts) if item["slug"] == post["slug"])
    cards = []
    if index > 0:
        prev_post = posts[index - 1]
        cards.append(
            f"""<a href="{esc(relative_href(post['path'], prev_post['path']))}" class="nav-article-card">
              {img_tag(site_prefix(post['path']), prev_post, 'nav-card-img')}
              <span class="nav-kicker">&larr; Previous</span>
              <p class="nav-card-heading">{esc(prev_post['h1'])}</p>
            </a>"""
        )
    if index < len(posts) - 1:
        next_post = posts[index + 1]
        cards.append(
            f"""<a href="{esc(relative_href(post['path'], next_post['path']))}" class="nav-article-card">
              {img_tag(site_prefix(post['path']), next_post, 'nav-card-img')}
              <span class="nav-kicker">Next &rarr;</span>
              <p class="nav-card-heading">{esc(next_post['h1'])}</p>
            </a>"""
        )
    return "\n            ".join(cards)


def render_post(config: dict, post: dict, prepared: dict, posts: list[dict], ids: IdFactory) -> str:
    canonical = abs_url(config["baseUrl"], post["path"])
    root = site_prefix(post["path"])
    content_html = wrap_tables(ids.stamp(render_markdown(prepared["content_md"])))
    sources_html = wrap_tables(ids.stamp(render_markdown(prepared["sources_md"])))
    short_html = render_markdown(prepared["short"])
    faq_block, answer_html = faq_html(prepared["faqs"])
    talk_id = ids.make("Talk it through with acre&key")
    toc_entries = heading_entries(content_html)
    toc_entries.append(("frequently-asked-questions", "Frequently asked questions"))
    toc_entries.append((talk_id, "Talk it through with acre&key"))
    toc_entries.extend(heading_entries(sources_html))
    published = post.get("published") or config["datePublished"]
    minutes = read_time(prepared["words"])
    shown_date = format_date(published)
    share_text = esc(post["h1"])
    share_url = esc(canonical)
    # quote for share endpoints separately
    from urllib.parse import quote

    wa = quote(f"{post['h1']} {canonical}")
    linkedin = quote(canonical, safe="")
    tweet = quote(post["h1"])
    tweet_url = quote(canonical, safe="")
    ld = json_ld(config, post, canonical, prepared["faqs"], answer_html, prepared.get("howto"))
    talk_rest = wrap_tables(render_markdown(prepared["talk_rest"])) if prepared["talk_rest"] else ""
    profile = AUTHOR_PROFILES.get(
        post["author"],
        {
            "name": post["author"],
            "role": "Market Strategy · Product · Tech",
            "avatar": "https://acrenkey.com/style-guide/assets/gaurav-mongia-founder-acre-key.webp",
            "linkedin": "https://www.linkedin.com/in/gaurav-a-mongia/",
        },
    )
    crumb = section_crumb(post, config["baseUrl"])
    if crumb:
        bc_section_html = (
            f'\n        <li class="meta-sep" aria-hidden="true">/</li>'
            f'\n        <li><a href="{esc(crumb[1])}">{esc(crumb[0])}</a></li>'
        )
    else:
        bc_section_html = ""

    blocks = post.get("_related_blocks") or ([post["_related_block"]] if post.get("_related_block") and post["_related_block"].get("title") else [])
    related_blocks_markup = "\n        ".join(related_block_html(b["title"], b["items"]) for b in blocks)

    page = f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
  {head_tags(post['seo_title'], post['meta'], canonical, root, 'article', published, ld, abs_url(config['baseUrl'], post['image']), post['author'])}
</head>
<body>
  <div id="scroll-progress-bar" aria-hidden="true"></div>
  {header(root, nav_current(post), config['baseUrl'])}
  <main id="main-content" class="container blog-detail-container">
    <nav aria-label="Breadcrumb">
      <ol class="breadcrumb">
        <li><a href="https://acrenkey.com/">Home</a></li>
        <li class="meta-sep" aria-hidden="true">/</li>
        <li><a href="{esc(config['baseUrl'])}">Blog</a></li>{bc_section_html}
        <li class="meta-sep" aria-hidden="true">/</li>
        <li class="bc-current" aria-current="page" title="{esc(post['h1'])}">{esc(post['seo_title'])}</li>
      </ol>
    </nav>
    <header class="article-header">
      <h1 class="article-title">{esc(post['h1'])}</h1>
      <div class="author-byline-card">
        <div class="author-byline-main">
          <a href="https://acrenkey.com/#about-us" class="author-avatar-link" aria-label="{esc(profile['name'])}">
            <img src="{esc(profile['avatar'].replace('.webp','-96.webp'))}" alt="{esc(profile['name'])}" class="author-avatar-img" width="46" height="46" loading="lazy" decoding="async">
          </a>
          <div class="author-meta-wrap">
            <div class="author-name-row">
              <a href="https://acrenkey.com/#about-us" class="author-name-link"><span class="author-details-name">{esc(profile['name'])}</span></a>
              <a href="{esc(profile['linkedin'])}" class="author-linkedin-badge" target="_blank" rel="noopener noreferrer" aria-label="{esc(profile['name'])} on LinkedIn">
                <svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
              </a>
            </div>
            <div class="author-subline author-details-sub byline">
              <span>{esc(profile['role'])}</span>
              <span class="author-subline-dot" aria-hidden="true">&bull;</span>
              <span>Published: <time datetime="{esc(published)}">{esc(shown_date)}</time></span>
              <span class="author-subline-dot" aria-hidden="true">&bull;</span>
              <span>{minutes} min read</span>
            </div>
          </div>
        </div>
        <div class="share-strip">
          <span class="share-label">Share:</span>
          <a href="https://api.whatsapp.com/send?text={wa}" target="_blank" rel="noopener noreferrer" class="share-btn" aria-label="Share on WhatsApp" title="Share on WhatsApp">{SHARE_WA}</a>
          <a href="https://www.linkedin.com/sharing/share-offsite/?url={linkedin}" target="_blank" rel="noopener noreferrer" class="share-btn" aria-label="Share on LinkedIn" title="Share on LinkedIn">{SHARE_LI}</a>
          <a href="https://twitter.com/intent/tweet?text={tweet}&amp;url={tweet_url}" target="_blank" rel="noopener noreferrer" class="share-btn" aria-label="Share on X" title="Share on X">{SHARE_X}</a>
          <button type="button" class="share-btn" data-copy-link aria-label="Copy link to clipboard" title="Copy article link">{SHARE_COPY}</button>
        </div>
      </div>
    </header>
    <figure class="article-hero">
      {img_tag(root, post, 'article-hero-img', hero=True)}
    </figure>
    <div class="blog-layout-grid">
      <article class="article-content">
        <div class="short-answer">{short_html}</div>
        {takeaway_html(prepared['takeaways'])}
        {toc_html(toc_entries)}
        <div class="article-prose">
          {content_html}
        </div>
        {faq_block}
        <div class="article-prose">
          {banner_html(prepared['talk_first'], talk_id)}
          {talk_rest}
          {sources_html}
        </div>
        <div class="author-bio-card">
          <img class="author-bio-avatar" src="{esc(profile['avatar'].replace('.webp','-144.webp'))}" srcset="{esc(profile['avatar'].replace('.webp','-96.webp'))} 1x, {esc(profile['avatar'].replace('.webp','-144.webp'))} 2x" alt="{esc(profile['name'])}" width="72" height="72" loading="lazy" decoding="async">
          <div>
            <p class="author-bio-title">Written by {esc(profile['name'])}</p>
            <span class="author-bio-role">Acrenkey Realty LLP</span>
            <p class="author-bio-desc">Published by Acrenkey Realty LLP, a property advisory for people buying a home in Bengaluru.</p>
          </div>
        </div>
        {related_blocks_markup}
        <section class="related-section" aria-label="More guides">
          <div class="related-grid">
            {prev_next(post, posts)}
          </div>
        </section>
      </article>
      <aside class="blog-sidebar">
        <div class="sidebar-widget">
          <span class="widget-kicker">Advisory</span>
          <h3>Buying a home in Bengaluru?</h3>
          <p>Acrenkey Realty LLP reads the price, the papers and the area with you.</p>
          {cta_link('sidebar-btn-full')}
        </div>
        <div class="sidebar-widget" style="background: rgba(128, 69, 38, 0.04); border-color: rgba(128, 69, 38, 0.2);">
          <span class="widget-kicker">Calculators</span>
          <h3>Work out the numbers</h3>
          <p>Stamp duty, registration and EMI calculators stay on acrenkey.com.</p>
          <a href="https://acrenkey.com/calculators/" class="primary-cta-btn sidebar-btn-full" style="background: var(--obsidian-black);">
            <span>Open calculators</span>
          </a>
        </div>
        <div class="sidebar-widget">
          <span class="widget-kicker">Related guides</span>
          <h3>Keep reading</h3>
          <ul class="widget-links">
            {related_sidebar(post, posts)}
          </ul>
        </div>
      </aside>
    </div>
  </main>
  {footer(root)}
  <script src="{root}{asset("site.js")}"></script>
  {consult_modal(root)}
</body>
</html>
"""
    # silence unused locals kept for clarity if a future share label needs them
    del share_text, share_url
    return page


def render_index(config: dict, posts: list[dict], excerpts: dict[str, str]) -> str:
    canonical = abs_url(config["baseUrl"])
    description = (
        "Plain-language guides for people buying a home in Bengaluru: costs, loans, "
        "legal checks, and how neighbourhoods differ."
    )
    title = "Bengaluru home buying guides: costs, loans, legal checks"
    topic_counts = {topic: sum(1 for post in posts if post.get("topic") == topic) for topic in TOPIC_SLUG}
    cards = []
    for post in posts:
        topic = post.get("topic") or ""
        pillar_slug = TOPIC_SLUG.get(topic, "")
        badge_text = topic or SECTION_LABEL.get(post["section"], "Guide")
        search = " ".join(
            [
                post["h1"],
                excerpts[post["slug"]],
                post["meta"],
                post["seo_title"],
                topic,
                pillar_slug,
                SECTION_LABEL[post["section"]],
                post["section"],
            ]
        ).lower()
        author_prof = AUTHOR_PROFILES[post["author"]]
        author_thumb = author_prof.get("thumb") or author_prof["avatar"]
        author_name = author_prof["name"]
        cards.append(
            f"""<article class="blog-card" data-section="{esc(post['section'])}" data-pillar="{esc(pillar_slug)}" data-rank="{post['rank']}" data-search="{esc(search)}">
        <a href="{esc(post['path'])}" class="blog-card-media tone-{esc(post['section'])}" aria-label="Read {esc(post['h1'])}">
          {img_tag('', post, 'blog-card-img')}
          <span class="cat-badge">{esc(badge_text)}</span>
        </a>
        <div class="blog-card-body">
          <div class="blog-card-author">
            <img src="{esc(author_thumb)}" alt="{esc(author_name)}" class="card-author-img" width="28" height="28" loading="lazy">
            <span class="card-author-name">{esc(author_name)}</span>
          </div>
          <h2 class="blog-card-title">
            <a href="{esc(post['path'])}">{esc(post['h1'])}</a>
          </h2>
        </div>
      </article>"""
        )
    grid = "\n\n      ".join(cards)
    ld = json_ld_index(config, posts)
    page = f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
  {head_tags(title, description, canonical, '', 'website', None, ld, abs_url(config['baseUrl'], 'assets/img/first-time-home-buyer-guide-bengaluru.webp'))}
</head>
<body>
  {header('', 'index', config['baseUrl'])}
  <section class="blog-home-hero">
    <div class="hero-wrap">
      <div class="kicker-badge">Bengaluru home buying</div>
      <h1>Guides for buying a home in Bengaluru.</h1>
      <p class="hero-lead">
        Costs, paperwork, loans and neighbourhood notes for people choosing a home in Bengaluru.
      </p>
      <div class="search-container">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input type="text" id="blogSearchInput" class="search-input" placeholder="Search guides, for example Whitefield, khata, stamp duty" aria-label="Search guides">
        <button type="button" class="search-clear-btn" id="searchClearBtn" aria-label="Clear search query" hidden>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>
  </section>
  <main id="main-content" class="container">
    <div class="category-filter-strip" role="tablist" aria-label="Filter guides by topic">
      <a href="{esc(abs_url(config['baseUrl']))}" class="cat-btn active" data-pillar="all" data-count="{len(posts)}" role="tab" aria-selected="true">All Guides</a>
      <a href="{esc(abs_url(config['baseUrl'], 'topic/localities-corridors/'))}" class="cat-btn" data-pillar="localities-corridors" data-count="{topic_counts.get('Localities & Corridors', 0)}" role="tab" aria-selected="false">Localities &amp; Corridors</a>
      <a href="{esc(abs_url(config['baseUrl'], 'topic/buying-checklists/'))}" class="cat-btn" data-pillar="buying-checklists" data-count="{topic_counts.get('Buyer Checklists & Process', 0)}" role="tab" aria-selected="false">Buyer Checklists &amp; Process</a>
      <a href="{esc(abs_url(config['baseUrl'], 'topic/legal-rera/'))}" class="cat-btn" data-pillar="legal-rera" data-count="{topic_counts.get('Legal, Title & RERA', 0)}" role="tab" aria-selected="false">Legal, Title &amp; RERA</a>
      <a href="{esc(abs_url(config['baseUrl'], 'topic/loans-costs-tax/'))}" class="cat-btn" data-pillar="loans-costs-tax" data-count="{topic_counts.get('Loans, Taxes & Total Costs', 0)}" role="tab" aria-selected="false">Loans, Taxes &amp; Total Costs</a>
      <a href="{esc(abs_url(config['baseUrl'], 'topic/water-environment/'))}" class="cat-btn" data-pillar="water-environment" data-count="{topic_counts.get('Environment & Water Checks', 0)}" role="tab" aria-selected="false">Environment &amp; Water Checks</a>
    </div>
    <div class="blog-grid" id="blogGrid">
      {grid}
    </div>
    <div id="noResults" style="display:none; text-align:center; padding: 4rem 1rem; color: var(--neutral-grey);">
      <p style="font-family: var(--font-serif); font-size: 1.5rem; color: var(--obsidian-black); margin-bottom: 0.5rem;">No matching guides.</p>
      <p>Try another word, or choose All.</p>
    </div>
  </main>
  {footer('')}
  <script src="{asset("site.js")}"></script>
  {consult_modal('')}
</body>
</html>
"""
    return page


def render_hub(config: dict, hub: dict, children: list[dict], excerpts: dict[str, str]) -> str:
    base = config["baseUrl"]
    canonical = abs_url(base, hub["path"])
    root = site_prefix(hub["path"])
    published = config["datePublished"]
    cards = []
    for post in children:
        href = relative_href(hub["path"], post["path"])
        topic = post.get("topic") or ""
        pillar_slug = TOPIC_SLUG.get(topic, "")
        badge_text = topic or SECTION_LABEL.get(post["section"], "Guide")
        search = " ".join(
            [
                post["h1"],
                excerpts.get(post["slug"], ""),
                post.get("meta") or "",
                post.get("seo_title") or "",
                topic,
                pillar_slug,
                SECTION_LABEL[post["section"]],
                post["section"],
            ]
        ).lower()
        shown = post.get("published") or published
        author_prof = AUTHOR_PROFILES[post["author"]]
        author_thumb = author_prof.get("thumb") or author_prof["avatar"]
        author_name = author_prof["name"]
        cards.append(
            f"""<article class="blog-card" data-section="{esc(post['section'])}" data-pillar="{esc(pillar_slug)}" data-rank="{post['rank']}" data-search="{esc(search)}">
        <a href="{esc(href)}" class="blog-card-media tone-{esc(post['section'])}" aria-label="Read {esc(post['h1'])}">
          {img_tag(root, post, 'blog-card-img')}
          <span class="cat-badge">{esc(badge_text)}</span>
        </a>
        <div class="blog-card-body">
          <div class="blog-card-author">
            <img src="{esc(author_thumb)}" alt="{esc(author_name)}" class="card-author-img" width="28" height="28" loading="lazy">
            <span class="card-author-name">{esc(author_name)}</span>
          </div>
          <h2 class="blog-card-title">
            <a href="{esc(href)}">{esc(post['h1'])}</a>
          </h2>
        </div>
      </article>"""
        )
    image = abs_url(base, children[0]["image"]) if children else None
    items = []
    for index, post in enumerate(children, start=1):
        items.append(
            {
                "@type": "ListItem",
                "position": index,
                "url": abs_url(base, post["path"]),
                "name": post["h1"],
            }
        )
    graph = [
        {
            "@type": "Organization",
            "@id": "https://acrenkey.com/#organization",
            "name": config["organization"]["brand"],
            "url": config["organization"]["url"],
        },
        {
            "@type": "CollectionPage",
            "@id": canonical,
            "url": canonical,
            "name": hub["h1"],
            "description": hub["description"],
            "isPartOf": {"@id": abs_url(base) + "#blog"},
            "inLanguage": "en-IN",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acrenkey.com/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": abs_url(base)},
                {"@type": "ListItem", "position": 3, "name": hub["h1"], "item": canonical},
            ],
        },
        {"@type": "ItemList", "itemListElement": items},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("<", "\\u003c")
    grid = "\n\n      ".join(cards)
    return f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
  {head_tags(hub['title'], hub['description'], canonical, root, 'website', published, ld, image)}
</head>
<body>
  {header(root, hub['key'], base)}
  <main id="main-content" class="container">
    <nav aria-label="Breadcrumb">
      <ol class="breadcrumb">
        <li><a href="https://acrenkey.com/">Home</a></li>
        <li class="meta-sep" aria-hidden="true">/</li>
        <li><a href="{esc(abs_url(base))}">Blog</a></li>
        <li class="meta-sep" aria-hidden="true">/</li>
        <li class="bc-current" aria-current="page">{esc(hub['h1'])}</li>
      </ol>
    </nav>
    <header class="hub-header">
      <h1>{esc(hub['h1'])}</h1>
      <p class="hub-lead">{esc(hub['lead'])}</p>
    </header>
    {hub_intro(hub, base)}
    {browse_row(base, hub['key'])}
    <div class="search-container">
      <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
      <input type="text" id="blogSearchInput" class="search-input" placeholder="Search these guides" aria-label="Search these guides">
    </div>
    <div class="blog-grid" id="blogGrid">
      {grid}
    </div>
    {related_block_html("Related reading", [(label, url) for url, label in ZONE_LINKS]) if hub["key"] == "areas" else ""}
    <div id="noResults" style="display:none; text-align:center; padding: 4rem 1rem; color: var(--neutral-grey);">
      <p style="font-family: var(--font-serif); font-size: 1.5rem; color: var(--obsidian-black); margin-bottom: 0.5rem;">No matching guides.</p>
      <p>Try another word.</p>
    </div>
  </main>
  {footer(root)}
  <script src="{root}{asset("site.js")}"></script>
  {consult_modal(root)}
</body>
</html>
"""


def render_sitemap(config: dict, posts: list[dict], extras: list[dict] | None = None) -> str:
    dated = [(abs_url(config["baseUrl"]), config["datePublished"])]
    dated.extend((abs_url(config["baseUrl"], hub["path"]), config["datePublished"]) for hub in HUBS)
    dated.extend(
        (abs_url(config["baseUrl"], post["path"]), post.get("published") or config["datePublished"])
        for post in posts
    )
    dated.extend(
        (abs_url(config["baseUrl"], post["path"]), post.get("published") or config["datePublished"])
        for post in (extras or [])
    )
    body = []
    for url, lastmod in dated:
        body.append(
            "  <url>\n"
            f"    <loc>{esc(url)}</loc>\n"
            f"    <lastmod>{esc(lastmod)}</lastmod>\n"
            "  </url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(body)
        + "\n</urlset>\n"
    )


def render_robots(config: dict) -> str:
    sitemap = abs_url(config["baseUrl"], "sitemap.xml")
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {sitemap}\n"
    )


def render_llms(config: dict, posts: list[dict], excerpts: dict[str, str], extras: list[dict] | None = None) -> str:
    lines = [
        "# acre&key",
        "",
        "> Guides from Acrenkey Realty LLP for people buying a home in Bengaluru.",
        "",
        "Published by the organization Acrenkey Realty LLP. Each guide carries a byline from one of the team: Gaurav, Nitin or Arvind.",
        "",
    ]
    for section in SECTIONS:
        lines.append(f"## {SECTION_LABEL[section]}")
        lines.append("")
        for post in posts:
            if post["section"] != section:
                continue
            url = abs_url(config["baseUrl"], post["path"])
            lines.append(f"- [{post['h1']}]({url}) (by {post['author']}): {excerpts[post['slug']]}")
        if section == "blog":
            for post in extras or []:
                url = abs_url(config["baseUrl"], post["path"])
                lines.append(f"- [{post['h1']}]({url}) (by {post['author']}): {excerpts[post['slug']]}")
        lines.append("")
    lines.append("## Hubs")
    lines.append("")
    for hub in HUBS:
        lines.append(f"- [{hub['h1']}]({abs_url(config['baseUrl'], hub['path'])}): {hub['description']}")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def visible_text(page: str) -> str:
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", page, flags=re.I | re.S)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<head\b[^>]*>.*?</head>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)


def head_text(page: str) -> str:
    match = re.search(r"<head\b[^>]*>(.*?)</head>", page, flags=re.I | re.S)
    if not match:
        return ""
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", match.group(1), flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)


def find_banned(text: str) -> list[tuple[str, str]]:
    hits = []
    for pattern, name in BANNED:
        for match in pattern.finditer(text):
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            snippet = re.sub(r"\s+", " ", text[start:end]).strip()
            hits.append((name, snippet))
    return hits


def validate(config: dict, posts: list[dict], unlinked: list[dict], pages: dict[Path, str]) -> dict:
    problems = []
    by_path = {ROOT / post["path"] / "index.html": post for post in posts}
    for post in posts:
        image_file = ROOT / post["image"]
        if not image_file.is_file():
            problems.append(f"missing image file {post['image']}")
        elif image_file.stat().st_size > 150 * 1024:
            problems.append(f"{post['image']} is over 150 KB")
    body_hits = []
    head_hits = []
    bangalore_body = []
    for path, page in pages.items():
        rel = str(path.relative_to(ROOT))
        h1s = re.findall(r"<h1\b", page)
        if len(h1s) != 1:
            problems.append(f"{rel} has {len(h1s)} h1 tags")
        if 'rel="canonical"' not in page:
            problems.append(f"{rel} missing canonical")
        if "/blogs/blogs/" in page:
            problems.append(f"{rel} still uses a doubled /blogs/blogs/ path")
        if "100%" in re.sub(r"https?://\S+", " ", visible_text(page)):
            problems.append(f"{rel} still contains 100% in visible copy")
        if path.name == "index.html" and path.parent == ROOT:
            if "institutional and high-net-worth asset acquisitions" in page:
                problems.append("index meta was not replaced")
            if "Blog" not in page or "WebSite" not in page or "RealEstateAgent" not in page:
                problems.append("index.html missing JSON-LD schemas")
            continue
        if is_hub_page(path):
            if "CollectionPage" not in page or "BreadcrumbList" not in page:
                problems.append(f"{rel} missing hub schema")
            blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
            if not blocks:
                problems.append(f"{rel} missing JSON-LD")
            for block in blocks:
                try:
                    json.loads(block)
                except ValueError as exc:
                    problems.append(f"{rel} JSON-LD does not parse: {exc}")
        else:
            for token in ("BlogPosting", "FAQPage", "BreadcrumbList"):
                if token not in page:
                    problems.append(f"{rel} missing {token}")
            post_for_date = by_path.get(path)
            static_meta = static_by_slug(path.parent.name) if path.name == "index.html" else None
            published = (post_for_date or {}).get("published") or (static_meta or {}).get("published") or config["datePublished"]
            if published not in page:
                problems.append(f"{rel} missing datePublished")
            post = by_path.get(path)
            if post:
                blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
                try:
                    graph = [node for block in blocks for node in json.loads(block)["@graph"]]
                except (ValueError, KeyError) as exc:
                    problems.append(f"{rel} JSON-LD does not parse: {exc}")
                    graph = []
                article = next((node for node in graph if node.get("@type") == "BlogPosting"), {})
                author = article.get("author", {})
                prof = AUTHOR_PROFILES[post["author"]]
                if author.get("@type") != "Person" or author.get("name") != prof["name"]:
                    problems.append(f"{rel} JSON-LD author is not {prof['name']}")
                if article.get("publisher", {}).get("@type") != "Organization":
                    problems.append(f"{rel} publisher is not the Organization")
                if article.get("speakable", {}).get("@type") != "SpeakableSpecification":
                    problems.append(f"{rel} missing speakable schema")
                want_img = abs_url(config["baseUrl"], post["image"])
                if article.get("image") != want_img:
                    problems.append(f"{rel} Article image mismatch")
                for prop in ('property="og:image"', 'name="twitter:image"'):
                    if f'{prop} content="{want_img}"' not in page:
                        problems.append(f"{rel} missing {prop}")
                if not re.search(r'class="author-details-name">' + re.escape(post["author"]), page):
                    problems.append(f"{rel} byline does not show {post['author']}")
                if 'fetchpriority="high"' not in page or 'class="article-hero-img" loading="eager"' not in page:
                    problems.append(f"{rel} hero image missing eager/fetchpriority")
        old_hrefs = [
            href
            for href in re.findall(r'href="([^"]+)"', page)
            if re.search(r"https://acrenkey\.com/(?:blog(?!s)/|insights/)", href)
        ]
        if old_hrefs:
            problems.append(f"{rel} still links to an old blog path")
        body = re.sub(r"https?://\S+", " ", visible_text(page))
        for name, snippet in find_banned(body):
            body_hits.append((rel, name, snippet))
        for name, snippet in find_banned(head_text(page)):
            head_hits.append((rel, name, snippet))
        for match in re.finditer(r"Bangalore", body):
            start = max(0, match.start() - 40)
            end = min(len(body), match.end() + 40)
            bangalore_body.append((rel, re.sub(r"\s+", " ", body[start:end])))

    # Images: every <img> has a non-empty alt, size attributes and a file that exists.
    for path, page in pages.items():
        for tag in re.findall(r"<img\b[^>]*>", page):
            src = re.search(r'src="([^"]*)"', tag)
            alt = re.search(r'alt="([^"]*)"', tag)
            if not alt or not alt.group(1).strip():
                problems.append(f"{path.relative_to(ROOT)} img without alt: {tag[:80]}")
            if 'width="' not in tag or 'height="' not in tag:
                problems.append(f"{path.relative_to(ROOT)} img without width/height")
            if src and not src.group(1).startswith(("http://", "https://", "data:")):
                target = (path.parent / src.group(1)).resolve()
                if not target.is_file():
                    problems.append(f"{path.relative_to(ROOT)} -> missing image {src.group(1)}")
        for attr, value in re.findall(r'\b(href|src)="(/[^"]*)"', page):
            if not value.startswith("//"):
                problems.append(f"{path.relative_to(ROOT)} has root-relative {attr}={value}")
                break

    # Internal relative links resolve.
    for path, page in pages.items():
        for href in re.findall(r'href="([^"]+)"', page):
            if href.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            href = href.split("#", 1)[0].split("?", 1)[0]
            if not href:
                continue
            target = (path.parent / href).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                problems.append(f"{path.relative_to(ROOT)} -> missing {href}")

    if body_hits or head_hits:
        sample = body_hits[:8] + head_hits[:4]
        problems.append("brand check still has hits: " + "; ".join(f"{name} in {rel}" for rel, name, _ in sample))
    if problems:
        raise SystemExit("Validation failed:\n" + "\n".join(problems[:40]))

    return {
        "pages": len(posts),
        "unlinked": len(unlinked),
        "unlinked_slugs": sorted({item["slug"] for item in unlinked}),
        "body_hits": body_hits,
        "head_hits": head_hits,
        "bangalore_body": bangalore_body,
    }


def patch_static_page(page: str, item: dict, links: list[dict], base: str, sentences: list[str] | None = None) -> str:
    """Refresh the shared header and add planned links on an HTML-only guide."""
    page = re.sub(r"\s*<nav class=\"blog-subnav\"[\s\S]*?</nav>", "", page, count=1)
    current = TOPIC_SLUG.get(item.get("topic") or "", "")
    updated, count = re.subn(
        r'<a href="#main-content" class="skip-link">Skip to main content</a>\s*<header\b[\s\S]*?</header>',
        header("../", current, base),
        page,
        count=1,
    )
    if count != 1:
        raise SystemExit(f"Could not replace header in {item['slug']}")
    page = inject_static_html(updated, links, item, sentences)
    topic = item.get("topic") or ""
    topic_slug = TOPIC_SLUG.get(topic)
    if topic_slug:
        topic_url = abs_url(base, f"topic/{topic_slug}/")
        head, sep, tail = page.partition("</head>")
        if not sep:
            raise SystemExit(f"No head in {item['slug']}")
        if f'"item": "{topic_url}"' not in head:
            topic_json = json.dumps(
                {"@type": "ListItem", "position": 3, "name": topic, "item": topic_url},
                ensure_ascii=False,
            )
            head, json_count = re.subn(
                r'\{"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://acrenkey.com/blogs/"\}, \{"@type": "ListItem", "position": 3,',
                '{"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://acrenkey.com/blogs/"}, '
                + topic_json
                + ', {"@type": "ListItem", "position": 4,',
                head,
                count=1,
            )
            if json_count != 1:
                raise SystemExit(f"Could not patch breadcrumb JSON-LD in {item['slug']}")
            page = head + sep + tail
        crumb = re.search(r'(<ol class="breadcrumb">)(.*?)(</ol>)', page, re.S)
        if not crumb:
            raise SystemExit(f"No breadcrumb in {item['slug']}")
        inner = crumb.group(2)
        if topic_url not in inner:
            insertion = (
                f'<li><a href="{esc(topic_url)}">{esc(topic)}</a></li>\n'
                '        <li class="meta-sep" aria-hidden="true">/</li>\n'
                "        "
            )
            inner, crumb_count = re.subn(
                r'<li class="bc-current"',
                insertion + '<li class="bc-current"',
                inner,
                count=1,
            )
            if crumb_count != 1:
                raise SystemExit(f"Could not patch visible breadcrumb in {item['slug']}")
            page = page[: crumb.start(2)] + inner + page[crumb.end(2) :]
    digest = asset("style.css").split("?v=", 1)[1]
    page = re.sub(r"style\.css\?v=[A-Za-z0-9]+", f"style.css?v={digest}", page)
    fav_lines = [
        f'<link rel="icon" type="image/svg+xml" sizes="any" href="../{asset("favicon.svg")}">',
        f'<link rel="icon" type="image/png" sizes="48x48" href="../{asset("favicon-48x48.png")}">',
        f'<link rel="icon" type="image/png" sizes="32x32" href="../{asset("favicon-32x32.png")}">',
        f'<link rel="icon" type="image/png" sizes="16x16" href="../{asset("favicon-16x16.png")}">',
        f'<link rel="apple-touch-icon" sizes="180x180" href="../{asset("apple-touch-icon.png")}">',
        f'<link rel="shortcut icon" href="../{asset("favicon.ico")}">',
        f'<link rel="manifest" href="../{asset("site.webmanifest")}">',
    ]
    fav_block = "\n  ".join(fav_lines)
    page = re.sub(
        r'  <link rel="(?:icon|apple-touch-icon|shortcut icon|manifest)"[^\n]*\n?', "", page
    )
    page = re.sub(
        r'(<link rel="preload"[^\n]*cormorant-garamond-latin\.woff2"[^\n]*\n)',
        r"\1  " + fav_block + "\n",
        page,
    )
    return page


def hub_children(hub: dict, posts: list[dict], extras: list[dict]) -> list[dict]:
    if hub.get("section") == "areas":
        return [post for post in posts if post["section"] == "areas"]
    if hub.get("section") == "insights":
        return [post for post in posts if post["section"] == "insights"]
    topic = hub.get("topic")
    chosen = [post for post in posts if post.get("topic") == topic]
    chosen.extend(post for post in extras if post.get("topic") == topic)
    chosen.sort(key=lambda post: post["rank"])
    return chosen


def main() -> None:
    config = load_config()
    posts, _ = load_posts(config)
    topics = load_topic_map()
    for post in posts:
        post["topic"] = topics.get(post["slug"], "")
    plan = plan_by_source(load_plan())
    extras = static_posts()
    ordered = sorted([*posts, *extras], key=lambda item: (item["rank"], item["slug"]))
    slug_section = {post["slug"]: post["section"] for post in posts}
    unlinked: list[dict] = []
    prepared = {}
    dropped = 0
    for post in posts:
        source = abs_url(config["baseUrl"], post["path"])
        prepared[post["slug"]] = prepare_body(
            post,
            slug_section,
            unlinked,
            config["baseUrl"],
            plan.get(source, []),
            [
                sibling_sentence(post["section"], short_anchor(item["h1"]) or "", abs_url(config["baseUrl"], item["path"]))
                for item in section_siblings(post, ordered)
            ],
        )
        dropped += prepared[post["slug"]]["dropped_images"]

    legacy_blog = ROOT / "blog"
    if legacy_blog.is_dir():
        shutil.rmtree(legacy_blog)
    for section in ("insights", "areas", "topic"):
        destination = ROOT / section
        if destination.exists():
            shutil.rmtree(destination)
        if section != "topic":
            destination.mkdir()

    pages: dict[Path, str] = {}
    excerpts = {slug: item["short_plain"] for slug, item in prepared.items()}
    for item in extras:
        excerpts[item["slug"]] = item["excerpt"]
    for post in posts:
        ids = IdFactory()
        html_page = render_post(config, post, prepared[post["slug"]], posts, ids)
        path = ROOT / post["path"] / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html_page)
        pages[path] = html_page

    display = list(posts) + extras
    display.sort(key=lambda post: post["rank"])
    index_html = render_index(config, display, excerpts)
    index_path = ROOT / "index.html"
    index_path.write_text(index_html)
    pages[index_path] = index_html

    for hub in HUBS:
        children = hub_children(hub, posts, extras)
        html_page = render_hub(config, hub, children, excerpts)
        path = ROOT / hub["path"] / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html_page)
        pages[path] = html_page

    for item in extras:
        path = ROOT / item["path"] / "index.html"
        source = abs_url(config["baseUrl"], item["path"])
        page = patch_static_page(
            path.read_text(),
            item,
            plan.get(source, []),
            config["baseUrl"],
            [
                sibling_sentence(item["section"], short_anchor(other["h1"]) or "", abs_url(config["baseUrl"], other["path"]))
                for other in section_siblings(item, ordered)
            ],
        )
        path.write_text(page)
        pages[path] = page

    (ROOT / "sitemap.xml").write_text(render_sitemap(config, posts, extras))
    (ROOT / "robots.txt").write_text(render_robots(config))
    (ROOT / "llms.txt").write_text(render_llms(config, posts, excerpts, extras))

    decisions = []
    for post in posts:
        decisions.extend(post.get("_decisions") or [])
    for item in extras:
        decisions.extend(item.get("_decisions") or [])
    decisions.extend(classify_index_links(plan.get(abs_url(config["baseUrl"]), [])))
    write_decisions(decisions, CONTENT / "link_decisions.csv")

    report = validate(config, posts, unlinked, pages)
    report["dropped_images"] = dropped
    report["sections"] = {section: sum(1 for post in posts if post["section"] == section) for section in SECTIONS}
    # Compact hit counts for the console.
    from collections import Counter

    print(json.dumps(
        {
            "pages": report["pages"],
            "sections": report["sections"],
            "unlinked": report["unlinked"],
            "unlinked_posts": sum(1 for item in unlinked if item.get("kind") == "unpublished-post"),
            "unlinked_files": sum(1 for item in unlinked if item.get("kind") == "missing-file"),
            "unlinked_slugs": report["unlinked_slugs"],
            "dropped_images": report["dropped_images"],
            "body_banned": dict(Counter(name for _, name, _ in report["body_hits"])),
            "head_banned": dict(Counter(name for _, name, _ in report["head_hits"])),
            "bangalore_body": len(report["bangalore_body"]),
            "baseUrl": config["baseUrl"],
            "hubs": len(HUBS),
            "link_decisions": dict(Counter(row["status"] for row in decisions)),
            "link_skips": dict(Counter(row["reason"] for row in decisions if row["status"] == "skipped")),
            "unmatched_sections": {
                post["slug"]: post.get("_unmatched_sections")
                for post in posts
                if post.get("_unmatched_sections")
            },
        },
        indent=2,
    ))
    detail_path = Path("/tmp/blog-build-report.json")
    detail_path.write_text(json.dumps({
        "unlinked": unlinked,
        "body_hits": report["body_hits"],
        "head_hits": [{"file": rel, "word": name, "snippet": snippet} for rel, name, snippet in report["head_hits"]],
        "bangalore_body": report["bangalore_body"],
    }, indent=2))


if __name__ == "__main__":
    main()
