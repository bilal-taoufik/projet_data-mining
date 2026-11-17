"""Point de départ : collecte des sources puis conversion en Parquet."""
import argparse
import sys

from . import instacart, openfoodfacts, rappelconso, openprices
from .parquet import convertir

SOURCES = ['instacart', 'openfoodfacts', 'rappelconso', 'openprices']


def main():
    # Ces options sont transmises par telecharger_donnees.sh.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', nargs='+', choices=SOURCES, default=SOURCES,
                        help='Sources à traiter (par défaut : les quatre)')
    parser.add_argument('--instacart-dir', help='Dossier des CSV locaux au lieu de Kaggle')
    parser.add_argument('--off-pages', type=int, default=1, help='Nombre de pages Open Food Facts, 100 produits maximum par page')
    parser.add_argument('--parquet-only', action='store_true', help='Convertir les fichiers présents sans télécharger')
    args = parser.parse_args()
    if args.off_pages < 1:
        parser.error('--off-pages doit être positif')

    erreurs = []
    for source in args.sources:
        try:
            # Étape 1 : récupérer les CSV/JSON, sauf avec --parquet-only.
            if not args.parquet_only:
                if source == 'instacart':
                    instacart.collecter(args.instacart_dir)
                elif source == 'openfoodfacts':
                    openfoodfacts.collecter(args.off_pages)
                elif source == 'rappelconso':
                    rappelconso.collecter()
                elif source == 'openprices':
                    openprices.collecter()

            # Étape 2 : créer les Parquet dans data/<source>/.
            convertir(source)
        except Exception as error:
            # Une erreur sur une source n'empêche pas de traiter les suivantes.
            print(f'ERREUR {source} : {error}', file=sys.stderr)
            erreurs.append(source)

    # 0 = succès ; 1 = au moins une erreur (utile pour Bash et cron).
    return 1 if erreurs else 0


if __name__ == '__main__':
    sys.exit(main())
