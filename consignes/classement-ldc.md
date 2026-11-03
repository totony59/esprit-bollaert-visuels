# Consignes : post « CLASSEMENT » de la Ligue des champions (phase de ligue)

Demande d'Anthony validée le 03/11/2026 : après le DERNIER match de chaque journée de la phase de
ligue de la Ligue des champions (en général le mercredi soir), publier le classement complet des
36 clubs avec le visuel classement_ldc.py. Publication automatique autorisée par Anthony.
Le dossier bretagne/ concerne une autre page : n'y touche jamais.

## 0. Y a-t-il eu une journée cette semaine ?
- La tâche tourne chaque mercredi de novembre, décembre et janvier. Si aucune journée de la phase
  de ligue ne s'est jouée cette semaine (mardi/mercredi), ou si la phase de ligue est terminée
  (8 journées jouées), arrête-toi tout de suite sans rien faire. Les phases à élimination directe
  n'ont pas de classement.
- Si data/classement-ldc-precedent.json porte déjà ce numéro de journée : déjà publié, arrête-toi.

## 1. La journée est-elle terminée ?
Les 18 matchs de la journée doivent avoir un score FINAL (pas un score en direct). Sinon, crée une
tâche ponctuelle (mcp__claude-code-remote__create_trigger, run_once_at = dans 30 minutes en UTC, même
nom suivi de « (relance) », initiation « own_followup », même message que celui qui t'a lancé), puis
arrête-toi. Jusqu'à 4 relances.

## 2. Le classement
Rang, points et différence de buts des 36 clubs, sur DEUX sources qui concordent exactement
(ex. uefa.com, L'Équipe, RC Lensois, Sports Infos, CNews, Foot Mercato). Vérifie que chaque club a
joué le bon nombre de matchs. Au moindre écart, une 3e source ; sans concordance, ne publie pas.
Écris data/classement-ldc-actuel.json (même format que data/classement-ldc-precedent.json, noms de
clubs courts en français : Paris SG, Côme, Club Bruges, Naples, Inter Milan, Bodø/Glimt…).

## 3. Le visuel
python3 classement_ldc.py visuels/AAAA-MM-JJ_classement-ldc_jN.png data/classement-ldc-actuel.json data/classement-ldc-precedent.json <fond>
- fond selon le résultat de Lens dans la journée : victoire / nul / defaite (sinon match).
- Regarde l'image (Read) : rien de coupé, Lens bien en évidence, chiffres corrects.
- Puis remplace data/classement-ldc-precedent.json par classement-ldc-actuel.json et supprime ce dernier.

## 4. Le texte (style d'Anthony)
Ultra naturel, première personne, phrases courtes, 1 à 3 emojis, 0 hashtag, aucune formule de
communicant ou « IA ». La place de Lens et ce qui a bougé, l'écart avec le top 24 (barrages) ou le
top 8, les journées restantes, un mot sur les autres clubs français si pertinent, puis une question
qui fait réagir (« On passe en barrages, vous y croyez ? »…). Ne présente jamais la page comme officielle.

## 5. Publication
queue/AAAA-MM-JJTHHMM_classement-ldc_jN.json : {"publish_at": "<maintenant, fuseau de Paris>",
"message": "<texte>", "image": "visuels/<fichier>.png"}. Commit + push (visuel et
data/classement-ldc-precedent.json inclus), git -c user.name=Claude -c user.email=noreply@anthropic.com,
git pull --rebase avant. Vérifie qu'un run de publier.yml démarre dans la minute, sinon force-le :
gh api -X POST repos/totony59/esprit-bollaert-visuels/actions/workflows/publier.yml/dispatches -f ref=main.
Puis git pull : le fichier doit être dans published/ avec un facebook_post_id. En cas d'échec :
annotations (gh api repos/totony59/esprit-bollaert-visuels/check-runs/<job_id>/annotations), corrige ;
en dernier recours Metricool (blogId 7644973, media = URL raw GitHub du visuel).
Problèmes techniques : règle-les seul, sans prévenir Anthony.
