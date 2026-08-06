"""
This script builds the football database by creating the necessary tables and importing data for all leagues and seasons defined in the LEAGUES and SEASONS constants.
"""

from config.constants import LEAGUES
from config.settings import SEASONS, SQL_DIR, DATA_DIR
from database.import_season import import_season

import sqlite3


def main():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(DATA_DIR / "football.db")

    # Create countries table and insert unique countries from LEAGUES
    countries_sql = (SQL_DIR / "inserts" / "countries.sql").read_text(encoding="utf-8")
    countries = {league["country"] for league in LEAGUES.values()}

    for country in countries:
        conn.execute(countries_sql, {"country": country})

    conn.commit()
    print("Countries inserted successfully.")

    # Import seasons one by one for each league and year, and insert into the database
    for league_code, league in LEAGUES.items():
        for season in SEASONS:
            import_season(conn, league_code, league, season)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()