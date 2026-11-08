"""Visuel « LE FACE-À-FACE » : stats des confrontations entre Lens et un adversaire (1080x1080).
Usage : python3 stats_h2h.py <out.png> <stats.json>
stats.json : {"titre": "LENS – OM", "periode": "EN LIGUE 1 DEPUIS 2000", "matchs": 34,
  "lens": 14, "nuls": 7, "adv": 13, "adv_nom": "OM", "buts": "37 - 40",
  "tuiles": [["7 V. en 12", "depuis la remontée en 2020"], ...]   (4 tuiles max)
  "question": "..."}"""
import html, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gen
from playwright.sync_api import sync_playwright
e = html.escape
out, d = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
t = d["lens"] + d["nuls"] + d["adv"]
pct = lambda x: f"{100*x/t:.1f}%"
bg, fg, _ = gen.CLUBS.get(d.get("adv_cle", d["adv_nom"]).lower(), gen.DEFAUT)
tuiles = "".join(f'<div class="tu"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in d["tuiles"][:4])
inner = f"""<style>
.st{{display:flex;flex-direction:column;align-items:center;width:100%;text-align:center;padding-top:150px}}
.tt{{font-weight:900;font-style:italic;font-size:80px;line-height:.95;color:#fff;text-shadow:0 6px 0 #c8102e,0 0 40px rgba(0,0,0,.7);margin-top:18px}}
.pp{{font-weight:800;font-style:italic;font-size:32px;color:#ffc400;margin-top:8px;letter-spacing:2px}}
.bar{{display:flex;width:920px;height:104px;border-radius:18px;overflow:hidden;margin-top:22px;border:4px solid #ffd400;box-shadow:0 12px 40px rgba(0,0,0,.6)}}
.bar div{{display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:900;font-style:italic}}
.bar b{{font-size:54px;line-height:1}} .bar span{{font-size:22px;margin-top:4px}}
.lg{{display:flex;justify-content:space-between;width:920px;margin-top:10px;font-weight:800;font-size:26px;color:#fff;text-shadow:0 2px 8px #000}}
.tus{{display:grid;grid-template-columns:1fr 1fr;gap:14px;width:920px;margin-top:18px}}
.tu{{background:rgba(15,6,8,.88);border:3px solid rgba(255,212,0,.8);border-radius:16px;padding:14px 16px;display:flex;flex-direction:column}}
.tu b{{font-weight:900;font-style:italic;font-size:40px;color:#ffc400;line-height:1}} .tu span{{font-weight:700;font-size:23px;color:#fff;margin-top:6px}}
.q{{margin-top:18px;font-weight:800;font-style:italic;font-size:36px;color:#fff;text-shadow:0 2px 12px #000}}
</style><div class="st">
<div class="kicker">LE FACE-À-FACE</div>
<div class="tt">{e(d["titre"])}</div><div class="pp">{e(d["periode"])} · {d["matchs"]} MATCHS</div>
<div class="bar"><div style="width:{pct(d['lens'])};background:#c8102e;color:#ffd400"><b>{d['lens']}</b><span>LENS</span></div>
<div style="width:{pct(d['nuls'])};background:#f2f2f2;color:#0a0405"><b>{d['nuls']}</b><span>NULS</span></div>
<div style="width:{pct(d['adv'])};background:{bg};color:{fg}"><b>{d['adv']}</b><span>{e(d['adv_nom'])}</span></div></div>
<div class="lg"><span>Buts : {e(d['buts'])}</span><span>Victoires · nuls · défaites</span></div>
<div class="tus">{tuiles}</div>
<div class="q">{e(d['question']).replace(' ?', '&nbsp;?')} 👇</div></div>"""
doc = gen.page("STATS", inner, True, fond="match")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1080})
    pg.set_content(doc, wait_until="load"); pg.wait_for_timeout(150); pg.screenshot(path=out); b.close()
print(out)
