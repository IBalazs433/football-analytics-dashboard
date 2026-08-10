from config.settings import DATA_DIR
import pandas as pd
import sqlite3


def get_connection() -> sqlite3.Connection:
    database_path = DATA_DIR / "football.db"
    return sqlite3.connect(database_path)


# -----------------------------
# Sidebar Queries
# -----------------------------

def get_countries(conn: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql(
        "SELECT name FROM countries ORDER BY name",
        conn
    )


def get_teams(conn: sqlite3.Connection, country: str) -> pd.DataFrame:
    return pd.read_sql(
        """
        SELECT t.name
        FROM teams t
        JOIN countries c
          ON c.id = t.country_id
        WHERE c.name = ?
        ORDER BY t.name
        """,
        conn,
        params=(country,)
    )


def get_leagues(conn: sqlite3.Connection, country: str) -> pd.DataFrame:
    return pd.read_sql(
        """
        SELECT l.name
        FROM leagues l
        JOIN countries c
          ON c.id = l.country_id
        WHERE c.name = ?
        ORDER BY l.code
        """,
        conn,
        params=(country,)
    )


def get_seasons(conn: sqlite3.Connection, league: str) -> pd.DataFrame:
    return pd.read_sql(
        """
        SELECT s.season
        FROM seasons s
        JOIN leagues l
          ON l.id = s.league_id
        WHERE l.name = ?
        ORDER BY s.season DESC
        """,
        conn,
        params=(league,)
    )


def get_teams_from_season(conn, country, league, season):
    return pd.read_sql(
        """
        SELECT DISTINCT t.name
        FROM matches m
        JOIN teams t ON t.id IN (m.home_team_id, m.away_team_id)
        JOIN seasons s ON s.id = m.season_id
        JOIN leagues l ON l.id = s.league_id
        JOIN countries c ON c.id = l.country_id
        WHERE c.name = ? AND l.name = ? AND s.season = ?
        ORDER BY t.name
        """,
        conn,
        params=(country, league, season)
    )


def get_match_dates(conn, country, league, season, home_team, away_team):
    return pd.read_sql(
        """
        SELECT m.date
        FROM matches m
        JOIN teams ht ON ht.id = m.home_team_id
        JOIN teams at ON at.id = m.away_team_id
        JOIN seasons s ON s.id = m.season_id
        JOIN leagues l ON l.id = s.league_id
        JOIN countries c ON c.id = l.country_id
        WHERE c.name = ? AND l.name = ? AND s.season = ?
          AND ht.name = ? AND at.name = ?
        ORDER BY m.date DESC
        """,
        conn,
        params=(country, league, season, home_team, away_team)
    )


# -----------------------------
# Landing Page Queries
# -----------------------------

def get_number_of_countries(conn: sqlite3.Connection) -> int:
    return pd.read_sql(
        "SELECT COUNT(*) AS count FROM countries",
        conn
    ).iloc[0]["count"]


def get_number_of_leagues(conn: sqlite3.Connection) -> int:
    return pd.read_sql(
        "SELECT COUNT(*) AS count FROM leagues",
        conn
    ).iloc[0]["count"]


def get_number_of_seasons(conn: sqlite3.Connection) -> int:
    return pd.read_sql(
        "SELECT COUNT(DISTINCT season) AS count FROM seasons",
        conn
    ).iloc[0]["count"]


def get_number_of_teams(conn: sqlite3.Connection) -> int:
    return pd.read_sql(
        "SELECT COUNT(*) AS count FROM teams",
        conn
    ).iloc[0]["count"]


def get_number_of_matches(conn: sqlite3.Connection) -> int:
    return pd.read_sql(
        "SELECT COUNT(*) AS count FROM matches",
        conn
    ).iloc[0]["count"]


def get_number_of_goals(conn: sqlite3.Connection) -> int:
    return pd.read_sql(
        "SELECT SUM(home_goals) + SUM(away_goals) AS count FROM matches",
        conn
    ).iloc[0]["count"]


def get_first_match_date(conn: sqlite3.Connection) -> str:
    return pd.read_sql(
        "SELECT MIN(date) AS first_match_date FROM matches",
        conn
    ).iloc[0]["first_match_date"]


def get_last_match_date(conn: sqlite3.Connection) -> str:
    return pd.read_sql(
        "SELECT MAX(date) AS last_match_date FROM matches",
        conn
    ).iloc[0]["last_match_date"]


# -----------------------------
# League Analysis Page Queries
# -----------------------------


def get_number_of_league_matches(conn, league, season):
    return pd.read_sql(
        """
        SELECT COUNT(*) AS count
        FROM matches m
        JOIN seasons s
          ON s.id = m.season_id
        JOIN leagues l
          ON l.id = s.league_id
        WHERE s.season = ? AND l.name = ?
        """,
        conn,
        params=(season, league)
    ).iloc[0]["count"]


def get_league_statistics(conn, league, season):
    return pd.read_sql(
        """
        SELECT s.season,
               COUNT(*) AS total_matches,
               SUM(m.home_goals + m.away_goals) as total_goals,
               ROUND(1.0 * SUM(m.home_shots + m.away_shots) / COUNT(*), 2) AS average_shots_per_match,
               ROUND(1.0 * SUM(m.home_shots_on_target + m.away_shots_on_target) / COUNT(*), 2) AS average_shots_on_target,
               ROUND(1.0 * SUM(m.home_yellow_cards + m.away_yellow_cards) / COUNT(*), 2) AS average_yellow_cards_per_match,
               ROUND(1.0 * SUM(m.home_red_cards + m.away_red_cards) / COUNT(*), 2) AS average_red_cards_per_match
        FROM matches m
        JOIN seasons s
          ON s.id = m.season_id
        JOIN leagues l
          ON l.id = s.league_id
        WHERE s.season = ? AND l.name = ?
        GROUP BY s.season
        ORDER BY s.season DESC
        """,
        conn,
        params=(season, league)
    )


def get_league_table(conn, league, season):
    return pd.read_sql(
        """
        SELECT t.name AS team,
               COUNT(*) AS matches,
               SUM(CASE WHEN (m.home_team_id = t.id AND m.home_goals > m.away_goals) OR (m.away_team_id = t.id AND m.away_goals > m.home_goals) THEN 1 ELSE 0 END) AS wins,
               SUM(CASE WHEN m.home_goals = m.away_goals THEN 1 ELSE 0 END) AS draws,
               SUM(CASE WHEN (m.home_team_id = t.id AND m.home_goals < m.away_goals) OR (m.away_team_id = t.id AND m.away_goals < m.home_goals) THEN 1 ELSE 0 END) AS losses,
               SUM(CASE WHEN m.home_team_id = t.id THEN m.home_goals ELSE m.away_goals END) AS goals_for,
               SUM(CASE WHEN m.home_team_id = t.id THEN m.away_goals ELSE m.home_goals END) AS goals_against,
               SUM(CASE WHEN (m.home_team_id = t.id AND m.home_goals > m.away_goals) OR (m.away_team_id = t.id AND m.away_goals > m.home_goals) THEN 3
                        WHEN m.home_goals = m.away_goals THEN 1 ELSE 0 END) AS points
        FROM teams t
        JOIN matches m ON t.id IN (m.home_team_id, m.away_team_id)
        JOIN seasons s ON s.id = m.season_id
        JOIN leagues l ON l.id = s.league_id
        WHERE s.season = ? AND l.name = ?
        GROUP BY t.name
        ORDER BY points DESC, goals_for - goals_against DESC, goals_for DESC
        """,
        conn,
        params=(season, league)
    )


def get_league_home_table(conn, league, season):
    return pd.read_sql(
        """
        SELECT t.name AS team,
               COUNT(*) AS matches,
               SUM(CASE WHEN m.home_goals > m.away_goals THEN 1 ELSE 0 END) AS wins,
               SUM(CASE WHEN m.home_goals = m.away_goals THEN 1 ELSE 0 END) AS draws,
               SUM(CASE WHEN m.home_goals < m.away_goals THEN 1 ELSE 0 END) AS losses,
               SUM(m.home_goals) AS goals_for,
               SUM(m.away_goals) AS goals_against,
               SUM(CASE WHEN m.home_goals > m.away_goals THEN 3
                        WHEN m.home_goals = m.away_goals THEN 1 ELSE 0 END) AS points
        FROM teams t
        JOIN matches m ON t.id = m.home_team_id
        JOIN seasons s ON s.id = m.season_id
        JOIN leagues l ON l.id = s.league_id
        WHERE s.season = ? AND l.name = ?
        GROUP BY t.name
        ORDER BY points DESC, goals_for - goals_against DESC, goals_for DESC
        """,
        conn,
        params=(season, league)
    )


def get_league_away_table(conn, league, season):
    return pd.read_sql(
        """
        SELECT t.name AS team,
               COUNT(*) AS matches,
               SUM(CASE WHEN m.away_goals > m.home_goals THEN 1 ELSE 0 END) AS wins,
               SUM(CASE WHEN m.away_goals = m.home_goals THEN 1 ELSE 0 END) AS draws,
               SUM(CASE WHEN m.away_goals < m.home_goals THEN 1 ELSE 0 END) AS losses,
               SUM(m.away_goals) AS goals_for,
               SUM(m.home_goals) AS goals_against,
               SUM(CASE WHEN m.away_goals > m.home_goals THEN 3
                        WHEN m.away_goals = m.home_goals THEN 1 ELSE 0 END) AS points
        FROM teams t
        JOIN matches m ON t.id = m.away_team_id
        JOIN seasons s ON s.id = m.season_id
        JOIN leagues l ON l.id = s.league_id
        WHERE s.season = ? AND l.name = ?
        GROUP BY t.name
        ORDER BY points DESC, goals_for - goals_against DESC, goals_for DESC
        """,
        conn,
        params=(season, league)
    )


def get_league_trend_statistics(conn, league):
    return pd.read_sql(
        """
        SELECT s.season,
               ROUND(1.0 * SUM(m.home_goals + m.away_goals) / COUNT(*), 2) AS average_goals_per_match,
               ROUND(1.0 * SUM(m.home_shots + m.away_shots) / COUNT(*), 2) AS average_shots_per_match,
               ROUND(1.0 * SUM(m.home_shots_on_target + m.away_shots_on_target) / COUNT(*), 2) AS average_shots_on_target,
               ROUND(1.0 * SUM(m.home_corners + m.away_corners) / COUNT(*), 2) AS average_corners_per_match,
               ROUND(1.0 * SUM(m.home_yellow_cards + m.away_yellow_cards) / COUNT(*), 2) AS average_yellow_cards_per_match,
               ROUND(1.0 * SUM(m.home_red_cards + m.away_red_cards) / COUNT(*), 2) AS average_red_cards_per_match
        FROM matches m
        JOIN seasons s
          ON s.id = m.season_id
        JOIN leagues l
          ON l.id = s.league_id
        WHERE l.name = ?
        GROUP BY s.season
        ORDER BY s.season DESC
        """,
        conn,
        params=(league,)
    )


# -----------------------------
# Team Analysis Page Queries
# -----------------------------


def get_team_statistics(conn, team, window):
    return pd.read_sql(
        """
        SELECT t.name AS team,
               COUNT(*) AS matches,
               SUM(CASE WHEN (m.home_team_id = t.id AND m.home_goals > m.away_goals) OR (m.away_team_id = t.id AND m.away_goals > m.home_goals) THEN 1 ELSE 0 END) AS wins,
               SUM(CASE WHEN m.home_goals = m.away_goals THEN 1 ELSE 0 END) AS draws,
               SUM(CASE WHEN (m.home_team_id = t.id AND m.home_goals < m.away_goals) OR (m.away_team_id = t.id AND m.away_goals < m.home_goals) THEN 1 ELSE 0 END) AS losses,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.home_goals ELSE m.away_goals END) / COUNT(*), 2) AS avg_goals_for,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.away_goals ELSE m.home_goals END) / COUNT(*), 2) AS avg_goals_against,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.home_corners ELSE m.away_corners END) / COUNT(*), 2) AS avg_corners_for,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.away_corners ELSE m.home_corners END) / COUNT(*), 2) AS avg_corners_against,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.home_shots ELSE m.away_shots END) / COUNT(*), 2) AS avg_shots_for,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.away_shots ELSE m.home_shots END) / COUNT(*), 2) AS avg_shots_against,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.home_shots_on_target ELSE m.away_shots_on_target END) / COUNT(*), 2) AS avg_shots_on_target_for,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.away_shots_on_target ELSE m.home_shots_on_target END) / COUNT(*), 2) AS avg_shots_on_target_against,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.home_yellow_cards ELSE m.away_yellow_cards END) / COUNT(*), 2) AS avg_yellow_cards_for,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.away_yellow_cards ELSE m.home_yellow_cards END) / COUNT(*), 2) AS avg_yellow_cards_against,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.home_red_cards ELSE m.away_red_cards END) / COUNT(*), 2) AS avg_red_cards_for,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.away_red_cards ELSE m.home_red_cards END) / COUNT(*), 2) AS avg_red_cards_against
        FROM teams t
        JOIN matches m ON m.home_team_id = t.id OR m.away_team_id = t.id
        WHERE t.name = ? AND m.id IN (
            SELECT id FROM matches m2 
            WHERE (m2.home_team_id = t.id OR m2.away_team_id = t.id)
            ORDER BY m2.date DESC
            LIMIT ?
        )
        GROUP BY t.name
        """,
        conn,
        params=(team, window)
    )


def get_team_trend_statistics(conn, team):
    return pd.read_sql(
        """
        SELECT s.season,
               COUNT(*) AS matches,
               SUM(CASE WHEN (m.home_team_id = t.id AND m.home_goals > m.away_goals) OR (m.away_team_id = t.id AND m.away_goals > m.home_goals) THEN 1 ELSE 0 END) AS wins,
               SUM(CASE WHEN m.home_goals = m.away_goals THEN 1 ELSE 0 END) AS draws,
               SUM(CASE WHEN (m.home_team_id = t.id AND m.home_goals < m.away_goals) OR (m.away_team_id = t.id AND m.away_goals < m.home_goals) THEN 1 ELSE 0 END) AS losses,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.home_goals ELSE m.away_goals END) / COUNT(*), 2) AS avg_goals_for,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.away_goals ELSE m.home_goals END) / COUNT(*), 2) AS avg_goals_against,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.home_corners ELSE m.away_corners END) / COUNT(*), 2) AS avg_corners_for,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.away_corners ELSE m.home_corners END) / COUNT(*), 2) AS avg_corners_against,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.home_shots ELSE m.away_shots END) / COUNT(*), 2) AS avg_shots_for,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.away_shots ELSE m.home_shots END) / COUNT(*), 2) AS avg_shots_against,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.home_shots_on_target ELSE m.away_shots_on_target END) / COUNT(*), 2) AS avg_shots_on_target_for,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.away_shots_on_target ELSE m.home_shots_on_target END) / COUNT(*), 2) AS avg_shots_on_target_against,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.home_yellow_cards ELSE m.away_yellow_cards END) / COUNT(*), 2) AS avg_yellow_cards_for,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.away_yellow_cards ELSE m.home_yellow_cards END) / COUNT(*), 2) AS avg_yellow_cards_against,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.home_red_cards ELSE m.away_red_cards END) / COUNT(*), 2) AS avg_red_cards_for,
               ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t.id THEN m.away_red_cards ELSE m.home_red_cards END) / COUNT(*), 2) AS avg_red_cards_against
        FROM teams t
        JOIN matches m ON m.home_team_id = t.id OR m.away_team_id = t.id
        JOIN seasons s ON s.id = m.season_id
        WHERE t.name = ?
        GROUP BY s.season
        ORDER BY s.season DESC
        """,
        conn,
        params=(team,)
    )


def get_recent_team_form(conn, team, window):
    recent_matches = pd.read_sql(
        """
        SELECT m.date, ht.name AS home_team, at.name AS away_team,
               m.home_goals, m.away_goals,
               CASE WHEN m.home_team_id = t.id THEN ht.name ELSE at.name END AS name
        FROM matches m
        JOIN teams t ON t.id IN (m.home_team_id, m.away_team_id)
        JOIN teams ht ON ht.id = m.home_team_id
        JOIN teams at ON at.id = m.away_team_id
        WHERE t.name = ?
        ORDER BY m.date DESC
        LIMIT ?
        """,
        conn,
        params=(team, window)
    )

    form = ["?"]
    for _, row in recent_matches.iterrows():
        if row["home_team"] == row["name"]:
            if row["home_goals"] > row["away_goals"]:
                form.append("W")
            elif row["home_goals"] < row["away_goals"]:
                form.append("L")
            else:
                form.append("D")
        else:
            if row["away_goals"] > row["home_goals"]:
                form.append("W")
            elif row["away_goals"] < row["home_goals"]:
                form.append("L")
            else:
                form.append("D")

    return " ".join(form)


def get_recent_team_matches(conn, team, window):
    return pd.read_sql(
        """
        SELECT 
            m.date, 
            ht.name AS home_team, 
            at.name AS away_team,
            m.home_goals, 
            m.away_goals,
            CASE WHEN ht.name = ? THEN
                CASE WHEN m.home_goals > m.away_goals THEN 'W'
                     WHEN m.home_goals < m.away_goals THEN 'L'
                     ELSE 'D' END
            ELSE
                CASE WHEN m.away_goals > m.home_goals THEN 'W'
                     WHEN m.away_goals < m.home_goals THEN 'L'
                     ELSE 'D' END
            END AS result
        FROM matches m
        JOIN teams ht ON ht.id = m.home_team_id
        JOIN teams at ON at.id = m.away_team_id
        WHERE ht.name = ? OR at.name = ?
        ORDER BY m.date DESC
        LIMIT ?
        """,
        conn,
        params=(team, team, team, window)
    )   


# -----------------------------
# Head-to-Head Page Queries
# -----------------------------

def get_recent_head_to_head_statistics(conn, team_a, team_b, window):
    return pd.read_sql(
        """
        SELECT
            COUNT(*) AS matches,
            SUM(CASE WHEN m.home_team_id = t_a.id AND m.home_goals > m.away_goals THEN 1
                     WHEN m.away_team_id = t_a.id AND m.away_goals > m.home_goals THEN 1 ELSE 0 END) AS team_a_wins,
            SUM(CASE WHEN m.home_goals = m.away_goals THEN 1 ELSE 0 END) AS draws,
            SUM(CASE WHEN m.home_team_id = t_b.id AND m.home_goals > m.away_goals THEN 1
                     WHEN m.away_team_id = t_b.id AND m.away_goals > m.home_goals THEN 1 ELSE 0 END) AS team_b_wins,
            ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t_a.id THEN m.home_goals ELSE m.away_goals END) / COUNT(*), 2) AS avg_team_a_goals,
            ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t_b.id THEN m.home_goals ELSE m.away_goals END) / COUNT(*), 2) AS avg_team_b_goals,
            ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t_a.id THEN m.home_shots ELSE m.away_shots END) / COUNT(*), 2) AS avg_team_a_shots,
            ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t_b.id THEN m.home_shots ELSE m.away_shots END) / COUNT(*), 2) AS avg_team_b_shots,
            ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t_a.id THEN m.home_shots_on_target ELSE m.away_shots_on_target END) / COUNT(*), 2) AS avg_team_a_shots_on_target,
            ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t_b.id THEN m.home_shots_on_target ELSE m.away_shots_on_target END) / COUNT(*), 2) AS avg_team_b_shots_on_target,
            ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t_a.id THEN m.home_corners ELSE m.away_corners END) / COUNT(*), 2) AS avg_team_a_corners,
            ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t_b.id THEN m.home_corners ELSE m.away_corners END) / COUNT(*), 2) AS avg_team_b_corners,
            ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t_a.id THEN m.home_yellow_cards ELSE m.away_yellow_cards END) / COUNT(*), 2) AS avg_team_a_yellow_cards,
            ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t_b.id THEN m.home_yellow_cards ELSE m.away_yellow_cards END) / COUNT(*), 2) AS avg_team_b_yellow_cards,
            ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t_a.id THEN m.home_red_cards ELSE m.away_red_cards END) / COUNT(*), 2) AS avg_team_a_red_cards,
            ROUND(1.0 * SUM(CASE WHEN m.home_team_id = t_b.id THEN m.home_red_cards ELSE m.away_red_cards END) / COUNT(*), 2) AS avg_team_b_red_cards
        FROM matches m
        JOIN teams t_a ON t_a.name = ?
        JOIN teams t_b ON t_b.name = ?
        WHERE (m.home_team_id = t_a.id AND m.away_team_id = t_b.id) OR (m.home_team_id = t_b.id AND m.away_team_id = t_a.id)
        AND m.id IN (
            SELECT id FROM matches m2
            WHERE (m2.home_team_id = t_a.id AND m2.away_team_id = t_b.id) OR (m2.home_team_id = t_b.id AND m2.away_team_id = t_a.id)
            ORDER BY m2.date DESC
            LIMIT ?
        )
        """,
        conn,
        params=(team_a, team_b, window)
    )


def get_recent_head_to_head_matches(conn, team_a, team_b, window):
    return pd.read_sql(
        """
        SELECT
            m.date,
            ht.name AS home_team,
            at.name AS away_team,
            m.home_goals,
            m.away_goals,
            m.home_shots,
            m.away_shots,
            m.home_shots_on_target,
            m.away_shots_on_target,
            m.home_corners,
            m.away_corners,
            m.home_yellow_cards,
            m.away_yellow_cards,
            m.home_red_cards,
            m.away_red_cards
        FROM matches m
        JOIN teams ht ON ht.id = m.home_team_id
        JOIN teams at ON at.id = m.away_team_id
        WHERE (ht.name = ? AND at.name = ?) OR (ht.name = ? AND at.name = ?)
        ORDER BY m.date DESC
        LIMIT ?
        """,
        conn,
        params=(team_a, team_b, team_b, team_a, window)
    )


# -----------------------------
# Match Analysis Page Queries
# -----------------------------

def get_match_statistics(conn, country, league, season, home_team, away_team, date):
    return pd.read_sql(
        """
        SELECT m.date, ht.name AS home_team, at.name AS away_team,
               m.home_goals, m.away_goals,
               m.home_shots, m.away_shots,
               m.home_shots_on_target, m.away_shots_on_target,
               m.home_corners, m.away_corners,
               m.home_yellow_cards, m.away_yellow_cards,
               m.home_red_cards, m.away_red_cards
        FROM matches m
        JOIN teams ht ON ht.id = m.home_team_id
        JOIN teams at ON at.id = m.away_team_id
        JOIN seasons s ON s.id = m.season_id
        JOIN leagues l ON l.id = s.league_id
        JOIN countries c ON c.id = l.country_id
        WHERE c.name = ? AND l.name = ? AND s.season = ?
          AND ht.name = ? AND at.name = ? AND m.date = ?
        """,
        conn,
        params=(country, league, season, home_team, away_team, date)
    )


def get_recent_team_form_before_date(conn, team, window, date):
    recent_matches = pd.read_sql(
        """
        SELECT m.date, ht.name AS home_team, at.name AS away_team,
               m.home_goals, m.away_goals,
               CASE WHEN m.home_team_id = t.id THEN ht.name ELSE at.name END AS name
        FROM matches m
        JOIN teams t ON t.id IN (m.home_team_id, m.away_team_id)
        JOIN teams ht ON ht.id = m.home_team_id
        JOIN teams at ON at.id = m.away_team_id
        WHERE t.name = ? AND m.date < ?
        ORDER BY m.date DESC
        LIMIT ?
        """,
        conn,
        params=(team, date, window)
    )

    form = ["?"]
    for _, row in recent_matches.iterrows():
        if row["home_team"] == row["name"]:
            if row["home_goals"] > row["away_goals"]:
                form.append("W")
            elif row["home_goals"] < row["away_goals"]:
                form.append("L")
            else:
                form.append("D")
        else:
            if row["away_goals"] > row["home_goals"]:
                form.append("W")
            elif row["away_goals"] < row["home_goals"]:
                form.append("L")
            else:
                form.append("D")

    return " ".join(form)


def get_head_to_head_matches_before_date(conn, team_a, team_b, window, date):
    return pd.read_sql(
        """
        SELECT 
            m.date,
            ht.name AS home_team,
            at.name AS away_team,
            m.home_goals,
            m.away_goals,
            m.home_shots,
            m.away_shots,
            m.home_shots_on_target,
            m.away_shots_on_target,
            m.home_corners,
            m.away_corners,
            m.home_yellow_cards,
            m.away_yellow_cards,
            m.home_red_cards,
            m.away_red_cards
        FROM matches m
        JOIN teams ht ON ht.id = m.home_team_id
        JOIN teams at ON at.id = m.away_team_id
        WHERE ((ht.name = ? AND at.name = ?) OR (ht.name = ? AND at.name = ?))
          AND m.date < ?
        ORDER BY m.date DESC
        LIMIT ?
        """,
        conn,
        params=(team_a, team_b, team_b, team_a, date, window)
    )
