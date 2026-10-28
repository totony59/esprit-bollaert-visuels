"""Visuels de la page « Cap sur la Bretagne » (1080x1350, format portrait du fil Facebook).

Fond crème semé d'hermines, bandeau noir à hermines, grand triskell en filigrane, bandes du
Gwenn-ha-du en pied, et une couleur par rubrique. Symboles dessinés en code (bretagne/symboles.py).
Aucune dépendance autre que Pillow. Polices Inter Display incluses dans bretagne/polices/ (licence OFL).

Exemples :
  python3 bretagne/visuel.py bretagne/visuels/2026-11-03_mot_kenavo.png \
      --rubrique "LE MOT BRETON" --titre "Kenavo" --texte "Ça veut dire « au revoir ». Et vous, vous le dites encore ?"
  python3 bretagne/visuel.py bretagne/visuels/2026-11-01_quiz_x.png --rubrique "LE QUIZ DU DIMANCHE" \
      --titre "Où est né le kouign-amann ?" --options "Douarnenez|Quimper|Concarneau" --texte "Réponse ce soir en commentaire"
  Illustration (ChatGPT) optionnelle : --fond bretagne/fonds/legende-1.png (affichée en grand sous le bandeau, texte dessous).
  Couleur forcée : --couleur "#1E4E79".

Le texte s'adapte tout seul (taille et retours à la ligne). Vérifier l'image avant publication.
"""
import argparse
import math
import pathlib
import sys
import unicodedata

from PIL import Image, ImageDraw, ImageFont

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import symboles  # noqa: E402

POL = ICI / "polices"
W, H, S = 1080, 1350, 2  # S : suréchantillonnage pour un rendu net
NOIR, CREME, BLANC = (21, 21, 21), (244, 238, 226), (255, 255, 255)
TEXTE = (70, 66, 60)
MARGE = 84
HAUT_BANDEAU = 168
HAUT_PIED = 72

# Une couleur par rubrique (assez foncée pour du texte blanc)
COULEURS = {
    "CE JOUR-LA": (30, 78, 121),      # bleu océan
    "LE MOT BRETON": (163, 59, 42),   # rouge brique
    "LA QUESTION": (176, 108, 20),    # ocre
    "LEGENDE": (40, 98, 72),          # vert lande
    "LA RECETTE": (176, 108, 20),     # ocre
    "LE QUIZ": (30, 78, 121),         # bleu océan
}


def sans_accents(t):
    return "".join(c for c in unicodedata.normalize("NFD", t.upper()) if unicodedata.category(c) != "Mn")


def couleur_rubrique(rubrique):
    r = sans_accents(rubrique)
    for cle, c in COULEURS.items():
        if r.startswith(cle):
            return c
    return (30, 78, 121)


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


def boussole(d, cx, cy, r, couleur, fond):
    """Petite rose des vents (même dessin que le logo)."""
    cx, cy, r = cx * S, cy * S, r * S
    d.ellipse([cx - r * .72, cy - r * .72, cx + r * .72, cy + r * .72],
              outline=couleur + (110,), width=int(1.8 * S))
    k = r / 190
    def p(x, y):
        a = math.radians(45)
        return (cx + (x * math.cos(a) - y * math.sin(a)) * k, cy + (x * math.sin(a) + y * math.cos(a)) * k)
    d.polygon([p(0, -180), p(42, 0), p(-42, 0)], fill=couleur)
    d.polygon([p(-42, 0), p(42, 0), p(0, 180)], fill=couleur + (120,))
    hr = 15 * k
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=fond, outline=couleur, width=max(2, int(5 * k)))


