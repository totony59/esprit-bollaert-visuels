"""Visuel du jeu de la carte (1080x1350) pour « Cap sur - le Pays basque » : bandeau rouge, carte exacte
Lambert-93 des 158 communes du Pays basque (Communauté d'agglomération Pays Basque), grille 10 x 8 (cases de 9 km).
Sources des contours : geo.api.gouv.fr (communes, mairies, contour de l'agglomération), france-geojson
(communes voisines des Pyrénées-Atlantiques et des Landes), Natural Earth (Espagne).
usage : python3 carte_jeu.py sortie.png "Espelette" [--reponse]"""
import sys, json, csv, pathlib
ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI)); sys.path.insert(0, str(ICI.parent))
import geo, symboles
from PIL import Image, ImageDraw, ImageFont
CINZEL = str(ICI / 'Cinzel.ttf')   # police Cinzel, licence SIL OFL
INTER = str(ICI.parent / 'polices' / 'InterDisplay-ExtraBold.otf')
G = json.load(open(ICI / 'grille.json'))
XMIN, XMAX, YMIN, YMAX, NC, NL = G['x_min'], G['x_max'], G['y_min'], G['y_max'], G['colonnes'], G['lignes']
CW, CH = (XMAX - XMIN) / NC, (YMAX - YMIN) / NL
W, H = 1080, 1350
ROUGE, VERT, CREME, NAVY = (190, 32, 38), (0, 122, 61), (246, 240, 230), (24, 38, 70)
MER, TERRE, PB, TRAIT = (186, 220, 238), (222, 219, 211), (250, 243, 226), (214, 200, 176)
def font(s, w=700):
    f = ImageFont.truetype(CINZEL, s); f.set_variation_by_axes([w]); return f
def charge(n): return json.load(open(ICI / n, encoding='utf-8'))['features']

