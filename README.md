# Esprit Bollaert Design – visuels

Visuels générés automatiquement pour la page Facebook de supporters « Esprit Bollaert Design » (page non officielle).

`gen.py` crée les images 1080×1080 (types : match, prono, resultat, homme, question, design) avec Playwright/Chromium.
Les images publiées sont dans `visuels/`.

## Fonctionnement du robot de publication

- `queue/` : posts à publier (`publish_at` avec fuseau, `message`, `image` et/ou `link`).
- Un post prévu dans plus de 15 min est confié immédiatement au programmateur de Facebook
  (dossier `scheduled/`) : Facebook le publie à l'heure exacte. Visible aussi dans Meta
  Business Suite › Planificateur.
- Un post dont l'heure est passée est publié tout de suite (dossier `published/`).
- Pour annuler un post programmé : créer `annuler/<même nom de fichier>.json` (contenu `{}`),
  commit + push ; le robot le supprime chez Facebook et le range dans `skipped/`.
- Pour MODIFIER un post déjà programmé : l'annuler (ci-dessus) puis créer un nouveau fichier
  dans `queue/` avec un nom différent.
- Commentaire différé (ex. réponse d'un quiz) : fichier de `queue/` avec `"comment_on"` (nom du
  fichier du post visé) ; publié en commentaire sous ce post à l'heure `publish_at`.

## Page « Cap sur la Bretagne »

Même robot, avec ses propres dossiers sous `bretagne/` (`queue/`, `scheduled/`, `published/`,
`skipped/`, `annuler/`, `visuels/`) et son workflow « Publier sur Facebook – Cap sur la Bretagne »
(secret `FB_PAGE_TOKEN_BRETAGNE`). Consignes éditoriales : `bretagne/consignes.md`. Visuels :
`bretagne/visuel.py`. Bilan chaque lundi : workflow « Bilan du lundi » (fiche GitHub + e-mail).
