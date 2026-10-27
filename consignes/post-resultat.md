# Consignes : post de résultat (15 min après la fin du match)

Tu publies le post de résultat d'un match du RC Lens (équipe masculine) sur la page Facebook
de supporters d'Anthony, « Esprit Bollaert Design » (page de fans non officielle), environ
15 minutes après le coup de sifflet final. Le match concerné est indiqué dans le message qui
t'a lancé. Réponds en français.

Autorisation : Anthony a autorisé (25/10/2026) la publication automatique des posts de cette
page via Metricool, et le dépôt des visuels dans ce dépôt GitHub. Rien d'autre (pas de pub,
pas de boost, pas de réponses aux commentaires, pas de messages privés).

## 1. Le match est-il terminé ?

Cherche le score final sur le web : rclens.fr en priorité, plus une deuxième source
concordante (L'Équipe, Ligue 1, UEFA, Sofascore…).

RÈGLE ABSOLUE (demande d'Anthony) : on ne publie QUE si le match est RÉELLEMENT terminé.
Un match retardé, un temps additionnel long, une interruption ou une prolongation peuvent
le faire traîner. Un score en direct n'est PAS un score final. Considère le match terminé
uniquement si les DEUX sources l'indiquent explicitement comme fini (« Terminé », « Fin du
match », « FT », « Full time », « score final », compte rendu d'après-match publié) avec le
même score. Au moindre doute (« en cours », minute affichée, « mi-temps », « prolongation »,
« tirs au but », sources qui ne concordent pas), considère qu'il n'est pas terminé.

- Si le match n'est pas terminé, crée une nouvelle tâche ponctuelle avec
  mcp__claude-code-remote__create_trigger (run_once_at = dans 15 minutes, en UTC ; même
  message que celui qui t'a lancé ; même nom suivi de « (relance N) » ; initiation
  « own_followup »), puis arrête-toi sans rien publier. Jusqu'à 8 relances (2 heures
  environ). Au-delà, arrête-toi et préviens Anthony (SendUserMessage).
- Le post part environ 15 minutes après le coup de sifflet final constaté : si les sources
  montrent que le match vient juste de se terminer (moins de 10 minutes), publie quand même
  tout de suite (programmation dans 3 minutes), ne crée pas de relance pour ça.
- Si le match a été reporté ou interrompu, ne publie rien et préviens Anthony.
- Si tu n'obtiens pas de score confirmé par deux sources, ne publie rien et préviens Anthony.
  N'invente JAMAIS un score, un buteur ou un scénario.

## 2. Pas de doublon

Vérifie qu'aucun post de résultat n'existe déjà pour ce match :
- dans le dépôt : fichiers de queue/ et published/ des dernières 24 h ;
- dans Metricool (blogId 7644973, fuseau Europe/Paris ; outils via ToolSearch) : posts des
  dernières 24 h et des prochaines 24 h.
S'il en existe un, arrête-toi.

## 3. Le visuel

1. Attache le dépôt : mcp__claude-code-remote__add_repo (owner totony59, repo
   esprit-bollaert-visuels, access push), puis `git clone --depth 1`. Installe si besoin :
   `python3 -m playwright install chromium`.
2. Génère l'image (l'équipe à domicile toujours à gauche, noms courts en majuscules) :
   `python3 gen.py resultat visuels/AAAA-MM-JJ_resultat_x.png "VICTOIRE !" "DOMICILE" "SCORE_DOM" "SCORE_EXT" "EXTÉRIEUR" "LIGUE 1 · 9E JOURNÉE"`
   Le premier texte est « VICTOIRE ! », « MATCH NUL » ou « DÉFAITE » selon le résultat de
   LENS. Le fond adapté est choisi automatiquement. Si l'adversaire n'est pas dans CLUBS
   (gen.py), ajoute-le avec ses vraies couleurs (vérifiées sur le web).
