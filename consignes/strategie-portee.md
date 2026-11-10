# Stratégie de portée (décidée avec Anthony le 08/11/2026) — PRIORITAIRE sur toutes les autres consignes

Constat (Metricool, 25/10 → 08/11) : les posts « lien » touchent 1 à 14 personnes, les posts image
15 à 40, et la page publie trop (3-4 posts/jour) : Facebook montre de moins en moins chaque post.
Pas de reels pour l'instant (Anthony l'a refusé le 08/11).

## 1. Moins de posts, plus forts
- MAXIMUM 2 posts par jour au total sur la page (hors post de résultat d'un match de Lens et hors
  posts RÉSULTATS / CLASSEMENT du dimanche soir et CLASSEMENT LDC du mercredi soir, qui restent).
  Compte tout : info du jour, alertes, prono, jour de match, question, posts d'Anthony (Metricool).
- Jour de match : SEULEMENT le post « jour de match » (12h) + le résultat. Rien d'autre, sauf
  composition officielle très attendue ou info majeure.
- Veille de match : le pronostic (12h) + au plus 1 autre post (l'info la plus forte du jour).
- Les ALERTES (tâche « Veille actu ») : seulement les vraies grosses infos officielles (entraîneur,
  transfert officiel, blessure longue d'un cadre, sanction, changement d'horaire, entraînement
  ouvert au public avant un match) — et seulement si le maximum de 2 posts du jour n'est pas atteint.
  Plus d'alerte pour une conférence de presse, une ambiance de vestiaire, un arbitre, une stat.
- Dans le doute, NE PUBLIE PAS : un post de moins vaut mieux qu'un post qui ne touche personne.

## 2. Le lien de l'article en premier commentaire (plus dans le post)
Pour l'info du jour et les alertes :
- Le post = notre texte seul (pas de champ "link", pas d'URL dans le texte, pas d'image de presse).
  Anthony ne veut pas de texte écrit sur une image pour les infos : donc post texte simple.
  Cite toujours la source par son nom dans le texte (« d'après L'Équipe… »).
- Juste après, un 2e fichier dans queue/ qui publie le lien en commentaire :
  queue/AAAA-MM-JJTHHMM_lien_<sujet>.json :
  {"publish_at": "<heure du post + 2 minutes>", "comment_on": "<nom exact du fichier du post>",
   "message": "📰 L'article (<nom du média>) : <URL>"}
  (le robot publie ce commentaire sous le post à l'heure indiquée).

## 3. Des questions faciles, qui se répondent en un mot ou un emoji
- Fin de chaque post : UNE question courte, à réponse immédiate. Exemples :
  « Victoire, nul ou défaite ce soir ? », « Note le match sur 10 👇 », « Titulaire ou remplaçant :
  vous dites quoi ? », « 🔥 si t'y crois, 😬 si t'as peur », « Ton homme du match en un nom ? »,
  « Oui ou non ? ». Après un match, garder les tops et les flops (demande d'Anthony), en version
  courte : « Ton top et ton flop, en deux noms 👇 ».
- Interdit : les questions longues à plusieurs branches (« Vous pensez que… ou plutôt… ? »),
  les questions qui demandent une réflexion ou un paragraphe.
- Textes plus courts : 2 à 4 phrases maximum avant la question.
- Toujours pas d'« engagement bait » (« commentez OUI », « partagez si… », « tag 3 amis »).

## 4. Post « JOUR DE MATCH » = visuel de VOTE (validé par Anthony le 08/11/2026)
Le jour d'un match, le post de 12h utilise le visuel de vote (et non plus gen.py match) :
  python3 gen.py vote visuels/AAAA-MM-JJ_vote_<adversaire>.png "DOMICILE" "EXTÉRIEUR" "CE SOIR · 20H45" "LIGUE 1 · 10E JOURNÉE"
Les 3 choix sont dessinés sur l'image, avec les réactions Facebook : ❤️ VICTOIRE, 👍 NUL, 😡 DÉFAITE
(on vote en appuyant longtemps sur « J'aime »). Texte court : « C'EST JOUR DE MATCH 🔴🟡 », l'heure,
UN fait d'historique confirmé par deux sources, puis exactement « Allez, votez : ❤️ victoire, 👍 nul, 😡 défaite 👇 ».
Toujours ces trois réactions-là, dans cet ordre (simples à trouver pour tout le monde).

## 5. Une publication maison CHAQUE jour (validé par Anthony le 08/11/2026)
Applique consignes/rubriques.md : chaque jour une rubrique à 10h00 (jour de match = vote, veille = pronostic).
Elle passe AVANT l'info du jour, qui ne sort en plus que si elle est vraiment forte (2 posts/jour maximum).

## 6. « LE FACE-À-FACE » le jour de match (demandé par Anthony le 08/11/2026)
Le jour d'un match, 2e post de la journée (après le vote) vers 15h00 : les stats des confrontations
Lens – adversaire depuis 2000 (en championnat ; sinon toutes compétitions, à préciser sur le visuel),
uniquement s'il y a au moins 4 matchs (sinon pas de face-à-face).
- Liste de TOUS les matchs (date, lieu, score) confirmée par DEUX sources (foot-direct.com/resultats/<club>-vs-<club>,
  rclensois.fr/confrontations, matchendirect.fr/statistique, madeinlens.com…). Calcule les chiffres en Python, jamais de tête.
- data/h2h-<adv>.json puis python3 stats_h2h.py visuels/AAAA-MM-JJ_face-a-face_<adv>.png data/h2h-<adv>.json
  (bilan V/N/D, buts, 4 tuiles : forme récente, bilan à domicile ou à l'extérieur, série, buts par match…).
- Texte : 2-3 phrases, les 2 chiffres les plus parlants, question courte. Regarde l'image (Read) : rien de coupé.

## 7. Ne JAMAIS modifier un fichier de queue/ après l'avoir poussé (doublon du quiz du 10/11/2026)
Le push lance le robot tout de suite : si tu modifies ensuite le fichier (texte, heure…), le robot a déjà pu
envoyer l'ancienne version à Facebook, et la nouvelle repart en double. Relis tout AVANT le push. Pour corriger
un post déjà poussé : attends qu'il soit dans scheduled/ (ou published/), puis annuler/<même nom>.json + nouveau
fichier avec un autre nom (seulement s'il est encore programmé ; s'il est publié, laisse-le).
