"""Apply the blog internal-link plan during the static build.

The plan CSV is content/link_plan.csv. Markdown posts receive the links as
prose. The three HTML-only guides are patched in place. Hub pages and the
blog nav are rendered by build_site.py using the constants here.
"""

from __future__ import annotations

import csv
import html
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN_PATH = ROOT / "content" / "link_plan.csv"
TOPIC_MAP_PATH = ROOT / "content" / "topic_map.csv"

TOPIC_SLUG = {
    "Localities & Corridors": "localities-corridors",
    "Buyer Checklists & Process": "buying-checklists",
    "Legal, Title & RERA": "legal-rera",
    "Loans, Taxes & Total Costs": "loans-costs-tax",
    "Environment & Water Checks": "water-environment",
}

# Order matches the 5-pillar taxonomy. The sibling ring uses this order.
HUBS = [
    {
        "key": "areas",
        "name": "Area guides",
        "path": "areas/",
        "h1": "Area guides",
        "title": "Area guides for Bengaluru homebuyers",
        "description": "Neighbourhood notes for people buying a home in Bengaluru: property rates, metro access, water and flood checks by area.",
        "lead": "Neighbourhood notes on rates, metro, water and flood checks.",
        "section": "areas",
    },
    {
        "key": "insights",
        "name": "Data insights",
        "path": "insights/",
        "h1": "Data insights",
        "title": "Data insights for Bengaluru homebuyers",
        "description": "Data notes for people buying a home in Bengaluru: prices, loans, RERA filings and infrastructure, with the source named.",
        "lead": "Prices, loans, RERA filings and infrastructure, with the source named.",
        "section": "insights",
    },
    {
        "key": "localities-corridors",
        "name": "Localities & Corridors",
        "path": "topic/localities-corridors/",
        "h1": "Localities & Corridors",
        "title": "Bengaluru Localities and Corridors Guide",
        "description": "Hyperlocal notes on property rates, metro access, civic infrastructure, and corridor comparisons across Bengaluru.",
        "lead": "Hyperlocal notes on property rates, metro access, and corridor comparisons.",
        "topic": "Localities & Corridors",
    },
    {
        "key": "buying-checklists",
        "name": "Buyer Checklists & Process",
        "path": "topic/buying-checklists/",
        "h1": "Buyer Checklists & Process",
        "title": "Buying Process and Checklists for Bengaluru Flats",
        "description": "Stage-by-stage checklists, token verification, negotiation points, and handover steps for Bengaluru home buyers.",
        "lead": "Stage-by-stage checklists, negotiation points, and handover steps for home buyers.",
        "topic": "Buyer Checklists & Process",
    },
    {
        "key": "legal-rera",
        "name": "Legal, Title & RERA",
        "path": "topic/legal-rera/",
        "h1": "Legal, Title & RERA",
        "title": "Legal, Title and RERA Guides for Karnataka Buyers",
        "description": "Title search, A-Khata vs B-Khata, RERA complaint filing, builder delay interest, and legal verification for Bengaluru homes.",
        "lead": "Title search, A-Khata vs B-Khata, RERA rights, and legal verification.",
        "topic": "Legal, Title & RERA",
    },
    {
        "key": "loans-costs-tax",
        "name": "Loans, Taxes & Total Costs",
        "path": "topic/loans-costs-tax/",
        "h1": "Loans, Taxes & Total Costs",
        "title": "Home Loans, Stamp Duty, Tax and Total Flat Costs",
        "description": "Loan eligibility, Kaveri 2.0 e-stamps, total flat cost breakdowns, 1% TDS, and stamp duty calculators for Bengaluru homebuyers.",
        "lead": "Loan eligibility, Kaveri 2.0 e-stamps, total cost breakdowns, and 1% TDS.",
        "topic": "Loans, Taxes & Total Costs",
    },
    {
        "key": "water-environment",
        "name": "Environment & Water Checks",
        "path": "topic/water-environment/",
        "h1": "Environment & Water Checks",
        "title": "Water Supply, Flood Records and Environment Checks",
        "description": "Official KSNDMC flood spots, lake buffer zones, rajakaluve maps, CGWB groundwater levels, Cauvery Stage V water, and AQI data.",
        "lead": "Official flood spots, lake buffer zones, rajakaluve maps, and groundwater levels.",
        "topic": "Environment & Water Checks",
    },
]

