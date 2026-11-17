"""Récupère les CSV Instacart depuis Kaggle ou un dossier local."""
from pathlib import Path
import shutil

from .config import DATA


def collecter(dossier_local=None):
    target = DATA / 'instacart'
    target.mkdir(parents=True, exist_ok=True)

    # L'option --instacart-dir permet d'utiliser les CSV de l'encadrant.
    if dossier_local:
        source = Path(dossier_local).resolve()
    else:
        import kagglehub
        source = Path(kagglehub.dataset_download('psparks/instacart-market-basket-analysis'))

    # KaggleHub conserve un cache : on copie ses CSV dans le dossier du projet.
    files = sorted(source.rglob('*.csv'))
    if not files:
        raise ValueError(f'Aucun CSV trouvé dans {source}')
    if len({file.name for file in files}) != len(files):
        raise ValueError('Plusieurs CSV portent le même nom : copie ambiguë.')
    for file in files:
        destination = target / file.name
        if file.resolve() != destination.resolve():
            shutil.copy2(file, destination)
    print(f'Instacart : {len(files)} CSV disponibles.')
