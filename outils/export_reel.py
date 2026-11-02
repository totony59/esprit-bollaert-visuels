"""Export complet (lecture seule) d'un réel : stats, commentaires, réponses, autres réels.
Le résultat est écrit dans export.json, chiffré ensuite par le workflow (rien n'est affiché en clair)."""
import json, os, urllib.error, urllib.parse, urllib.request, datetime as dt

API = "https://graph.facebook.com/v23.0"
TOK, PAGE = os.environ["FB_PAGE_TOKEN"].strip(), os.environ["FB_PAGE_ID"].strip()
CIBLE = dt.datetime(2026, 10, 29, 16, 8, tzinfo=dt.timezone.utc)   # 17 h 08 heure de Paris
erreurs = []

def get(path, **p):
    url = path if path.startswith("http") else f"{API}/{path}?{urllib.parse.urlencode({**p, 'access_token': TOK})}"
    try:
        with urllib.request.urlopen(url, timeout=40) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="replace").replace(TOK, "***")[:400]
        erreurs.append({"requete": path.split("?")[0].replace(TOK, "***")[-80:], "params": list(p), "erreur": msg})
        return {}

def toutes(path, **p):
    out, r = [], get(path, **p)
    while r:
        out += r.get("data", [])
        nxt = r.get("paging", {}).get("next")
        r = get(nxt) if nxt else None
    return out

def quand(s):
    return dt.datetime.fromisoformat(s.replace("+0000", "+00:00"))

# 1. Les réels / vidéos de la page
reels = toutes(f"{PAGE}/video_reels", fields="id,description,created_time,permalink_url,length,post_id", limit=50)
videos = toutes(f"{PAGE}/videos", fields="id,description,created_time,permalink_url,length,post_id", limit=50)
tous = {v["id"]: v for v in videos + reels}
cible = min(tous.values(), key=lambda v: abs(quand(v["created_time"]) - CIBLE)) if tous else None

METRICS = ["blue_reels_play_count", "fb_reels_total_plays", "fb_reels_replay_count", "post_impressions_unique",
           "post_video_avg_time_watched", "post_video_view_time", "post_video_followers", "post_video_social_actions",
           "post_video_likes_by_reaction_type", "post_video_retention_graph"]

def insights(vid):
    res = {}
    for m in METRICS:
        r = get(f"{vid}/video_insights", metric=m)
        for d in r.get("data", []):
            res[d["name"]] = d.get("values", [{}])[0].get("value")
    return res

def details(v):
    vid = v["id"]
    info = get(vid, fields="id,description,created_time,permalink_url,length,post_id,views,"
                           "comments.summary(true).limit(0),likes.summary(true).limit(0)")
    post = {}
    pid = info.get("post_id") or v.get("post_id")
    if pid:
        full = pid if "_" in str(pid) else f"{PAGE}_{pid}"
        post = get(full, fields="id,shares,reactions.summary(total_count).limit(0),comments.summary(total_count).limit(0)")
    return {"video": info, "post": post, "insights": insights(vid)}

export = {"genere_le": dt.datetime.now(dt.timezone.utc).isoformat(), "reel_cible": None,
          "commentaires": [], "autres_reels": [], "erreurs": erreurs}
if cible:
    export["reel_cible"] = details(cible)
    # 2. Commentaires + réponses (toutes les pages)
    coms = toutes(f"{cible['id']}/comments", filter="toplevel", limit=100, order="chronological",
                  fields="id,message,created_time,like_count,comment_count,from{id,name},"
                         "reactions.summary(total_count).limit(0)")
    if not coms and export["reel_cible"]["video"].get("post_id"):
        pid = export["reel_cible"]["video"]["post_id"]
        coms = toutes(f"{pid if '_' in str(pid) else PAGE + '_' + str(pid)}/comments", filter="toplevel", limit=100,
                      fields="id,message,created_time,like_count,comment_count,from{id,name}")
    for c in coms:
        c["reponses"] = toutes(f"{c['id']}/comments", limit=100,
                               fields="id,message,created_time,like_count,from{id,name}") if c.get("comment_count") else []
    export["commentaires"] = coms
    # 3. Autres réels de la période (20/10 → aujourd'hui)
    for v in sorted(tous.values(), key=lambda v: v["created_time"]):
        if v["id"] != cible["id"] and quand(v["created_time"]) >= CIBLE - dt.timedelta(days=10):
            export["autres_reels"].append(details(v))

# Anonymisation des auteurs (Auteur_001…), la page garde son nom
ids = {}
def anon(f):
    if not f: return None
    if f.get("id") == PAGE: return "La page"
    ids.setdefault(f.get("id") or f.get("name"), f"Auteur_{len(ids)+1:03d}")
    return ids[f.get("id") or f.get("name")]
for c in export["commentaires"]:
    c["auteur"] = anon(c.pop("from", None))
    for r in c["reponses"]:
        r["auteur"] = anon(r.pop("from", None))

json.dump(export, open("export.json", "w"), ensure_ascii=False, indent=1)
print(f"OK : {len(export['commentaires'])} commentaires, {sum(len(c['reponses']) for c in export['commentaires'])} réponses, "
      f"{len(export['autres_reels'])} autres réels, {len(erreurs)} requêtes refusées")
