"""Contrôle des doublons (lecture seule) : posts publiés (3 derniers jours) et programmés de la page,
regroupés par début de texte. N'affiche que les doublons (textes de la page elle-même, déjà publics)."""
import json, os, urllib.parse, urllib.request, datetime as dt
API = "https://graph.facebook.com/v23.0"
TOK, PAGE, NOM = os.environ["FB_PAGE_TOKEN"].strip(), os.environ["FB_PAGE_ID"].strip(), os.environ.get("NOM", "")
def lire(bord, champs):
    q = urllib.parse.urlencode({"fields": champs, "limit": 50, "access_token": TOK})
    try:
        with urllib.request.urlopen(f"{API}/{PAGE}/{bord}?{q}", timeout=40) as r:
            return json.loads(r.read()).get("data", [])
    except Exception as e:
        print(f"::warning::{NOM} {bord} illisible : {type(e).__name__}"); return []
limite = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=3)
posts = [("publié", p) for p in lire("published_posts", "id,message,created_time")
         if dt.datetime.fromisoformat(p["created_time"].replace("+0000", "+00:00")) > limite]
posts += [("programmé", p) for p in lire("scheduled_posts", "id,message,scheduled_publish_time")]
groupes = {}
for etat, p in posts:
    cle = " ".join((p.get("message") or "").split())[:50].lower()
    if cle:
        groupes.setdefault(cle, []).append((etat, p["id"], p.get("created_time") or p.get("scheduled_publish_time")))
d = {k: v for k, v in groupes.items() if len(v) > 1}
print(f"{NOM} : {len(posts)} posts vérifiés, {len(d)} doublon(s)")
for k, v in d.items():
    print(f"::warning::DOUBLON {NOM} « {k} » -> {v}")
