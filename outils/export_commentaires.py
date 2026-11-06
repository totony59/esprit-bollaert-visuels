"""Outil TEMPORAIRE (lecture seule) : commentaires des posts récents de la page, pour la carte des lieux
d'Anthony. Écrit export.json, chiffré ensuite par le workflow (rien n'est affiché en clair)."""
import json, os, urllib.error, urllib.parse, urllib.request
API = "https://graph.facebook.com/v23.0"
TOK, PAGE = os.environ["FB_PAGE_TOKEN"].strip(), os.environ["FB_PAGE_ID"].strip()
erreurs = []
def get(path, **p):
    url = path if path.startswith("http") else f"{API}/{path}?{urllib.parse.urlencode({**p, 'access_token': TOK})}"
    try:
        with urllib.request.urlopen(url, timeout=40) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        erreurs.append({"requete": path.split("?")[0][-60:], "erreur": e.read().decode(errors="replace").replace(TOK, "***")[:300]})
        return {}
def toutes(path, maxi=5000, **p):
    out, r = [], get(path, **p)
    while r and len(out) < maxi:
        out += r.get("data", []); nxt = r.get("paging", {}).get("next")
        r = get(nxt) if nxt else None
    return out
posts = toutes(f"{PAGE}/published_posts", maxi=40, limit=40,
               fields="id,message,created_time,permalink_url,comments.summary(true).limit(0)")
res = []
for p in posts:
    n = p.get("comments", {}).get("summary", {}).get("total_count", 0)
    item = {"id": p["id"], "date": p.get("created_time"), "lien": p.get("permalink_url"),
            "texte": (p.get("message") or "")[:300], "nb_commentaires": n}
    if n >= 5:
        item["commentaires"] = [{"texte": c.get("message", ""), "date": c.get("created_time"),
                                 "auteur": (c.get("from") or {}).get("name"), "likes": c.get("like_count")}
                                for c in toutes(f"{p['id']}/comments", filter="stream", limit=100,
                                                fields="message,created_time,from,like_count")]
    res.append(item)
json.dump({"posts": res, "erreurs": erreurs}, open("export.json", "w"), ensure_ascii=False)
print("posts :", len(res), "| erreurs :", len(erreurs))
