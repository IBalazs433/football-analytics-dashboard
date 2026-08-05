"""
This module contains configuration settings for the football analytics dashboard project.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

# DATABASE_PATH = DATA_DIR / "football.db"

SEASONS = [
    "2526",
    "2425",
    "2324",
    "2223",
    "2122",
]

CURRENT_SEASON = "2526"