def creer(sortie, commune, reponse=False):
    r = next(r for r in csv.DictReader(open(ICI / 'communes_grille.csv', encoding='utf-8')) if r['nom'] == commune)
    assert r['fiable'] == 'oui', 'commune trop près d’une ligne : à éviter'
    img = Image.new('RGB', (W, H), CREME); d = ImageDraw.Draw(img)
    # bandeau
    d.rectangle([0, 0, W, 112], fill=ROUGE)
    d.text((70, 56), 'CAP SUR - LE PAYS BASQUE', font=ImageFont.truetype(INTER, 36), fill='white', anchor='lm')
    rgba = img.convert('RGBA')
    for x in (W - 150, W - 92):
        symboles.lauburu(rgba, x, 56, 22, (255, 255, 255))
    img = rgba.convert('RGB'); d = ImageDraw.Draw(img)
    d.rectangle([0, 112, W, 122], fill=VERT)
    d.text((W / 2, 172), 'LE JEU DE LA CARTE', font=font(52, 800), fill=NAVY, anchor='mm')
    # carte
    LAB = 34; mx0, my0 = 48, 214; mw = W - 2 * mx0 - LAB
    S = mw / (XMAX - XMIN); mh = (YMAX - YMIN) * S
    ox, oy = mx0 + LAB, my0 + LAB
    def P(x, y): return (ox + (x - XMIN) * S, oy + (YMAX - y) * S)
    SS = 3; LW, LH = round(mw), round(mh)
    lay = Image.new('RGB', (LW * SS, LH * SS), MER); dl = ImageDraw.Draw(lay)
    def Q(x, y): px, py = P(x, y); return ((px - ox) * SS, (py - oy) * SS)
    def poly(geom, **k):
        for p in geo.anneaux(geom):
            dl.polygon([Q(*geo.l93(*q)) for q in p[0]], **k)
    for f in charge('terres.geojson'): poly(f['geometry'], fill=TERRE)
    # côte française : redessinée ensuite à partir des communes exactes (la côte Natural Earth est grossière)
    dl.polygon([Q(*geo.l93(lo, la)) for lo, la in ((-1.80, 43.375), (-1.80, 44.0), (-0.4, 44.0), (-0.4, 43.375))], fill=MER)
    for f in charge('voisins.geojson'): poly(f['geometry'], fill=TERRE, outline=TERRE)
    for f in charge('communes.geojson'): poly(f['geometry'], fill=PB, outline=TRAIT)
    for f in charge('contour.geojson'):
        for p in geo.anneaux(f['geometry']):
            pts = [Q(*geo.l93(*q)) for q in p[0]]; dl.line(pts + pts[:1], fill=NAVY, width=2 * SS, joint='curve')
    for i in range(NC + 1):
        dl.line([Q(XMIN + i * CW, YMAX), Q(XMIN + i * CW, YMIN)], fill=(70, 95, 150), width=SS)
    for j in range(NL + 1):
        dl.line([Q(XMIN, YMAX - j * CH), Q(XMAX, YMAX - j * CH)], fill=(70, 95, 150), width=SS)
    lay = lay.resize((LW, LH), Image.LANCZOS); img.paste(lay, (round(ox), round(oy)))
    d = ImageDraw.Draw(img)
    gris = (120, 116, 106)
    for txt, lo, la in (('OCÉAN', -1.72, 43.50), ('ATLANTIQUE', -1.72, 43.47), ('ESPAGNE', -1.62, 43.03), ('BÉARN', -0.80, 43.43), ('LANDES', -1.02, 43.535)):
        d.text(P(*geo.l93(lo, la)), txt, font=font(17, 700), fill=(90, 120, 150) if txt in ('OCÉAN', 'ATLANTIQUE') else gris, anchor='mm')
    for i in range(NC):
        d.text((P(XMIN + (i + .5) * CW, 0)[0], my0 + LAB / 2), 'ABCDEFGHIJ'[i], font=font(24, 800), fill=NAVY, anchor='mm')
    for j in range(NL):
        d.text((mx0 + LAB / 2, P(0, YMAX - (j + .5) * CH)[1]), str(j + 1), font=font(22, 800), fill=NAVY, anchor='mm')
    # cadre question
    by0 = round(oy + mh) + 26; by1 = H - 92
    d.rounded_rectangle([60, by0, W - 60, by1], radius=22, fill='white', outline=ROUGE, width=4)
    cy = (by0 + by1) / 2
    def fit(t, size, w8, maxw=900):
        while font(size, w8).getlength(t) > maxw: size -= 2
        return font(size, w8)
    if not reponse:
        t = f'OÙ SE TROUVE {commune.upper()} ?'
        d.text((W / 2, cy - 30), t, font=fit(t, 52, 800), fill=NAVY, anchor='mm')
        t2 = 'Répondez en commentaire : lettre + chiffre'
        d.text((W / 2, cy + 34), t2, font=fit(t2, 30, 700), fill=(90, 70, 50), anchor='mm')
    else:
        x, y = P(float(r['x_l93']), float(r['y_l93']))
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=ROUGE, outline='white', width=3)
        gauche = x > ox + mw * 0.7
        d.text((x - 14 if gauche else x + 14, y - 2), commune, font=font(20, 800), fill=(150, 20, 20),
               anchor='rm' if gauche else 'lm', stroke_width=3, stroke_fill='white')
        d.text((W / 2, cy - 28), f'RÉPONSE : {r["case"]}', font=font(60, 800), fill=NAVY, anchor='mm')
        t = f'{commune} · Pays basque'
        d.text((W / 2, cy + 36), t, font=fit(t, 32, 700), fill=(90, 70, 50), anchor='mm')
    symboles.linge_basque(d, 0, H - 64, W, H, ROUGE, VERT, CREME)
    img.save(sortie, optimize=True)
    return r['case']

if __name__ == '__main__':
    print(creer(sys.argv[1], sys.argv[2], '--reponse' in sys.argv))
