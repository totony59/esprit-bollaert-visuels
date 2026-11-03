"""Visuel « CLASSEMENT » de Ligue 1 (1080x1080).

Usage : python3 classement.py <sortie.png> <classement.json> [precedent.json] [fond]
classement.json : {"journee": 10, "clubs": [{"club": "PSG", "pts": 20, "diff": 11}, ...]}  (18 clubs, dans l'ordre du classement)
precedent.json  : même format (classement de la journée précédente) -> flèches ▲▼ ; absent = « = » partout.
fond            : nom d'un fond de fonds/ (match, victoire, nul, defaite...). Défaut : match.
"""
import sys, html, json, unicodedata, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gen
from playwright.sync_api import sync_playwright

CODES = {"psg":"PSG","paris saint-germain":"PSG","lille":"LOSC","lyon":"OL","paris fc":"PFC","rennes":"SRFC",
 "marseille":"OM","monaco":"ASM","nice":"OGCN","lens":"RCL","brest":"SB29","lorient":"FCL","toulouse":"TFC",
 "strasbourg":"RCSA","auxerre":"AJA","angers":"SCO","troyes":"ESTAC","le mans":"LMFC","le havre":"HAC",
 "nantes":"FCN","metz":"FCM","saint-etienne":"ASSE","montpellier":"MHSC","reims":"SDR","bordeaux":"FCGB"}
EXTRA = {"le mans": ("#d50f25","#ffd400","#ffd400"), "lens": ("#ffd400","#c8102e","#ffffff")}
def norm(x):
    return "".join(c for c in unicodedata.normalize("NFD", x.lower()) if unicodedata.category(c) != "Mn").strip()

out, cur = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
prev = None
fond_name = "match"
for a in sys.argv[3:]:
    if a.endswith(".json"):
        if pathlib.Path(a).exists(): prev = json.load(open(a, encoding="utf-8"))
    else: fond_name = a
prev_rank = {norm(c["club"]): i for i, c in enumerate(prev["clubs"], 1)} if prev else {}
DATA = []
for i, c in enumerate(cur["clubs"], 1):
    k = norm(c["club"])
    ev = prev_rank[k] - i if k in prev_rank else 0
    DATA.append((c["club"].upper(), CODES.get(k, c["club"][:4].upper()), c["pts"], c["diff"], ev))
JOURNEE = cur["journee"]
def zone(r):
    return {1:"ldc",2:"ldc",3:"ldc",4:"ldcq",5:"el",6:"ecl",16:"barr",17:"rel",18:"rel"}.get(r,"")
def style(name):
    k=norm(name); bg,fg,bd = EXTRA.get(k) or gen.CLUBS.get(k, gen.DEFAUT)
    return bg,fg,bd
