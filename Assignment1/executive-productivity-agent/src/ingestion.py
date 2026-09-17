import json
from pathlib import Path

ROOT = Path(__file__).parent.parent

def load_demo_data(path: str):
    p = Path(path)
    if not p.exists():
        p = ROOT / path
    with p.open('r', encoding='utf-8') as f:
        return json.load(f)


def list_sources(data):
    return data.get('sources', [])
