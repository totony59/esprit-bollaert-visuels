"""Publie sur la page Facebook les posts de la file d'attente (queue/) arrivés à échéance.

Chaque post est un fichier JSON dans queue/ :
{
  "publish_at": "2026-10-31T10:00:00+01:00",   # heure de publication (avec fuseau)
  "message": "Texte du post…",
  "image": "visuels/xxx.png",                   # optionnel : chemin dans le dépôt
  "link": "https://…"                            # optionnel : lien vers l'article source
}

Un post dont l'heure est à plus de 15 min est confié tout de suite au programmateur de
Facebook (il part dans scheduled/) : Facebook le publie à la minute près.
Après publication immédiate, le fichier part dans published/ avec l'identifiant du post Facebook.
Un post en retard de plus de MAX_RETARD_H heures n'est pas publié (il part dans skipped/),
pour ne jamais sortir un « jour de match » après le match.

Variables d'environnement : FB_PAGE_ID, FB_PAGE_TOKEN (secrets GitHub), DRY_RUN=1 pour tester.
Commentaire différé (ex. réponse d'un quiz) : un fichier de queue/ avec "comment_on" (nom du fichier
du post visé, ex. "2026-11-01T1000_quiz_x.json") et "message" est publié EN COMMENTAIRE sous ce
post à l'heure "publish_at" (Facebook ne programme pas les commentaires : le robot attend l'heure).

DOSSIER_PAGE (optionnel) : sous-dossier de la page (ex. « bretagne ») qui contient ses propres
queue/, published/, scheduled/, skipped/ et annuler/. Vide = dossiers à la racine (page Lens).
Les chemins d'image restent relatifs à la racine du dépôt.
"""
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

API = "https://graph.facebook.com/v23.0"
ROOT = pathlib.Path(__file__).resolve().parent
BASE = ROOT / os.environ.get("DOSSIER_PAGE", "").strip()   # dossier propre à la page
QUEUE, PUBLISHED, SKIPPED = BASE / "queue", BASE / "published", BASE / "skipped"
SCHEDULED = BASE / "scheduled"   # posts confiés au programmateur de Facebook
ANNULER = BASE / "annuler"       # déposer ici un fichier du même nom pour annuler un post programmé
MAX_RETARD_H = 6
PROG_MIN = dt.timedelta(minutes=15)  # Facebook exige au moins 10 min d'avance
PROG_MAX = dt.timedelta(days=25)     # et au plus ~30 jours


