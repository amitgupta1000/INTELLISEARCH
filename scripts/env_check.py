"""
env_check.py — report available optional components in the current Python env
Run: python scripts/env_check.py
"""
import importlib
import logging

optional_packages = [
    ('langchain', 'langchain'),
    ('langgraph', 'langgraph'),
    ('pydantic', 'pydantic'),
    ('faiss', 'faiss'),
    ('chromadb', 'chromadb'),
    ('pymupdf', 'fitz'),
    ('rank_bm25', 'rank_bm25'),
    ('fpdf', 'fpdf'),
    ('dotenv', 'dotenv'),
]

found = {}
for name, pkg in optional_packages:
    try:
        importlib.import_module(pkg)
        found[name] = True
    except Exception:
        found[name] = False

for k, v in found.items():
    logging.info("%s: %s", k, 'available' if v else 'missing')

print('\nSummary:')
for k, v in found.items():
    print(f" - {k}: {'available' if v else 'missing'}")
