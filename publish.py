"""Publie sur la page Facebook les posts de la file d'attente (queue/) arrivés à échéance.

Chaque post est un fichier JSON dans queue/ :
{
  "publish_at": "2026-10-31T10:00:00+01:00",   # heure de publication (avec fuseau)
  "message": "Texte du post…",
  "image": "visuels/xxx.png"                    # optionnel : chemin dans le dépôt
}

Après publication, le fichier part dans published/ avec l'identifiant du post Facebook.
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
import urllib.request
import uuid

API = "https://graph.facebook.com/v23.0"
ROOT = pathlib.Path(__file__).resolve().parent
QUEUE, PUBLISHED, SKIPPED = ROOT / "queue", ROOT / "published", ROOT / "skipped"
MAX_RETARD_H = 6


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
        # ne jamais afficher le jeton
        raise SystemExit(f"Erreur API Facebook {e.code} : {detail}")


def publier(post, page_id, token):
    image = post.get("image")
    if image:
        f = ROOT / image
        if not f.exists():
            raise SystemExit(f"Image introuvable : {image}")
        rep = appel(f"{API}/{page_id}/photos", {"caption": post["message"], "access_token": token}, f)
        return rep.get("post_id") or rep.get("id")
    rep = appel(f"{API}/{page_id}/feed", {"message": post["message"], "access_token": token})
    return rep.get("id")


def main():
    dry = os.environ.get("DRY_RUN") == "1"
    page_id = os.environ.get("FB_PAGE_ID", "")
    token = os.environ.get("FB_PAGE_TOKEN", "")
    if not dry and (not page_id or not token):
        sys.exit("Secrets FB_PAGE_ID / FB_PAGE_TOKEN manquants.")
    maintenant = dt.datetime.now(dt.timezone.utc)
    for d in (PUBLISHED, SKIPPED):
        d.mkdir(exist_ok=True)
    fichiers = sorted(QUEUE.glob("*.json")) if QUEUE.exists() else []
    traites = 0
    for f in fichiers:
        post = json.loads(f.read_text(encoding="utf-8"))
        quand = dt.datetime.fromisoformat(post["publish_at"])
        if quand.tzinfo is None:
            sys.exit(f"{f.name} : publish_at doit contenir le fuseau (ex. +01:00).")
        if quand > maintenant:
            continue
        if maintenant - quand > dt.timedelta(hours=MAX_RETARD_H):
            post["skipped_reason"] = f"plus de {MAX_RETARD_H} h de retard"
            (SKIPPED / f.name).write_text(json.dumps(post, ensure_ascii=False, indent=2), encoding="utf-8")
            f.unlink()
            print(f"Ignoré (trop en retard) : {f.name}")
            traites += 1
            continue
        if dry:
            print(f"[test] serait publié : {f.name}")
            continue
        post_id = publier(post, page_id, token)
        post["facebook_post_id"] = post_id
        post["published_at"] = maintenant.isoformat()
        (PUBLISHED / f.name).write_text(json.dumps(post, ensure_ascii=False, indent=2), encoding="utf-8")
        f.unlink()
        print(f"Publié : {f.name} -> {post_id}")
        traites += 1
    print(f"{traites} post(s) traité(s).")


if __name__ == "__main__":
    main()