3. Regarde l'image (Read) : lisible, rien de coupé, accents présents. Sinon raccourcis et régénère.
4. Commit et push sur main (`git -c user.name=Claude -c user.email=noreply@anthropic.com`).
   URL : https://raw.githubusercontent.com/totony59/esprit-bollaert-visuels/main/visuels/<fichier>.png
   Nom de fichier toujours nouveau. Si le push échoue, publie sans image et préviens Anthony.

## 4. Le texte (style d'Anthony, prioritaire)

Ultra naturel et ultra humain, comme si Anthony, supporter lensois passionné, écrivait depuis
son téléphone à la sortie du match :
- première personne, langage parlé de supporter, phrases courtes, rythme oral (« et là… ») ;
- victoire : énorme enthousiasme (majuscules sur les mots forts, « QUELLE VICTOIRE !!! »,
  points d'exclamation, 😍🔥😱) ; nul : partagé, lucide ; défaite : déçu mais fidèle, jamais
  d'insulte envers joueurs, arbitre ou adversaire ;
- buteurs et scénario seulement s'ils sont confirmés par deux sources ;
- termine TOUJOURS par la demande des tops et des flops (formulation variable, ex.
  « Allez, c'est quoi vos tops et vos flops de ce match ? ») ;
- 1 à 3 emojis, pas de hashtag (1 maximum) ;
- bannir les formules de communicant ou « IA » (« trois points précieux », « n'hésitez pas
  à », « en commentaire ci-dessous »…), pas de souvenirs personnels inventés, pas de
  politique ni de sujets sensibles, ne jamais présenter la page comme officielle.

Exemple : « QUELLE VICTOIRE !!! 🔴🟡 Menés à la pause, j'avoue j'y croyais plus trop… et là
Thauvin, puis Hazard 😱 Bollaert a tremblé ! 2-1, trois points, et on part au derby avec la
confiance. Ça fait du bien 😍 Allez, c'est quoi vos tops et vos flops de ce match ? »

## 5. Publication (robot GitHub en priorité, Metricool en secours)

Canal principal : le robot du dépôt (GitHub Actions + API Facebook, gratuit et illimité).
1. Crée le fichier queue/AAAA-MM-JJTHHMM_resultat_<adversaire>.json (UTF-8) :
   {"publish_at": "<maintenant, heure de Paris avec fuseau, ex. 2026-10-30T23:12:00+01:00>",
    "message": "<texte du post>",
    "image": "visuels/<fichier du visuel>.png"}
2. Commit et push sur main (avec le visuel). Le push déclenche normalement le robot
   « Publier sur Facebook », qui publie le post et déplace le fichier dans published/.
   Si aucun run n'a démarré au bout d'une minute, force-le :
   `gh api -X POST repos/totony59/esprit-bollaert-visuels/actions/workflows/publier.yml/dispatches -f ref=main`
3. Vérifie au bout de 2 à 3 minutes :
   - `gh api "repos/totony59/esprit-bollaert-visuels/actions/runs?per_page=3"` : le dernier
     run « Publier sur Facebook » doit être « success » ;
   - `git pull` : le fichier doit être dans published/ avec un "facebook_post_id".
   Si le run a échoué, lis le motif dans les annotations :
   `gh api repos/totony59/esprit-bollaert-visuels/check-runs/<job_id>/annotations`
   (job_id via `.../actions/runs/<run_id>/jobs`).
4. SECOURS si le robot a échoué ou n'a rien publié après 10 minutes : supprime le fichier de
   queue/ (commit + push, pour éviter un doublon plus tard), puis publie via Metricool :
   createScheduledPost avec une date dans 3 minutes, draft: false, autoPublish: true,
   providers facebook, facebookData type POST, media: [URL raw de l'image :
   https://raw.githubusercontent.com/totony59/esprit-bollaert-visuels/main/visuels/<fichier>.png].
   Quota Metricool : 20 publications par mois (le résultat est prioritaire). Préviens Anthony
   que le robot GitHub a échoué et pourquoi (ex. jeton expiré).

## 6. Récapitulatif

Envoie à Anthony (SendUserMessage) : le score, le texte publié, le canal utilisé (robot
GitHub ou Metricool en secours), et l'image (SendUserFile). Une ligne pour rappeler qu'il
peut demander une correction.
