"""Bilan hebdomadaire de la page « Cap sur la Bretagne » (lancé chaque lundi par GitHub Actions).

Lit avec la clé de page : abonnés, et pour chaque post des 7 derniers jours les réactions,
commentaires et partages. Écrit le bilan en Markdown (fichier donné en argument) et ajoute une
ligne à bretagne/stats.csv pour suivre l'évolution des abonnés d'une semaine à l'autre.
Variables : FB_PAGE_ID, FB_PAGE_TOKEN.
"""
import csv
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.facebook.com/v23.0"
ICI = pathlib.Path(__file__).resolve().parent
STATS = ICI / "stats.csv"
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def get(chemin, **params):
    token = os.environ["FB_PAGE_TOKEN"].strip()
    q = urllib.parse.urlencode({**params, "access_token": token})
    try:
        with urllib.request.urlopen(f"{API}/{chemin}?{q}", timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"::error::Facebook {e.code} : {e.read().decode(errors='replace').replace(token, '***')}")
        sys.exit(1)


def main(sortie):
    page_id = os.environ["FB_PAGE_ID"].strip()
    maintenant = dt.datetime.now(dt.timezone.utc)
    depuis = maintenant - dt.timedelta(days=7)
    page = get(page_id, fields="name,followers_count,fan_count")
    abonnes = page.get("followers_count") or page.get("fan_count") or 0

    precedent = None
    if STATS.exists():
        lignes = list(csv.DictReader(STATS.open(encoding="utf-8")))
        if lignes:
            precedent = int(lignes[-1]["abonnes"])
    nouveau = not STATS.exists()
    with STATS.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if nouveau:
            w.writerow(["date", "abonnes"])
        w.writerow([maintenant.date().isoformat(), abonnes])

    rep = get(f"{page_id}/posts", since=int(depuis.timestamp()), limit=50,
              fields="message,created_time,permalink_url,shares,"
                     "reactions.summary(total_count).limit(0),comments.summary(total_count).limit(0)")
    posts = []
    for p in rep.get("data", []):
        r = p.get("reactions", {}).get("summary", {}).get("total_count", 0)
        c = p.get("comments", {}).get("summary", {}).get("total_count", 0)
        s = p.get("shares", {}).get("count", 0)
        quand = dt.datetime.fromisoformat(p["created_time"].replace("+0000", "+00:00"))
        texte = (p.get("message") or "(sans texte)").replace("\n", " ")
        posts.append({"r": r, "c": c, "s": s, "score": r + 3 * c + 5 * s, "jour": JOURS[quand.weekday()],
                      "date": quand.strftime("%d/%m"), "texte": texte[:90] + ("…" if len(texte) > 90 else ""),
                      "lien": p.get("permalink_url", "")})

    tot_r, tot_c, tot_s = (sum(p[k] for p in posts) for k in ("r", "c", "s"))
    evol = "" if precedent is None else f" ({abonnes - precedent:+d} en une semaine)"
    md = [f"Bilan de la semaine du {depuis.strftime('%d/%m')} au {maintenant.strftime('%d/%m/%Y')} "
          f"pour **{page.get('name', 'Cap sur la Bretagne')}**.", "",
          f"- **Abonnés** : {abonnes}{evol}",
          f"- **Posts publiés** : {len(posts)}",
          f"- **Réactions** : {tot_r} · **Commentaires** : {tot_c} · **Partages** : {tot_s}", ""]
    if posts:
        md += ["## Les posts, du plus engageant au moins engageant", "",
               "| Date | Jour | Post | ❤️ | 💬 | 🔁 |", "|---|---|---|---|---|---|"]
        for p in sorted(posts, key=lambda p: -p["score"]):
            t = p["texte"].replace("|", "/")
            t = f"[{t}]({p['lien']})" if p["lien"] else t
            md.append(f"| {p['date']} | {p['jour']} | {t} | {p['r']} | {p['c']} | {p['s']} |")
        meilleur = max(posts, key=lambda p: p["score"])
        md += ["", f"**Post de la semaine** : celui du {meilleur['jour']} {meilleur['date']}, "
                   f"avec {meilleur['r']} réactions, {meilleur['c']} commentaires et {meilleur['s']} partages."]
    else:
        md.append("Aucun post publié sur la page cette semaine.")
    md += ["", "_Score de classement : réactions + 3 × commentaires + 5 × partages "
               "(les commentaires et partages font le plus grandir une page)._"]
    pathlib.Path(sortie).write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "bilan.md")
