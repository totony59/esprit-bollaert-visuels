"""Génère les visuels des posts Facebook « Esprit Bollaert Design ».

Usage :
  python3 gen.py match    out.png "LILLE" "LENS" "VENDREDI 30 OCT." "21H05" "DERBY DU NORD"
  python3 gen.py prono    out.png "LILLE" "LENS" "VENDREDI 21H05"
  python3 gen.py homme    out.png "LENS 2 - 1 PARIS FC"
  python3 gen.py question out.png "VOTRE PLUS BEAU" "SOUVENIR À BOLLAERT ?"
  python3 gen.py design   out.png "QUEL PROCHAIN" "DESIGN ?"

Ligue des champions : ajouter --ldc (thème « nuit européenne » bleu nuit / argent / étoiles,
sans logo ni ballon étoilé officiels de l'UEFA) :
  python3 gen.py match    out.png "LENS" "CÔME" "MER. 4 NOV." "21H" --ldc
  python3 gen.py prono    out.png "LENS" "CÔME" "MERCREDI 21H" --ldc
  python3 gen.py resultat out.png "VICTOIRE" "LENS" "2" "1" "CÔME" "LIGUE DES CHAMPIONS" --ldc
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
    "come": ("#1d3f8f", "#ffffff", "#7fb2e5"),
    "leipzig": ("#ffffff", "#dd0741", "#dd0741"),
    "rb leipzig": ("#ffffff", "#dd0741", "#dd0741"),
    "bodø/glimt": ("#ffd200", "#000000", "#000000"),
    "bodø": ("#ffd200", "#000000", "#000000"),
    "bodo/glimt": ("#ffd200", "#000000", "#000000"),
    "bodo": ("#ffd200", "#000000", "#000000"),
    "man city": ("#6cabdd", "#ffffff", "#1c2c5b"),
    "manchester city": ("#6cabdd", "#ffffff", "#1c2c5b"),
    "liverpool": ("#c8102e", "#ffffff", "#f6eb61"),
    "slavia prague": ("#ffffff", "#e30613", "#e30613"),
    "slavia": ("#ffffff", "#e30613", "#e30613"),
    "como": ("#1d3f8f", "#ffffff", "#7fb2e5"),
}
DEFAUT = ("#0a0405", "#ffffff", "#ffc400")

# Adversaires de Ligue des champions 2026-2027 : le thème « nuit européenne » s'active tout seul.
# Phase de ligue (sources : Nordsports Mag + SeatPick, vérifié le 01/11/2026) : Slavia Prague (ext.),
# Sporting (dom.), Club Bruges (ext.), Côme (dom. 04/11), RB Leipzig (ext. 24/11), Bodø/Glimt (dom. 09/12),
# Manchester City (dom. 20/01/2027), Liverpool (ext. 27/01/2027). Ajouter ici les adversaires des barrages / phases finales.
LDC_ADVERSAIRES = {"come", "como", "leipzig", "rb leipzig", "bodø/glimt", "bodø", "bodo/glimt", "bodo",
                   "man city", "manchester city", "liverpool", "slavia prague", "slavia",
                   "sporting", "bruges", "club bruges"}


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
    return fond_url("prono") if name != "prono" else None


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

# --- Thème Ligue des champions : nuit européenne (création originale, aucun élément officiel UEFA) ---
LDC_CSS = r"""
body.ldc{background:#030817}
.ldc .bg{background:
  radial-gradient(ellipse 80% 50% at 50% 112%, rgba(60,120,255,.55), rgba(20,40,120,.4) 45%, transparent 72%),
  radial-gradient(circle at 15% 15%, rgba(80,110,220,.35), transparent 40%),
  radial-gradient(circle at 88% 10%, rgba(255,212,0,.18), transparent 34%),
  linear-gradient(165deg,#0a1640 0%,#030817 55%,#0b1a4d 100%)}
.ldc.photo .bg{filter:saturate(.8) brightness(.8)}
.ldc .shade{display:block;background:
  linear-gradient(180deg,rgba(4,12,48,.97) 0%,rgba(8,24,90,.88) 30%,rgba(10,30,110,.6) 52%,rgba(10,30,110,.15) 72%,rgba(3,8,30,.55) 90%,rgba(3,8,30,.92) 100%)}
.ldc .smoke{display:none}
.ldc .rays{display:block;background:repeating-conic-gradient(from 0deg at 50% 0%, rgba(190,215,255,.09) 0 4deg, transparent 4deg 13deg)}
.ldc .slash,.ldc .terrils,.ldc .ghost{display:none}
.stars{position:absolute;inset:0;display:none}
.ldc .stars{display:block}
.ldc .kicker{background:linear-gradient(90deg,#c9d6f2,#ffffff 50%,#c9d6f2);color:#0a1640;box-shadow:8px 8px 0 #c8102e;letter-spacing:8px}
.ldc .big .l1{text-shadow:0 6px 0 #1d3f8f,0 0 40px rgba(120,170,255,.75)}
.ldc .big .l2{background:linear-gradient(180deg,#ffffff 0%,#e3ebff 35%,#9fb4e0 70%,#6f86bf 100%);
 -webkit-background-clip:text;background-clip:text;filter:drop-shadow(0 8px 0 #c8102e) drop-shadow(0 0 34px rgba(140,180,255,.7))}
.ldc .vs{color:#e3ebff;text-shadow:0 0 25px rgba(140,180,255,.9)}
.ldc .team{box-shadow:0 0 34px rgba(140,180,255,.55)}
.ldc .when{background:#ffffff;color:#0a1640;box-shadow:8px 8px 0 #c8102e}
.ldc .score{color:#ffffff;text-shadow:0 8px 0 #c8102e,0 0 40px rgba(140,180,255,.9)}
.ldc .cta{border-bottom-color:#e3ebff}
.ldc .brand span{color:#9fb4e0}
.nuit{display:none}
.ldc.photo .content{padding-top:96px}
.ldc .nuit{display:block;position:absolute;top:30px;left:0;width:100%;text-align:center;font-weight:800;font-style:italic;
 font-size:26px;letter-spacing:12px;color:#c9d6f2;text-shadow:0 0 14px rgba(140,180,255,.9)}
"""


def stars_svg():
    import random
    r = random.Random(62)
    pts = []
    for _ in range(140):
        x, y = r.uniform(0, 1080), r.uniform(0, 640)
        rad = r.choice([0.8, 1, 1.2, 1.6, 2.2])
        op = r.uniform(.35, .95)
        pts.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad}" fill="#fff" opacity="{op:.2f}"/>')
    def star(cx, cy, s, op):
        return (f'<path d="M{cx} {cy-s} L{cx+s*.18} {cy-s*.18} L{cx+s} {cy} L{cx+s*.18} {cy+s*.18} L{cx} {cy+s} '
                f'L{cx-s*.18} {cy+s*.18} L{cx-s} {cy} L{cx-s*.18} {cy-s*.18} Z" fill="#fff" opacity="{op}"/>')
    sparks = "".join(star(*t) for t in [(120, 140, 22, .9), (960, 210, 18, .85), (880, 70, 12, .7),
                                         (210, 420, 10, .6), (1010, 470, 14, .7), (60, 300, 9, .6)])
    return (f'<svg class="stars" viewBox="0 0 1080 1080"><defs><filter id="glow"><feGaussianBlur stdDeviation="2.4"/></filter></defs>'
            f'<g filter="url(#glow)">{sparks}</g>{sparks}{"".join(pts)}</svg>')


GRAIN = """<svg class="grain" width="1080" height="1080"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>"""


LDC = False


def page(ghost, inner, mid=False, fond=None):
    e = html.escape
    url = fond_url(fond) if fond else None
    cls = (["photo"] if url else []) + (["ldc"] if LDC else [])
    body_cls = f' class="{" ".join(cls)}"' if cls else ""
    bg_style = f' style="background:url({url})"' if url else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{LDC_CSS}</style></head><body{body_cls}>
<div class="bg"{bg_style}></div><div class="shade"></div><div class="rays"></div>
<div class="smoke s1"></div><div class="smoke s2"></div><div class="smoke s3"></div>
<div class="ghost">{e(ghost)}</div>
<div class="slash sl1"></div><div class="slash sl2"></div>
{TERRILS}{stars_svg() if LDC else ""}{GRAIN}
<div class="nuit">★ NUIT EUROPÉENNE ★</div>
<div class="content{' mid' if mid else ''}">{inner}</div>
<div class="brand"><span>///</span> {BRAND} <span>///</span></div>
</body></html>"""


def build(kind, a):
    e = html.escape
    if kind == "match":
        home, away, day, hour = a[0], a[1], a[2], a[3]
        kicker = a[4] if len(a) > 4 else ("LIGUE DES CHAMPIONS" if LDC else "LIGUE 1")
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
        kicker = a[3] if len(a) > 3 else ("J-1 · LIGUE DES CHAMPIONS" if LDC else "J-1")
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
<div class="cta">{e(a[2]) if len(a) > 2 else "Racontez-nous"} 👇</div>"""
        return page("62", inner, True, fond="question")
    if kind == "design":
        inner = f"""<div class="kicker">L'ATELIER</div>
<div class="big"><span class="l1 q1">{e(a[0])}</span><span class="l2 q2">{e(a[1])}</span></div>
<div class="cta">Votez en commentaire 👇</div>"""
        return page("DESIGN", inner, True, fond="design")
    if kind == "info":
        # "L'INFO DU JOUR" : bandeau (ex. source), titre en 2 lignes écrit avec NOS mots, appel à l'action
        kicker, l1, l2 = a[0], a[1], a[2]
        cta = a[3] if len(a) > 3 else "Votre avis ?"
        inner = f"""<div class="kicker">{e(kicker)}</div>
<div class="big"><span class="l1 q1">{e(l1)}</span><span class="l2 q2">{e(l2)}</span></div>
<div class="cta">{e(cta)} 👇</div>"""
        return page("INFO", inner, True, fond="info")
    if kind == "vote":
        # Vote en un emoji : les 3 choix sont DESSINÉS sur le visuel (demande d'Anthony du 08/11/2026)
        home, away, when = a[0], a[1], a[2]
        kicker = a[3] if len(a) > 3 else ("LIGUE DES CHAMPIONS" if LDC else "LIGUE 1")
        choix = [("❤️", "VICTOIRE", "#c8102e", "#ffd400"), ("👍", "NUL", "#ffffff", "#0a0405"), ("😡", "DÉFAITE", "#1b1b1b", "#ffffff")]  # = réactions Facebook J'adore / J'aime / Grrr
        tuiles = "".join(f'<div class="vt" style="background:{bg};color:{fg}"><span class="ve">{em}</span><span class="vl">{lab}</span></div>'
                         for em, lab, bg, fg in choix)
        inner = f"""<style>
.vote .team{{font-size:62px;padding:4px 22px 8px}} .vote .vs{{font-size:48px}} .vote .versus{{margin-top:18px}}
.vote{{display:flex;flex-direction:column;align-items:center;text-align:center;width:100%}} .vote .when{{margin-top:22px}}
.vq{{margin-top:34px;font-weight:900;font-style:italic;font-size:64px;letter-spacing:-1px;color:#fff;text-shadow:0 4px 0 #c8102e,0 0 30px rgba(0,0,0,.8)}}
.vts{{display:flex;gap:22px;justify-content:center;margin-top:26px}}
.vt{{width:270px;height:200px;border-radius:22px;border:5px solid #ffd400;display:flex;flex-direction:column;align-items:center;justify-content:center;
  box-shadow:0 12px 40px rgba(0,0,0,.6);transform:rotate(-2deg)}}
.ve{{font-size:92px;line-height:1}} .vl{{margin-top:10px;font-weight:900;font-style:italic;font-size:40px;letter-spacing:1px}}
.vc{{margin-top:30px;font-weight:800;font-style:italic;font-size:38px;color:#fff;text-shadow:0 2px 12px #000}}
</style><div class="vote">
<div class="kicker">{e(kicker)}</div>
<div class="versus">{team(home)}<div class="vs">VS</div>{team(away)}</div>
<div class="when">{e(when)}</div>
<div class="vq">VOTEZ AVEC UNE RÉACTION</div>
<div class="vts">{tuiles}</div>
<div class="vc">Appuyez longtemps sur « J'aime » pour choisir 👇</div></div>"""
        return page("VOTE", inner, fond="prono")
    raise SystemExit(f"type inconnu : {kind}")


def main():
    global LDC
    argv = sys.argv[1:]
    if "--ldc" in argv:
        LDC = True
        argv = [x for x in argv if x != "--ldc"]
    # Détection automatique : un bandeau qui parle de Ligue des champions active le thème
    if any("CHAMPIONS" in x.upper() or "LDC" in x.upper().split() for x in argv[2:]):
        LDC = True
    # Adversaires de Lens en Ligue des champions cette saison (à compléter au fil des tirages)
    norm = lambda x: "".join(c for c in unicodedata.normalize("NFD", x.lower()) if unicodedata.category(c) != "Mn").strip()
    if any(norm(x) in LDC_ADVERSAIRES for x in argv[2:]):
        LDC = True
    kind, out, *args = argv
    # typo française : ? ! : ; jamais seuls en début de ligne (espace insécable)
    args = [a.replace(" ?", "\u00a0?").replace(" !", "\u00a0!").replace(" :", "\u00a0:").replace(" ;", "\u00a0;")
            for a in args]
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
