"""
This script updates the football database with the latest season data for all leagues defined in the LEAGUES constant.
"""

from config.constants import LEAGUES
from config.settings import SEASONS, SQL_DIR, DATA_DIR, CURRENT_SEASON
from database.import_season import import_season

import sqlite3


def main():
    conn = sqlite3.connect(DATA_DIR / "football.db")

    for league_code, league in LEAGUES.items():
        import_season(conn, league_code, league, CURRENT_SEASON)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()