"""Récupère un échantillon de produits et leurs informations nutritionnelles."""
import json
import time
from urllib.parse import urlencode

from .config import DATA
from .commun import fetch, save


def collecter(pages=1):
    products = []
    # Chaque page contient au plus 100 produits commercialisés en France.
    for page in range(1, pages + 1):
        parameters = urlencode({
            'countries_tags': 'en:france', 'page': page, 'page_size': 100,
            'fields': 'code,product_name,brands,categories_tags,ingredients_text,nutriments,nutriscore_grade,nova_group,allergens_tags',
        })
        response = json.loads(fetch('https://world.openfoodfacts.org/api/v2/search?' + parameters))
        batch = response['products']
        products.extend(batch)
        if len(batch) < 100:
            break
        # Espacer les recherches pour respecter la limite de l'API.
        if page < pages:
            time.sleep(7)
    save(DATA / 'openfoodfacts' / 'produits.json', products)
    print(f'Open Food Facts : {len(products)} produits.')
