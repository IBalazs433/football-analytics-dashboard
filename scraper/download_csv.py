"""
This script downloads football match data in CSV format from football-data.co.uk for specified leagues and seasons.
"""

import requests

from config.constants import BASE_URL
from config.settings import RAW_DATA_DIR


def download_csv(country: str, league_name: str, league_code: str, season: str) -> None:
    """
    Download CSV data for a given league and season from football-data.co.uk.
    """

    url = f"{BASE_URL}/{season}/{league_code}.csv"
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"{RAW_DATA_DIR}/{country}/{league_code}_{season}.csv", "wb") as f:
            f.write(response.content)
        print(f"Downloaded {league_name} {season} data.")
    else:
        print(f"Failed to download {league_code} {league_name} {season} data. Status code: {response.status_code}")
