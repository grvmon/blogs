#!/usr/bin/env python3
"""Check the blog internal-link plan against the built HTML."""

from __future__ import annotations

import csv
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_site as b  # noqa: E402

BASE = "https://acrenkey.com/blogs/"
PLAN_PATH = ROOT / "content" / "link_plan.csv"
DECISIONS_PATH = ROOT / "content" / "link_decisions.csv"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
SKIP_TAGS = {"nav", "header", "footer", "aside"}
SKIP_CLASSES = {
    "blog-card",
    "toc-box",
    "breadcrumb",
    "blog-sidebar",
    "browse-row",
    "blog-subnav",
    "share-strip",
    "author-byline",
    "in-article-advisory-banner",
    "primary-cta-btn",
}
VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}
OLD_BLOG = re.compile(r"/blog(?!s)(/|$|\?|#)")


def norm_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def same_anchor(left: str, right: str) -> bool:
    return norm_text(left).casefold() == norm_text(right).casefold()


def norm_url(value: str) -> str:
    parsed = urlparse(value.strip())
    path = parsed.path or "/"
    if not path.endswith("/"):
        path += "/"
    return f"{parsed.scheme}://{parsed.netloc}{path}"


def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT)
    if rel.as_posix() == "index.html":
        return BASE
    return f"{BASE}{rel.parent.as_posix()}/"


def blogs_file(url: str) -> Path | None:
    parsed = urlparse(url)
    if parsed.netloc != "acrenkey.com":
        return None
    path = parsed.path or "/"
    if path.rstrip("/") == "/blogs":
        return ROOT / "index.html"
    if not path.startswith("/blogs/"):
        return None
    rel = path[len("/blogs/") :]
    if not rel or rel == "/":
        return ROOT / "index.html"
    if rel.endswith("index.html"):
        return ROOT / rel
    if rel.endswith("/"):
        return (ROOT / rel).joinpath("index.html")
    candidate = ROOT / rel
    if candidate.suffix:
        return candidate
    return candidate / "index.html"


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, bool]] = []
        self.current: dict | None = None
        self.links: list[dict] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag, attrs):
        self._start(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs, True)

    def _start(self, tag, attrs, ended):
        attr = {key: value or "" for key, value in attrs}
        classes = set(attr.get("class", "").split())
        parent_skip = self.stack[-1][1] if self.stack else False
        skip = parent_skip or tag in SKIP_TAGS or bool(classes & SKIP_CLASSES)
        if tag == "a":
            self.current = {"href": attr.get("href", ""), "parts": [], "in_text": not skip}
        if ended or tag in VOID_TAGS:
            return
        self.stack.append((tag, skip))

    def handle_endtag(self, tag):
        if tag == "a" and self.current is not None:
            self.links.append(
                {
                    "href": self.current["href"],
                    "text": norm_text("".join(self.current["parts"])),
                    "in_text": self.current["in_text"],
                }
            )
            self.current = None
        if tag in VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"extra </{tag}>")
            return
        if self.stack[-1][0] != tag:
            if any(item[0] == tag for item in self.stack):
                while self.stack and self.stack[-1][0] != tag:
                    self.errors.append(f"unclosed <{self.stack.pop()[0]}>")
                if self.stack:
                    self.stack.pop()
            else:
                self.errors.append(f"unexpected </{tag}>")
            return
        self.stack.pop()

    def close(self):
        super().close()
        for tag, _skip in self.stack:
            self.errors.append(f"unclosed <{tag}>")

    def handle_data(self, data):
        if self.current is not None:
            self.current["parts"].append(data)


def load_pages() -> list[Path]:
    pages = []
    for path in ROOT.rglob("index.html"):
        rel = path.relative_to(ROOT).as_posix()
        if rel == "posts/hello-world/index.html":
            continue
        pages.append(path)
    return sorted(pages)


