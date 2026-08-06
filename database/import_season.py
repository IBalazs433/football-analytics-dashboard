from config.settings import SQL_DIR, DATA_DIR, MATCH_COLUMNS

import pandas as pd
import sqlite3


def import_season(conn: sqlite3.Connection, league_code: str, league: dict, season: str) -> None:
    """
    Imports match data for a specific league and season into the database.
    """

    csv_path = DATA_DIR / "raw" / league["country"] / f"{league_code}_{season}.csv"
    df = pd.read_csv(csv_path)
    df = df[MATCH_COLUMNS]  # Select only the relevant columns
    df.to_sql("staging", conn, if_exists="append", index=False)

    teams_home_sql = (SQL_DIR / "inserts" / "teams_home.sql").read_text(encoding="utf-8")
    conn.execute(teams_home_sql, {"country": league["country"]})

    teams_away_sql = (SQL_DIR / "inserts" / "teams_away.sql").read_text(encoding="utf-8")
    conn.execute(teams_away_sql, {"country": league["country"]})

    league_sql = (SQL_DIR / "inserts" / "leagues.sql").read_text(encoding="utf-8")
    conn.execute(league_sql, {"league_code": league_code, "league_name": league["name"], "country": league["country"]})

    season_sql = (SQL_DIR / "inserts" / "seasons.sql").read_text(encoding="utf-8")
    conn.execute(season_sql, {"league_code": league_code, "season": f"{season[:2]}-{season[2:4]}", "country": league["country"]})

    matches_sql = (SQL_DIR / "inserts" / "matches.sql").read_text(encoding="utf-8")
    conn.execute(matches_sql, {"season": f"{season[:2]}-{season[2:4]}"})
    print(f"Inserted {league['name']} {season} data into the database.")

    conn.execute("DELETE FROM staging") # Clear the staging table after processing