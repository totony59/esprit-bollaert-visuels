# Consignes : « L'info du jour » (actu du RC Lens qui fait réagir)

But : repérer dans la presse sportive l'actu du RC Lens la plus susceptible de faire réagir
les supporters, et en faire un post de la page « Esprit Bollaert Design » : l'info racontée
AVEC NOS MOTS, la source citée et le lien, et une question qui lance le débat.

## 1. Chercher l'actu (dernières 24 à 48 h)

Sources à parcourir (WebSearch / WebFetch) : rclens.fr, La Voix du Nord, L'Équipe, RMC Sport,
Lensois.com, Foot Mercato, Ouest-France sport, Le Parisien sport, France Bleu Nord.
Garde 3 à 5 sujets candidats.

## 2. Choisir LE sujet qui fera réagir

Bons sujets (débat, émotion, fierté) : déclaration forte du coach ou d'un joueur, compo
probable ou choix tactique, joueur en grande forme, retour de blessure (bénigne), série en
cours, classement, stat marquante, rumeur de mercato (présentée comme une rumeur), jeune
du centre de formation qui perce, record d'affluence à Bollaert, tifo, équipe féminine.

À éviter : blessures graves, décès, affaires judiciaires, violences, incidents de supporters,
polémiques arbitrales agressives, politique, tout ce qui moque un joueur ou un autre club,
toute info non vérifiable.

Vérification : un fait présenté comme sûr doit être confirmé par deux sources. Une rumeur
reste une rumeur (« d'après L'Équipe… », « ça parle de… ») et n'est jamais présentée comme acquise.

Si aucun sujet ne vaut le coup ce jour-là, ne fais pas de post « info » : remplace-le par une
question du jour (voir le RYTHME de la tâche principale).

## 3. Droits d'auteur (impératif)

- NE JAMAIS recopier le texte d'un article, ni même un paragraphe. Tout est reformulé avec
  nos mots, en 2 ou 3 phrases maximum.
- Citation directe autorisée seulement si elle est très courte (moins de 15 mots), entre
  guillemets, attribuée (ex. « … », a lâché le coach en conférence de presse), et une seule par post.
- NE JAMAIS reprendre une photo de presse ou du club. Le visuel est toujours le nôtre (gen.py « info »).
- Toujours citer la source par son nom dans le texte et mettre le lien de l'article dans le
  champ "link" du fichier de file d'attente.

## 4. Le visuel

`python3 gen.py info visuels/AAAA-MM-JJ_info_<sujet>.png "L'INFO DU JOUR" "LIGNE 1" "LIGNE 2 ?" ["APPEL À L'ACTION", défaut "Votre avis ?"]`
- Bandeau : « L'INFO DU JOUR », « MERCATO », « CONF' DE PRESSE », « LE CHIFFRE »…
- Titre très court avec NOS mots, souvent sous forme de question (ex. « LE COACH FAIT » / « TOURNER ? »).
- Regarde l'image (Read) : rien de coupé, pas de mot isolé, accents présents.

## 5. Le texte (style d'Anthony, prioritaire)

Comme si Anthony réagissait à l'info sur son téléphone : première personne, langage parlé
de supporter, phrases courtes, 1 à 3 emojis, pas de hashtag (1 maximum), pas de formules de
communicant ou « IA ». Structure :
1. Accroche perso (« Vous avez vu ça ? », « Alors là… », « Bon, j'ai lu un truc ce matin… »).
2. L'info en 1 à 3 phrases avec nos mots + la source (« d'après La Voix du Nord »).
3. Une prise de position légère ou un ressenti (sans insulter personne).
4. Une question ouverte qui oblige à donner son avis (« Vous en pensez quoi ? »,
   « Bonne idée ou pas ? », « Vous le titularisez, vous ? »).
Pas d'engagement bait (« commentez OUI », « partagez si… », « tag 3 amis »).

## 6. Publication

Fichier queue/AAAA-MM-JJTHHMM_info_<sujet>.json :
{"publish_at": "<heure de plus forte affluence, avec fuseau>", "message": "<texte>",
 "image": "visuels/<fichier>.png", "link": "<URL de l'article source>"}
Le robot ajoute le lien à la fin du texte. Commit + push (voir la tâche principale pour le
contrôle et le secours Metricool).
Comme l'actu périme vite : prépare le post « info » LE JOUR MÊME (tâche du matin), pour
publication le jour même à l'heure de pic (ou dès que possible si l'heure est passée).