def markup_for_balance(page: str) -> str:
    page = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", "", page, flags=re.I)
    page = re.sub(r"<style\b[^>]*>[\s\S]*?</style>", "", page, flags=re.I)
    return page


def main() -> int:
    with PLAN_PATH.open(newline="") as handle:
        plan = list(csv.DictReader(handle))
    pages = load_pages()
    parsed: dict[Path, Collector] = {}
    html_errors = []
    json_errors = []
    banned = []
    broken = []
    old_blog = []
    incoming: dict[str, set[str]] = {}

    for path in pages:
        raw = path.read_text()
        source = page_url(path)
        collector = Collector()
        try:
            collector.feed(markup_for_balance(raw))
            collector.close()
        except Exception as exc:  # noqa: BLE001
            html_errors.append(f"{path.relative_to(ROOT)}: parser {exc}")
        if collector.errors:
            html_errors.append(f"{path.relative_to(ROOT)}: {collector.errors[:4]}")
        parsed[path] = collector
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
            try:
                json.loads(block)
            except ValueError as exc:
                json_errors.append(f"{path.relative_to(ROOT)}: {exc}")
        visible = re.sub(r"https?://\S+", " ", b.visible_text(raw))
        hits = b.find_banned(visible) + b.find_banned(b.head_text(raw))
        if hits:
            banned.append(f"{path.relative_to(ROOT)}: {hits[0][0]}")
        if re.search(r"developers pay", visible, re.I):
            banned.append(f"{path.relative_to(ROOT)}: developers pay")
        for link in collector.links:
            href = link["href"]
            if not href or href.startswith(("mailto:", "tel:", "javascript:", "#")):
                continue
            absolute = urljoin(source, href)
            host = urlparse(absolute).netloc
            if host.endswith("acrenkey.com") and OLD_BLOG.search(urlparse(absolute).path):
                old_blog.append(f"{path.relative_to(ROOT)} -> {href}")
            local = blogs_file(absolute)
            if local is not None and not local.exists():
                broken.append(f"{path.relative_to(ROOT)} -> {href}")
            elif not href.startswith(("http://", "https://")):
                target = (path.parent / href.split("#", 1)[0].split("?", 1)[0]).resolve()
                if href.endswith("/") or target.is_dir():
                    target = target / "index.html"
                if not target.exists():
                    broken.append(f"{path.relative_to(ROOT)} -> {href}")
            if link["in_text"] and local is not None and local.exists():
                target_url = page_url(local) if local.name == "index.html" else norm_url(absolute)
                if target_url != source and local.suffix == ".html" and local.name == "index.html":
                    incoming.setdefault(target_url, set()).add(source)

    with DECISIONS_PATH.open(newline="") as handle:
        decisions = list(csv.DictReader(handle))
    decision_key = {
        (row["source"].rstrip("/") + "/", norm_url(row["target"]), norm_text(row["anchor"]).casefold()): row
        for row in decisions
    }
    missing_decision = []
    missing_placed = []
    skipped = []
    status_counts: dict[str, int] = {}
    for row in plan:
        source_url = row["source"].rstrip("/") + "/"
        key = (source_url, norm_url(row["target"]), norm_text(row["anchor"]).casefold())
        decision = decision_key.get(key)
        if decision is None:
            missing_decision.append((source_url, row["target"], row["anchor"]))
            continue
        status = decision["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
        if status == "skipped":
            skipped.append((source_url, row["target"], row["anchor"], decision["reason"]))
            continue
        source_path = blogs_file(source_url)
        if source_path is None or source_path not in parsed:
            missing_placed.append((source_url, row["target"], row["anchor"], "source page missing"))
            continue
        want_href = norm_url(row["target"])
        found = False
        for link in parsed[source_path].links:
            absolute = urljoin(page_url(source_path), link["href"])
            if same_anchor(link["text"], row["anchor"]) and norm_url(absolute) == want_href:
                found = True
                break
        if not found:
            missing_placed.append((source_url, row["target"], row["anchor"], status))

    block_errors = []
    for path, collector in parsed.items():
        raw = path.read_text()
        if 'class="plan-links"' in raw:
            block_errors.append(f"{path.relative_to(ROOT)} still has a keyword list")
        for block in re.findall(r'<p class="plan-sentence">(.*?)</p>', raw, re.S):
            if block.count("<a") != 1:
                block_errors.append(f"{path.relative_to(ROOT)} plan sentence has {block.count('<a')} links")
                break
        for block in re.findall(r'<ul class="related-reading-list">(.*?)</ul>', raw, re.S):
            count = block.count("<li")
            if count < 3 or count > 6:
                block_errors.append(f"{path.relative_to(ROOT)} related block has {count} items")

    hub_urls = {f"{BASE}{hub['path']}" for hub in b.HUBS} | {BASE}
    thin = []
    for path in pages:
        url = page_url(path)
        if url in hub_urls:
            continue
        count = len(incoming.get(url, ()))
        if count < 3:
            thin.append(f"{url} ({count})")

    sitemap_errors = []
    try:
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        locs = [node.text or "" for node in root.findall("sm:url/sm:loc", SITEMAP_NS)]
    except ET.ParseError as exc:
        locs = []
        sitemap_errors.append(f"sitemap does not parse: {exc}")
    if len(locs) != len(set(locs)):
        sitemap_errors.append("sitemap has duplicate loc values")
    required = [BASE]
    required.extend(f"{BASE}{hub['path']}" for hub in b.HUBS)
    required.extend(f"{BASE}{item['path']}" for item in b.STATIC_POSTS)
    manifest_posts, _ = b.load_posts(b.load_config())
    required.extend(f"{BASE}{post['path']}" for post in manifest_posts)
    missing_locs = [url for url in required if url not in set(locs)]
    if missing_locs:
        sitemap_errors.append(f"sitemap missing {len(missing_locs)} URLs, first: {missing_locs[:5]}")
    for loc in locs:
        parsed_loc = urlparse(loc)
        if parsed_loc.scheme != "https" or not loc.endswith("/"):
            sitemap_errors.append(f"bad sitemap loc {loc}")
            break

    print(f"planned {len(plan)}")
    print(f"decisions {len(decisions)}")
    for status, count in sorted(status_counts.items()):
        print(f"status {status} {count}")
    print(f"skipped {len(skipped)}")
    for item in skipped:
        print("SKIP", " | ".join(item))
    print(f"missing_decision {len(missing_decision)}")
    for item in missing_decision[:40]:
        print("NO_DECISION", " | ".join(item))
    print(f"missing_placed {len(missing_placed)}")
    for item in missing_placed[:40]:
        print("MISSING", " | ".join(item))
    print(f"broken_internal {len(broken)}")
    for item in broken[:40]:
        print("BROKEN", item)
    print(f"old_blog {len(set(old_blog))}")
    for item in sorted(set(old_blog))[:20]:
        print("OLD_BLOG", item)
    print(f"thin_pages {len(thin)}")
    for item in thin:
        print("THIN", item)
    print(f"html_errors {len(html_errors)}")
    for item in html_errors[:20]:
        print("HTML", item)
    print(f"jsonld_errors {len(json_errors)}")
    for item in json_errors[:20]:
        print("JSONLD", item)
    print(f"sitemap_errors {len(sitemap_errors)}")
    for item in sitemap_errors:
        print("SITEMAP", item)
    print(f"banned {len(banned)}")
    for item in banned[:20]:
        print("BANNED", item)
    print(f"block_errors {len(block_errors)}")
    for item in block_errors[:20]:
        print("BLOCK", item)
    print(f"pages {len(pages)}")

    failed = any(
        [missing_decision, missing_placed, broken, old_blog, thin, html_errors, json_errors, sitemap_errors, banned, block_errors]
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
