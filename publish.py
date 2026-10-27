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
QUEUE, PUBLISHED, SKIPPED = ROOT / "queue", ROOT / "published", ROOT / "skipped"
SCHEDULED = ROOT / "scheduled"   # posts confiés au programmateur de Facebook
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
                  f"filename=\"{fichier.name}\"\r\nContent-Type: image/png\r\n\r\n").encode()
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


def publier(post, page_id, token, quand=None):
    """Publie maintenant, ou programme chez Facebook si `quand` (datetime futur) est donné."""
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


def main():
    dry = os.environ.get("DRY_RUN") == "1"
    page_id = os.environ.get("FB_PAGE_ID", "").strip()
    token = os.environ.get("FB_PAGE_TOKEN", "").strip()
    if os.environ.get("VERIFIER") == "1":
        verifier(page_id, token)
        return
    maintenant = dt.datetime.now(dt.timezone.utc)
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
            post_id = publier(post, page_id, token)
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
