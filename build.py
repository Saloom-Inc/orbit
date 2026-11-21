#!/usr/bin/env python3
"""Build index.html from src/template.html + data/library.txt (+ thumbs/). No dependencies."""
import hashlib, json
from pathlib import Path

root = Path(__file__).parent
ONSHAPE = "https://cad.onshape.com/documents/"
data = (root / "data" / "library.txt").read_text(encoding="utf-8")
if "</script" in data.lower():
    raise SystemExit("library.txt must not contain '</script'")

lines = [l for l in data.splitlines() if l.strip() and not l.startswith("#")]
thumbs = []
for l in lines:
    url = l.split("|")[2]
    url = ONSHAPE + url[1:] if url.startswith("~") else url
    k = hashlib.sha1(url.encode()).hexdigest()[:12]
    thumbs.append(k if (root / "thumbs" / f"{k}.webp").exists() else None)

html = (root / "src" / "template.html").read_text(encoding="utf-8")
html = html.replace("__DATA__", data).replace("__THUMBS__", json.dumps(thumbs, separators=(",", ":")))
(root / "index.html").write_text(html, encoding="utf-8")
print(f"Built index.html: {sum(not l.startswith('R') for l in lines)} CAD files, "
      f"{sum(l.startswith('R') for l in lines)} resources, {sum(t is not None for t in thumbs)} thumbnails")
