"""
This script downloads football match data in CSV format from football-data.co.uk for specified leagues and seasons.
It saves the downloaded CSV files in the specified raw data directory.
"""

from config.constants import LEAGUES
from config.settings import SEASONS
from scraper.download_csv import download_csv


if __name__ == "__main__":
    print("Downloading football-data.co.uk datasets...")

    for league_code, league in LEAGUES.items():
        for season in SEASONS:
            download_csv(league["country"], league["name"], league_code, season)

    print("Finished.")
