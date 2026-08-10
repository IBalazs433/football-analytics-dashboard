"""
This script downloads football match data in CSV format from football-data.co.uk for specified leagues and seasons.
"""

import requests

from config.constants import BASE_URL
from config.settings import RAW_DATA_DIR


def download_csv(country: str, league_name: str, league_code: str, season: str) -> None:
    """Download a single league-season CSV file and save it under the raw data directory."""

    target_dir = RAW_DATA_DIR / country
    target_dir.mkdir(parents=True, exist_ok=True)

    url = f"{BASE_URL}/{season}/{league_code}.csv"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Failed to download {league_code} {league_name} {season} data. Reason: {exc}")
        return

    target_path = target_dir / f"{league_code}_{season}.csv"
    with open(target_path, "wb") as f:
        f.write(response.content)

    print(f"Downloaded {league_name} {season} data.")
