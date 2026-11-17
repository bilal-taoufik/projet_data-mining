"""Transforme les CSV et JSON d'une source en fichiers Parquet."""
import csv
import json

from .config import DATA


def convertir(source):
    import pyarrow as pa
    import pyarrow.csv as arrow_csv
    import pyarrow.parquet as pq

    folder = DATA / source
    extension = '*.csv' if source == 'instacart' else '*.json'
    files = sorted(folder.glob(extension))
    if not files:
        raise ValueError(f'Aucun fichier à convertir dans {folder}')

    for file in files:
        output = file.with_suffix('.parquet')
        temporary = output.with_suffix('.parquet.tmp')
        try:
            if file.suffix == '.csv':
                # Lire par lots : les gros CSV Instacart ne tiennent pas tous en mémoire.
                with file.open(encoding='utf-8-sig', newline='') as stream:
                    columns = next(csv.reader(stream))
                # Garder le texte d'origine (par exemple les zéros des codes produits).
                options = arrow_csv.ConvertOptions(column_types={name: pa.string() for name in columns})
                with arrow_csv.open_csv(file, convert_options=options) as reader:
                    with pq.ParquetWriter(temporary, reader.schema, compression='snappy') as writer:
                        for batch in reader:
                            writer.write_batch(batch)
            else:
                records = json.loads(file.read_text(encoding='utf-8'))
                if isinstance(records, dict):
                    records = [records]
                if not records:
                    raise ValueError(f'Aucun enregistrement dans {file} : ancien Parquet conservé.')
                # Une colonne par clé JSON. Les objets et listes restent du texte JSON.
                columns = sorted({key for record in records for key in record})
                values = {}
                for key in columns:
                    values[key] = pa.array([en_texte(record.get(key)) for record in records], type=pa.string())
                pq.write_table(pa.table(values), temporary, compression='snappy')

            # Ne remplacer l'ancien Parquet qu'une fois la conversion terminée.
            temporary.replace(output)
        finally:
            temporary.unlink(missing_ok=True)
        print(f'Parquet : {output}')


def en_texte(value):
    """Conserve les valeurs manquantes et sérialise les valeurs complexes."""
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)
