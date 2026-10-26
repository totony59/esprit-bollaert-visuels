"""Génère les visuels des posts Facebook « Esprit Bollaert Design ».

Usage :
  python3 gen.py match    out.png "LILLE" "LENS" "VENDREDI 30 OCT." "21H05" "DERBY DU NORD"
  python3 gen.py prono    out.png "LILLE" "LENS" "VENDREDI 21H05"
  python3 gen.py homme    out.png "LENS 2 - 1 PARIS FC"
  python3 gen.py question out.png "VOTRE PLUS BEAU" "SOUVENIR À BOLLAERT ?"
  python3 gen.py design   out.png "QUEL PROCHAIN" "DESIGN ?"
"""
import sys, html, pathlib, base64, unicodedata
from playwright.sync_api import sync_playwright

BRAND = "ESPRIT BOLLAERT DESIGN"
FONDS = pathlib.Path(__file__).resolve().parent / "fonds"


# Couleurs des clubs : (fond de la carte, texte, bordure)
CLUBS = {
    "lens": ("#c8102e", "#ffd400", "#ffd400"),
    "lille": ("#d6001c", "#ffffff", "#1b2a5a"),
    "paris fc": ("#13294b", "#ffffff", "#7fb2e5"),
    "psg": ("#004170", "#ffffff", "#da291c"),
    "paris sg": ("#004170", "#ffffff", "#da291c"),
    "paris saint-germain": ("#004170", "#ffffff", "#da291c"),
    "marseille": ("#2faee0", "#ffffff", "#ffffff"),
    "om": ("#2faee0", "#ffffff", "#ffffff"),
    "lyon": ("#ffffff", "#1b3c87", "#da291c"),
    "ol": ("#ffffff", "#1b3c87", "#da291c"),
    "monaco": ("#e2001a", "#ffffff", "#ffffff"),
    "nice": ("#d4021d", "#000000", "#000000"),
    "rennes": ("#e2001a", "#000000", "#000000"),
    "brest": ("#e30613", "#ffffff", "#ffffff"),
    "nantes": ("#fcd405", "#00843d", "#00843d"),
    "strasbourg": ("#009fe3", "#ffffff", "#ffffff"),
    "toulouse": ("#4f2d84", "#ffffff", "#ffffff"),
    "auxerre": ("#ffffff", "#0d3b85", "#0d3b85"),
    "angers": ("#000000", "#ffffff", "#ffffff"),
    "le havre": ("#8ecae6", "#0b1f3a", "#0b1f3a"),
    "lorient": ("#f58220", "#000000", "#000000"),
    "metz": ("#7a1630", "#ffffff", "#ffffff"),
    "troyes": ("#005ba9", "#ffffff", "#ffffff"),
    "saint-etienne": ("#00843d", "#ffffff", "#ffffff"),
    "st etienne": ("#00843d", "#ffffff", "#ffffff"),
    "bordeaux": ("#0b1f3a", "#ffffff", "#ffffff"),
    "montpellier": ("#f58220", "#1b2a5a", "#1b2a5a"),
    "reims": ("#e30613", "#ffffff", "#ffffff"),
    "sporting": ("#00805a", "#ffffff", "#ffffff"),
    "bruges": ("#0052a5", "#000000", "#000000"),
    "club bruges": ("#0052a5", "#000000", "#000000"),
}
DEFAUT = ("#0a0405", "#ffffff", "#ffc400")


def club_style(name):
    key = unicodedata.normalize("NFD", name.lower())
    key = "".join(c for c in key if unicodedata.category(c) != "Mn").strip()
    bg, fg, bd = CLUBS.get(key, DEFAUT)
    return f'style="background:{bg};color:{fg};border-color:{bd}"'


def team(name):
    return f'<div class="team" {club_style(name)}>{html.escape(name)}</div>'


def fond_url(name):
    """Image de fond (fonds/<name>.png|jpg) en data URL, ou None si absente."""
    for ext, mime in (("png", "png"), ("jpg", "jpeg"), ("jpeg", "jpeg"), ("webp", "webp")):
        f = FONDS / f"{name}.{ext}"
        if f.exists():
            return f"data:image/{mime};base64," + base64.b64encode(f.read_bytes()).decode()
    return None


def verdict_fond(verdict):
    v = unicodedata.normalize("NFD", verdict.upper())
    v = "".join(c for c in v if unicodedata.category(c) != "Mn")
    if "VICTOIRE" in v or "GAGN" in v:
        return "victoire"
    if "NUL" in v:
        return "nul"
    if "DEFAITE" in v or "PERDU" in v:
        return "defaite"
    return "match"

CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1080px;overflow:hidden;background:#0a0405}
body{font-family:'Inter Display','Inter',sans-serif;color:#fff;position:relative}
.bg{position:absolute;inset:0;
 background:
  radial-gradient(ellipse 70% 55% at 50% 108%, rgba(255,120,0,.85), rgba(200,16,46,.55) 40%, transparent 70%),
  radial-gradient(circle at 12% 20%, rgba(200,16,46,.55), transparent 38%),
  radial-gradient(circle at 92% 12%, rgba(255,196,0,.35), transparent 34%),
  linear-gradient(160deg,#1a0508 0%,#0a0405 55%,#250608 100%);}
.smoke{position:absolute;border-radius:50%;filter:blur(60px);mix-blend-mode:screen}
.s1{width:620px;height:620px;left:-180px;top:380px;background:rgba(220,20,40,.55)}
.s2{width:560px;height:560px;right:-160px;top:420px;background:rgba(255,190,0,.42)}
.s3{width:420px;height:420px;left:330px;top:-180px;background:rgba(200,16,46,.35)}
.rays{position:absolute;inset:-200px;
 background:repeating-conic-gradient(from 0deg at 50% 70%, rgba(255,210,0,.07) 0 6deg, transparent 6deg 14deg);
 mask-image:radial-gradient(circle at 50% 70%, #000 0%, transparent 70%);
 -webkit-mask-image:radial-gradient(circle at 50% 70%, #000 0%, transparent 70%)}
.slash{position:absolute;left:-200px;width:1500px;transform:rotate(-12deg)}
.sl1{top:690px;height:34px;background:#c8102e;box-shadow:0 0 40px rgba(200,16,46,.9)}
.sl2{top:736px;height:16px;background:#ffc400;box-shadow:0 0 30px rgba(255,196,0,.9)}
.terrils{position:absolute;left:0;bottom:0;width:100%;height:330px}
.grain{position:absolute;inset:0;opacity:.22;mix-blend-mode:overlay}
.ghost{position:absolute;left:50%;top:50%;transform:translate(-50%,-56%) rotate(-8deg);
 font-weight:900;font-style:italic;font-size:430px;letter-spacing:-18px;white-space:nowrap;
 color:transparent;-webkit-text-stroke:3px rgba(255,196,0,.16);line-height:1}
.content.mid{justify-content:center;padding-top:0;padding-bottom:200px}
.content{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding-top:96px}
.kicker{font-weight:900;font-style:italic;font-size:46px;letter-spacing:6px;color:#fff;
 background:#c8102e;padding:8px 26px 10px;transform:skew(-10deg) rotate(-3deg);
 box-shadow:8px 8px 0 #ffc400}
.big{font-weight:900;font-style:italic;text-transform:uppercase;line-height:.86;text-align:center;
 letter-spacing:-1px;word-spacing:18px;transform:rotate(-4deg) scaleY(1.12);margin-top:34px}
.big .l1{display:block;font-size:128px;white-space:nowrap;color:#fff;text-shadow:0 6px 0 #c8102e, 0 0 40px rgba(255,80,0,.6)}
.big .l2{display:block;font-size:236px;padding-top:.16em;margin-top:-.16em;
 background:linear-gradient(180deg,#fff6b0 0%,#ffd400 38%,#ffb000 70%,#e07a00 100%);
 -webkit-background-clip:text;background-clip:text;color:transparent;
 filter:drop-shadow(0 8px 0 #c8102e) drop-shadow(0 0 30px rgba(255,170,0,.65))}
.versus{margin-top:56px;display:flex;align-items:center;gap:26px;transform:rotate(-4deg)}
.team{font-weight:900;font-style:italic;font-size:88px;letter-spacing:-2px;padding:6px 30px 12px;
 background:#0a0405;border:5px solid #ffc400;box-shadow:0 0 30px rgba(255,196,0,.45)}
.team.home{color:#fff}
.team.away{color:#fff;background:#c8102e;border-color:#fff}
.vs{font-weight:900;font-style:italic;font-size:70px;color:#ffc400;text-shadow:0 0 25px rgba(255,196,0,.8)}
.when{margin-top:40px;font-weight:900;font-style:italic;font-size:54px;letter-spacing:3px;transform:rotate(-4deg);
 color:#0a0405;background:#ffc400;padding:6px 28px 10px;box-shadow:8px 8px 0 #c8102e}
.when b{color:#c8102e}
.score{font-weight:900;font-style:italic;font-size:150px;line-height:1;color:#ffc400;text-shadow:0 8px 0 #c8102e,0 0 40px rgba(255,196,0,.8)}
.score i{color:#fff;margin:0 10px}
.q2p{font-size:140px!important}
.q1{font-size:100px!important}
.q2{font-size:136px!important}
.brand{position:absolute;bottom:34px;left:0;width:100%;text-align:center;font-weight:900;font-style:italic;
 font-size:30px;letter-spacing:10px;color:#fff;text-shadow:0 2px 12px #000}
.brand span{color:#ffc400}
.photo .bg{background-size:cover!important;background-position:center!important}
.photo .rays,.photo .smoke,.photo .ghost,.photo .slash,.photo .terrils{display:none}
.photo .grain{opacity:.12}
.shade{position:absolute;inset:0;display:none;
 background:
  linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,.15) 30%,rgba(0,0,0,.05) 55%,rgba(0,0,0,.35) 80%,rgba(0,0,0,.85) 100%),
  radial-gradient(ellipse 65% 45% at 50% 42%,rgba(0,0,0,.45),transparent 75%)}
.photo .shade{display:block}
.photo .content{padding-top:70px}
.photo .content.mid{padding-bottom:300px}
.cta{margin-top:64px;font-weight:800;font-style:italic;font-size:44px;transform:rotate(-4deg);
 color:#fff;border-bottom:6px solid #ffc400;padding-bottom:4px}
"""

TERRILS = """<svg class="terrils" viewBox="0 0 1080 330" preserveAspectRatio="none">
<defs><linearGradient id="t" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#140608"/><stop offset="1" stop-color="#050203"/></linearGradient></defs>
<path d="M0 330 L0 210 L170 70 L360 230 L470 160 L690 20 L900 180 L1000 120 L1080 175 L1080 330 Z" fill="url(#t)"/>
<path d="M170 70 L360 230 M690 20 L900 180" stroke="rgba(255,120,0,.25)" stroke-width="3"/>
<g fill="#050203"><rect x="790" y="40" width="10" height="150"/><rect x="850" y="40" width="10" height="150"/>
<path d="M780 40 L870 40 L825 0 Z"/><circle cx="825" cy="30" r="18" fill="none" stroke="#050203" stroke-width="8"/>
<path d="M795 60 L855 120 M855 60 L795 120" stroke="#050203" stroke-width="6"/></g>
</svg>"""

GRAIN = """<svg class="grain" width="1080" height="1080"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>"""


def page(ghost, inner, mid=False, fond=None):
    e = html.escape
    url = fond_url(fond) if fond else None
    body_cls = ' class="photo"' if url else ""
    bg_style = f' style="background:url({url})"' if url else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body{body_cls}>
<div class="bg"{bg_style}></div><div class="shade"></div><div class="rays"></div>
<div class="smoke s1"></div><div class="smoke s2"></div><div class="smoke s3"></div>
<div class="ghost">{e(ghost)}</div>
<div class="slash sl1"></div><div class="slash sl2"></div>
{TERRILS}{GRAIN}
<div class="content{' mid' if mid else ''}">{inner}</div>
<div class="brand"><span>///</span> {BRAND} <span>///</span></div>
</body></html>"""


def build(kind, a):
    e = html.escape
    if kind == "match":
        home, away, day, hour = a[0], a[1], a[2], a[3]
        kicker = a[4] if len(a) > 4 else "LIGUE 1"
        inner = f"""<div class="kicker">{e(kicker)}</div>
<div class="big"><span class="l1">C'est jour de</span><span class="l2">match</span></div>
<div class="versus">{team(home)}<div class="vs">VS</div>{team(away)}</div>
<div class="when">{e(day)} · <b>{e(hour)}</b></div>"""
        return page("ALLEZ", inner, fond="match")
    if kind == "resultat":
        verdict, home, sh, sa, away, info = a[0], a[1], a[2], a[3], a[4], a[5]
        inner = f"""<div class="kicker">{e(info)}</div>
<div class="big"><span class="l2 q2">{e(verdict)}</span></div>
<div class="versus">{team(home)}<div class="score">{e(sh)}<i>-</i>{e(sa)}</div>{team(away)}</div>
<div class="cta">Vos tops &amp; vos flops ? 👇</div>"""
        return page(verdict, inner, True, fond=verdict_fond(verdict))
    if kind == "prono":
        home, away, when = a[0], a[1], a[2]
        kicker = a[3] if len(a) > 3 else "J-1"
        inner = f"""<div class="kicker">{e(kicker)}</div>
<div class="big"><span class="l1">Votre</span><span class="l2 q2p">pronostic ?</span></div>
<div class="versus">{team(home)}<div class="vs">?-?</div>{team(away)}</div>
<div class="when">{e(when)}</div>"""
        return page("PRONO", inner, fond="prono")
    if kind == "homme":
        score = a[0]
        inner = f"""<div class="kicker">{e(score)}</div>
<div class="big"><span class="l1 q1">Votre homme</span><span class="l2 q2">du match ?</span></div>
<div class="cta">Dites-le en commentaire 👇</div>"""
        return page("MVP", inner, True)
    if kind == "question":
        inner = f"""<div class="kicker">LA QUESTION DU JOUR</div>
<div class="big"><span class="l1 q1">{e(a[0])}</span><span class="l2 q2">{e(a[1])}</span></div>
<div class="cta">Racontez-nous 👇</div>"""
        return page("62", inner, True, fond="question")
    if kind == "design":
        inner = f"""<div class="kicker">L'ATELIER</div>
<div class="big"><span class="l1 q1">{e(a[0])}</span><span class="l2 q2">{e(a[1])}</span></div>
<div class="cta">Votez en commentaire 👇</div>"""
        return page("DESIGN", inner, True, fond="design")
    raise SystemExit(f"type inconnu : {kind}")


def main():
    kind, out, *args = sys.argv[1:]
    doc = build(kind, args)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1080})
        pg.set_content(doc, wait_until="load")
        pg.wait_for_timeout(150)
        pg.screenshot(path=out, type="png")
        b.close()
    print(pathlib.Path(out).resolve())


if __name__ == "__main__":
    main()