ZONE_LINKS = [
    ("https://acrenkey.com/property/area/east-bengaluru/", "East Bengaluru projects"),
    ("https://acrenkey.com/property/area/north-bengaluru/", "North Bengaluru projects"),
    ("https://acrenkey.com/property/area/south-bengaluru/", "South Bengaluru projects"),
    ("https://acrenkey.com/property/area/west-bengaluru/", "West Bengaluru projects"),
]

# HTML-only guides. The markdown build does not emit these files.
STATIC_POSTS = [
    {
        "slug": "bengaluru-air-quality-by-neighbourhood-kspcb-stations",
        "section": "blog",
        "topic": "Environment & Water Checks",
        "h1": "Bengaluru air quality by neighbourhood: what 11 KSPCB stations recorded",
        "seo_title": "Bengaluru Air Quality by Neighbourhood: KSPCB Data",
        "meta": "Mean daily AQI, good and moderate days, and the worst months at 11 KSPCB air quality stations in Bengaluru, June 2025 to May 2026, with a map and CSV.",
        "excerpt": "From June 2025 to May 2026, the 11 KSPCB stations in Bengaluru averaged a daily AQI of 78, in the Satisfactory band. Saneguruvanahalli was lowest at 49, and Silk Board was highest at 111, with 254 Moderate days. No station had a Poor day. Air was worst from December to April and cleanest in July and August.",
        "author": "Gaurav",
        "published": "2026-10-22",
        "image_alt": "A city highway with streetlights fading into thick haze",
        "rank": 203,
        "readmore": "Read guide",
        "path": "bengaluru-air-quality-by-neighbourhood-kspcb-stations/",
    },
    {
        "slug": "carpet-area-and-loading-calculator-bengaluru",
        "section": "blog",
        "topic": "Buyer Checklists & Process",
        "h1": "Carpet area and loading calculator for Bengaluru flat buyers",
        "seo_title": "Carpet Area and Loading Calculator for Bengaluru Flats",
        "meta": "Work out the loading, carpet share and price per sq ft of RERA carpet area for a Bengaluru flat, with the RERA Act definition and a worked example.",
        "excerpt": "Loading is the super built-up area minus the RERA carpet area, divided by the carpet area. A flat quoted at 1,350 sq ft with a 1,000 sq ft carpet area has 35% loading, so you pay 1.35 times the quoted rate for each square foot you can use. RERA sets no loading limit. It defines carpet area and makes builders disclose it.",
        "author": "Nitin",
        "published": "2026-10-22",
        "image_alt": "An empty apartment with wooden flooring, an open kitchen and tall windows",
        "rank": 204,
        "readmore": "Open calculator",
        "path": "carpet-area-and-loading-calculator-bengaluru/",
    },
    {
        "slug": "free-letter-templates-bengaluru-buyers-documents-to-rera",
        "section": "blog",
        "topic": "Legal, Title & RERA",
        "h1": "Free letter templates for Bengaluru home buyers: from document requests to a RERA complaint",
        "seo_title": "Free Letter Templates for Bengaluru Buyers: Documents to RERA",
        "meta": "Three free letter templates for Bengaluru home buyers: a document request to the builder, a defect notice under RERA section 14(3) and a Karnataka RERA complaint draft in Form N.",
        "excerpt": "Use three letters, in order. First, ask the builder in writing for the sanctioned plans, specifications and stage-wise schedule, which sections 11(3) and 19 of the RERA Act entitle you to. Second, report defects within five years of possession under section 14(3), which gives the builder 30 days to fix them free. Third, if that fails, complain to Karnataka RERA in Form N with a ₹1,000 fee.",
        "author": "Arvind",
        "published": "2026-10-23",
        "image_alt": "A fountain pen resting on a polished wooden desk",
        "rank": 205,
        "readmore": "Get templates",
        "path": "free-letter-templates-bengaluru-buyers-documents-to-rera/",
    },
]

STATIC_SLUGS = {item["slug"] for item in STATIC_POSTS}
SKIP_SECTIONS = {
    "Frequently asked questions",
    "Talk it through with acre&key",
    "Sources",
    "Suggested images",
    "Structured data (JSON-LD)",
}


def load_plan() -> list[dict]:
    with PLAN_PATH.open(newline="") as handle:
        return list(csv.DictReader(handle))


