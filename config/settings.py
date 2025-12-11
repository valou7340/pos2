# config/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = f"sqlite:///{BASE_DIR / 'pos.db'}"

# Taxes restaurant France 2025
TVA_RESTAURATION = 0.10   # 10% sur place
TVA_A_EMPORTER = 0.10     # même taux depuis 2023
TVA_ALCOOL = 0.20         # 20% sur alcools

DEVISE = "€"
NOM_RESTO = "Le Bon Plat"
ADRESSE_RESTO = "123 Rue de la Gastronomie, 75000 Paris"
