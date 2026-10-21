#!/usr/bin/env python3
"""Stamp every local CSS link with a hash of that file's contents.

Without this a browser keeps serving the stylesheet it already has, so a CSS
change looks like it did nothing — the markup updates, the rules do not, and
new elements render with browser defaults. Re-run after editing any CSS.
"""
import hashlib, pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
digests = {p.name: hashlib.md5(p.read_bytes()).hexdigest()[:8]
           for p in (root / "css").glob("*.css")}

changed = 0
for page in root.glob("*.html"):
    text = original = page.read_text()
    def stamp(m):
        name = m.group(1)
        return f'href="css/{name}?v={digests[name]}"' if name in digests else m.group(0)
    text = re.sub(r'href="css/([A-Za-z0-9_-]+\.css)(?:\?v=[a-f0-9]+)?"', stamp, text)
    if text != original:
        page.write_text(text); changed += 1
        print(f"  stamped {page.name}")
print(f"{changed} page(s) updated")
