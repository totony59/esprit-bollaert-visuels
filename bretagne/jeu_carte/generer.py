"""« Le jeu de la carte » (Cap sur la Bretagne) — demande d'Anthony du 04/11/2026.
Un jour sur deux à partir du 05/11/2026 : question à 10h00 (10h30 le week-end et les mercredis
des semaines ISO impaires, où un autre post sort déjà à 10h) + réponse en commentaire, avec image, à 18h00.
Prépare les visuels et les fichiers JSON dans bretagne/queue/ ; le robot de publication fait le reste.
usage : python3 bretagne/jeu_carte/generer.py [--date AAAA-MM-JJ] [--force]"""
import argparse, datetime as dt, json, pathlib, sys, unicodedata
from zoneinfo import ZoneInfo
ICI = pathlib.Path(__file__).resolve().parent
BRE = ICI.parent
sys.path.insert(0, str(ICI)); import carte_jeu
PARIS = ZoneInfo('Europe/Paris')
DEBUT = dt.date(2026, 11, 5)
QUESTIONS = [
    "🧭 Le jeu de la carte !\nSur notre carte de la Bretagne, dans quelle case se trouve {c} ?\n"
    "Répondez en commentaire avec une lettre et un chiffre 👇\nJe donne la réponse ce soir à 18h !",
    "🗺️ C'est l'heure du jeu de la carte !\nOù placez-vous {c} ? Une lettre + un chiffre, en commentaire.\n"
    "Réponse ce soir à 18h 😉",
    "🧭 Le jeu de la carte est de retour !\nCette fois, c'est {c}. Vous la mettez dans quelle case ?\n"
    "Réponse à 18h… et pas de triche avec Google Maps 😄",
]
REPONSE = ("✅ La réponse : {case} !\n{c} ({dep}) se trouve bien en {case}. "
           "Bravo à tous ceux qui l'ont trouvée 👏\nProchain jeu de la carte dans 2 jours !")

def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return '-'.join(''.join(ch if ch.isalnum() else ' ' for ch in t).split())

def deja():
    """Fichiers de jeu existants (toutes étapes)."""
    return [f.name for d in ('queue', 'scheduled', 'published', 'skipped') for f in (BRE / d).glob('*_jeucarte_*.json')]

def main():
    a = argparse.ArgumentParser(); a.add_argument('--date'); a.add_argument('--force', action='store_true')
    x = a.parse_args()
    jour = dt.date.fromisoformat(x.date) if x.date else dt.datetime.now(PARIS).date()
    if not x.force and ((jour - DEBUT).days < 0 or (jour - DEBUT).days % 2):
        print('Pas de jeu de la carte aujourd’hui.'); return
    existants = deja()
    if any(n.startswith(jour.isoformat()) for n in existants):
        print('Jeu déjà préparé pour', jour); return
    lieux = [l.strip() for l in (ICI / 'lieux.txt').read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')]
    faits = {n.split('_jeucarte_', 1)[1].removesuffix('.json') for n in existants if '_reponse_' not in n}
    reste = [l for l in lieux if slug(l) not in faits]
    if not reste:
        print('::warning::Plus aucun lieu dans lieux.txt : ajoute de nouvelles communes.'); return
    c = reste[0]; s = slug(c)
    weekend = jour.weekday() >= 5
    mercredi_impair = jour.weekday() == 2 and jour.isocalendar()[1] % 2 == 1
    h, m = (10, 30) if (weekend or mercredi_impair) else (10, 0)
    q_t = dt.datetime(jour.year, jour.month, jour.day, h, m, tzinfo=PARIS)
    r_t = dt.datetime(jour.year, jour.month, jour.day, 18, 0, tzinfo=PARIS)
    vis = BRE / 'visuels'; vis.mkdir(exist_ok=True)
    vq, vr = vis / f'{jour}_jeucarte_{s}.png', vis / f'{jour}_jeucarte_{s}_reponse.png'
    case = carte_jeu.creer(vq, c); carte_jeu.creer(vr, c, reponse=True)
    import csv
    dep = next(r for r in csv.DictReader(open(ICI / 'communes_grille.csv', encoding='utf-8')) if r['nom'] == c)['dep']
    nq = f'{jour}T{h:02d}{m:02d}_jeucarte_{s}.json'
    q = {'publish_at': q_t.isoformat(), 'message': QUESTIONS[len(faits) % len(QUESTIONS)].format(c=c),
         'image': str(vq.relative_to(BRE.parent)), 'lieu': c}
    r = {'publish_at': r_t.isoformat(), 'comment_on': nq,
         'message': REPONSE.format(c=c, case=case, dep=carte_jeu.DEPS[dep]),
         'image': str(vr.relative_to(BRE.parent))}
    (BRE / 'queue').mkdir(exist_ok=True)
    (BRE / 'queue' / nq).write_text(json.dumps(q, ensure_ascii=False, indent=1), encoding='utf-8')
    (BRE / 'queue' / f'{jour}T1800_reponse_jeucarte_{s}.json').write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding='utf-8')
    print('Jeu préparé :', c, '→', case, '|', nq)

if __name__ == '__main__':
    main()
