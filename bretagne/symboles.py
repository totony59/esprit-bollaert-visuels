"""Symboles bretons dessinés en code (Pillow) : moucheture d'hermine, triskell, bandes du Gwenn-ha-du.

Dessins originaux, sans image externe. Coordonnées en pixels du calque passé en argument.
"""
import math


def hermine(d, cx, cy, h, couleur):
    """Moucheture d'hermine stylisée, hauteur h, centrée en (cx, cy)."""
    u = h / 1.6
    def P(x, y):
        return (cx + x * u, cy + y * u)
    # trois points au-dessus
    for (x, y, r) in ((0, -0.66, 0.13), (-0.25, -0.48, 0.11), (0.25, -0.48, 0.11)):
        X, Y = P(x, y)
        d.ellipse([X - r * u, Y - r * u, X + r * u, Y + r * u], fill=couleur)
    # corps en cloche terminé par trois pointes
    pts = [(0, -0.44), (0.07, -0.28), (0.13, -0.08), (0.22, 0.14), (0.34, 0.34), (0.46, 0.52),
           (0.52, 0.7), (0.3, 0.58), (0.2, 0.8), (0.08, 0.62), (0.0, 0.86), (-0.08, 0.62),
           (-0.2, 0.8), (-0.3, 0.58), (-0.52, 0.7), (-0.46, 0.52), (-0.34, 0.34), (-0.22, 0.14),
           (-0.13, -0.08), (-0.07, -0.28)]
    d.polygon([P(x, y) for x, y in pts], fill=couleur)


def triskell(d, cx, cy, R, couleur, epaisseur, rotation=0.0):
    """Triskell : trois bras en spirale qui partent du centre, rayon R."""
    for k in range(3):
        phi = math.radians(rotation) + k * 2 * math.pi / 3
        C = (cx + 0.5 * R * math.cos(phi), cy + 0.5 * R * math.sin(phi))
        r0 = 0.5 * R
        theta0 = phi + math.pi          # le bras part du centre du triskell
        n = 900
        for i in range(n + 1):
            t = i / n
            r = r0 * (1 - 0.86 * t)
            th = theta0 - t * 2.15 * math.pi
            x, y = C[0] + r * math.cos(th), C[1] + r * math.sin(th)
            e = epaisseur / 2 * (1 - 0.3 * t)   # le bras s'affine vers le cœur de la spirale
            d.ellipse([x - e, y - e, x + e, y + e], fill=couleur)


def gwenn_ha_du(d, x0, y0, x1, y1, noir, blanc=None):
    """Neuf bandes horizontales alternées (noir en premier), dans le rectangle donné."""
    h = (y1 - y0) / 9
    for i in range(9):
        if i % 2 == 0:
            d.rectangle([x0, y0 + i * h, x1, y0 + (i + 1) * h], fill=noir)
        elif blanc:
            d.rectangle([x0, y0 + i * h, x1, y0 + (i + 1) * h], fill=blanc)
