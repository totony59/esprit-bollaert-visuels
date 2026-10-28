"""Visuels de la page « Cap sur la Bretagne » (1080x1350, format portrait du fil Facebook).

Aucune dépendance autre que Pillow. Polices Inter Display incluses dans bretagne/polices/ (licence OFL).

Exemples :
  python3 bretagne/visuel.py bretagne/visuels/2026-11-03_mot_kenavo.png \
      --rubrique "LE MOT BRETON" --titre "Kenavo" --texte "Ça veut dire « au revoir ». Et vous, vous le dites encore ?"
  python3 bretagne/visuel.py bretagne/visuels/2026-11-01_quiz_x.png --rubrique "LE QUIZ DU DIMANCHE" \
      --titre "Où est né le kouign-amann ?" --options "Douarnenez|Quimper|Concarneau" --texte "Réponse ce soir 👇"
  Fond illustré (ChatGPT) optionnel : --fond bretagne/fonds/legende-1.png (recadré, voile blanc derrière le texte).

Le texte s'adapte tout seul (taille et retours à la ligne). Vérifier l'image avant publication.
"""
import argparse
import math
import pathlib

from PIL import Image, ImageDraw, ImageFont

ICI = pathlib.Path(__file__).resolve().parent
POL = ICI / "polices"
W, H, S = 1080, 1350, 2  # S : suréchantillonnage pour un rendu net
ENCRE, GRIS, PAPIER = (17, 17, 17), (105, 105, 105), (255, 255, 255)
MARGE = 84


def police(nom, taille):
    return ImageFont.truetype(str(POL / f"InterDisplay-{nom}.otf"), int(taille * S))


def couper(texte, f, largeur, d):
    """Retours à la ligne au mot près ; évite un mot seul en dernière ligne si possible."""
    lignes = []
    for para in texte.split("\n"):
        mots, cur = para.split(), ""
        for m in mots:
            essai = f"{cur} {m}".strip()
            if d.textlength(essai, font=f) <= largeur or not cur:
                cur = essai
            else:
                lignes.append(cur)
                cur = m
        lignes.append(cur)
    if len(lignes) >= 2 and " " not in lignes[-1] and len(lignes[-2].split()) > 2:
        avant = lignes[-2].rsplit(" ", 1)
        if d.textlength(f"{avant[1]} {lignes[-1]}", font=f) <= largeur:
            lignes[-2], lignes[-1] = avant[0], f"{avant[1]} {lignes[-1]}"
    return lignes


def ajuster(texte, nom, t_max, t_min, largeur, hauteur, d, interligne=1.12):
    for t in range(t_max, t_min - 1, -2):
        f = police(nom, t)
        lignes = couper(texte, f, largeur * S, d)
        if len(lignes) * t * S * interligne <= hauteur * S and \
                all(d.textlength(l, font=f) <= largeur * S for l in lignes):
            return f, lignes, t
    f = police(nom, t_min)
    return f, couper(texte, f, largeur * S, d), t_min


def boussole(d, cx, cy, r):
    """Petite rose des vents (même dessin que le logo)."""
    cx, cy, r = cx * S, cy * S, r * S
    d.ellipse([cx - r * .72, cy - r * .72, cx + r * .72, cy + r * .72], outline=(190, 190, 190), width=int(1.6 * S))
    k = r / 190
    def p(x, y):
        a = math.radians(45)
        dx, dy = x, y
        return (cx + (dx * math.cos(a) - dy * math.sin(a)) * k, cy + (dx * math.sin(a) + dy * math.cos(a)) * k)
    d.polygon([p(0, -180), p(42, 0), p(-42, 0)], fill=ENCRE)
    d.polygon([p(-42, 0), p(42, 0), p(0, 180)], fill=(180, 180, 180))
    hr = 15 * k
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=PAPIER, outline=ENCRE, width=max(2, int(5 * k)))


def bandes(d, y, hauteur):
    """Rappel discret du Gwenn-ha-du : 9 bandes noires et blanches en pied de visuel."""
    h = hauteur / 9
    for i in range(9):
        if i % 2 == 0:
            d.rectangle([0, (y + i * h) * S, W * S, (y + (i + 1) * h) * S], fill=ENCRE)