def semis_hermines(img):
    """Hermines très discrètes semées sur le fond (quinconce)."""
    calque = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(calque)
    pas_x, pas_y = 150, 150
    for j, y in enumerate(range(HAUT_BANDEAU + 40, H - HAUT_PIED, pas_y)):
        for x in range(40 + (pas_x // 2 if j % 2 else 0), W, pas_x):
            symboles.hermine(d, x * S, (y + 30) * S, 40 * S, NOIR + (16,))
    img.alpha_composite(calque)


def creer(sortie, rubrique, titre, texte=None, options=None, fond=None, couleur=None):
    acc = couleur or couleur_rubrique(rubrique)
    img = Image.new("RGBA", (W * S, H * S), CREME + (255,))
    semis_hermines(img)

    # Grand triskell en filigrane, en bas à droite (coupé par le bord)
    calque = Image.new("RGBA", img.size, (0, 0, 0, 0))
    symboles.triskell(ImageDraw.Draw(calque), (W - 215) * S, (H - 315) * S, 255 * S, acc + (40,), 46 * S, rotation=-20)
    img.alpha_composite(calque)

    zone_haut, zone_bas = HAUT_BANDEAU + 70, H - HAUT_PIED - 70
    if fond:
        # Illustration (ChatGPT) en grand sous le bandeau, recadrée au centre ; le texte va dessous
        y0, hi = HAUT_BANDEAU + 10, (400 if options else 560)
        f = Image.open(fond).convert("RGBA")
        r = max(W * S / f.width, hi * S / f.height)
        f = f.resize((round(f.width * r), round(f.height * r)), Image.LANCZOS)
        g, h = (f.width - W * S) // 2, (f.height - hi * S) // 2
        img.paste(f.crop((g, h, g + W * S, h + hi * S)), (0, y0 * S))
        zone_haut = y0 + hi + 50
    d = ImageDraw.Draw(img, "RGBA")

    # Bandeau noir : boussole + nom de la page + hermines
    d.rectangle([0, 0, W * S, HAUT_BANDEAU * S], fill=NOIR)
    boussole(d, MARGE + 30, HAUT_BANDEAU / 2, 44, BLANC, NOIR)
    fb = police("ExtraBold", 34)
    d.text(((MARGE + 86) * S, (HAUT_BANDEAU / 2 - 22) * S), "CAP SUR LA BRETAGNE", font=fb, fill=BLANC)
    for i, x in enumerate((W - MARGE - 112, W - MARGE - 56, W - MARGE)):
        symboles.hermine(d, x * S, (HAUT_BANDEAU / 2 + 4) * S, 50 * S, BLANC)
    d.rectangle([0, HAUT_BANDEAU * S, W * S, (HAUT_BANDEAU + 10) * S], fill=acc)

    # Pied : bandes du Gwenn-ha-du
    symboles.gwenn_ha_du(d, 0, (H - HAUT_PIED) * S, W * S, H * S, NOIR)

    largeur = W - 2 * MARGE
    dispo = zone_bas - zone_haut
    h_opts = len(options) * 112 + 10 if options else 0
    h_texte = 0
    if texte:
        fx, lx, tx = ajuster(texte, "Medium", 46, 30, largeur, min(360, int(dispo * 0.36)), d, 1.28)
        h_texte = len(lx) * tx * 1.28
    h_titre = dispo - 112 - h_opts - h_texte - (40 if texte else 0)
    t_max = 150 if len(titre) <= 14 else 116
    ft, lt, tt = ajuster(titre, "ExtraBold", t_max, 52, largeur, h_titre, d, 1.06)
    fr = police("Bold", 30)

    def bloc(y, dessiner):
        """Rubrique, titre, options, texte ; renvoie le bas du bloc (sans dessiner si dessiner=False)."""
        def centre(ligne, f, yy, couleur):
            d.text(((W * S - d.textlength(ligne, font=f)) / 2, yy * S), ligne, font=f, fill=couleur)

        if dessiner:
            lt_ = d.textlength(rubrique, font=fr) / S + 52
            x0 = (W - lt_) / 2
            d.rounded_rectangle([x0 * S, y * S, (x0 + lt_) * S, (y + 58) * S], radius=29 * S, fill=acc)
            centre(rubrique, fr, y + 13, BLANC)
        y += 58 + 50
        for l in lt:
            if dessiner:
                centre(l, ft, y, NOIR)
            y += tt * 1.06
        if options:
            y += 30
            for i, o in enumerate(options):
                if dessiner:
                    lettre = "ABCDEFG"[i]
                    d.rounded_rectangle([MARGE * S, y * S, (W - MARGE) * S, (y + 92) * S], radius=46 * S,
                                        outline=NOIR, width=3 * S, fill=BLANC)
                    d.ellipse([(MARGE + 14) * S, (y + 14) * S, (MARGE + 78) * S, (y + 78) * S], fill=acc)
                    fl = police("ExtraBold", 34)
                    lw = d.textlength(lettre, font=fl) / S
                    d.text(((MARGE + 46 - lw / 2) * S, (y + 25) * S), lettre, font=fl, fill=BLANC)
                    fo, lo, _ = ajuster(o, "SemiBold", 44, 30, largeur - 240, 60, d)
                    centre(lo[0], fo, y + 21, NOIR)
                y += 112
            y -= 20
        if texte:
            y += 40
            for l in lx:
                if dessiner:
                    centre(l, fx, y, TEXTE)
                y += tx * 1.28
        return y

    hauteur = bloc(0, False)
    bloc(zone_haut + max(0, (dispo - hauteur) / 2) - 20, True)

    img.convert("RGB").resize((W, H), Image.LANCZOS).save(sortie, optimize=True)
    return sortie


if __name__ == "__main__":
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("sortie")
    a.add_argument("--rubrique", required=True,
                   help="CE JOUR-LÀ EN BRETAGNE, LE MOT BRETON, LA QUESTION, LÉGENDE & PATRIMOINE, LA RECETTE, LE QUIZ DU DIMANCHE")
    a.add_argument("--titre", required=True)
    a.add_argument("--texte")
    a.add_argument("--options", help="propositions du quiz séparées par |")
    a.add_argument("--fond", help="image de fond (ChatGPT) dans bretagne/fonds/")
    a.add_argument("--couleur", help="couleur forcée, ex. #1E4E79")
    x = a.parse_args()
    col = tuple(int(x.couleur.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)) if x.couleur else None
    pathlib.Path(x.sortie).parent.mkdir(parents=True, exist_ok=True)
    print(creer(x.sortie, x.rubrique, x.titre, x.texte, x.options.split("|") if x.options else None, x.fond, col))
