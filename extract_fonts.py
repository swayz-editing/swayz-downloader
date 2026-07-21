# -*- coding: utf-8 -*-
"""Extrait les polices base64 de l'artifact DA vers des fichiers .woff2."""
import os, re, base64

ART = r"C:\Users\nopti 01\.claude\projects\C--Users-nopti-01-Downloads\60009f75-43b5-4240-a9dc-bbd8ce3a9a3f\tool-results\artifact-d4470b41-1784626218-3c17.html"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
os.makedirs(OUT, exist_ok=True)

html = open(ART, "r", encoding="utf-8", errors="replace").read()

blocks = re.findall(r"@font-face\s*\{(.*?)\}", html, re.S)
names = {"Display": "display", "Body": "body", "Serif": "serif"}
seen = {}
css = []
for b in blocks:
    fam = re.search(r"font-family:\s*'([^']+)'", b)
    data = re.search(r"data:font/woff2;base64,([A-Za-z0-9+/=]+)", b)
    if not fam or not data:
        continue
    family = fam.group(1)
    if family not in names:
        continue
    style = "italic" if re.search(r"font-style:\s*italic", b) else "normal"
    weight = re.search(r"font-weight:\s*([\d ]+)", b)
    weight = weight.group(1).strip() if weight else "400"
    slug = names[family] + ("-italic" if style == "italic" else "")
    if slug in seen:
        continue
    seen[slug] = True
    fname = f"swayz-{slug}.woff2"
    raw = base64.b64decode(data.group(1))
    with open(os.path.join(OUT, fname), "wb") as f:
        f.write(raw)
    css.append(
        "@font-face{font-family:'%s';src:url('fonts/%s') format('woff2');"
        "font-weight:%s;font-style:%s;font-display:swap}"
        % (family, fname, weight, style)
    )
    print(f"  {fname}  ({len(raw)//1024} Ko)  family={family} style={style} weight={weight}")

with open(os.path.join(OUT, "fonts.css"), "w", encoding="utf-8") as f:
    f.write("\n".join(css))
print("\n--- @font-face à coller ---")
print("\n".join(css))
