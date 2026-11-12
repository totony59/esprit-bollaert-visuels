"""Statistiques (lecture seule) des derniers posts publiés de la page : réactions, commentaires, partages.
Aucun nom, uniquement des totaux."""
import json, os, urllib.parse, urllib.request
API = "https://graph.facebook.com/v23.0"
TOK, PAGE = os.environ["FB_PAGE_TOKEN"].strip(), os.environ["FB_PAGE_ID"].strip()
q = urllib.parse.urlencode({"fields": "created_time,message,shares,reactions.summary(true).limit(0),comments.summary(true).filter(stream).limit(0)", "limit": 100, "access_token": TOK})
with urllib.request.urlopen(f"{API}/{PAGE}/published_posts?{q}", timeout=60) as r:
    data = json.loads(r.read()).get("data", [])
for p in data:
    m = " ".join((p.get("message") or "").split())[:55]
    print(f"STAT {p["id"]} {p["created_time"][:16]} | R {p.get('reactions',{}).get('summary',{}).get('total_count',0):4} | C {p.get('comments',{}).get('summary',{}).get('total_count',0):4} | P {p.get('shares',{}).get('count',0):3} | {m}")
