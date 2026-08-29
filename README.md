# KOMA (コマ) — citations manga

Application web de citations de manga et anime : recherche par mot-clé, filtre par série ou par
thème, page de détail avec copie en un clic, et une API REST publique. Construite avec Django.

## Pourquoi Django plutôt que Laravel

Le projet a démarré avec l'intention d'utiliser Laravel (le framework PHP le plus proche de
l'esprit "MVC + conventions" recherché), mais Composer/Packagist n'était pas joignable depuis
l'environnement de build utilisé pour ce projet. Django a été choisi comme équivalent le plus
proche : conventions fortes, ORM intégré, admin auto-générée, routing par fichier dédié — et
Django REST Framework couvre exactement le rôle que l'API Resource de Laravel aurait joué ici.

## Design — parti pris

Le brief était « un framework, et un design à la fois otaku et minimaliste, en évitant les
patterns et logos cliché ». Concrètement, ça a donné :

- **Pas de logo illustré.** Le nom du site — KOMA (コマ), qui désigne une case de planche de
  manga — sert de repère visuel, en typographie seule.
- **Pas de grille de cartes.** La liste des citations est un index numéroté avec des filets fins,
  plus proche d'un sommaire de recueil que d'un flux de réseau social.
- **Palette papier + encre.** Fond crème (rappel du papier), texte quasi noir, un seul accent
  rouge (sceau/hanko) — pas de dégradés, pas d'ombres portées, pas de coins arrondis.
- **Deux polices, un rôle chacune.** Shippori Mincho (serif japonais) pour le texte des
  citations, JetBrains Mono pour toute l'interface (labels, métadonnées, boutons) — auto-
  hébergées en local (`static/fonts/`), sans dépendance à une CDN externe au chargement.
- **Le guillemet 「 plutôt que des guillemets occidentaux** comme unique élément décoratif.

## Fonctionnalités

- Page d'accueil : une citation aléatoire à chaque visite (« une autre » pour en tirer une autre).
- Page « Parcourir » : recherche libre (texte, personnage, série), filtres par série et par
  thème, pagination, compteur de résultats.
- Page de détail : citation complète, bouton de copie dans le presse-papiers.
- **Mode sombre** (bouton en haut à droite) — même charte papier/encre, inversée. Préférence
  mémorisée (`localStorage`), appliquée avant le premier rendu pour éviter un flash au mauvais
  thème, et respecte `prefers-color-scheme` par défaut si rien n'est encore choisi.
- **Citations bilingues FR/VO** (bouton "afficher en FR/VO") — chaque citation qui a une
  traduction affiche les deux versions ; le bouton bascule laquelle est visible, sans recharger
  la page. Voir la section *Traductions* ci-dessous pour la fiabilité de ces traductions.
- API REST en lecture seule :
  - `GET /api/quotes/` — liste paginée, filtrable via `?q=&series=&theme=`
  - `GET /api/quotes/<id>/` — une citation
  - `GET /api/quotes/random/` — une citation aléatoire (respecte les mêmes filtres)
- Admin Django (`/admin/`) pour gérer les citations.

## Traductions

Chaque citation peut avoir une version française (`text_fr`) accompagnée de sa provenance
(`fr_origin`) :

- **Traduction assistée** — générée pour ce projet, pas issue d'un doublage/sous-titrage
  officiel ni relue par un locuteur natif. C'est le cas de toutes les traductions actuellement
  en base. L'appli l'indique clairement sous la citation (« traduction assistée, non vérifiée »)
  plutôt que de la faire passer pour une traduction officielle.
- **Traduction communautaire** — réservé aux traductions provenant d'une source déjà vérifiée
  par des tiers (dictionnaire de citations communautaire, doublage officiel, etc.). Aucune
  citation n'est actuellement dans ce cas — le champ existe pour pouvoir distinguer proprement
  les deux niveaux de confiance si des traductions vérifiées sont ajoutées plus tard.

## Stack

- Django 5 + Django REST Framework
- SQLite en développement (zéro configuration) ; compatible Postgres en production via
  `DATABASE_URL` (voir Déploiement ci-dessous)
- Templates Django (pas de framework JS) + un peu de JS natif pour la copie presse-papiers
- Polices auto-hébergées (`@fontsource/shippori-mincho`, `@fontsource/jetbrains-mono`, sous-
  ensemble latin uniquement)
- Gunicorn (serveur WSGI de prod) + WhiteNoise (fichiers statiques compressés, servis sans
  serveur/CDN séparé)

## Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

pip install -r requirements-dev.txt

python manage.py migrate
python manage.py seed_quotes   # peuple la base avec ~34 citations (idempotent)

python manage.py runserver
```

Le site est alors disponible sur `http://localhost:8000/`.

Variables d'environnement optionnelles (valeurs par défaut adaptées au développement local) :

| Variable                 | Rôle                                      | Défaut                     |
| ------------------------- | ------------------------------------------ | --------------------------- |
| `DJANGO_SECRET_KEY`       | Clé secrète Django                         | valeur de secours incluse   |
| `DJANGO_DEBUG`            | Mode debug (`True`/`False`)                | `True`                      |
| `DJANGO_ALLOWED_HOSTS`    | Hôtes autorisés, séparés par des virgules  | `localhost,127.0.0.1`       |

En production, définir au minimum `DJANGO_SECRET_KEY` et `DJANGO_DEBUG=False`.

## Déploiement (Render)

Le repo est prêt pour un déploiement en un clic sur [Render](https://render.com) (offre
gratuite) via `render.yaml` :

1. Pousser ce repo sur GitHub (public ou privé, un compte Render gratuit suffit).
2. Sur [dashboard.render.com](https://dashboard.render.com), **New +** → **Blueprint**, puis
   sélectionner ce repo. Render lit `render.yaml` et configure le service automatiquement
   (build, démarrage, `DJANGO_SECRET_KEY` généré, `DJANGO_DEBUG=False`).
3. Une fois le premier déploiement terminé, ajouter le domaine attribué par Render
   (`monapp.onrender.com`) à la variable d'env `DJANGO_ALLOWED_HOSTS` — en pratique cette étape
   est automatique : `RENDER_EXTERNAL_HOSTNAME` est ajouté par Render et pris en compte
   directement par `config/settings.py`, rien à faire manuellement.

Ce que fait `build.sh` à chaque déploiement (build/migrate/seed idempotents, donc rejouable sans
risque à chaque push) :

```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_quotes
```

**Persistance des données.** Le tier gratuit de Render a un disque éphémère : la base SQLite est
réinitialisée (et re-seedée) à chaque redéploiement. Pour un déploiement permanent où les
données doivent survivre (ex. si le modèle évolue vers du contenu géré via l'admin plutôt que
seedé), ajouter une base Postgres gratuite Render, définir la variable d'env `DATABASE_URL`
qu'elle fournit, et ajouter `psycopg[binary]` à `requirements.txt` — `dj-database-url` (déjà en
place) bascule automatiquement dessus dès que `DATABASE_URL` est présente, sans autre changement
de code.

## Tests

```bash
python manage.py test quotes -v 2
```

28 tests couvrant le modèle (dont les champs de traduction), les vues web (accueil, parcours
avec filtres/pagination, détail, rendu bilingue), l'API REST (liste, détail, aléatoire, filtres,
404, champs de traduction) et l'idempotence de la commande de seed.

