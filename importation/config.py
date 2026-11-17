"""Les paramètres utilisés par tous les collecteurs."""
import os
from pathlib import Path

# On part du fichier actuel pour retrouver le dépôt, quel que soit le terminal.
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'

# Nom envoyé aux sites pour identifier notre programme.
AGENT = os.getenv('COLLECT_USER_AGENT', 'ProjetDataMining/1.0 (educational data collection)')