def appel(url, champs, fichier=None):
    """POST multipart vers l'API Graph ; renvoie le JSON de réponse."""
    limite = uuid.uuid4().hex
    corps = bytearray()
    for k, v in champs.items():
        corps += f"--{limite}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    if fichier:
        corps += (f"--{limite}\r\nContent-Disposition: form-data; name=\"source\"; "
                  f"filename=\"{fichier.name}\"\r\nContent-Type: "
                  f"{'image/png' if fichier.suffix.lower() == '.png' else 'image/jpeg'}\r\n\r\n").encode()
        corps += fichier.read_bytes() + b"\r\n"
    corps += f"--{limite}--\r\n".encode()
    req = urllib.request.Request(url, data=bytes(corps), method="POST",
                                 headers={"Content-Type": f"multipart/form-data; boundary={limite}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        tok = champs.get("access_token", "")
        if tok:
            detail = detail.replace(tok, "***")  # ne jamais afficher le jeton
        print(f"::error::Erreur API Facebook {e.code} sur {url.split('?')[0].rsplit('/', 1)[-1]} : {detail}")
        raise SystemExit(1)


def telecharger(url):
    """Télécharge une photo libre de droits (ex. Wikimedia Commons) dans un fichier temporaire."""
    import tempfile
    ext = ".png" if url.lower().split("?")[0].endswith(".png") else ".jpg"
    req = urllib.request.Request(url, headers={"User-Agent": "CapSurPublication/1.0 (github.com/totony59)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    f = pathlib.Path(tempfile.mkdtemp()) / f"photo{ext}"
    f.write_bytes(data)
    return f


def publier(post, page_id, token, quand=None):
    """Publie maintenant, ou programme chez Facebook si `quand` (datetime futur) est donné."""
    if post.get("image_url") and not post.get("image"):
        post = dict(post, image=str(telecharger(post["image_url"])))
    image = post.get("image")
    lien = post.get("link")
    prog = {}
    if quand is not None:
        prog = {"published": "false", "scheduled_publish_time": str(int(quand.timestamp()))}
    if image and lien:
        # sur une photo, le lien va à la fin de la légende (cliquable)
        post = dict(post, message=f"{post['message']}\n\n👉 {lien}")
    if not image and lien:
        rep = appel(f"{API}/{page_id}/feed", {"message": post["message"], "link": lien, **prog, "access_token": token})
        return rep.get("id")
    if image:
        f = ROOT / image
        if not f.exists():
            raise SystemExit(f"Image introuvable : {image}")
        rep = appel(f"{API}/{page_id}/photos", {"caption": post["message"], **prog, "access_token": token}, f)
        return rep.get("post_id") or rep.get("id")
    rep = appel(f"{API}/{page_id}/feed", {"message": post["message"], **prog, "access_token": token})
    return rep.get("id")


def commenter(post, token):
    """Publie post["message"] en commentaire sous le post dont le fichier est post["comment_on"]."""
    cible = post["comment_on"]
    for d in (PUBLISHED, SCHEDULED):
        f = d / cible
        if f.exists():
            fb_id = json.loads(f.read_text(encoding="utf-8")).get("facebook_post_id")
            if fb_id:
                rep = appel(f"{API}/{fb_id}/comments", {"message": post["message"], "access_token": token})
                return rep.get("id")
    raise SystemExit(f"Post visé introuvable ou sans facebook_post_id : {cible}")


def verifier(page_id, token):
    """Vérifie la clé sans rien publier : lit le nom de la page avec le jeton."""
    if not page_id or not token:
        manquants = [n for n, v in (("FB_PAGE_ID", page_id), ("FB_PAGE_TOKEN", token)) if not v]
        print(f"::error::Secret(s) absent(s) : {', '.join(manquants)}")
        sys.exit(1)
    q = urllib.parse.urlencode({"fields": "id,name", "access_token": token})
    try:
        with urllib.request.urlopen(f"{API}/me?{q}", timeout=30) as r:
            moi = json.loads(r.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace").replace(token, "***")
        print(f"::error::Jeton refusé par Facebook ({e.code}) : {detail}")
        sys.exit(1)
    if str(moi.get("id")) != page_id.strip():
        print(f"::error::Le jeton correspond à « {moi.get('name')} » (id {moi.get('id')}), "
              f"mais FB_PAGE_ID vaut {page_id.strip()} : jeton utilisateur au lieu du jeton de PAGE, ou mauvais id.")
        sys.exit(1)
    print(f"::notice::OK : jeton de page valide pour « {moi.get('name')} » (id {moi.get('id')}). Rien n'a été publié.")


def annuler(page_id, token, dry):
    """annuler/<nom>.json : supprime le post programmé correspondant (chez Facebook ou dans queue/)."""
    demandes = sorted(ANNULER.glob("*.json")) if ANNULER.exists() else []
    for d in demandes:
        nom = d.name
        SKIPPED.mkdir(exist_ok=True)
        if (QUEUE / nom).exists():
            post = json.loads((QUEUE / nom).read_text(encoding="utf-8"))
            (QUEUE / nom).unlink()
        elif (SCHEDULED / nom).exists():
            post = json.loads((SCHEDULED / nom).read_text(encoding="utf-8"))
            if not dry:
                if not token:
                    sys.exit("Secret FB_PAGE_TOKEN manquant : impossible d'annuler.")
                q = urllib.parse.urlencode({"access_token": token})
                req = urllib.request.Request(f"{API}/{post['facebook_post_id']}?{q}", method="DELETE")
                try:
                    urllib.request.urlopen(req, timeout=30).read()
                except urllib.error.HTTPError as e:
                    detail = e.read().decode(errors="replace").replace(token, "***")
                    print(f"::error::Annulation refusée par Facebook pour {nom} ({e.code}) : {detail}")
                    raise SystemExit(1)
            (SCHEDULED / nom).unlink()
        else:
            print(f"::warning::Rien à annuler pour {nom} (déjà publié ou introuvable).")
            d.unlink()
            continue
        post["skipped_reason"] = "annulé à la demande"
        (SKIPPED / nom).write_text(json.dumps(post, ensure_ascii=False, indent=2), encoding="utf-8")
        d.unlink()
        print(f"Annulé : {nom}")


def main():
    dry = os.environ.get("DRY_RUN") == "1"
    page_id = os.environ.get("FB_PAGE_ID", "").strip()
    token = os.environ.get("FB_PAGE_TOKEN", "").strip()
    if os.environ.get("VERIFIER") == "1":
        verifier(page_id, token)
        return
    maintenant = dt.datetime.now(dt.timezone.utc)
    annuler(page_id, token, dry)
    fichiers = sorted(QUEUE.glob("*.json")) if QUEUE.exists() else []
    if not fichiers:
        print("File d'attente vide, rien à publier.")
        return
    a_traiter = []
    for f in fichiers:
        post = json.loads(f.read_text(encoding="utf-8"))
        quand = dt.datetime.fromisoformat(post["publish_at"])
        if quand.tzinfo is None:
            sys.exit(f"{f.name} : publish_at doit contenir le fuseau (ex. +01:00).")
        if quand <= maintenant:
            a_traiter.append((f, post, quand, "maintenant"))
        elif post.get("comment_on"):
            continue  # un commentaire ne se programme pas chez Facebook : on attend l'heure
        elif PROG_MIN <= quand - maintenant <= PROG_MAX:
            a_traiter.append((f, post, quand, "programmer"))
        # sinon : trop proche (publié au prochain passage) ou trop lointain (programmé plus tard)
    if not a_traiter:
        print("Rien à publier ni à programmer pour l'instant.")
        return
    if not dry and (not page_id or not token):
        sys.exit("Secrets FB_PAGE_ID / FB_PAGE_TOKEN manquants : impossible de publier.")
    for d in (PUBLISHED, SKIPPED, SCHEDULED):
        d.mkdir(exist_ok=True)
    traites = 0
    for f, post, quand, action in a_traiter:
        if action == "maintenant" and maintenant - quand > dt.timedelta(hours=MAX_RETARD_H):
            post["skipped_reason"] = f"plus de {MAX_RETARD_H} h de retard"
            (SKIPPED / f.name).write_text(json.dumps(post, ensure_ascii=False, indent=2), encoding="utf-8")
            f.unlink()
            print(f"::warning::Ignoré (trop en retard) : {f.name}")
            traites += 1
            continue
        if dry:
            print(f"[test] {action} : {f.name}")
            continue
        if action == "programmer":
            # Facebook publiera lui-même à l'heure exacte (plus de dépendance au réveil du robot).
            try:
                post_id = publier(post, page_id, token, quand)
            except SystemExit:
                print(f"::warning::Programmation Facebook refusée pour {f.name} : il reste dans queue/ "
                      "et sera publié directement à l'heure prévue.")
                continue
            post["facebook_post_id"] = post_id
            post["scheduled_on_facebook_at"] = maintenant.isoformat()
            (SCHEDULED / f.name).write_text(json.dumps(post, ensure_ascii=False, indent=2), encoding="utf-8")
            f.unlink()
            print(f"Programmé chez Facebook : {f.name} -> {post_id} pour {post['publish_at']}")
        else:
            post_id = commenter(post, token) if post.get("comment_on") else publier(post, page_id, token)
            post["facebook_post_id"] = post_id
            post["published_at"] = maintenant.isoformat()
            (PUBLISHED / f.name).write_text(json.dumps(post, ensure_ascii=False, indent=2), encoding="utf-8")
            f.unlink()
            print(f"Publié : {f.name} -> {post_id}")
        traites += 1
    print(f"{traites} post(s) traité(s).")


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code not in (0, None, 1):
            msg = str(e.code)
            tok = os.environ.get("FB_PAGE_TOKEN", "")
            if tok:
                msg = msg.replace(tok, "***")
            print(f"::error::{msg}")
            raise SystemExit(1)
        raise
    except Exception as e:  # toute autre erreur : on la remonte en annotation (sans le jeton)
        import traceback
        msg = f"{type(e).__name__}: {e} | " + traceback.format_exc().splitlines()[-3].strip()
        tok = os.environ.get("FB_PAGE_TOKEN", "")
        if tok:
            msg = msg.replace(tok, "***")
        print(f"::error::{msg}")
        raise SystemExit(1)