## Lint

```bash
ruff check .
```

## CI

Le workflow `.github/workflows/ci.yml` installe les dépendances, exécute `ruff check .` puis la
suite de tests Django, sur Python 3.11 et 3.12 à chaque push/pull request vers `main`.

## Contenu des citations

73 citations, sur 38 séries. Attribuées à leurs personnages et séries d'origine, à des fins non
commerciales (projet personnel). Le champ `source` (chapitre/épisode précis) est volontairement
laissé vide plutôt que rempli avec une attribution approximative.

**Pourquoi 73 et pas 500-1000.** Un jeu de données externe permettant d'atteindre ~800 citations
avait été identifié, mais son contenu s'est révélé en grande partie inventé (des répliques
génériques générées automatiquement, faussement attribuées à de vrais personnages — parfois même
sur des séries très documentées comme Dragon Ball). Plutôt que d'importer ce volume au risque de
diffuser de fausses citations, l'extension au-delà des 34 initiales a été faite à la main, une
par une, en ne gardant que celles dont l'authenticité et l'attribution semblaient fiables — d'où
un total plus modeste mais qui garde le même niveau de confiance que le lot de départ.

## Provenance, droits et retrait

Les citations, noms de personnages, titres de séries et traductions peuvent relever de droits détenus par leurs auteurs, éditeurs ou ayants droit. Le projet ne revendique pas la propriété de ces éléments et les présente dans un cadre personnel et non commercial. Le champ `source` doit rester renseigné uniquement lorsqu’une référence vérifiable est disponible ; il ne faut pas inventer de chapitre ou d’épisode pour compléter une fiche.

Avant toute publication publique, ajouter pour chaque entrée une provenance vérifiable, une date de vérification et, lorsque nécessaire, une attribution. Une demande de retrait ou de correction doit pouvoir être traitée en supprimant ou corrigeant l’entrée concernée sans casser l’API. Les traductions assistées restent explicitement non officielles et ne doivent pas être présentées comme des sous-titres ou doublages autorisés.