def load_topic_map() -> dict[str, str]:
    topics = {}
    with TOPIC_MAP_PATH.open(newline="") as handle:
        for row in csv.DictReader(handle):
            topics[row["slug"]] = row["topic"]
    return topics


def plan_by_source(rows: list[dict] | None = None) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows if rows is not None else load_plan():
        grouped[row["source"].rstrip("/") + "/"].append(row)
    return grouped


def _kind(link: dict) -> str:
    target = link["target"]
    target_type = link.get("target_type") or ""
    path = target.rstrip("/")
    if target_type == "property":
        return "property"
    if (
        target_type in {"PROPOSED hub", "property-hub", "answers-hub"}
        or "/property/area/" in target
        or "/blogs/topic/" in target
        or path in {
            "https://acrenkey.com/blogs/areas",
            "https://acrenkey.com/blogs/insights",
            "https://acrenkey.com/property",
        }
    ):
        return "hub"
    if target_type == "calculator" or "/calculators/" in target:
        return "calculator"
    if target_type == "answer" or "answers.acrenkey.com" in target:
        return "answer"
    if target_type == "contact" or path.endswith("/contact"):
        return "contact"
    return "guide"


def _md_link(anchor: str, url: str) -> str:
    label = anchor.replace("\\", "").replace("[", "").replace("]", "")
    return f"[{label}]({url})"


def _html_link(anchor: str, url: str) -> str:
    return f'<a href="{html.escape(url, quote=True)}">{html.escape(anchor)}</a>'