rows=[]
for i,(n,c,p,d,ev) in enumerate(DATA,1):
    bg,fg,bd=style(n)
    arrow = f'<span class="ev up">▲{ev}</span>' if ev>0 else (f'<span class="ev dn">▼{-ev}</span>' if ev<0 else '<span class="ev eq">=</span>')
    ds = f"+{d}" if d>0 else str(d)
    rows.append(f'''<div class="row {zone(i)} {'lens' if norm(n)=='lens' else ''}"><span class="z"></span><span class="rk">{i}</span>
<span class="bd" style="background:{bg};color:{fg};border-color:{bd}">{c}</span><span class="nm">{html.escape(n)}</span>
{arrow}<span class="df">{ds}</span><span class="pt">{p}</span></div>''')
col1="".join(rows[:9]); col2="".join(rows[9:])
fond=gen.fond_url(fond_name)
doc=f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1080px;overflow:hidden;background:#0a0405;font-family:'Inter Display','Inter',sans-serif;color:#fff}}
.bg{{position:absolute;inset:0;background:url({fond}) center/cover}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,4,5,.55),rgba(10,4,5,.78) 30%,rgba(10,4,5,.85))}}
.top{{position:absolute;top:44px;width:100%;text-align:center}}
.t1{{font-weight:900;font-style:italic;font-size:118px;line-height:.9;letter-spacing:-2px;color:#fff;text-shadow:0 6px 0 #c8102e,0 0 40px rgba(255,80,0,.6)}}
.t2{{display:inline-block;margin-top:18px;font-weight:900;font-style:italic;font-size:34px;letter-spacing:6px;background:#ffc400;color:#0a0405;padding:6px 22px;transform:rotate(-2deg)}}
.cols{{position:absolute;top:262px;left:34px;right:34px;display:flex;gap:22px}}
.col{{flex:1;display:flex;flex-direction:column;gap:9px}}
.row{{position:relative;height:64px;display:flex;align-items:center;background:rgba(20,8,10,.82);border:2px solid rgba(255,255,255,.12);border-radius:10px;padding:0 14px 0 20px;overflow:hidden}}
.z{{position:absolute;left:0;top:0;bottom:0;width:8px}}
.ldc .z{{background:#2d6cff}} .ldcq .z{{background:#7fb2ff}} .el .z{{background:#ff8a00}} .ecl .z{{background:#1fc16b}}
.barr .z{{background:#ffcf33}} .rel .z{{background:#ff2a2a}}
.rk{{width:40px;font-weight:900;font-style:italic;font-size:32px;text-align:center}}
.bd{{width:76px;height:44px;margin:0 12px 0 6px;border:2px solid;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:18px;letter-spacing:.5px}}
.nm{{flex:1;font-weight:900;font-style:italic;font-size:24px;letter-spacing:-.3px;white-space:nowrap}}
.ev{{width:44px;font-weight:800;font-size:17px;text-align:center}} .up{{color:#38e07b}} .dn{{color:#ff4d4d}} .eq{{color:#9a9a9a}}
.df{{width:52px;font-weight:700;font-size:20px;color:#cfcfcf;text-align:right;margin-right:12px}}
.pt{{width:58px;height:46px;border-radius:8px;background:#fff;color:#0a0405;font-weight:900;font-size:30px;display:flex;align-items:center;justify-content:center}}
.lens{{background:linear-gradient(90deg,#c8102e,#8e0b20);border:3px solid #ffd400;box-shadow:0 0 30px rgba(255,212,0,.65);transform:scale(1.04)}}
.lens .nm,.lens .rk{{color:#ffd400}} .lens .pt{{background:#ffd400}} .lens .df{{color:#fff}}
.leg{{position:absolute;bottom:84px;width:100%;display:flex;justify-content:center;gap:22px;font-weight:700;font-size:17px;color:#e8e8e8}}
.leg i{{display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:7px;vertical-align:-1px}}
.brand{{position:absolute;bottom:34px;width:100%;text-align:center;font-weight:900;font-style:italic;font-size:28px;letter-spacing:10px;text-shadow:0 2px 12px #000}}
.brand span{{color:#c8102e}}
</style></head><body><div class="bg"></div><div class="sh"></div>
<div class="top"><div class="t1">CLASSEMENT</div><div class="t2">LIGUE 1 · {JOURNEE}{'RE' if JOURNEE==1 else 'E'} JOURNÉE</div></div>
<div class="cols"><div class="col">{col1}</div><div class="col">{col2}</div></div>
<div class="leg"><span><i style="background:#2d6cff"></i>Ligue des champions</span><span><i style="background:#7fb2ff"></i>Barrage LDC</span><span><i style="background:#ff8a00"></i>Ligue Europa</span><span><i style="background:#1fc16b"></i>Conférence</span><span><i style="background:#ffcf33"></i>Barrage</span><span><i style="background:#ff2a2a"></i>Relégation</span></div>
<div class="brand"><span>///</span> ESPRIT BOLLAERT DESIGN <span>///</span></div>
</body></html>"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1080})
    pg.set_content(doc,wait_until="load"); pg.wait_for_timeout(200); pg.screenshot(path=out); b.close()
