"""Symboles basques dessinés en code (Pillow) : lauburu et rayures du linge basque.

Dessins originaux, sans image externe. Coordonnées en pixels du calque passé en argument.
"""
from PIL import Image, ImageDraw


def lauburu(img, cx, cy, R, couleur, rotation=0.0):
    """Lauburu (croix basque à quatre têtes en virgule), rayon R, collé sur img (RGBA)."""
    taille = int(2 * R) + 4
    c = taille / 2
    a = R / 2
    bras = Image.new("L", (taille, taille), 0)
    d = ImageDraw.Draw(bras)
    # grand demi-disque (au-dessus de l'axe), du centre jusqu'au bord
    d.pieslice([c, c - a, c + 2 * a, c + a], 180, 360, fill=255)
    # petit creux côté centre (au-dessus), petite bosse côté bord (en dessous)
    d.pieslice([c, c - a / 2, c + a, c + a / 2], 180, 360, fill=0)
    d.pieslice([c + a, c - a / 2, c + 2 * a, c + a / 2], 0, 180, fill=255)
    masque = Image.new("L", (taille, taille), 0)
    for k in range(4):
        tourne = bras.rotate(90 * k, resample=Image.BICUBIC, center=(c, c))
        masque = Image.composite(tourne, masque, tourne)
    if rotation:
        masque = masque.rotate(rotation, resample=Image.BICUBIC, center=(c, c))
    couche = Image.new("RGBA", (taille, taille), couleur[:3] + (0,))
    alpha = couleur[3] if len(couleur) == 4 else 255
    couche.putalpha(masque.point(lambda v: v * alpha // 255))
    img.alpha_composite(couche, (int(cx - c), int(cy - c)))


def linge_basque(d, x0, y0, x1, y1, rouge, vert, fond):
    """Rayures de linge basque (fond clair, bandes rouges et vertes) dans le rectangle donné."""
    d.rectangle([x0, y0, x1, y1], fill=fond)
    motif = [(rouge, 10), (fond, 6), (rouge, 4), (fond, 8), (vert, 14), (fond, 8), (rouge, 4), (fond, 6), (rouge, 10)]
    total = sum(h for _, h in motif)
    k = (y1 - y0) / total
    y = y0
    for col, h in motif:
        if col != fond:
            d.rectangle([x0, y, x1, y + h * k], fill=col)
        y += h * k
