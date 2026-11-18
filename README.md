# Projet Datamining - MSPR


### Lancement du projet

Les collectes créent automatiquement des fichiers `.parquet` dans `data/` pour chaque données.

Copier le fichier .env : 

```bash
cp .env.example .env
```

Lancer les conteneurs :

```bash
make start
```

Lancer l'importation des données :
```bash
make collecte
```

Arrêter les conteneurs :
```bash
make stop
```

Le dossier `importation/` regroupe les traitements : un fichier par source (`instacart.py`, `openfoodfacts.py`, `rappelconso.py`, `openprices.py`), `parquet.py` pour la conversion, `commun.py` pour les requêtes et écritures, `config.py` pour les chemins, et `collecter_donnees.py` pour lancer le téléchargement.

### URLs

Jupiter : [link Jupiter](http://localhost:18888/lab?token=projet)
RustFS : [link RustFS](http://localhost:19001)
