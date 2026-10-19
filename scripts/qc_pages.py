"""Per-page QC for images, bylines, JSON-LD, brand words and links. Run after build_site.py."""
import csv, json, re, sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_site as b  # noqa: E402

config = b.load_config()
posts, _ = b.load_posts(config)
checks = ["image_file", "image_size_dims", "alt", "byline_author", "jsonld_parse_author", "og_twitter_image", "brand", "links", "no_root_relative"]
results = {c: Counter() for c in checks}
fails = []
try:
    from PIL import Image
except ImportError:
    Image = None
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
    r["byline_author"] = f'By <span class="author-details-name">{post["author"]}</span>' in page
    try:
        graph = [n for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S) for n in json.loads(blk)["@graph"]]
        art = next(n for n in graph if n["@type"] == "Article")
        r["jsonld_parse_author"] = art["author"] == {"@type": "Person", "name": post["author"], "worksFor": {"@type": "Organization", "name": "Acrenkey Realty LLP", "url": "https://acrenkey.com/"}} and art["publisher"]["@type"] == "Organization" and art["image"] == b.abs_url(config["baseUrl"], post["image"])
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
