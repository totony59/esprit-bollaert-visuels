"""Analyse anonyme des commentaires du réel le plus commenté de la page (14 derniers jours).
N'affiche AUCUN nom ni commentaire complet : uniquement des comptages (phares cités, mots fréquents)."""
import collections, json, os, re, unicodedata, urllib.parse, urllib.request, datetime as dt

API = "https://graph.facebook.com/v23.0"
TOK, PAGE = os.environ["FB_PAGE_TOKEN"].strip(), os.environ["FB_PAGE_ID"].strip()

def get(path, **p):
    q = urllib.parse.urlencode({**p, "access_token": TOK})
    with urllib.request.urlopen(f"{API}/{path}?{q}", timeout=30) as r:
        return json.loads(r.read())

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

PHARES = {
 "Ar Men": ["ar men", "armen"], "La Jument": ["jument"], "Kéréon": ["kereon"], "Le Créac'h": ["creac"],
 "Le Stiff": ["stiff"], "Nividic": ["nividic"], "Eckmühl": ["eckmuhl", "eckmul", "penmarc"],
 "Petit Minou": ["minou"], "Saint-Mathieu": ["saint-mathieu", "saint mathieu", "st mathieu"],
 "Île Vierge": ["ile vierge", "vierge"], "Ploumanac'h / Mean Ruz": ["ploumanac", "mean ruz"],
 "Cap Fréhel": ["frehel"], "Le Grand Jardin": ["grand jardin"], "Les Pierres Noires": ["pierres noires"],
 "La Vieille": ["la vieille", "pointe du raz", "raz de sein"], "Tévennec": ["tevennec"], "Île de Sein / Goulenez": ["sein", "goulenez"],
 "Les Héaux de Bréhat": ["heaux", "brehat"], "Le Four": ["le four", "phare du four"], "Trézien": ["trezien"],
 "Goulphar (Belle-Île)": ["goulphar", "belle-ile", "belle ile", "belle-ile-en-mer"], "Pen Men (Groix)": ["pen men", "groix"],
 "Batz": ["ile de batz", "batz"], "Port-Navalo": ["port-navalo", "port navalo"], "Le Rosédo (Bréhat)": ["rosedo"],
 "Les Sept-Îles": ["sept-iles", "sept iles"], "Phare de Penfret / Glénan": ["glenan", "penfret"], "Pointe de Penmarc'h": [],
 "Phare du Portzic": ["portzic"], "Phare de l'Île Wrac'h": ["wrach", "wrac'h"], "Phare de la Teignouse": ["teignouse"],
}
STOP = set(norm(w) for w in """le la les de des du un une et a à au aux en est c ce ça ca qui que quoi pour pas plus
 tres très trop bien beau belle beaux belles magnifique super merci je j il elle on nous vous ils y ma mon mes ta ton
 tes sa son ses dans sur avec par ou où mais si comme tout tous toute toutes the of and n ne d l s qu m t me te se
 phare phares bretagne breizh photo photos video aussi deja déjà encore vraiment fait faire vu voir""".split())

since = int((dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=14)).timestamp())
posts = get(f"{PAGE}/posts", since=since, limit=50, fields="id,created_time,message,comments.summary(total_count).limit(0)")
vids = get(f"{PAGE}/videos", since=since, limit=50, fields="id,created_time,description,comments.summary(total_count).limit(0)")
cands = [(x.get("comments", {}).get("summary", {}).get("total_count", 0), x["id"], (x.get("message") or x.get("description") or "")[:60])
         for x in posts.get("data", []) + vids.get("data", [])]
cands.sort(reverse=True)
total, oid, apercu = cands[0]
textes, url = [], f"{oid}/comments"
params = dict(limit=100, fields="message,comment_count", filter="stream")
while url:
    r = get(url, **params) if not url.startswith("http") else json.loads(urllib.request.urlopen(url, timeout=30).read())
    textes += [c.get("message", "") for c in r.get("data", [])]
    url, params = r.get("paging", {}).get("next"), {}

cpt = collections.Counter()
for t in textes:
    n = norm(t)
    for nom, motifs in PHARES.items():
        if any(m and m in n for m in motifs):
            cpt[nom] += 1
mots = collections.Counter(w for t in textes for w in re.findall(r"[a-z'-]{3,}", norm(t)) if w not in STOP)

lignes = [f"## Analyse du post le plus commenté ({total} commentaires annoncés, {len(textes)} lus)",
          f"Début du texte : « {apercu} »", "", "### Phares cités", "| Phare | Commentaires qui le citent |", "|---|---|"]
lignes += [f"| {k} | {v} |" for k, v in cpt.most_common()] or ["| (aucun) | 0 |"]
lignes += ["", "### Mots les plus fréquents (hors mots courants)", ", ".join(f"{w} ({c})" for w, c in mots.most_common(40))]
out = "\n".join(lignes)
print(out)
with open(os.environ.get("GITHUB_STEP_SUMMARY", "/dev/null"), "a") as f:
    f.write(out + "\n")
