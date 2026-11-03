"""Visuel « RÉSULTATS » d'une journée de Ligue 1 (1080x1080).
Usage : python3 resultats.py <sortie.png> <resultats.json> [fond]
resultats.json : {"journee": 9, "matchs": [{"dom": "Nice", "sd": 5, "se": 2, "ext": "Rennes"}, ...]}"""
import sys, html, json, unicodedata, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gen
from playwright.sync_api import sync_playwright
def norm(x): return "".join(c for c in unicodedata.normalize("NFD", x.lower()) if unicodedata.category(c) != "Mn").strip()
CODES = {"psg":"PSG","lille":"LOSC","lyon":"OL","paris fc":"PFC","rennes":"SRFC","marseille":"OM","monaco":"ASM","nice":"OGCN",
 "lens":"RCL","brest":"SB29","lorient":"FCL","toulouse":"TFC","strasbourg":"RCSA","auxerre":"AJA","angers":"SCO","troyes":"ESTAC",
 "le mans":"LMFC","le havre":"HAC","nantes":"FCN","metz":"FCM","saint-etienne":"ASSE"}
EXTRA = {"le mans": ("#d50f25","#ffd400","#ffd400"), "lens": ("#ffd400","#c8102e","#ffffff")}
out, data = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
fond_name = sys.argv[3] if len(sys.argv) > 3 else "match"
def badge(n):
    k=norm(n); bg,fg,bd = EXTRA.get(k) or gen.CLUBS.get(k, gen.DEFAUT)
    return f'<span class="bd" style="background:{bg};color:{fg};border-color:{bd}">{CODES.get(k, n[:4].upper())}</span>'
rows=[]
for m in data["matchs"]:
    sd,se=m["sd"],m["se"]
    cd="win" if sd>se else ("lose" if sd<se else "draw"); ce="win" if se>sd else ("lose" if se<sd else "draw")
    lens=" lens" if "lens" in (norm(m["dom"]),norm(m["ext"])) else ""
    rows.append(f'''<div class="row{lens}"><div class="side l {cd}"><span class="nm">{html.escape(m["dom"].upper())}</span>{badge(m["dom"])}</div>
<div class="sc"><span class="{cd}">{sd}</span><i>-</i><span class="{ce}">{se}</span></div>
<div class="side r {ce}">{badge(m["ext"])}<span class="nm">{html.escape(m["ext"].upper())}</span></div></div>''')
J=data["journee"]; fond=gen.fond_url(fond_name)
doc=f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1080px;overflow:hidden;background:#0a0405;font-family:'Inter Display','Inter',sans-serif;color:#fff}}
.bg{{position:absolute;inset:0;background:url({fond}) center/cover}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,4,5,.55),rgba(10,4,5,.78) 30%,rgba(10,4,5,.85))}}
.top{{position:absolute;top:44px;width:100%;text-align:center}}
.t1{{font-weight:900;font-style:italic;font-size:118px;line-height:.9;letter-spacing:-2px;text-shadow:0 6px 0 #c8102e,0 0 40px rgba(255,80,0,.6)}}
.t2{{display:inline-block;margin-top:18px;font-weight:900;font-style:italic;font-size:34px;letter-spacing:6px;background:#ffc400;color:#0a0405;padding:6px 22px;transform:rotate(-2deg)}}
.list{{position:absolute;top:268px;left:60px;right:60px;display:flex;flex-direction:column;gap:12px}}
.row{{height:63px;display:flex;align-items:center;background:rgba(20,8,10,.84);border:2px solid rgba(255,255,255,.12);border-radius:12px;padding:0 16px}}
.side{{flex:1;display:flex;align-items:center;gap:14px}} .side.l{{justify-content:flex-end}}
.nm{{font-weight:900;font-style:italic;font-size:27px;white-space:nowrap}}
.bd{{width:76px;height:42px;border:2px solid;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:17px}}
.lose .nm{{opacity:.55}}
.sc{{width:150px;margin:0 18px;height:48px;border-radius:9px;background:#fff;color:#0a0405;display:flex;align-items:center;justify-content:center;gap:10px;font-weight:900;font-size:32px}}
.sc i{{font-style:normal;color:#888}} .sc .lose{{color:#8a8a8a}}
.lens{{background:linear-gradient(90deg,#8e0b20,#c8102e,#8e0b20);border:3px solid #ffd400;box-shadow:0 0 30px rgba(255,212,0,.65);transform:scale(1.03)}}
.lens .sc{{background:#ffd400}}
.brand{{position:absolute;bottom:34px;width:100%;text-align:center;font-weight:900;font-style:italic;font-size:28px;letter-spacing:10px;text-shadow:0 2px 12px #000}}
.brand span{{color:#c8102e}}
</style></head><body><div class="bg"></div><div class="sh"></div>
<div class="top"><div class="t1">RÉSULTATS</div><div class="t2">LIGUE 1 · {J}{'RE' if J==1 else 'E'} JOURNÉE</div></div>
<div class="list">{''.join(rows)}</div>
<div class="brand"><span>///</span> ESPRIT BOLLAERT DESIGN <span>///</span></div></body></html>"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1080})
    pg.set_content(doc,wait_until="load"); pg.wait_for_timeout(200); pg.screenshot(path=out); b.close()
