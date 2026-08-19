#!/usr/bin/env bash
# Script de build utilisé par Render (voir render.yaml). Exécuté à chaque
# déploiement : installe les dépendances, prépare les fichiers statiques et
# met la base à jour. `migrate` et `seed_quotes` sont tous les deux
# idempotents, donc ce script peut être relancé sans risque à chaque push.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_quotes
