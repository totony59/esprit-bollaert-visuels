"""Outil TEMPORAIRE (lecture seule) : statistiques publiques des posts récents de la page (aucun commentaire,
aucun nom). Résultat dans stats.json (artefact)."""
import json, os, urllib.error, urllib.parse, urllib.request
API = "https://graph.facebook.com/v23.0"
TOK, PAGE = os.environ["FB_PAGE_TOKEN"].strip(), os.environ["FB_PAGE_ID"].strip()
err = []
def get(path, **p):
    url = path if path.startswith("http") else f"{API}/{path}?{urllib.parse.urlencode({**p, 'access_token': TOK})}"
    try:
        with urllib.request.urlopen(url, timeout=40) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e:
        err.append(e.read().decode(errors="replace").replace(TOK, "***")[:200]); return {}
out, r = [], get(f"{PAGE}/published_posts", limit=50, fields="id,message,created_time,permalink_url,status_type,"
         "shares,reactions.summary(total_count).limit(0),comments.summary(total_count).limit(0)")
while r and len(out) < 80:
    out += r.get("data", []); n = r.get("paging", {}).get("next"); r = get(n) if n else None
res = [{"id": p["id"], "date": p["created_time"], "type": p.get("status_type"), "lien": p.get("permalink_url"),
        "texte": (p.get("message") or "")[:120], "reactions": p.get("reactions", {}).get("summary", {}).get("total_count", 0),
        "commentaires": p.get("comments", {}).get("summary", {}).get("total_count", 0),
        "partages": p.get("shares", {}).get("count", 0)} for p in out]
page = get(PAGE, fields="followers_count,fan_count")
vids = get(f"{PAGE}/video_reels", limit=20, fields="id,post_id,created_time,description,views")
json.dump({"page": page, "posts": res, "reels": vids.get("data", []), "erreurs": err[:5]}, open("stats.json", "w"), ensure_ascii=False)
print(len(res), "posts")
