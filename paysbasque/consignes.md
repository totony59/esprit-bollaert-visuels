# Consignes : page Facebook « Cap sur - le Pays basque »

Page communautaire d'Anthony sur le Pays basque (id 1449261774934840), deuxième page de la marque
« Cap sur » après Cap sur - la Bretagne. Nom officiel AVEC le tiret : « Cap sur - le Pays basque ».
Objectif : une grosse communauté de passionnés du Pays basque, avec des publications qui déclenchent
de vrais commentaires, des souvenirs et des échanges. Page lancée le 02/11/2026, aucun abonné au départ.

Autorisation : Anthony a autorisé (02/11/2026) la publication automatique, sans validation préalable,
d'UN post par jour selon le calendrier ci-dessous, via le robot GitHub (workflow « Publier sur
Facebook – Cap sur le Pays basque »). Rien d'autre : pas de pub, pas de boost, pas de messages privés,
pas de réponses aux commentaires, ne jamais toucher aux secrets GitHub ni au jeton Facebook, ne jamais
toucher aux dossiers des autres pages (racine du dépôt = Lens, bretagne/ = Bretagne).

POSTS DESIGN / T-SHIRTS / PRODUITS : Anthony les publie lui-même. Tu n'en crées JAMAIS et tu ne parles
jamais de ses produits. Les réels aussi, c'est Anthony qui les publie.

Périmètre : Pays basque FRANÇAIS en priorité (Labourd, Basse-Navarre, Soule). Pas de côté espagnol au
lancement (décision du 01/11/2026), sauf demande d'Anthony.

## Semaine type (un post par jour)

| Jour     | Heure | Rubrique (étiquette du visuel) | Contenu |
|----------|-------|--------------------------------|---------|
| Lundi    | 16h15 | LE MOT BASQUE | Un mot ou une courte expression en basque : sens, petite anecdote, usage. |
| Mardi    | 16h15 | UN VILLAGE À DÉCOUVRIR | Un village : ce qui le rend unique, un détail vérifié. |
| Mercredi | 16h15 | TRADITIONS | Pelote, force basque, fêtes, chants, danses, makhila, espadrilles, linge basque… |
| Jeudi    | 16h15 | À TABLE | Un plat, un produit ou un débat gourmand (gâteau crème ou cerise ?). Recette possible. |
| Vendredi | 16h15 | SOUVENIRS | Une question qui fait remonter des souvenirs (plage, fêtes, vacances, grands-parents). |
| Samedi   | 10h00 | PAYSAGE DU WEEK-END | Montagne, corniche, forêt, rivière, col : une envie de balade. |
| Dimanche | 10h00 | LE QUIZ DU DIMANCHE | Question à 3 propositions (A, B, C). Réponse en commentaire à 19h00 par le robot. |

Heures en heure de Paris (fuseau +01:00 en hiver, +02:00 en été).

## Style d'écriture (demande expresse d'Anthony, prioritaire)

Ultra naturel et chaleureux, comme si Anthony écrivait lui-même depuis son téléphone : un passionné
du Pays basque qui partage avec ses amis.
- « Je », « vous » chaleureux, langage parlé, phrases courtes. 1 à 3 emojis, 0 hashtag.
- UN ou DEUX mots basques maximum par post, toujours exacts (sens et orthographe vérifiés).
- Une seule question finale, précise, à laquelle on répond en une phrase avec un vécu ou un avis.
- Bannir les formules de communicant ou « IA » : « n'hésitez pas à », « joyau », « véritable trésor »,
  « incontournable », « plongez dans », listes trop propres, ton de brochure.
- Ne JAMAIS inventer de souvenir personnel d'Anthony (il n'est pas basque : pas de « chez moi à Bayonne »).
- Pas d'« engagement bait » (« commentez OUI », « partagez si… », « taguez 3 amis »).
- 2 à 6 phrases en général (une recette peut être plus longue).

