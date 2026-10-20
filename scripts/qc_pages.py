"""Per-page QC for images, bylines, JSON-LD, brand words and links. Run after build_site.py."""
import csv, json, re, sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_site as b  # noqa: E402

config = b.load_config()
posts, _ = b.load_posts(config)
checks = ["image_file", "image_size_dims", "alt", "byline_author", "jsonld_parse_author", "og_twitter_image", "brand", "links", "no_root_relative", "no_index_html_href", "header_footer"]
results = {c: Counter() for c in checks}
fails = []
try:
    from PIL import Image
except ImportError:
    Image = None
HEADER_FOOTER_MARKERS = (
    'class="header-nav', 'class="nav-brand"',
    'id="mobile-toggle-btn"', 'id="mobile-drawer"', '<footer class="site-footer ak-footer" id="footer">',
    'assets/ak-chrome.css', 'assets/ak-chrome.js', 'favicon.svg',
)
def internal_index_href(page):
    """index.html in any internal href (relative or acrenkey.com). External sites are out of scope."""
    refs = re.findall(r'href=(?:"([^"]*)"|([^\s>]+))', page)
    return [r for pair in refs for r in pair if "index.html" in r and (not r.startswith(("http://", "https://")) or "acrenkey.com" in r)]


idx = (ROOT / "index.html").read_text()
idx_graph = []
try:
    idx_graph = [n for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', idx, re.S) for n in json.loads(blk)["@graph"]]
except Exception:
    pass
idx_types = set()
for n in idx_graph:
    t = n.get("@type")
    if isinstance(t, list):
        idx_types.update(t)
    elif isinstance(t, str):
        idx_types.add(t)
idx_ok = (
    not internal_index_href(idx)
    and all(x in idx for x in HEADER_FOOTER_MARKERS)
    and "RealEstateAgent" in idx_types
    and "WebSite" in idx_types
    and "Blog" in idx_types
)
for post in posts:
    path = ROOT / post["path"] / "index.html"
    page = path.read_text()
    img = ROOT / post["image"]
    r = {}
    r["image_file"] = img.is_file()
    ok = r["image_file"] and img.stat().st_size <= 150 * 1024
    if ok and Image:
        with Image.open(img) as im:
            ok = im.size == (1200, 675) and im.format == "WEBP"
    r["image_size_dims"] = ok
    tags = re.findall(r"<img\b[^>]*>", page)
    r["alt"] = bool(tags) and all(re.search(r'alt="[^"]+\S[^"]*"|alt="\S+"', t) for t in tags)
    r["byline_author"] = "author-byline-card" in page and "author-details-name" in page and post["author"] in page
    try:
        graph = [n for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S) for n in json.loads(blk)["@graph"]]
        art = next(n for n in graph if n["@type"] == "BlogPosting")
        prof = b.AUTHOR_PROFILES[post["author"]]
        author_ok = (
            art["author"]["@type"] == "Person"
            and art["author"]["name"] == prof["name"]
            and art["author"]["image"] == prof["avatar"]
            and art["author"]["sameAs"] == [prof["linkedin"]]
        )
        pub_type = art["publisher"]["@type"]
        pub_ok = pub_type == "Organization" or (isinstance(pub_type, list) and "Organization" in pub_type)
        r["jsonld_parse_author"] = (
            author_ok
            and pub_ok
            and art["image"] == b.abs_url(config["baseUrl"], post["image"])
            and art.get("speakable", {}).get("@type") == "SpeakableSpecification"
        )
    except Exception:
        r["jsonld_parse_author"] = False
    want = b.abs_url(config["baseUrl"], post["image"])
    r["og_twitter_image"] = f'property="og:image" content="{want}"' in page and f'name="twitter:image" content="{want}"' in page
    body = re.sub(r"https?://\S+", " ", b.visible_text(page))
    r["brand"] = not b.find_banned(body) and not b.find_banned(b.head_text(page)) and "100%" not in body
    bad = []
    for ref in re.findall(r'(?:href|src)="([^"]+)"', page):
        if ref.startswith(("http://", "https://", "mailto:", "#", "data:")):
            continue
        ref = ref.split("#")[0].split("?")[0]
        if not ref:
            continue
        t = (path.parent / ref).resolve()
        if t.is_dir():
            t = t / "index.html"
        if not t.exists():
            bad.append(ref)
    r["links"] = not bad
    r["no_root_relative"] = not re.search(r'(?:href|src)="/(?!/)', page)
    r["no_index_html_href"] = not internal_index_href(page)
    r["header_footer"] = all(x in page for x in HEADER_FOOTER_MARKERS)
    for c in checks:
        results[c]["pass" if r[c] else "fail"] += 1
        if not r[c]:
            fails.append((post["slug"], c))
print(f"{'check':22} pass fail")
for c in checks:
    print(f"{c:22} {results[c]['pass']:4} {results[c]['fail']:4}")
print("authors:", dict(Counter(p["author"] for p in posts)))
for f in fails[:30]:
    print("FAIL", *f)
print("index.html page: no_index_html_href+header_footer", "PASS" if idx_ok else "FAIL")
