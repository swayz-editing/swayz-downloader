# -*- coding: utf-8 -*-
"""Génère icon.ico — œil SWΛYZ (orange / turquoise sur fond sombre)."""
import os
from PIL import Image, ImageDraw

APP_DIR = os.path.dirname(os.path.abspath(__file__))
S = 512
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# Fond arrondi sombre
r = 96
d.rounded_rectangle([0, 0, S, S], radius=r, fill=(11, 13, 16, 255))

# Halo orange (haut-droite) + turquoise (bas-gauche)
def glow(cx, cy, rad, color):
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    steps = 60
    for i in range(steps, 0, -1):
        a = int(70 * (i / steps) ** 2)
        rr = rad * i / steps
        ld.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=color+(a,))
    return layer

img.alpha_composite(glow(int(S*0.72), int(S*0.28), int(S*0.5), (255, 106, 26)))
img.alpha_composite(glow(int(S*0.28), int(S*0.74), int(S*0.5), (23, 182, 201)))
# re-masquer aux coins arrondis
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, S, S], radius=r, fill=255)
img.putalpha(mask)
d = ImageDraw.Draw(img)

cx, cy = S/2, S/2

# Forme d'œil (amande) — intersection de deux ellipses
eye_w, eye_h = S*0.74, S*0.5
eye = Image.new("L", (S, S), 0)
ed = ImageDraw.Draw(eye)
ed.ellipse([cx-eye_w/2, cy-eye_h/2, cx+eye_w/2, cy+eye_h/2], fill=255)

# Contour orange de l'œil
d.ellipse([cx-eye_w/2, cy-eye_h/2, cx+eye_w/2, cy+eye_h/2], outline=(255, 150, 60, 255), width=10)

# Iris turquoise
ir = S*0.20
for i in range(int(ir), 0, -1):
    t = i/ir
    col = (int(20+30*t), int(150+60*(1-t)), int(180+40*(1-t)))
    d.ellipse([cx-i, cy-i, cx+i, cy+i], fill=col+(255,))
# Anneau orange autour de l'iris
d.ellipse([cx-ir, cy-ir, cx+ir, cy+ir], outline=(255, 138, 60, 255), width=8)

# Pupille
pr = S*0.085
d.ellipse([cx-pr, cy-pr, cx+pr, cy+pr], fill=(6, 8, 10, 255))
# Reflet
hr = S*0.03
d.ellipse([cx-pr*0.5-hr, cy-pr*0.5-hr, cx-pr*0.5+hr, cy-pr*0.5+hr], fill=(255, 255, 255, 230))

# Sauvegarde multi-tailles
out = os.path.join(APP_DIR, "icon.ico")
img.save(out, sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
img.save(os.path.join(APP_DIR, "icon.png"))
print("Icone creee:", out)
