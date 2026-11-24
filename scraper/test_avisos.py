"""Pruebas de los avisos y del informe (python scraper/test_avisos.py)."""
import sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from avisos import best, parse, decide

T = date(2026, 11, 24)
it = {"prices": {"a": {"p": 50, "d": "2026-11-24"}, "b": {"p": 40, "d": "2026-11-01"}, "c": {"p": 45, "d": "2026-11-20", "stock": False}, "d": {"p": 48, "d": "2026-11-23"}}}
assert best(it, T) == (48, "d")                       # el de 40 es viejo y el de 45 está agotado
assert parse("Hola\nid: dior-sauvage-edt-100\nprecio: 79,5\n") == ("dior-sauvage-edt-100", 79.5)
assert parse("sin datos") is None
assert decide((48, "d"), 50, None) and not decide((52, "d"), 50, None)
assert not decide((48, "d"), 50, 48) and decide((46, "d"), 50, 48)   # solo vuelve a avisar si baja más
print("OK: avisos")
