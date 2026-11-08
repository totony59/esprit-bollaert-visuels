# Rubriques quotidiennes de la page Lens (validées par Anthony le 08/11/2026)

Chaque jour, UNE publication « maison » avec son visuel (rubriques.py), à 10h00 (heure de Paris ;
si la tâche passe après 10h, dans les 15 minutes). Exceptions :
- JOUR DE MATCH de Lens : pas de rubrique, c'est le visuel de VOTE (gen.py vote, voir strategie-portee.md §4) ;
- VEILLE DE MATCH : pas de rubrique, c'est le PRONOSTIC à 12h00 (gen.py prono).
La rubrique compte dans le maximum de 2 posts par jour ; l'info du jour ne sort EN PLUS que si elle est
vraiment forte (sinon rien).

| Jour | Rubrique | Commande |
|---|---|---|
| Lundi | CE JOUR-LÀ AU RACING : un moment de l'histoire du club à la date du jour (ou de la semaine) | python3 rubriques.py jour <out.png> "9 MAI 1998" "LENS CHAMPION" "DE FRANCE" "Vous vous en souvenez ?" |
| Mardi | LE QUIZ DU RACING : question à 3 choix ; réponse en commentaire à 19h00 | python3 rubriques.py quiz <out.png> "Question ?" "A" "B" "C" |
| Mercredi | LE CHIFFRE : un chiffre marquant en très grand + sa légende | python3 rubriques.py chiffre <out.png> "1933" "légende courte" "Vous saviez ?" |
| Jeudi | LE DUEL : deux légendes / deux buts / deux maillots ; ❤️ pour le 1er, 👍 pour le 2e | python3 rubriques.py duel <out.png> "sous-titre" "NOM 1" "NOM 2" |
| Vendredi | LE MOT CH'TI : un mot du Nord-Pas-de-Calais et son sens | python3 rubriques.py mot <out.png> "MOT" "Sens" "Vous le dites encore ?" |
| Samedi | SOUVENIRS DE BOLLAERT : une question nostalgie | python3 rubriques.py souvenir <out.png> "LIGNE 1" "LIGNE 2 ?" "Racontez-nous" |
| Dimanche | LE ONZE DE LÉGENDE : un poste par semaine (gardien, latéral droit, défenseur central…, puis entraîneur), 3 joueurs mythiques ; ❤️ / 👍 / 😮 | python3 rubriques.py onze <out.png> "LE GARDIEN" "NOM 1" "NOM 2" "NOM 3" |

Règles :
- EXACTITUDE : toute date, tout score, tout chiffre, tout sens de mot ch'ti, toute réponse de quiz confirmés
  par DEUX sources fiables (rclens.fr, L'Équipe, Wikipédia + une autre, Transfermarkt, ouvrages, dictionnaires
  de picard / ch'ti). Joueurs choisis parmi ceux qui ont vraiment marqué le club (vérifié). Sinon, change de sujet.
- Jamais deux fois le même sujet (regarde published/ et scheduled/ : fichiers *_rub-*). Le onze de légende
  suit l'ordre des postes et garde trace des gagnants (data/onze-legende.json, à créer/compléter : poste,
  3 joueurs, date ; le lundi suivant, ne rien publier à ce sujet).
- Pas de photo de joueur ni de presse, pas de logo du club, pas de paroles de chants, rien de politique.
- Texte du post : 2 à 4 phrases dans le style d'Anthony (« je », 1 à 3 emojis, 0 hashtag), puis la question
  courte reprise du visuel. Duel / onze : « Votez : ❤️ X, 👍 Y (😮 Z) 👇 ». Quiz : « Votre réponse : A, B ou C ? 👇 ».
- Fichiers : queue/AAAA-MM-JJT1000_rub-<rubrique>_<sujet>.json {"publish_at", "message", "image"} ; pour le
  quiz en plus queue/AAAA-MM-JJT1900_rub-quiz-reponse_<sujet>.json {"publish_at": "...T19:00:00+01:00",
  "comment_on": "<nom du fichier du quiz>", "message": "✅ Bonne réponse : <lettre> — <réponse + une phrase>"}.
- Regarde le visuel (Read) avant de publier : rien de coupé, accents présents ; sinon raccourcis.
