# Consignes : posts « RÉSULTATS » puis « CLASSEMENT » de Ligue 1 (chaque fin de journée)

Demande d'Anthony (03/11/2026) : publier le classement de Ligue 1 une fois le DERNIER match de la
journée joué (en général le dimanche soir), avec le visuel classement.py validé par Anthony
(fond illustré, 2 colonnes, pastilles aux couleurs des clubs, ligne de Lens en rouge et or,
flèches ▲▼, différence de buts, couleurs des zones). Publication automatique autorisée par Anthony.
Le dossier bretagne/ concerne une autre page : n'y touche jamais.

## 1. La journée est-elle terminée ?
- Trouve la journée de Ligue 1 en cours et la liste de ses 9 matchs (ligue1.com / L'Équipe / Foot Mercato).
- Tous les matchs doivent être TERMINÉS (score final, pas un score en direct), sauf un match
  officiellement REPORTÉ à une date ultérieure (dans ce cas, publie quand même et précise dans le
  texte qu'il manque ce match).
- Si un match n'est pas fini ou se joue plus tard (lundi, mardi…) : ne publie rien, crée une tâche
  ponctuelle (mcp__claude-code-remote__create_trigger, run_once_at = fin prévue du dernier match
  + 30 min, en UTC, même nom suivi de « (relance) », initiation « own_followup », même message que
  celui qui t'a lancé), puis arrête-toi.
- Si data/classement-precedent.json porte déjà ce numéro de journée : déjà publié, arrête-toi.

## 1 bis. Les RÉSULTATS de la journée (demande d'Anthony validée le 03/11/2026) — publiés EN PREMIER
- Si un fichier *_resultats-l1_jN* existe déjà dans published/ ou queue/ pour cette journée, passe directement au classement.
- Relève les 9 scores FINAUX de la journée sur DEUX sources qui concordent (ligue1.com, L'Équipe,
  Foot Mercato, Maxifoot…). Au moindre écart, une 3e source ; sans concordance, ne publie pas.
- Écris data/resultats-l1.json : {"journee": N, "matchs": [{"dom": "Nice", "sd": 5, "se": 2, "ext": "Rennes"}, ...]}
  dans l'ordre chronologique des matchs (noms courts, équipe à domicile en "dom").
- Visuel : python3 resultats.py visuels/AAAA-MM-JJ_resultats-l1_jN.png data/resultats-l1.json <fond>
  (fond victoire / nul / defaite selon le résultat de Lens, sinon match). Regarde l'image (Read).
- Texte court dans le style d'Anthony : le résultat de Lens en premier (avec l'émotion qui va avec),
  1 ou 2 faits marquants de la journée (gros score, surprise, résultat d'un concurrent direct), puis
  une question (« Le résultat qui vous a le plus surpris ? »…). Varie chaque semaine.
- Fichier queue/AAAA-MM-JJTHHMM_resultats-l1_jN.json (publish_at = maintenant), puis le classement
  (étapes 2 à 5) avec publish_at = 30 minutes après les résultats (Facebook le programmera).
- Supprime data/resultats-l1.json une fois le visuel créé.

## 2. Le classement
- Relève pour les 18 clubs : rang, points, différence de buts, sur DEUX sources qui doivent
  concorder exactement (ex. ligue1.com + Foot Mercato, L'Équipe, Alsa'Sports). Vérifie que chaque
  club a bien le bon nombre de matchs joués. Au moindre écart, cherche une 3e source ; sans
  concordance, ne publie pas.
- Écris data/classement-actuel.json : {"journee": N, "date": "AAAA-MM-JJ", "clubs": [{"club": "PSG",
  "pts": 20, "diff": 11}, ...]} dans l'ordre du classement (noms courts : PSG, Lille, Lyon, Paris FC,
  Rennes, Marseille, Monaco, Nice, Lens, Brest, Lorient, Toulouse, Strasbourg, Auxerre, Angers,
  Troyes, Le Mans, Le Havre).

## 3. Le visuel
python3 classement.py visuels/AAAA-MM-JJ_classement_jN.png data/classement-actuel.json data/classement-precedent.json <fond>
- fond selon le résultat de Lens dans la journée : victoire / nul / defaite (sinon match).
- Les flèches viennent de la comparaison avec data/classement-precedent.json.
- Regarde l'image (Read) : rien de coupé, Lens bien en évidence, chiffres corrects.
- Ensuite : remplace data/classement-precedent.json par le contenu de classement-actuel.json
  (il servira aux flèches la semaine suivante) et supprime classement-actuel.json.

## 4. Le texte (style d'Anthony)

Depuis le 08/11/2026 : 2 à 4 phrases maximum et une question COURTE à réponse en un mot ou un emoji (voir consignes/strategie-portee.md §3), ex. « Top 6 en fin de saison : oui ou non ? ».
Ultra naturel, première personne, phrases courtes, 1 à 3 emojis, 0 hashtag, aucune formule de
communicant ou « IA ». La place de Lens et ce qui a bougé (places gagnées ou perdues), l'écart avec
le podium / l'Europe ou la zone rouge (calculé à partir des chiffres vérifiés), un ressenti
(enthousiaste si ça monte, lucide si ça descend), puis une question qui fait réagir (« Vous nous
voyez où à la trêve ? », « Qui va lâcher en premier en haut ? »…). Varie la question chaque semaine.

## 5. Publication
queue/AAAA-MM-JJTHHMM_classement_jN.json : {"publish_at": "<30 min après les résultats, fuseau de Paris>",
"message": "<texte>", "image": "visuels/<fichier>.png"}. Commit + push (avec le visuel et
data/classement-precedent.json), git -c user.name=Claude -c user.email=noreply@anthropic.com,
git pull --rebase avant. Vérifie qu'un run de publier.yml démarre dans la minute, sinon force-le :
gh api -X POST repos/totony59/esprit-bollaert-visuels/actions/workflows/publier.yml/dispatches -f ref=main.
Puis git pull : les résultats doivent être dans published/ et le classement dans scheduled/ (ou published/), avec un facebook_post_id. En cas d'échec :
annotations (gh api repos/totony59/esprit-bollaert-visuels/check-runs/<job_id>/annotations), corrige ;
en dernier recours Metricool (blogId 7644973, media = URL raw GitHub du visuel).
Problèmes techniques : règle-les seul, sans prévenir Anthony. Aucun message de récap nécessaire,
sauf si quelque chose est impossible à régler.
