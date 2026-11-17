## Projet EduSmart


### Lancement du projet

Les collectes créent automatiquement des fichiers `.parquet` dans `data/` pour chaque données.

Copier le fichier .env : 

```bash
cp .env.example .env
```

Lancer les conteneurs docker :

```bash
docker compose up -d --build
docker compose exec jupyter bash script/telecharger_donnees.sh
```

Pour convertir uniquement les fichiers déjà téléchargés :

```bash
docker compose exec jupyter bash script/telecharger_donnees.sh --parquet-only
```

Le dossier `importation/` regroupe les traitements : un fichier par source (`instacart.py`, `openfoodfacts.py`, `rappelconso.py`, `openprices.py`), `parquet.py` pour la conversion, `commun.py` pour les requêtes et écritures, `config.py` pour les chemins, et `collecter_donnees.py` pour lancer le téléchargement.