"""Premier import des rappels, puis ajout des nouveaux identifiants uniquement."""
import json
import sqlite3
from urllib.parse import urlencode

from .config import DATA
from .commun import fetch, save

API = 'https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/rappelconso-v2-gtin-espaces/exports/json'


def collecter():
    folder = DATA / 'rappelconso'
    folder.mkdir(parents=True, exist_ok=True)

    # SQLite mémorise les rappels déjà collectés entre deux exécutions.
    with sqlite3.connect(folder / 'collecte.sqlite') as db:
        db.execute('CREATE TABLE IF NOT EXISTS rappels (id TEXT PRIMARY KEY, publication TEXT, contenu TEXT)')
        last_date = db.execute('SELECT MAX(publication) FROM rappels').fetchone()[0]
        parameters = {'limit': -1, 'order_by': 'date_publication ASC'}
        if last_date:
            # Inclure cette date pour récupérer aussi les publications simultanées.
            parameters['where'] = f"date_publication >= date'{last_date}'"
        records = json.loads(fetch(API + '?' + urlencode(parameters)))
        if not isinstance(records, list):
            raise ValueError('Réponse RappelConso invalide')
        added = 0
        for record in records:
            identifier = record.get('id') or record.get('rappel_guid')
            publication = record.get('date_publication')
            if identifier is None or not publication:
                raise ValueError('Rappel sans identifiant ou date de publication')
            # La clé primaire empêche de stocker deux fois le même rappel.
            added += db.execute('INSERT OR IGNORE INTO rappels VALUES (?, ?, ?)', (
                str(identifier), publication, json.dumps(record, ensure_ascii=False),
            )).rowcount
        db.commit()
        history = [json.loads(row[0]) for row in db.execute('SELECT contenu FROM rappels ORDER BY publication, id')]
        save(folder / 'rappels.json', history)
    print(f'RappelConso : {added} nouveaux rappels.')