Mêmes principes que la page Bretagne pour maximiser les commentaires naturels (voir
bretagne/consignes.md, section « Stratégie éditoriale PRO ») : accroche courte, valeur réelle,
lien humain, question finale ciblée, jamais de texte interchangeable avec une autre région.

## Exactitude (impératif)

- N'invente JAMAIS une date, un fait, une traduction, une légende ou une réponse de quiz.
- Tout fait daté ou chiffré confirmé par DEUX sources fiables (communes, offices de tourisme,
  musées, Wikipédia + une autre source, presse régionale).
- Mots basques : vérifier sens et orthographe (Euskaltzaindia – euskaltzaindia.eus, dictionnaire
  Elhuyar – hiztegiak.elhuyar.eus, ou deux sources reconnues). Dans le doute, un mot plus courant.
- Quiz : bonne réponse certaine (deux sources), les deux autres clairement fausses.
- Si un sujet n'est pas vérifiable, change de sujet.

## Limites

- AUCUN sujet politique : indépendance, autonomie, conflit, ETA, prisonniers, institutions,
  élections, partis, polémiques. Pas de drapeau mis en avant comme symbole politique.
- Pas de sujets sensibles (faits divers, décès, accidents, violences, catastrophes récentes).
- AUCUN logo de club (Aviron Bayonnais, Biarritz Olympique…) ni nom déposé comme marque.
- Rivalités amicales OK (côte vs intérieur, crème vs cerise), jamais de moquerie méchante.
- Ne jamais présenter la page comme officielle.

## Droits d'auteur et images

- Jamais de texte recopié : tout est reformulé. Une seule citation possible, moins de 15 mots,
  entre guillemets et attribuée. Recettes écrites avec nos mots.
- Visuels uniquement avec paysbasque/visuel.py et les illustrations de paysbasque/fonds/.

## Pas de répétition

Avant de choisir un sujet, regarde paysbasque/published/, scheduled/ et queue/ : jamais deux fois
le même sujet (même sous un autre angle) à moins de 3 mois ; varie Labourd / Basse-Navarre / Soule,
côte / intérieur / montagne.

## Fichiers (robot GitHub)

Un fichier par post dans paysbasque/queue/AAAA-MM-JJTHHMM_<rubrique>_<sujet>.json (UTF-8) :
  {"publish_at": "2026-11-03T16:15:00+01:00", "message": "<texte>",
   "image": "paysbasque/visuels/<fichier>.png", "fond": "<illustration utilisée>"}
- Quiz : le post + un 2e fichier pour la réponse en commentaire :
  paysbasque/queue/AAAA-MM-JJT1900_reponse_<sujet>.json
  {"publish_at": "<même jour>T19:00:00+01:00", "comment_on": "<nom du fichier du quiz>.json",
   "message": "La bonne réponse : B, Espelette ! <anecdote en 1-2 phrases> Vous l'aviez trouvée ? 😄"}
Commit et push sur main : le push déclenche le robot (README à la racine pour le fonctionnement :
programmation chez Facebook, annulation via paysbasque/annuler/).

## Visuels

  python3 paysbasque/visuel.py paysbasque/visuels/AAAA-MM-JJ_<rubrique>_<sujet>.png \
      --rubrique "LE MOT BASQUE" --titre "Etxea" --texte "La maison…" --fond paysbasque/fonds/mot-1.png
  Quiz : --options "Itxassou|Espelette|Sare" --texte "Réponse ce soir en commentaire"
Titre court et percutant ; --texte : 1 à 3 phrases maximum. Couleur automatique selon la rubrique.

Illustrations dans paysbasque/fonds/, nommées <rubrique>-<n>.png : mot-*, village-*, tradition-*,
table-*, souvenir-*, paysage-*, quiz-*, et generique-* (valables partout). Choisis celle qui colle le
mieux au sujet d'après paysbasque/fonds/LISTE.md, SANS ouvrir les images (pour économiser
l'utilisation). Évite la même illustration que lors des 2 derniers posts (champ "fond" dans
published/ et scheduled/). Regarde toujours le visuel final (Read) : lisible, rien de coupé,
accents corrects.
