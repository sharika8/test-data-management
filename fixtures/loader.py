"""fixtures/loader.py - Load static test fixtures"""
import json
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent

def load(name):
    p = FIXTURES_DIR / f"{name}.json"
    if p.exists(): return json.loads(p.read_text())
    raise FileNotFoundError(f"Fixture not found: {name}")
