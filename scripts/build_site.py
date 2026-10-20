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
        "linkedin": "https://www.linkedin.com/in/gaurav-a-mongia/",
        "description": "Building data-driven evaluation models and micro-market frameworks to give buyers absolute clarity.",
    },
    "Nitin": {
        "name": "Nitin Gupta",
        "role": "Investments · Decision Framework",
        "jobTitle": "Co-founder & Head of Investments",
        "avatar": "https://acrenkey.com/style-guide/assets/nitin-gupta-founder-acre-key.webp",
        "linkedin": "https://www.linkedin.com/in/nitin-gupta-7446864/",
        "description": "Former corporate finance leader applying institutional diligence and quantitative risk models to home buying in Bengaluru.",
    },
    "Arvind": {
        "name": "Arvind Patidar",
        "role": "Advisory · Execution",
        "jobTitle": "Co-founder & Head of Operations",
        "avatar": "https://acrenkey.com/style-guide/assets/arvind-patidar-founder-acre-key.webp",
        "linkedin": "https://www.linkedin.com/in/arvind-patidar/",
        "description": "Operations and engineering leader ensuring flawless execution, civic compliance, and zero-compromise due diligence.",
    },
}
IMAGE_W, IMAGE_H = 1200, 675


def img_tag(root: str, post: dict, cls: str, hero: bool = False) -> str:
    loading = 'loading="eager" fetchpriority="high"' if hero else 'loading="lazy"'
    return (
        f'<img src="{root}{esc(post["image"])}" width="{IMAGE_W}" height="{IMAGE_H}" '
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


def prepare_body(post: dict, slug_section: dict[str, str], unlinked: list[dict], base_url: str) -> dict:
    body = post["body"].split("\n## Suggested images", 1)[0].rstrip() + "\n"
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
    section_label = SECTION_LABEL[post["section"]]
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
            "itemListElement": (
                [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": org["url"]},
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Blog",
                        "item": abs_url(config["baseUrl"]),
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": post["h1"],
                        "item": canonical,
                    },
                ]
                if post["section"] == "blog"
                else [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": org["url"]},
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Blog",
                        "item": abs_url(config["baseUrl"]),
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": section_label,
                        "item": abs_url(config["baseUrl"], f"#{post['section']}"),
                    },
                    {
                        "@type": "ListItem",
                        "position": 4,
                        "name": post["h1"],
                        "item": canonical,
                    },
                ]
            ),
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
        f'<link rel="icon" type="image/svg+xml" href="{root}favicon.svg">',
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


def header(root: str) -> str:
    """acrenkey.com header, copied from grvmon/a-K index.html (scripts/partials/header.html)."""
    return '<a href="#main-content" class="skip-link">Skip to main content</a>\n  ' + (PARTIALS / "header.html").read_text().strip()


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
    section_label = SECTION_LABEL[post["section"]]
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
    if post["section"] == "blog":
        bc_section_html = ""
    else:
        bc_section_html = (
            f'\n        <li class="meta-sep" aria-hidden="true">/</li>'
            f'\n        <li><a href="{esc(config["baseUrl"])}#{esc(post["section"])}">{esc(section_label)}</a></li>'
        )

    page = f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
  {head_tags(post['seo_title'], post['meta'], canonical, root, 'article', published, ld, abs_url(config['baseUrl'], post['image']), post['author'])}