NAV_KINDS = {"breadcrumb", "chips", "nav", "hub-sidebar", "hub-intro"}
TRAILING_STOP = {"a", "an", "the", "of", "for", "in", "on", "and", "or", "to", "with", "from", "by", "vs"}


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[&'][A-Za-z0-9]+)*", text or ""))


def short_anchor(title: str) -> str | None:
    """A 2–5 word name taken from a guide title, without a trailing stop-word."""
    clause = re.split(r"[:|]", title or "", maxsplit=1)[0]
    clause = re.sub(r"\([^)]*\)", " ", clause)
    clause = re.sub(r"\s+", " ", clause).strip(" -–—")
    words = [word for word in clause.split() if word]
    chosen: list[str] = []
    for word in words:
        trial = " ".join(chosen + [word])
        if word_count(trial) > 5:
            break
        chosen.append(word)
    while chosen and chosen[-1].lower().strip(".,") in TRAILING_STOP:
        chosen.pop()
    if not chosen:
        return None
    anchor = " ".join(chosen).strip(".,")
    anchor = anchor.replace("[", "").replace("]", "")
    if word_count(anchor) < 2 or word_count(anchor) > 5:
        return None
    return anchor


def _priority(link: dict) -> int:
    return {"P0": 0, "P1": 1, "P2": 2}.get(link.get("priority") or "", 9)


def _protect_links(text: str) -> tuple[str, list[str]]:
    saved: list[str] = []

    def repl(match: re.Match) -> str:
        saved.append(match.group(0))
        return f"\x00{len(saved) - 1}\x00"

    return re.sub(r"\[[^\]]*\]\([^)]*\)", repl, text), saved


def _restore_links(text: str, saved: list[str]) -> str:
    return re.sub(r"\x00(\d+)\x00", lambda match: saved[int(match.group(1))], text)


def _wrap_paragraph(paragraph: str, pattern: re.Pattern, url: str) -> tuple[str, bool]:
    if not paragraph.strip() or paragraph.lstrip().startswith("#"):
        return paragraph, False
    if "**Short answer:**" in paragraph or paragraph.count("](") >= 2:
        return paragraph, False
    protected, saved = _protect_links(paragraph)
    match = pattern.search(protected)
    if not match or "\x00" in protected[match.start() : match.end()]:
        return paragraph, False
    before = protected[: match.start()]
    sentence_start = max(before.rfind(". "), before.rfind("? "), before.rfind("! "), before.rfind("\n"))
    after = protected[match.end() :]
    end_match = re.search(r"[.!?]\s|\n", after)
    sentence_end = match.end() + (end_match.end() if end_match else len(after))
    sentence = protected[sentence_start + 1 : sentence_end]
    if "](" in sentence or "\x00" in sentence:
        return paragraph, False
    linked = protected[: match.start()] + "[" + match.group(0) + "](" + url + ")" + protected[match.end() :]
    return _restore_links(linked, saved), True


def _try_wrap(blocks: list[dict], indexes: list[int], phrase: str, url: str) -> bool:
    if not phrase or not indexes:
        return False
    pattern = re.compile(r"(?<![A-Za-z0-9])" + re.escape(phrase) + r"(?![A-Za-z0-9])", re.I)
    for index in indexes:
        pieces = re.split(r"(\n\s*\n)", "".join(blocks[index]["lines"]))
        for piece_index, piece in enumerate(pieces):
            updated, ok = _wrap_paragraph(piece, pattern, url)
            if not ok:
                continue
            pieces[piece_index] = updated
            blocks[index]["lines"] = ["".join(pieces)]
            return True
    return False


def _bucket(placement: str) -> tuple[str, str]:
    text = placement.strip()
    if text == "Breadcrumb":
        return "breadcrumb", ""
    if text.startswith("Filter chips"):
        return "chips", ""
    if text.startswith("Blog header"):
        return "nav", ""
    if text.startswith("Hub sidebar"):
        return "hub-sidebar", ""
    if text.startswith("Hub intro"):
        return "hub-intro", ""
    if text.startswith("Intro +"):
        return "intro-cta", ""
    if "Projects in this area" in text:
        return "projects-area", ""
    if "See it applied" in text:
        return "see-applied", ""
    if "Projects nearby" in text:
        return "nearby", ""
    if "Related guides" in text:
        return "related", ""
    if text.startswith("In-body next to the worked"):
        return "worked", ""
    if text.startswith("In-body where the question"):
        return "faq-inline", ""
    if text.startswith("FAQ /"):
        return "quick", ""
    if text.startswith("Body,"):
        match = re.search(r'section "([^"]*)"', text)
        return "section", match.group(1) if match else "(intro)"
    return "other", ""


def _heading_score(title: str, name: str) -> int:
    if name == "(intro)":
        return 100 if title == "(intro)" else 0
    left = title.lower().strip()
    right = name.lower().strip()
    if not left or not right:
        return 0
    if left == right:
        return 100
    if left.startswith(right) or right.startswith(left):
        if min(len(left), len(right)) >= 12:
            return 90
    if right.startswith("worked") and left.startswith("worked"):
        return 80
    shared = 0
    for char_a, char_b in zip(left, right):
        if char_a != char_b:
            break
        shared += 1
    if shared >= 24:
        return 70
    return 0


def _split_blocks(body: str) -> list[dict]:
    lines = body.splitlines(keepends=True)
    blocks = [{"level": 0, "title": "(intro)", "lines": []}]
    for line in lines:
        match = re.match(r"^(#{2,3}) (.+?)\s*$", line)
        if match:
            blocks.append({"level": len(match.group(1)), "title": match.group(2).strip(), "lines": [line]})
        else:
            blocks[-1]["lines"].append(line)
    return blocks


def _join_blocks(blocks: list[dict]) -> str:
    parts = []
    for block in blocks:
        text = "".join(block["lines"])
        if text and not text.endswith("\n"):
            text += "\n"
        parts.append(text)
    return "".join(parts).rstrip() + "\n"


def _append(block: dict, paragraph: str) -> None:
    if not paragraph.strip():
        return
    text = "".join(block["lines"]).rstrip() + "\n\n" + paragraph.strip() + "\n"
    block["lines"] = [text]


def _best_block(blocks: list[dict], name: str) -> int | None:
    best_index = None
    best_score = 0
    for index, block in enumerate(blocks):
        score = _heading_score(block["title"], name)
        if score > best_score:
            best_score = score
            best_index = index
    return best_index


def _section_end(blocks: list[dict], name: str) -> int | None:
    """Last block of a section, including the ### blocks that follow an ##."""
    start = _best_block(blocks, name)
    if start is None:
        return None
    end = start
    if blocks[start]["level"] == 2:
        for index in range(start + 1, len(blocks)):
            if blocks[index]["level"] == 2:
                break
            end = index
    return end


def append_sentence(body: str, sentence: str) -> str:
    """Add one prose sentence to the last section before the FAQ."""
    if not sentence.strip():
        return body
    blocks = _split_blocks(body)
    end_index = None
    for index in range(len(blocks) - 1, -1, -1):
        if blocks[index]["title"] not in SKIP_SECTIONS and blocks[index]["title"] != "(intro)":
            end_index = index
            break
    if end_index is None:
        _append(blocks[0], sentence)
    else:
        _append(blocks[end_index], sentence)
    return _join_blocks(blocks)


def context_sentences(post: dict) -> list[str]:
    """One link per sentence. At most two sentences, each in its own paragraph later."""
    sentences = []
    section = post.get("section") or ""
    if section == "areas":
        sentences.append("More neighbourhood notes are in [Area guides](https://acrenkey.com/blogs/areas/).")
    elif section == "insights":
        sentences.append("More data notes are in [Data insights](https://acrenkey.com/blogs/insights/).")
    topic = post.get("topic") or ""
    slug = TOPIC_SLUG.get(topic)
    if slug:
        hub = next(item for item in HUBS if item["key"] == slug)
        anchor = hub.get("prose") or topic
        if 2 <= word_count(anchor) <= 5:
            sentences.append(
                f"More on this topic sits under [{anchor}](https://acrenkey.com/blogs/topic/{slug}/)."
            )
    return sentences[:2]


def sibling_sentence(section: str, anchor: str, url: str) -> str:
    link = _md_link(anchor, url)
    if section == "areas":
        return f"Buyers also compare this corridor with {link}."
    if section == "insights":
        return f"A related data note is {link}."
    return f"A related buyer note is {link}."


def weave_sentences(body: str, sentences: list[str]) -> str:
    """Drop each sentence into its own paragraph on successive sections."""
    if not sentences:
        return body
    blocks = _split_blocks(body)
    content = [
        index
        for index, block in enumerate(blocks)
        if block["title"] not in SKIP_SECTIONS and block["title"] != "(intro)" and block["level"] == 2
    ]
    if not content:
        content = [
            index
            for index, block in enumerate(blocks)
            if block["title"] not in SKIP_SECTIONS and block["title"] != "(intro)"
        ]
    if not content:
        content = [0]
    for offset, sentence in enumerate(sentences):
        start = content[min(offset, len(content) - 1)]
        end = start
        if blocks[start]["level"] == 2:
            for index in range(start + 1, len(blocks)):
                if blocks[index]["level"] == 2:
                    break
                end = index
        _append(blocks[end], sentence)
    return _join_blocks(blocks)


def _section_indexes(blocks: list[dict], link: dict) -> list[int]:
    kind, name = _bucket(link["placement"])
    if kind == "section":
        return _iter_section_indexes(blocks, name)
    if kind in {"intro-cta", "projects-area"}:
        return [0]
    if kind == "worked":
        found = _best_block(blocks, "Worked examples")
        return _iter_section_indexes(blocks, "Worked examples") if found is not None else []
    if kind in {"faq-inline", "quick"}:
        return _iter_section_indexes(blocks, "Frequently asked questions")
    usable = []
    for index, block in enumerate(blocks):
        if block["title"] in SKIP_SECTIONS:
            continue
        usable.append(index)
    return usable


def _iter_section_indexes(blocks: list[dict], name: str) -> list[int]:
    start = _best_block(blocks, name)
    if start is None:
        return []
    indexes = [start]
    if blocks[start]["level"] == 2:
        for index in range(start + 1, len(blocks)):
            if blocks[index]["level"] == 2:
                break
            indexes.append(index)
    return indexes


def _decide(link: dict, status: str, reason: str) -> dict:
    return {
        "priority": link.get("priority") or "",
        "source": link.get("source") or "",
        "target": link.get("target") or "",
        "anchor": link.get("anchor") or "",
        "placement": link.get("placement") or "",
        "status": status,
        "reason": reason,
    }


def apply_link_plan(body: str, links: list[dict], post: dict) -> str:
    """Link an existing phrase when it is already in the copy. Do not invent anchor lists."""
    blocks = _split_blocks(body)
    decisions = []
    short_rest: list[dict] = []
    for link in links:
        kind, _name = _bucket(link["placement"])
        if kind in NAV_KINDS:
            decisions.append(_decide(link, "placed-nav", "Rendered in the nav, breadcrumb or hub chrome"))
            continue
        count = word_count(link.get("anchor") or "")
        if count < 2 or count > 14:
            decisions.append(
                _decide(
                    link,
                    "skipped",
                    f"anchor is {count} words; in-sentence and block links use 2–14 words",
                )
            )
            continue
        indexes = [
            index
            for index in _section_indexes(blocks, link)
            if blocks[index]["title"] != "Talk it through with acre&key"
        ]
        if _try_wrap(blocks, indexes, link["anchor"], link["target"]):
            decisions.append(_decide(link, "placed-inline", "Existing phrase linked in the section"))
            continue
        short_rest.append(link)

    placed_blocks, block_decisions = build_blocks(short_rest, post)
    decisions.extend(block_decisions)

    post["_decisions"] = decisions
    post["_related_blocks"] = placed_blocks
    post["_related_block"] = placed_blocks[0] if placed_blocks else {"title": "", "items": []}
    return _join_blocks(blocks)


def build_blocks(short_rest: list[dict], post: dict) -> tuple[list[dict], list[dict]]:
    """Bottom link blocks (Calculators, Answers, Guides, Projects) disabled per design guidelines."""
    decisions = [
        _decide(link, "skipped", "bottom link blocks disabled per design guidelines")
        for link in short_rest
    ]
    return [], decisions


def sibling_hubs(key: str) -> list[dict]:
    index = next(i for i, hub in enumerate(HUBS) if hub["key"] == key)
    count = len(HUBS)
    return [HUBS[(index + offset) % count] for offset in (1, 2, 3, 4)]


def static_by_slug(slug: str) -> dict | None:
    for item in STATIC_POSTS:
        if item["slug"] == slug:
            return item
    return None


def _html_paragraph(sentence_md: str) -> str:
    """Turn one markdown sentence that contains a single link into a paragraph."""
    match = re.fullmatch(r"(.*)\[([^\]]+)\]\(([^)]+)\)(.*)", sentence_md.strip(), re.S)
    if not match:
        return f'<p class="plan-sentence">{html.escape(sentence_md.strip())}</p>'
    before, label, url, after = match.groups()
    return (
        '<p class="plan-sentence">'
        + html.escape(before)
        + f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>'
        + html.escape(after)
        + "</p>"
    )


def related_block_html(title: str, items: list[tuple[str, str]]) -> str:
    if not title or not items:
        return ""
    rows = "".join(
        f'<li><a href="{html.escape(url, quote=True)}">{html.escape(anchor)}</a></li>'
        for anchor, url in items
    )
    return (
        f'<section class="related-reading" aria-label="{html.escape(title)}">'
        f"<h2>{html.escape(title)}</h2>"
        f'<ul class="related-reading-list">{rows}</ul>'
        "</section>"
    )


def _forbidden_spans(page: str) -> list[tuple[int, int]]:
    patterns = (
        r"<form\b[\s\S]*?</form>",
        r"<script\b[\s\S]*?</script>",
        r"<style\b[\s\S]*?</style>",
        r"<header\b[\s\S]*?</header>",
        r'<div class="in-article-advisory-banner"[\s\S]*?</div>',
        r'<figure class="article-hero"[\s\S]*?</figure>',
        r'<div class="short-answer"[\s\S]*?</div>',
        r'<p class="hero-lead"[\s\S]*?</p>',
        r'<section class="blog-home-hero"[\s\S]*?</section>',
    )
    spans = []
    for pattern in patterns:
        spans.extend((match.start(), match.end()) for match in re.finditer(pattern, page, re.I))
    return spans


def _link_text_node(inner: str, phrase: str, url: str) -> tuple[str, bool]:
    """Wrap the phrase in a text node, outside an existing anchor and its sentence."""
    literal = re.compile(r"(?<![A-Za-z0-9])" + re.escape(phrase) + r"(?![A-Za-z0-9])", re.I)
    parts = re.split(r"(<[^>]+>)", inner)
    anchor_depth = 0
    text_so_far = ""
    for index, part in enumerate(parts):
        if part.startswith("<"):
            if re.match(r"<a\b", part, re.I):
                anchor_depth += 1
                text_so_far += "\x00"
            elif re.match(r"</a\b", part, re.I):
                anchor_depth = max(0, anchor_depth - 1)
            continue
        found = literal.search(part)
        if not found or anchor_depth:
            text_so_far += part
            continue
        before = text_so_far + part[: found.start()]
        sentence_start = max(before.rfind(". "), before.rfind("? "), before.rfind("! "))
        sentence = before[sentence_start + 1 :]
        if "\x00" in sentence:
            text_so_far += part
            continue
        parts[index] = (
            part[: found.start()]
            + f'<a href="{html.escape(url, quote=True)}">{found.group(0)}</a>'
            + part[found.end() :]
        )
        return "".join(parts), True
    return inner, False


def _wrap_html_paragraphs(page: str, phrase: str, url: str) -> tuple[str, bool]:
    """Link the first existing phrase in a paragraph outside heroes, CTAs and forms."""
    spans = _forbidden_spans(page)

    def occupied(pos: int) -> bool:
        return any(start <= pos < end for start, end in spans)

    for match in re.finditer(r"(<p\b[^>]*>)(.*?)(</p>)", page, re.I | re.S):
        if occupied(match.start()):
            continue
        opening, inner = match.group(1), match.group(2)
        if "plan-sentence" in opening or inner.count("<a") >= 2:
            continue
        plain = html.unescape(re.sub(r"<[^>]+>", " ", inner))
        found = re.search(r"(?<![A-Za-z0-9])" + re.escape(phrase) + r"(?![A-Za-z0-9])", plain, re.I)
        if not found:
            continue
        updated, ok = _link_text_node(inner, found.group(0), url)
        if not ok:
            continue
        return page[: match.start(2)] + updated + page[match.end(2) :], True
    return page, False


def inject_static_html(page: str, links: list[dict], post: dict, sentences: list[str] | None = None) -> str:
    """Add natural sentences and one related block without touching widgets or forms."""
    page = re.sub(r"\s*<p class=\"plan-sentence\">[\s\S]*?</p>", "", page)
    page = re.sub(r"\s*<p class=\"plan-links\">[\s\S]*?</p>", "", page)
    page = re.sub(r"\s*<section class=\"related-reading\"[\s\S]*?</section>", "", page)
    decisions = []
    short_rest: list[dict] = []
    for link in links:
        kind, _name = _bucket(link["placement"])
        if kind in NAV_KINDS:
            decisions.append(_decide(link, "placed-nav", "Rendered in the nav, breadcrumb or hub chrome"))
            continue
        count = word_count(link.get("anchor") or "")
        if count < 2 or count > 14:
            decisions.append(
                _decide(link, "skipped", f"anchor is {count} words; in-sentence and block links use 2–14 words")
            )
            continue
        page, wrapped = _wrap_html_paragraphs(page, link["anchor"], link["target"])
        if wrapped:
            decisions.append(_decide(link, "placed-inline", "Existing phrase linked in a paragraph"))
        else:
            short_rest.append(link)
    placed_blocks, block_decisions = build_blocks(short_rest, post)
    decisions.extend(block_decisions)

    post["_decisions"] = decisions
    post["_related_blocks"] = placed_blocks
    post["_related_block"] = placed_blocks[0] if placed_blocks else {"title": "", "items": []}
    sentences_html = ""
    blocks_html = "\n".join(related_block_html(b["title"], b["items"]) for b in placed_blocks)
    if sentences_html:
        marker = page.find('<section class="faq-section"')
        if marker < 0:
            marker = page.find('<section class="related-section"')
        if marker >= 0:
            page = page[:marker] + sentences_html + page[marker:]
    if blocks_html:
        marker = page.find('<section class="related-section"')
        if marker < 0:
            marker = page.find("</article>")
        if marker >= 0:
            page = page[:marker] + blocks_html + page[marker:]
    return page


def classify_index_links(links: list[dict]) -> list[dict]:
    """The guide index renders nav rows itself. Long anchors stay unplaced."""
    decisions = []
    for link in links:
        kind, _name = _bucket(link["placement"])
        count = word_count(link.get("anchor") or "")
        if kind in {"chips", "nav", "breadcrumb"}:
            decisions.append(_decide(link, "placed-nav", "Rendered in the nav, breadcrumb or hub chrome"))
            continue
        if kind == "hub-sidebar":
            decisions.append(_decide(link, "skipped", "Removed per user request"))
            continue
        if count < 2 or count > 14:
            decisions.append(
                _decide(link, "skipped", f"anchor is {count} words; in-sentence and block links use 2–14 words")
            )
            continue
        decisions.append(_decide(link, "skipped", "no natural sentence on this page for this anchor"))
    return decisions


DECISION_FIELDS = ["priority", "source", "target", "anchor", "placement", "status", "reason"]


def write_decisions(rows: list[dict], path: Path) -> None:
    ordered = sorted(rows, key=lambda row: (row.get("source") or "", row.get("target") or "", row.get("anchor") or ""))
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=DECISION_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(ordered)