def creer(sortie, rubrique, titre, texte=None, options=None, fond=None):
    img = Image.new("RGB", (W * S, H * S), PAPIER)
    if fond:
        f = Image.open(fond).convert("RGB")
        r = max(W * S / f.width, H * S / f.height)
        f = f.resize((round(f.width * r), round(f.height * r)), Image.LANCZOS)
        g, h = (f.width - W * S) // 2, (f.height - H * S) // 2
        img.paste(f.crop((g, h, g + W * S, h + H * S)))
    d = ImageDraw.Draw(img, "RGBA")

    zone_haut, zone_bas = 250, H - 140  # espace réservé au texte
    if fond:  # voile blanc derrière tout le bloc texte
        d.rounded_rectangle([(MARGE - 40) * S, 40 * S, (W - MARGE + 40) * S, (zone_bas + 40) * S],
                            radius=36 * S, fill=(255, 255, 255, 232))

    # En-tête : boussole + nom de la page
    boussole(d, MARGE + 34, 112, 46)
    d.text(((MARGE + 96) * S, 92 * S), "CAP SUR LA BRETAGNE", font=police("Bold", 30), fill=ENCRE)
    d.line([MARGE * S, 176 * S, (W - MARGE) * S, 176 * S], fill=ENCRE, width=3 * S)

    largeur = W - 2 * MARGE
    dispo = zone_bas - zone_haut
    h_opts = len(options) * 112 + 10 if options else 0
    h_texte = 0
    if texte:
        fx, lx, tx = ajuster(texte, "Medium", 46, 30, largeur, min(360, int(dispo * 0.36)), d, 1.28)
        h_texte = len(lx) * tx * 1.28
    h_titre = dispo - 112 - h_opts - h_texte - (40 if texte else 0)
    t_max = 150 if len(titre) <= 14 else 112
    ft, lt, tt = ajuster(titre, "ExtraBold", t_max, 52, largeur, h_titre, d, 1.08)
    fr = police("Bold", 30)

    def bloc(y, dessiner):
        """Rubrique, titre, options, texte ; renvoie le bas du bloc (sans dessiner si dessiner=False)."""
        if dessiner:
            lt_ = d.textlength(rubrique, font=fr) / S + 52
            d.rounded_rectangle([MARGE * S, y * S, (MARGE + lt_) * S, (y + 58) * S], radius=29 * S, fill=ENCRE)
            d.text(((MARGE + 26) * S, (y + 13) * S), rubrique, font=fr, fill=PAPIER)
        y += 58 + 54
        for l in lt:
            if dessiner:
                d.text((MARGE * S, y * S), l, font=ft, fill=ENCRE)
            y += tt * 1.08
        if options:
            y += 30
            for i, o in enumerate(options):
                if dessiner:
                    lettre = "ABCDEFG"[i]
                    d.rounded_rectangle([MARGE * S, y * S, (W - MARGE) * S, (y + 92) * S], radius=20 * S,
                                        outline=ENCRE, width=3 * S, fill=PAPIER)
                    d.ellipse([(MARGE + 18) * S, (y + 18) * S, (MARGE + 74) * S, (y + 74) * S], fill=ENCRE)
                    fl = police("ExtraBold", 32)
                    lw = d.textlength(lettre, font=fl) / S
                    d.text(((MARGE + 46 - lw / 2) * S, (y + 27) * S), lettre, font=fl, fill=PAPIER)
                    fo, lo, _ = ajuster(o, "SemiBold", 44, 30, largeur - 130, 60, d)
                    d.text(((MARGE + 100) * S, (y + 22) * S), lo[0], font=fo, fill=ENCRE)
                y += 112
            y -= 20
        if texte:
            y += 40
            for l in lx:
                if dessiner:
                    d.text((MARGE * S, y * S), l, font=fx, fill=GRIS if not fond else ENCRE)
                y += tx * 1.28
        return y

    hauteur = bloc(0, False)
    bloc(zone_haut + max(0, (dispo - hauteur) / 2) - 30, True)

    bandes(d, H - 72, 72)
    img.resize((W, H), Image.LANCZOS).save(sortie, optimize=True)
    return sortie


if __name__ == "__main__":
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("sortie")
    a.add_argument("--rubrique", required=True, help="ex. LE MOT BRETON, CE JOUR-LÀ, LE QUIZ DU DIMANCHE")
    a.add_argument("--titre", required=True)
    a.add_argument("--texte")
    a.add_argument("--options", help="propositions du quiz séparées par |")
    a.add_argument("--fond", help="image de fond (ChatGPT) dans bretagne/fonds/")
    x = a.parse_args()
    pathlib.Path(x.sortie).parent.mkdir(parents=True, exist_ok=True)
    print(creer(x.sortie, x.rubrique, x.titre, x.texte, x.options.split("|") if x.options else None, x.fond))
