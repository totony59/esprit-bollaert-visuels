# Règle anti-doublons – à lire par TOUT compte Claude avant de publier (11/11/2026)

Anthony utilise deux comptes Claude. Les deux connaissent les pages via Supermemory : sans règle commune,
chacun pourrait publier le même sujet de son côté. Pages concernées : Esprit Bollaert Design (racine du dépôt),
Cap sur la Bretagne (bretagne/), Cap sur - le Pays basque (paysbasque/).

1. Un seul canal de publication : le robot GitHub de ce dépôt (fichier dans queue/, commit + push).
   Jamais de publication directe sur Facebook. Metricool seulement en secours pour Lens, si le robot est en panne,
   et après avoir déposé le fichier dans queue/ comme indiqué dans consignes/post-resultat.md.
2. Les posts automatiques sont faits par les tâches programmées existantes (compte principal d'Anthony).
   Ne crée JAMAIS une deuxième tâche programmée pour une rubrique qui existe déjà.
3. Avant d'ajouter un post : regarde queue/, scheduled/ et published/ de la page (et Metricool pour Lens).
   Si un post du même type ou sur le même sujet existe déjà pour ce jour, arrête-toi.
4. Ne modifie jamais un fichier de queue/ déjà poussé (voir consignes/strategie-portee.md §7).
5. Après chaque publication : lance le workflow « Contrôle des doublons (lecture seule) » et vérifie qu'il
   n'affiche aucun doublon. S'il y en a un, préviens Anthony.
