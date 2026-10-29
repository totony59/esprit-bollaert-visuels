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
- NE JAMAIS télécharger ni republier une photo de presse ou du club comme image du post. La
  photo du média n'apparaît que via l'aperçu automatique du lien (voir section 4).
- Toujours citer la source par son nom dans le texte et mettre le lien de l'article dans le
  champ "link" du fichier de file d'attente.

## 4. Le format : post « lien » avec l'aperçu de l'article (demande d'Anthony)

Pour l'info du jour, PAS de texte sur l'image. Le post = notre texte + le lien de l'article.
Facebook génère tout seul l'aperçu de l'article (grande photo choisie par le média, titre,
nom du site) sous notre texte : c'est la façon légale d'afficher la photo du média, car c'est
le média lui-même qui la fournit via son lien. Ne JAMAIS télécharger ni republier la photo
du média comme image du post.
- Choisis de préférence un article dont l'aperçu a une belle photo (la plupart des grands
  médias en ont : L'Équipe, Foot Mercato, RMC, La Voix du Nord…).
- Dans le fichier de file d'attente : PAS de champ "image", seulement "link" (le robot publie
  alors un post lien avec aperçu).
- Ne mets PAS l'URL dans le texte (le robot l'ajoute en lien ; elle s'affiche en aperçu).

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
{"publish_at": "<maintenant, heure de Paris avec fuseau>", "message": "<texte>",
 "link": "<URL de l'article source>"}
Commit + push (voir la tâche principale pour le contrôle et le secours Metricool ; en secours,
mets l'URL à la fin du texte, sans média : Facebook affichera l'aperçu).
PUBLICATION IMMÉDIATE (demande d'Anthony du 29/10/2026) : dès que l'info est trouvée et
vérifiée, elle sort TOUT DE SUITE ("publish_at" = maintenant). On n'attend jamais l'heure de
pic pour une info : l'actu périme vite, et être le premier compte plus que l'horaire.
Seule exception : respecter 1 h 30 d'écart avec un post déjà prévu (sinon décale juste après).