</head>
<body>
  <div id="scroll-progress-bar" aria-hidden="true"></div>
  {header(root)}
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
            <img src="{esc(profile['avatar'])}" alt="{esc(profile['name'])}" class="author-avatar-img" width="46" height="46" loading="lazy" decoding="async">
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
          <div class="author-bio-avatar" aria-hidden="true">a&amp;k</div>
          <div>
            <p class="author-bio-title">Written by {esc(profile['name'])}</p>
            <span class="author-bio-role">Acrenkey Realty LLP</span>
            <p class="author-bio-desc">Published by Acrenkey Realty LLP, a property advisory for people buying a home in Bengaluru.</p>
          </div>
        </div>
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
    counts = {section: sum(1 for post in posts if post["section"] == section) for section in SECTIONS}
    cards = []
    for post in posts:
        search = " ".join(
            [
                post["h1"],
                excerpts[post["slug"]],
                post["meta"],
                post["seo_title"],
                SECTION_LABEL[post["section"]],
                post["section"],
            ]
        ).lower()
        cards.append(
            f"""<article class="blog-card" data-section="{esc(post['section'])}" data-rank="{post['rank']}" data-search="{esc(search)}">
        <a href="{esc(post['path'])}" class="blog-card-media tone-{esc(post['section'])}" aria-label="Read {esc(post['h1'])}">
          {img_tag('', post, 'blog-card-img')}
          <span class="cat-badge">{esc(SECTION_LABEL[post['section']])}</span>
        </a>
        <div class="blog-card-body">
          <div class="blog-card-meta">
            <span>By {esc(AUTHOR_PROFILES[post['author']]['name'])}</span>
            <span class="meta-sep" aria-hidden="true">&bull;</span>
            <time datetime="{esc(post.get('published') or config['datePublished'])}">{esc(format_date(post.get('published') or config['datePublished']))}</time>
          </div>
          <h2 class="blog-card-title">
            <a href="{esc(post['path'])}">{esc(post['h1'])}</a>
          </h2>
          <p class="blog-card-excerpt">{esc(excerpts[post['slug']])}</p>
          <a href="{esc(post['path'])}" class="blog-card-readmore">
            <span>Read guide</span>
            <span aria-hidden="true">&rarr;</span>
          </a>
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
  {header('')}
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
      </div>
    </div>
  </section>
  <main id="main-content" class="container">
    <div class="category-filter-strip" role="group" aria-label="Filter guides by section">
      <button type="button" class="cat-btn active" data-section="all" aria-pressed="true">All ({len(posts)})</button>
      <button type="button" class="cat-btn" data-section="blog" aria-pressed="false">Blog ({counts['blog']})</button>
      <button type="button" class="cat-btn" data-section="insights" aria-pressed="false">Insights ({counts['insights']})</button>
      <button type="button" class="cat-btn" data-section="areas" aria-pressed="false">Areas ({counts['areas']})</button>
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


def render_sitemap(config: dict, posts: list[dict]) -> str:
    dated = [(abs_url(config["baseUrl"]), config["datePublished"])]
    dated.extend(
        (abs_url(config["baseUrl"], post["path"]), post.get("published") or config["datePublished"])
        for post in posts
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


def render_llms(config: dict, posts: list[dict], excerpts: dict[str, str]) -> str:
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
        for token in ("BlogPosting", "FAQPage", "BreadcrumbList"):
            if token not in page:
                problems.append(f"{rel} missing {token}")
        post_for_date = by_path.get(path)
        published = (post_for_date or {}).get("published") or config["datePublished"]
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


def main() -> None:
    config = load_config()
    posts, _ = load_posts(config)
    slug_section = {post["slug"]: post["section"] for post in posts}
    unlinked: list[dict] = []
    prepared = {}
    dropped = 0
    for post in posts:
        prepared[post["slug"]] = prepare_body(post, slug_section, unlinked, config["baseUrl"])
        dropped += prepared[post["slug"]]["dropped_images"]

    legacy_blog = ROOT / "blog"
    if legacy_blog.is_dir():
        shutil.rmtree(legacy_blog)
    for section in ("insights", "areas"):
        destination = ROOT / section
        if destination.exists():
            shutil.rmtree(destination)
        destination.mkdir()

    pages: dict[Path, str] = {}
    excerpts = {slug: item["short_plain"] for slug, item in prepared.items()}
    for post in posts:
        ids = IdFactory()
        html_page = render_post(config, post, prepared[post["slug"]], posts, ids)
        path = ROOT / post["path"] / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html_page)
        pages[path] = html_page

    index_html = render_index(config, posts, excerpts)
    index_path = ROOT / "index.html"
    index_path.write_text(index_html)
    pages[index_path] = index_html
    (ROOT / "sitemap.xml").write_text(render_sitemap(config, posts))
    (ROOT / "robots.txt").write_text(render_robots(config))
    (ROOT / "llms.txt").write_text(render_llms(config, posts, excerpts))

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
