#!/usr/bin/env python3
"""Download a thumbnail for every library entry into thumbs/<key>.webp.

Sources, in order:
  1. The thumbnail cadbaseftc.com shows for the same CAD URL (one-time mirror).
  2. Onshape's thumbnail API, if ONSHAPE_ACCESS_KEY / ONSHAPE_SECRET_KEY are set
     (repo secrets). This covers new Onshape submissions.
Entries with no thumbnail keep the built-in line drawing on the site.
Existing files are never re-downloaded. Requires: requests, Pillow.
"""
import hashlib, io, os, re, sys, time
from pathlib import Path

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
THUMBS = ROOT / "thumbs"
ONSHAPE = "https://cad.onshape.com/documents/"
UA = {"User-Agent": "Orbit-x-Comet-OpenCAD-thumbnailer (+https://github.com/Saloom-Inc/orbit)"}
WIDTH = 640


def key(url: str) -> str:
    return hashlib.sha1(url.encode()).hexdigest()[:12]


def library_urls():
    for line in (ROOT / "data" / "library.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        kind, _title, url, *_ = line.split("|")
        if kind == "R":
            continue
        yield ONSHAPE + url[1:] if url.startswith("~") else url


def cadbase_map():
    """CAD URL -> absolute thumbnail URL, read from cadbaseftc.com's embedded page data."""
    try:
        html = requests.get("https://www.cadbaseftc.com/", headers=UA, timeout=60).text
    except requests.RequestException as e:
        print("cadbase unavailable:", e)
        return {}
    s = html.replace('\\\\"', '"').replace('\\"', '"').replace("\\u0026", "&")
    out = {}
    for chunk in s.split('{"id":"')[1:]:
        body = chunk.split("}")[0]
        u = re.search(r'"url":"([^"]*)"', body)
        t = re.search(r'"thumbnail":"([^"]*)"', body)
        if u and t and u.group(1) not in out:
            th = t.group(1)
            out[u.group(1)] = "https://www.cadbaseftc.com" + th if th.startswith("/") else th
    print(f"cadbase: {len(out)} thumbnails listed")
    return out


def onshape_thumb(url):
    ak, sk = os.environ.get("ONSHAPE_ACCESS_KEY"), os.environ.get("ONSHAPE_SECRET_KEY")
    m = re.match(r"https://cad\.onshape\.com/documents/(\w+)/([wvm])/(\w+)/e/(\w+)", url)
    if not (ak and sk and m):
        return None
    d, wvm, w, e = m.groups()
    api = f"https://cad.onshape.com/api/thumbnails/d/{d}/{wvm}/{w}/e/{e}/s/600x340"
    r = requests.get(api, auth=(ak, sk), headers={**UA, "Accept": "image/png"}, timeout=60)
    return r.content if r.ok and r.headers.get("content-type", "").startswith("image") else None


def save(raw: bytes, dest: Path) -> bool:
    try:
        im = Image.open(io.BytesIO(raw))
        im = im.convert("RGBA") if im.mode in ("P", "LA") else im
        if im.width > WIDTH:
            im = im.resize((WIDTH, round(im.height * WIDTH / im.width)), Image.LANCZOS)
        im.save(dest, "WEBP", quality=72, method=6)
        return True
    except Exception as e:  # corrupt or non-image response
        print("  bad image:", e)
        return False


def main():
    THUMBS.mkdir(exist_ok=True)
    urls = list(dict.fromkeys(library_urls()))
    todo = [u for u in urls if not (THUMBS / f"{key(u)}.webp").exists()]
    print(f"{len(urls)} CAD URLs, {len(todo)} without a thumbnail")
    if not todo:
        return
    src = cadbase_map()
    got = 0
    for u in todo:
        raw = None
        if u in src:
            try:
                r = requests.get(src[u], headers=UA, timeout=60)
                raw = r.content if r.ok else None
            except requests.RequestException as e:
                print("  fetch failed:", e)
        if raw is None:
            raw = onshape_thumb(u)
        if raw and save(raw, THUMBS / f"{key(u)}.webp"):
            got += 1
        time.sleep(0.15)
    print(f"saved {got} new thumbnails; {len(todo) - got} entries keep the line drawing")


if __name__ == "__main__":
    sys.exit(main())
