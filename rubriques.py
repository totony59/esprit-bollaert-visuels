"""Visuels des rubriques quotidiennes de la page Lens (1080x1080), dans le style de gen.py.

python3 rubriques.py jour     <out.png> "9 MAI 1998" "LENS CHAMPION" "DE FRANCE" "Vous y étiez ?"
python3 rubriques.py quiz     <out.png> "QUESTION" "réponse A" "réponse B" "réponse C"
python3 rubriques.py chiffre  <out.png> "1933" "L'année où Bollaert a ouvert ses portes" "Vous saviez ?"
python3 rubriques.py duel     <out.png> "SOUS-TITRE" "NOM 1" "NOM 2"            (❤️ pour 1, 👍 pour 2)
python3 rubriques.py mot      <out.png> "BRAIRE" "Pleurer" "Vous le dites encore ?"
python3 rubriques.py souvenir <out.png> "VOTRE PREMIER MATCH" "À BOLLAERT ?" "Racontez-nous"
python3 rubriques.py onze     <out.png> "LE GARDIEN" "NOM 1" "NOM 2" "NOM 3"    (❤️ / 👍 / 😮)
"""
import html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gen
from playwright.sync_api import sync_playwright

e = html.escape
NOMS = {"jour": "CE JOUR-LÀ AU RACING", "quiz": "LE QUIZ DU RACING", "chiffre": "LE CHIFFRE", "duel": "LE DUEL",
        "mot": "LE MOT CH'TI", "souvenir": "SOUVENIRS DE BOLLAERT", "onze": "LE ONZE DE LÉGENDE"}
CSS = """<style>
.rb{display:flex;flex-direction:column;align-items:center;text-align:center;width:100%}
.rt{font-weight:900;font-style:italic;letter-spacing:-1px;line-height:.95;color:#fff;text-shadow:0 6px 0 #c8102e,0 0 40px rgba(0,0,0,.7)}
.rt1{font-size:88px}.rt2{font-size:84px;color:#ffc400}
.rs{margin-top:26px;font-weight:800;font-style:italic;font-size:40px;color:#fff;text-shadow:0 2px 12px #000;max-width:900px}
.num{font-weight:900;font-style:italic;font-size:300px;line-height:.9;color:#ffc400;text-shadow:0 10px 0 #c8102e,0 0 60px rgba(255,150,0,.6)}
.opts{display:flex;flex-direction:column;gap:18px;margin-top:30px;width:880px}
.opt{display:flex;align-items:center;gap:24px;background:rgba(15,6,8,.88);border:4px solid #ffd400;border-radius:18px;padding:14px 26px;
 font-weight:900;font-style:italic;font-size:44px;text-align:left;box-shadow:0 10px 30px rgba(0,0,0,.5)}
.opt b{display:inline-flex;width:70px;height:70px;border-radius:14px;background:#c8102e;color:#ffd400;align-items:center;justify-content:center;font-size:46px}
.opt i{font-style:normal;font-size:60px;line-height:1}
.vsrow{display:flex;align-items:center;gap:26px;margin-top:34px}
.card{width:400px;height:330px;border-radius:24px;border:5px solid #ffd400;display:flex;flex-direction:column;align-items:center;justify-content:center;
 background:rgba(15,6,8,.9);box-shadow:0 12px 40px rgba(0,0,0,.6)}
.card i{font-style:normal;font-size:110px;line-height:1}.card span{margin-top:18px;font-weight:900;font-style:italic;font-size:54px;color:#fff;padding:0 14px}
.card.r{background:#c8102e}.card.r span{color:#ffd400}
.vsx{font-weight:900;font-style:italic;font-size:70px;color:#ffc400;text-shadow:0 0 25px rgba(255,196,0,.8)}
.cta2{margin-top:30px;font-weight:800;font-style:italic;font-size:38px;color:#fff;text-shadow:0 2px 12px #000}
</style>"""

def inner(kind, a):
    k = f'<div class="kicker">{e(NOMS[kind])}</div>'
    if kind == "jour":
        return k + f'<div class="kicker" style="margin-top:22px;background:#ffc400;color:#0a0405">{e(a[0])}</div><div class="rt rt1" style="margin-top:30px">{e(a[1])}</div><div class="rt rt2">{e(a[2])}</div><div class="rs">{e(a[3])} 👇</div>'
    if kind in ("mot", "souvenir"):
        sous = f'« {e(a[1])} »' if kind == "mot" else ""
        t = f'<div class="rt rt1" style="margin-top:40px">{e(a[0])}</div>'
        t += f'<div class="rs" style="font-size:54px;color:#ffc400">{sous}</div>' if kind == "mot" else f'<div class="rt rt2">{e(a[1])}</div>'
        return k + t + f'<div class="cta2">{e(a[2])} 👇</div>'
    if kind == "chiffre":
        return k + f'<div class="num" style="margin-top:30px">{e(a[0])}</div><div class="rs">{e(a[1])}</div><div class="cta2">{e(a[2])} 👇</div>'
    if kind == "quiz":
        opts = "".join(f'<div class="opt"><b>{l}</b>{e(t)}</div>' for l, t in zip("ABC", a[1:4]))
        return k + f'<div class="rs" style="font-size:50px;margin-top:30px">{e(a[0])}</div><div class="opts">{opts}</div><div class="cta2">Votre réponse : A, B ou C ? 👇</div>'
    if kind == "duel":
        return k + f'<div class="rs" style="margin-top:22px">{e(a[0])}</div><div class="vsrow"><div class="card r"><i>❤️</i><span>{e(a[1])}</span></div><div class="vsx">VS</div><div class="card"><i>👍</i><span>{e(a[2])}</span></div></div><div class="cta2">Votez avec une réaction 👇</div>'
    if kind == "onze":
        opts = "".join(f'<div class="opt"><i>{em}</i>{e(t)}</div>' for em, t in zip(("❤️", "👍", "😮"), a[1:4]))
        return k + f'<div class="rt rt1" style="font-size:80px;margin-top:24px">{e(a[0])}</div><div class="opts">{opts}</div><div class="cta2">Votez avec une réaction 👇</div>'
    raise SystemExit(f"rubrique inconnue : {kind}")

def main():
    kind, out, *a = sys.argv[1:]
    a = [x.replace(" ?", " ?").replace(" !", " !") for x in a]
    doc = gen.page(NOMS[kind].split()[-1], CSS + f'<div class="rb">{inner(kind, a)}</div>', True, fond="question")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1080})
        pg.set_content(doc, wait_until="load"); pg.wait_for_timeout(150); pg.screenshot(path=out); b.close()
    print(out)

if __name__ == "__main__":
    main()
