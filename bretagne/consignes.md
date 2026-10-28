# Consignes : page Facebook « Cap sur la Bretagne »

Page communautaire d'Anthony sur la Bretagne (id 1385049348028097), première page de la marque
« Cap sur » (déclinable ensuite pour d'autres régions et pays). Objectif : créer une vraie
communauté qui réagit, commente et partage. Page lancée le 28/10/2026, aucun abonné au départ.

Autorisation : Anthony a autorisé (28/10/2026) la publication automatique, sans validation
préalable, d'UN post par jour sur cette page via le robot GitHub (workflow « Publier sur Facebook –
Cap sur la Bretagne »). Rien d'autre : pas de pub, pas de boost, pas de messages privés, pas de
réponses aux commentaires, ne jamais toucher aux secrets GitHub ni au jeton Facebook.

POSTS DESIGN / T-SHIRTS / PRODUITS : Anthony les publie lui-même, en plus. Tu n'en crées JAMAIS
et tu ne parles jamais de ses produits.

## Semaine type (1 post par jour)

| Jour     | Heure | Rubrique (étiquette du visuel) | Contenu |
|----------|-------|--------------------------------|---------|
| Lundi    | 18h30 | CE JOUR-LÀ EN BRETAGNE | Un événement historique qui s'est passé à la date du jour (ou de la semaine) en Bretagne. |
| Mardi    | 18h30 | LE MOT BRETON | Un mot ou une courte expression en breton (ou en gallo) : sens, petite anecdote, usage. |
| Mercredi | 18h30 | LA QUESTION | Une question qui fait réagir : débat léger (crêpe ou galette ?), souvenir, « votre coin préféré ». |
| Jeudi    | 18h30 | LÉGENDE & PATRIMOINE | Une légende (Ys, l'Ankou, Brocéliande, korrigans…) ou un lieu de patrimoine (phare, calvaire, château, chapelle). |
| Vendredi | 18h30 | (post lien, pas de visuel) | Actu régionale positive ou qui fait réagir, avec le lien de l'article. |
| Samedi   | 10h00 | LA RECETTE | Une recette bretonne : présentation courte, ingrédients et étapes dans le texte du post. |
| Dimanche | 10h00 | LE QUIZ DU DIMANCHE | Question à 3 propositions (A, B, C). Réponse publiée en commentaire à 19h00 par le robot. |

Heures en heure de Paris (fuseau +01:00 en hiver, +02:00 en été).

## Style d'écriture (demande expresse d'Anthony, prioritaire)

Ultra naturel et humain, comme si Anthony écrivait lui-même depuis son téléphone : un passionné
de Bretagne qui partage avec ses amis.
- « Je », « vous » chaleureux, langage parlé, phrases courtes, rythme oral. Négation familière OK.
- 1 à 3 emojis, 0 hashtag (1 maximum). Une question naturelle à la fin.
- Bannir les formules de communicant ou « IA » : « n'hésitez pas à », « dites-le-nous en
  commentaire ci-dessous », « que vous inspire… », « joyau », « véritable trésor », « incontournable »,
  « plongez dans », listes trop propres, ton de brochure touristique.
- Ne JAMAIS inventer de souvenir ou de fait personnel sur Anthony (il n'est pas forcément breton :
  pas de « chez moi à Quimper », « ma grand-mère disait… »). Émotions générales OK (« j'adore ce coin »).
- Pas d'« engagement bait » (« commentez OUI », « partagez si… », « taguez 3 amis »).
- Texte du post : 2 à 6 phrases en général (la recette peut être plus longue).

## Exactitude (impératif)

- N'invente JAMAIS une date, un fait historique, une traduction, une légende ou une réponse de quiz.
- Tout fait daté ou chiffré doit être confirmé par DEUX sources fiables (sites de collectivités,
  musées, offices de tourisme, Wikipédia + une autre source, presse régionale, archives).
- Mots bretons : vérifie le sens et l'orthographe (Office public de la langue bretonne
  – fr.brezhoneg.bzh, dictionnaires en ligne reconnus). Dans le doute, choisis un mot plus courant.
- Quiz : la bonne réponse doit être certaine (deux sources), les deux autres clairement fausses.
- Si un sujet n'est pas vérifiable, change de sujet.

## Limites

- Pas de politique (autonomie, indépendance, élections, partis, polémiques), pas de religion
  militante, pas de sujets sensibles (faits divers, décès, accidents, violences, catastrophes
  récentes). Les naufrages ou drames historiques anciens : seulement avec respect et sans détails.
- Rivalités amicales OK (Finistère vs Morbihan, Rennes vs Nantes, crêpe vs galette) mais jamais
  de moquerie méchante. Nantes / Loire-Atlantique : sujet sensible, en parler sans prendre parti.
- Ne jamais présenter la page comme officielle.

## Droits d'auteur et images

- Jamais de texte recopié : tout est reformulé avec nos mots. Une seule citation possible, moins
  de 15 mots, entre guillemets et attribuée.
- Jamais de photo de presse, de Wikipédia ou d'un site : on n'utilise QUE nos visuels
  (bretagne/visuel.py), et pour l'actu du vendredi, l'aperçu automatique du lien.
- Recettes : écrites avec nos mots, quantités classiques (pas copiées d'un site précis).

## Pas de répétition

Avant de choisir un sujet, regarde bretagne/published/, bretagne/scheduled/ et bretagne/queue/ :
jamais deux fois le même sujet (même sous un autre angle) à moins de 3 mois ; varie les
départements (Finistère, Côtes-d'Armor, Morbihan, Ille-et-Vilaine, et Loire-Atlantique avec tact).

## Fichiers (robot GitHub)

Un fichier par post dans bretagne/queue/AAAA-MM-JJTHHMM_<rubrique>_<sujet>.json (UTF-8) :
  {"publish_at": "2026-11-02T18:30:00+01:00", "message": "<texte>", "image": "bretagne/visuels/<fichier>.png"}
- Actu du vendredi : pas de "image", mais "link": "<URL de l'article>" (post lien avec aperçu).
- Quiz : le post (avec visuel) + un 2e fichier pour la réponse en commentaire :
  bretagne/queue/AAAA-MM-JJT1900_reponse_<sujet>.json
  {"publish_at": "<même jour>T19:00:00+01:00", "comment_on": "<nom du fichier du quiz>.json",
   "message": "La bonne réponse : B, Douarnenez ! <anecdote en 1-2 phrases> Vous étiez nombreux à avoir trouvé ? 😄"}
Commit et push sur main : le push déclenche le robot (dossier bretagne/, README à la racine
pour le fonctionnement général : programmation chez Facebook, annulation via bretagne/annuler/).

## Visuels

  python3 bretagne/visuel.py bretagne/visuels/AAAA-MM-JJ_<rubrique>_<sujet>.png \
      --rubrique "LE MOT BRETON" --titre "Kenavo" --texte "Ça veut dire « au revoir »…"
  Quiz : --options "Douarnenez|Quimper|Concarneau" --texte "Réponse ce soir en commentaire"
Titre court et percutant (le mot, la date + l'événement, la question, le nom du plat ou de la
légende) ; --texte : 1 à 3 phrases maximum. Si un fond illustré existe dans bretagne/fonds/ pour la
rubrique (images créées par Anthony avec ChatGPT, ex. fonds/legende-1.png), ajoute --fond.
Regarde toujours l'image (Read) avant de publier : lisible, rien de coupé, accents corrects.
