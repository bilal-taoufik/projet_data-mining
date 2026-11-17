"""Petites fonctions communes : requête HTTP et sauvegarde JSON."""
import gzip
import json
import time
from urllib.request import Request, urlopen

from .config import AGENT


def fetch(url):
    """Télécharge du texte ; réessaie en cas de problème réseau temporaire."""
    for attempt in range(4):
        try:
            request = Request(url, headers={'User-Agent': AGENT})
            with urlopen(request, timeout=90) as response:
                content = response.read()
            # Certaines API renvoient du contenu compressé.
            if content[:2] == b'\x1f\x8b':
                content = gzip.decompress(content)
            return content.decode('utf-8-sig')
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


def save(path, content):
    """Écrit un JSON sans remplacer l'ancien fichier avant la fin de l'écriture."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(path)
