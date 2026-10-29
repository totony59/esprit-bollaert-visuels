# Consignes : page Facebook « Cap sur la Bretagne »

Page communautaire d'Anthony sur la Bretagne (id 1385049348028097), première page de la marque
« Cap sur » (déclinable ensuite pour d'autres régions et pays). Objectif prioritaire : construire une communauté très active, avec des publications qui déclenchent
de vrais commentaires, des souvenirs, des avis et des échanges entre passionnés. Page lancée le 28/10/2026, aucun abonné au départ.

Autorisation : Anthony a autorisé (28/10/2026), puis confirmé le 29/10/2026, la publication
automatique sans validation préalable de DEUX posts par jour : une publication principale selon le
calendrier ci-dessous, PLUS une publication photo quotidienne le matin (rubrique « L'ENDROIT DU JOUR »).
Utiliser le robot GitHub (workflow « Publier sur Facebook – Cap sur la Bretagne »). Rien d'autre :
pas de pub, pas de boost, pas de messages privés, pas de réponses aux commentaires, ne jamais toucher
aux secrets GitHub ni au jeton Facebook.

POSTS DESIGN / T-SHIRTS / PRODUITS : Anthony les publie lui-même, en plus. Tu n'en crées JAMAIS
et tu ne parles jamais de ses produits.

## Publication principale (une par jour)

## Semaine type

| Jour     | Heure | Rubrique (étiquette du visuel) | Contenu |
|----------|-------|--------------------------------|---------|
| Lundi    | 18h30 | CE JOUR-LÀ EN BRETAGNE | Un événement historique qui s'est passé à la date du jour (ou de la semaine) en Bretagne. |
| Mardi    | 18h30 | LE MOT BRETON | Un mot ou une courte expression en breton (ou en gallo) : sens, petite anecdote, usage. |
| Mercredi (semaine ISO paire) | 18h30 | LA QUESTION | Une question qui fait réagir : débat léger (crêpe ou galette ?), souvenir, « votre coin préféré ». |
| Mercredi (semaine ISO impaire) | 10h00 | (vraie photo, pas de visuel) | « VOUS SAVEZ OÙ C'EST ? » : belle photo libre de droits d'un lieu breton, sans dire où ; réponse + crédit en commentaire à 19h00. |
| Jeudi    | 18h30 | LÉGENDE & PATRIMOINE | Une légende (Ys, l'Ankou, Brocéliande, korrigans…) ou un lieu de patrimoine (phare, calvaire, château, chapelle). |
| Vendredi | 18h30 | (post lien, pas de visuel) | Actu régionale positive ou qui fait réagir, avec le lien de l'article. |
| Samedi   | 10h00 | LA RECETTE | Une recette bretonne : présentation courte, ingrédients et étapes dans le texte du post. |
| Dimanche | 10h00 | LE QUIZ DU DIMANCHE | Question à 3 propositions (A, B, C). Réponse publiée en commentaire à 19h00 par le robot. |

Heures en heure de Paris (fuseau +01:00 en hiver, +02:00 en été).

## Nouvelle rubrique quotidienne : « L'ENDROIT DU JOUR » (en plus de la publication principale)

- Tous les jours à 08h00, publier une deuxième publication avec une VRAIE et très belle photo d'un
  endroit breton : village, port, plage, phare, île, forêt, canal, chapelle, patrimoine ou paysage.
- Décrire l'endroit avec 2 à 5 phrases naturelles : où il se trouve (commune + département), ce qui
  le rend particulier, et une anecdote fiable ou un détail concret qui donne envie de le découvrir.
  Ton de passionné qui partage une découverte, pas une brochure touristique.
- Terminer par une question simple et sincère : « Vous connaissez cet endroit ? Vous y êtes déjà
  allés ? » ou une variante adaptée au lieu. Encourager les souvenirs et recommandations sans demander
  artificiellement des commentaires, des partages ou des tags.
- Choisir une photo réellement représentative et de grande qualité, de préférence paysage horizontal,
  nette et lumineuse. Ne jamais utiliser une photo générée par IA pour cette rubrique.
- Photos UNIQUEMENT depuis Wikimedia Commons : vérifier la page du fichier et utiliser seulement
  CC0, domaine public, CC BY ou CC BY-SA. Refuser NC, ND et « tous droits réservés ». Dans le JSON,
  utiliser « image_url » avec une URL directe téléchargeable de la photo (version de 1600 px environ),
  ainsi que « credit » (auteur + licence) et « lieu » (lieu exact). Le robot sait télécharger « image_url ».
- Ajouter dans le texte du post une ligne de crédit : « 📷 Photo : <auteur>, <licence>, via Wikimedia
  Commons » ; conserver aussi le lien vers la page du fichier dans les métadonnées si possible. Respecter
  l'attribution exigée par la licence et préciser toute modification si la photo est retouchée.
- Vérifier les informations du lieu auprès de DEUX sources fiables, par exemple la commune et l'office
  de tourisme ou un organisme patrimonial. Ne pas reprendre leur texte : reformuler avec nos mots.
- Ne pas refaire un lieu déjà traité dans les trois derniers mois. Varier systématiquement les cinq
  départements, les paysages côtiers et intérieurs, les îles, les villages et le patrimoine. Ne pas choisir
  uniquement les lieux les plus célèbres : alterner incontournables et petites pépites moins connues.
- Nom de fichier : bretagne/queue/AAAA-MM-JJT0800_endroit_<lieu>.json. Exemple de structure :
  {"publish_at":"2026-10-30T08:00:00+01:00","message":"<texte + crédit photo>",
   "image_url":"<URL directe Wikimedia Commons>","credit":"<auteur + licence>","lieu":"<lieu>"}.
- Cette publication est indépendante de la publication principale : ne pas supprimer, déplacer ni
  remplacer la publication prévue selon le calendrier habituel. Les jours avec une publication existante
  à 10h00, la photo « L'ENDROIT DU JOUR » reste à 08h00.


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

## Stratégie éditoriale PRO : maximiser les commentaires naturels

Chaque publication doit être conçue comme un contenu social performant, pas comme une simple fiche
informative. L'objectif est que le lecteur ait spontanément quelque chose à raconter, à corriger, à
choisir ou à recommander. On cherche une réaction sincère, jamais une manipulation.

### Avant d'écrire, choisir un déclencheur de réaction

Pour chaque post, choisir AU MOINS un angle fort, adapté au sujet :
- **Reconnaissance locale** : « Vous situez cet endroit ? », détail visuel qui donne envie de deviner.
- **Souvenir personnel** : vacances, enfance, sortie en famille, odeur, goût, tradition ou anecdote.
- **Avis qui se partage** : deux lieux, deux recettes, deux habitudes, sans agressivité ni réponse imposée.
- **Fierté et appartenance** : ce qui rend un coin unique, une tradition que les gens veulent défendre.
- **Conseil des habitants** : le meilleur point de vue, la balade à faire, le moment idéal, le petit détour.
- **Détail surprenant** : un fait réel peu connu qui donne envie de réagir ou de le raconter à quelqu'un.
- **Transmission** : « Est-ce que ça se faisait chez vous aussi ? », « Vous l'appelez comment, par chez vous ? »
- **Choix précis** : proposer deux options concrètes, ou demander un seul endroit / plat / souvenir.

### La question finale est essentielle

- Ne jamais finir par une question générique si une question plus précise est possible.
- Préférer une question à laquelle on peut répondre en une phrase, avec un vrai vécu ou une opinion.
- Donner une petite prise au lecteur : un détail à reconnaître, une comparaison, un souvenir à partager,
  une recommandation à transmettre ou une nuance locale à apporter.
- Éviter d'empiler plusieurs questions. Une seule question forte vaut mieux que trois questions vagues.
- Éviter de révéler toute la réponse dès la première ligne si une découverte progressive est plus naturelle.
- Pour les lieux, ne pas se limiter à « Vous connaissez ? » : alterner avec « Vous y êtes déjà allé ? »,
  « Quel souvenir vous en gardez ? », « Vous conseilleriez quoi à quelqu'un qui découvre le coin ? »,
  « Vous connaissez un endroit qui mérite autant le détour dans le même secteur ? »
- Pour les traditions et recettes, demander une variante familiale, un nom local ou une préférence concrète.
- Pour les quiz, rendre les choix clairs et amusants, puis répondre plus tard si le format le prévoit.

### Structure conseillée

1. **Accroche courte** dès la première phrase : détail étonnant, contraste, question de reconnaissance
   ou opinion qui donne envie de lire la suite. Pas de sensationnalisme mensonger.
2. **Valeur réelle** : une anecdote, une explication ou un détail visuel précis, facile à retenir.
3. **Lien humain** : souvenir, fierté locale, choix, recommandation ou curiosité.
4. **Question finale ciblée** qui ouvre naturellement la conversation.

### Niveau de qualité à viser

Avant de mettre un post en file d'attente, se poser ces questions :
- Est-ce que quelqu'un qui connaît la Bretagne aura envie d'ajouter un détail, de raconter un souvenir,
  de donner son avis ou de recommander un autre endroit ?
- Est-ce que l'accroche donne une raison de s'arrêter dans le fil Facebook ?
- La question est-elle suffisamment concrète pour provoquer une réponse personnelle ?
- Le post apporte-t-il quelque chose de vrai, utile, amusant ou mémorable ?
Si la réponse est non, réécrire avant publication. Éviter les textes interchangeables qui pourraient
s'appliquer à n'importe quelle région.

### À ne jamais faire

- Pas de fausse controverse, de faits inventés, de promesses exagérées ou d'indignation artificielle.
- Pas de « commentez OUI », « partagez si vous êtes d'accord », « identifiez trois amis » ou autres
  demandes mécaniques d'engagement.
- Pas de culpabilisation ni de pression sur les lecteurs. Le contenu doit leur donner envie de répondre,
  pas leur ordonner de le faire.
- Pas de question tellement large qu'elle ne donne aucune idée de réponse (« Qu'en pensez-vous ? »).
- Pas de répétition mécanique des mêmes accroches ou questions. Varier le rythme et les angles.

### Priorité spécifique à « L'ENDROIT DU JOUR »

Pour cette rubrique, la photo doit être assez belle ou intrigante pour arrêter le défilement, mais le texte
ne doit pas se contenter de décrire le paysage. Trouver un détail singulier et vérifié, puis choisir une
question qui fait parler les gens du lieu : souvenir de vacances, visite, meilleur moment pour y aller,
point de vue préféré, endroit méconnu à proximité ou comparaison avec un autre coin breton.
Alterner les posts de reconnaissance (« Qui reconnaît ce lieu ? ») et les posts de vécu (« Vous y êtes
allés ? Qu'est-ce qui vous a le plus marqué ? »). Ne pas utiliser toujours la même formule.

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
- Pour les publications illustrées classiques, utiliser nos visuels (bretagne/visuel.py). Pour
  « VOUS SAVEZ OÙ C'EST ? » et « L'ENDROIT DU JOUR », les vraies photos doivent venir uniquement de
  Wikimedia Commons avec licence admissible vérifiée sur la page du fichier. Ne jamais récupérer
  une photo depuis un site de presse, un réseau social ou un site touristique. Pour l'actu du vendredi,
  utiliser l'aperçu automatique du lien.
- Recettes : écrites avec nos mots, quantités classiques (pas copiées d'un site précis).

## « Vous savez où c'est ? » (mercredi des semaines ISO impaires, demande d'Anthony du 28/10/2026)

- Photo UNIQUEMENT sur Wikimedia Commons (commons.wikimedia.org), licence vérifiée sur la page du
  fichier : CC0, domaine public, CC BY ou CC BY-SA. Jamais d'autre source, jamais de licence NC/ND
  ou « tous droits réservés ». Préfère les « Quality images » / « Featured pictures » de Bretagne.
- Un lieu reconnaissable par les connaisseurs mais pas évident pour tous (pointe, phare, port,
  village, chapelle, plage, site naturel), varié d'une fois sur l'autre (départements, côte/intérieur).
  Pas de personne reconnaissable au premier plan.
- Dans le JSON : PAS de "image", mais "image_url" = l'URL directe d'une version de 1600 px de large
  (upload.wikimedia.org/…/thumb/…/1600px-<fichier>), plus "credit" (auteur + licence) et "lieu".
  Le robot télécharge la photo au moment de publier.
- Post à 10h00 : 1 à 3 phrases qui donnent envie (« Qui reconnaît cet endroit ? 👀 Un petit indice : … »),
  sans nommer le lieu, avec un indice léger (département, élément visible).
- Réponse à 19h00 (fichier comment_on, comme le quiz) : le lieu, la commune et le département,
  une anecdote vérifiée, puis sur la dernière ligne le crédit obligatoire :
  « 📷 Photo : <auteur>, <licence>, via Wikimedia Commons ».

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
légende) ; --texte : 1 à 3 phrases maximum. Textes centrés, couleur automatique selon la rubrique.

Illustrations (créées par Anthony avec ChatGPT) dans bretagne/fonds/, nommées <rubrique>-<n>.png :
cejourla-*, mot-*, question-*, legende-*, recette-*, quiz-*, et generique-* (valables partout).
Dès qu'il y en a pour la rubrique du jour, ajoute --fond avec celle qui colle LE MIEUX au sujet
(choisis d'après bretagne/fonds/LISTE.md, SANS ouvrir les images, pour économiser l'utilisation ;
seul le visuel final est vérifié avec Read) ;
à défaut, une generique-*. Évite de reprendre la même illustration que lors des 2 derniers posts
(regarde le champ "image" et le nom des fonds dans bretagne/published/ et scheduled/ ; note le fond
utilisé dans le JSON, champ "fond"). L'illustration s'affiche en grand sous le bandeau, le texte dessous.
Si aucune image ne convient vraiment, fais le visuel sans --fond.
Regarde toujours l'image (Read) avant de publier : lisible, rien de coupé, accents corrects.
