from config.constants import LEAGUES
from config.settings import CURRENT_SEASON
from scraper.download_csv import download_csv


if __name__ == "__main__":
    print("Updating football-data.co.uk datasets...")

    for league_code, league in LEAGUES.items():
        download_csv(league["country"], league["name"], league_code, CURRENT_SEASON)

    print("Finished.")