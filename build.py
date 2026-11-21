#!/usr/bin/env python3
"""Build index.html from src/template.html + data/library.txt (no dependencies)."""
from pathlib import Path

root = Path(__file__).parent
data = (root / "data" / "library.txt").read_text(encoding="utf-8")
if "</script" in data.lower():
    raise SystemExit("library.txt must not contain '</script'")
html = (root / "src" / "template.html").read_text(encoding="utf-8").replace("__DATA__", data)
(root / "index.html").write_text(html, encoding="utf-8")
lines = [l for l in data.splitlines() if l.strip() and not l.startswith("#")]
print(f"Built index.html: {sum(not l.startswith('R') for l in lines)} CAD files, "
      f"{sum(l.startswith('R') for l in lines)} resources")
