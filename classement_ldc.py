"""Visuel « CLASSEMENT » de la phase de ligue de Ligue des champions (36 clubs, 1080x1080).

Usage : python3 classement_ldc.py <sortie.png> <classement.json> [precedent.json] [fond]
Même format JSON que classement.py ; fond par défaut : match (teinté bleu nuit).
"""
import sys, html, json, unicodedata, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gen
from playwright.sync_api import sync_playwright
def norm(x): return "".join(c for c in unicodedata.normalize("NFD", x.lower()) if unicodedata.category(c) != "Mn").strip()
FR = {"lens","paris sg","psg","paris saint-germain","lille","marseille","monaco","lyon","nice","rennes","brest","strasbourg","paris fc"}
out, cur = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
prev=None; fond_name="match"
for a in sys.argv[3:]:
    if a.endswith(".json"):
        if pathlib.Path(a).exists(): prev=json.load(open(a,encoding="utf-8"))
    else: fond_name=a
pr={norm(c["club"]):i for i,c in enumerate(prev["clubs"],1)} if prev else {}
def zone(r): return "q8" if r<=8 else ("bar" if r<=24 else "out")
rows=[]
for i,c in enumerate(cur["clubs"],1):
    k=norm(c["club"]); ev=pr[k]-i if k in pr else 0
    arrow=f'<span class="ev up">▲{ev}</span>' if ev>0 else (f'<span class="ev dn">▼{-ev}</span>' if ev<0 else '<span class="ev eq">=</span>')
    d=c["diff"]; ds=f"+{d}" if d>0 else str(d)
    cls=zone(i)+(" lens" if k=="lens" else "")+(" fr" if k in FR and k!="lens" else "")
    rows.append(f'<div class="row {cls}"><span class="z"></span><span class="rk">{i}</span><span class="nm">{html.escape(c["club"].upper())}</span>{arrow}<span class="df">{ds}</span><span class="pt">{c["pts"]}</span></div>')
J=cur["journee"]
fond=gen.fond_url(fond_name)
doc=f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1080px;overflow:hidden;background:#05081a;font-family:'Inter Display','Inter',sans-serif;color:#fff}}
.bg{{position:absolute;inset:0;background:url({fond}) center/cover;filter:hue-rotate(195deg) saturate(.8) brightness(.8)}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,8,26,.45),rgba(5,8,26,.82) 26%,rgba(5,8,26,.9))}}
.stars{{position:absolute;inset:0;background-image:radial-gradient(2px 2px at 8% 12%,#fff,transparent),radial-gradient(2px 2px at 22% 6%,#cfe0ff,transparent),radial-gradient(1.5px 1.5px at 40% 14%,#fff,transparent),radial-gradient(2px 2px at 63% 7%,#fff,transparent),radial-gradient(1.5px 1.5px at 80% 15%,#cfe0ff,transparent),radial-gradient(2px 2px at 93% 5%,#fff,transparent);opacity:.9}}
.top{{position:absolute;top:30px;width:100%;text-align:center}}
.nuit{{font-weight:800;font-style:italic;font-size:22px;letter-spacing:12px;color:#c9d6f2;text-shadow:0 0 14px rgba(140,180,255,.9)}}
.t1{{margin-top:6px;font-weight:900;font-style:italic;font-size:96px;line-height:.9;letter-spacing:-2px;text-shadow:0 6px 0 #1d3fbf,0 0 40px rgba(90,140,255,.7)}}
.t2{{display:inline-block;margin-top:12px;font-weight:900;font-style:italic;font-size:28px;letter-spacing:5px;background:#ffc400;color:#05081a;padding:5px 20px;transform:rotate(-2deg)}}
.cols{{position:absolute;top:236px;left:30px;right:30px;display:flex;gap:20px}}
.col{{flex:1;display:flex;flex-direction:column;gap:4px}}
.row{{position:relative;height:36px;display:flex;align-items:center;background:rgba(10,16,48,.82);border:1px solid rgba(160,190,255,.16);border-radius:7px;padding:0 8px 0 16px}}
.z{{position:absolute;left:0;top:0;bottom:0;width:6px;border-radius:7px 0 0 7px}}
.q8 .z{{background:#1fc16b}} .bar .z{{background:#3d8bff}} .out .z{{background:#ff3b3b}}
.rk{{width:34px;font-weight:900;font-style:italic;font-size:20px;text-align:center}}
.nm{{flex:1;font-weight:800;font-style:italic;font-size:18.5px;white-space:nowrap;margin-left:6px}}
.ev{{width:36px;font-weight:800;font-size:13px;text-align:center}} .up{{color:#38e07b}} .dn{{color:#ff5a5a}} .eq{{color:#8a93a8}}
.df{{width:40px;font-weight:700;font-size:15px;color:#c7d0e6;text-align:right;margin-right:9px}}
.pt{{width:40px;height:28px;border-radius:6px;background:#fff;color:#05081a;font-weight:900;font-size:19px;display:flex;align-items:center;justify-content:center}}
.fr .nm::after{{content:"";display:inline-block;width:18px;height:11px;margin-left:8px;vertical-align:1px;background:linear-gradient(90deg,#1d3fbf 33%,#fff 33% 66%,#e1001a 66%);border-radius:2px}}
.lens{{background:linear-gradient(90deg,#c8102e,#8e0b20);border:2px solid #ffd400;box-shadow:0 0 24px rgba(255,212,0,.7);transform:scale(1.03);z-index:2}}
.lens .nm,.lens .rk{{color:#ffd400}} .lens .pt{{background:#ffd400}} .lens .df{{color:#fff}}
.leg{{position:absolute;bottom:76px;width:100%;display:flex;justify-content:center;gap:26px;font-weight:700;font-size:16px;color:#e8ecf8}}
.leg i{{display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:7px;vertical-align:-1px}}
.brand{{position:absolute;bottom:30px;width:100%;text-align:center;font-weight:900;font-style:italic;font-size:26px;letter-spacing:10px;text-shadow:0 2px 12px #000}}
.brand span{{color:#c8102e}}
</style></head><body><div class="bg"></div><div class="sh"></div><div class="stars"></div>
<div class="top"><div class="nuit">★ NUIT EUROPÉENNE ★</div><div class="t1">CLASSEMENT</div><div class="t2">LIGUE DES CHAMPIONS · {J}{'RE' if J==1 else 'E'} JOURNÉE</div></div>
<div class="cols"><div class="col">{''.join(rows[:18])}</div><div class="col">{''.join(rows[18:])}</div></div>
<div class="leg"><span><i style="background:#1fc16b"></i>Qualifiés 8es (1 à 8)</span><span><i style="background:#3d8bff"></i>Barrages (9 à 24)</span><span><i style="background:#ff3b3b"></i>Éliminés (25 à 36)</span></div>
<div class="brand"><span>///</span> ESPRIT BOLLAERT DESIGN <span>///</span></div>
</body></html>"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1080})
    pg.set_content(doc,wait_until="load"); pg.wait_for_timeout(200); pg.screenshot(path=out); b.close()
