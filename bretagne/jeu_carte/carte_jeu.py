"""Visuel du jeu de la carte (1080x1350) : décor ChatGPT + carte exacte Lambert-93 + grille 10x12.
usage : python3 carte_jeu.py sortie.png "Concarneau" [--reponse]"""
import sys, json, csv
import pathlib
ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI)); import geo
from PIL import Image, ImageDraw, ImageFont, ImageFilter
DECOR = ICI / 'decor.png'   # décor ChatGPT (validé par Anthony le 04/11/2026)
CINZEL = str(ICI / 'Cinzel.ttf')   # police Cinzel, licence SIL OFL
G = json.load(open(ICI / 'grille.json'))
XMIN, XMAX, YMIN, YMAX, NC, NL = G['x_min'], G['x_max'], G['y_min'], G['y_max'], G['colonnes'], G['lignes']
CW, CH = (XMAX - XMIN) / NC, (YMAX - YMIN) / NL
NAVY, OR, MER = (28, 43, 92), (196, 150, 60), (179, 226, 254)
DEPS = {'22': "Côtes-d'Armor", '29': 'Finistère', '35': 'Ille-et-Vilaine', '44': 'Loire-Atlantique', '56': 'Morbihan'}
TEINTE = {'29': (243, 231, 198), '22': (238, 222, 186), '56': (246, 236, 208), '35': (240, 226, 192), '44': (236, 224, 196)}
def font(s, w=700):
    f = ImageFont.truetype(CINZEL, s); f.set_variation_by_axes([w]); return f

def fond_4x5():
    d = Image.open(DECOR).convert('RGB'); k = 1080 / d.width
    d = d.resize((1080, round(d.height * k)), Image.LANCZOS)
    haut = d.crop((0, 0, 1080, round(985 * k)))                    # titre + cadre carte
    bas = d.crop((0, round(1290 * k), 1080, d.height))              # cadre question + bordure
    milieu = d.crop((0, round(1000 * k), 1080, round(1000 * k) + 1350 - haut.height - bas.height))
    milieu.paste(milieu.crop((250, 0, 560, milieu.height)), (700, 0))  # efface la pointe de la rose des vents
    milieu.paste(milieu.crop((330, 0, 590, milieu.height)), (70, 0))   # efface le haut du mât du voilier
    out = Image.new('RGB', (1080, 1350)); out.paste(haut, (0, 0)); out.paste(milieu, (0, haut.height))
    out.paste(bas, (0, haut.height + milieu.height))
    rose = d.crop((round(720 * k), round(990 * k), round(1005 * k), round(1285 * k)))
    return out, k, bas.height, rose

def creer(sortie, commune, reponse=False):
    img, k, hbas, rose = fond_4x5()
    rx0, ry0, rx1, ry1 = round(33 * k), round(324 * k), round(988 * k), round(977 * k)   # zone bleue
    LAB = 34
    mh = (ry1 - ry0) - LAB - 14; S = mh / (YMAX - YMIN); mw = (XMAX - XMIN) * S
    ox = rx0 + LAB + ((rx1 - rx0 - LAB) - mw) / 2; oy = ry0 + LAB
    def P(x, y): return (ox + (x - XMIN) * S, oy + (YMAX - y) * S)
    SS = 3                                                            # suréchantillonnage
    W, H = rx1 - rx0, ry1 - ry0
    lay = Image.new('RGB', (W * SS, H * SS), MER); d = ImageDraw.Draw(lay)
    def Q(x, y): px, py = P(x, y); return ((px - rx0) * SS, (py - ry0) * SS)
    deps = {f['properties']['code']: geo.anneaux(f['geometry']) for f in json.load(open(ICI / 'departements.geojson'))['features'] if f['properties']['code'] in DEPS}
    for c, ps in deps.items():
        for p in ps:
            d.polygon([Q(*geo.l93(*q)) for q in p[0]], fill=TEINTE[c])
    for c, ps in deps.items():                                        # contours
        for p in ps:
            pts = [Q(*geo.l93(*q)) for q in p[0]]; d.line(pts + pts[:1], fill=NAVY, width=2 * SS, joint='curve')
    for i in range(NC + 1):
        d.line([Q(XMIN + i * CW, YMAX), Q(XMIN + i * CW, YMIN)], fill=(70, 95, 150), width=SS)
    for j in range(NL + 1):
        d.line([Q(XMIN, YMAX - j * CH), Q(XMAX, YMAX - j * CH)], fill=(70, 95, 150), width=SS)
    lay = lay.resize((W, H), Image.LANCZOS); img.paste(lay, (rx0, ry0))
    d = ImageDraw.Draw(img)
    for c, ps in deps.items():                                        # noms des départements
        best = max(ps, key=lambda p: abs(geo.aire_centroide(p[0])[0]))
        lon, lat = geo.aire_centroide(best[0])[1]
        if c == '29': lon += 0.15
        x, y = P(*geo.l93(lon, lat))
        d.text((x, y), DEPS[c].upper(), font=font(13, 600), fill=(110, 95, 70), anchor='mm')
    for i in range(NC):
        d.text((P(XMIN + (i + .5) * CW, 0)[0], ry0 + LAB / 2 + 2), 'ABCDEFGHIJ'[i], font=font(24, 800), fill=NAVY, anchor='mm')
    for j in range(NL):
        d.text((ox - LAB / 2 - 2, P(0, YMAX - (j + .5) * CH)[1]), str(j + 1), font=font(20, 800), fill=NAVY, anchor='mm')
    rs = rose.resize((150, round(150 * rose.height / rose.width)), Image.LANCZOS)   # rose des vents dans la mer (cases vides)
    m = Image.new('L', rs.size, 0); ImageDraw.Draw(m).ellipse([4, 4, rs.width - 4, rs.height - 4], fill=255)
    img.paste(rs, (round(P(XMIN + 0.35 * CW, 0)[0]), round(P(0, YMAX - 9.35 * CH)[1])), m.filter(ImageFilter.GaussianBlur(3)))
    r = next(r for r in csv.DictReader(open(ICI / 'communes_grille.csv', encoding='utf-8')) if r['nom'] == commune)
    assert r['fiable'] == 'oui', 'commune trop près d’une ligne : à éviter'
    # zone question (cadre du bas)
    by0 = 1350 - hbas; cy = by0 + hbas * 0.47
    def fit(t, size, w8, maxw=930):
        while font(size, w8).getlength(t) > maxw: size -= 2
        return font(size, w8)
    if not reponse:
        t = f'OÙ SE TROUVE {commune.upper()} ?'
        d.text((540, cy - 38), t, font=fit(t, 60, 800), fill=NAVY, anchor='mm')
        d.text((540, cy + 38), 'Répondez en commentaire : lettre + chiffre', font=fit('Répondez en commentaire : lettre + chiffre', 32, 700), fill=(80, 65, 40), anchor='mm')
    else:
        x, y = P(float(r['x_l93']), float(r['y_l93']))
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(200, 40, 40), outline='white', width=3)
        d.text((x + 13, y - 2), commune, font=font(20, 800), fill=(150, 20, 20), anchor='lm', stroke_width=3, stroke_fill='white')
        d.text((540, cy - 36), f'RÉPONSE : {r["case"]}', font=font(68, 800), fill=NAVY, anchor='mm')
        t = f'{commune} · {DEPS[r["dep"]]}'
        d.text((540, cy + 40), t, font=fit(t, 36, 700), fill=(80, 65, 40), anchor='mm')
    img.save(sortie, optimize=True)
    return r['case']

if __name__ == '__main__':
    print(creer(sys.argv[1], sys.argv[2], '--reponse' in sys.argv))
