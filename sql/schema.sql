PRAGMA foreign_keys = ON;

--------------------------------------------------
-- Countries
--------------------------------------------------

CREATE TABLE IF NOT EXISTS "countries" (
    "id" INTEGER PRIMARY KEY,
    "name" TEXT NOT NULL UNIQUE
);

--------------------------------------------------
-- Teams
--------------------------------------------------

CREATE TABLE IF NOT EXISTS "teams" (
    "id" INTEGER PRIMARY KEY,
    "name" TEXT NOT NULL,
    "country_id" INTEGER NOT NULL,

    UNIQUE("country_id", "name"),

    FOREIGN KEY("country_id")
        REFERENCES "countries"("id")
);

--------------------------------------------------
-- Leagues
--------------------------------------------------

CREATE TABLE IF NOT EXISTS "leagues" (
    "id" INTEGER PRIMARY KEY,
    "code" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "country_id" INTEGER NOT NULL,

    UNIQUE("country_id", "code")

    FOREIGN KEY("country_id")
        REFERENCES "countries"("id")
);

--------------------------------------------------
-- Seasons
--------------------------------------------------

CREATE TABLE IF NOT EXISTS "seasons" (
    "id" INTEGER PRIMARY KEY,
    "league_id" INTEGER NOT NULL,
    "season" TEXT NOT NULL,

    UNIQUE("league_id", "season"),

    FOREIGN KEY("country_id")
        REFERENCES "countries"("id"),
    
    FOREIGN KEY("league_id")
        REFERENCES "leagues"("id")
);

--------------------------------------------------
-- Matches
--------------------------------------------------

CREATE TABLE IF NOT EXISTS "matches" (
    "id" INTEGER PRIMARY KEY,
    "date" TEXT NOT NULL,
    "league_id" INTEGER NOT NULL,
    "season_id" INTEGER NOT NULL,
    "home_team_id" INTEGER NOT NULL,
    "away_team_id" INTEGER NOT NULL,
    "home_goals" INTEGER NOT NULL,
    "away_goals" INTEGER NOT NULL,
    "result" TEXT NOT NULL,
    "home_shots" INTEGER,
    "away_shots" INTEGER,
    "home_shots_on_target" INTEGER,
    "away_shots_on_target" INTEGER,
    "home_corners" INTEGER,
    "away_corners" INTEGER,
    "home_yellow_cards" INTEGER,
    "away_yellow_cards" INTEGER,
    "home_red_cards" INTEGER,
    "away_red_cards" INTEGER,

    UNIQUE("season_id", "date", "home_team_id", "away_team_id"),

    FOREIGN KEY("season_id")
        REFERENCES "seasons"("id"),

    FOREIGN KEY("home_team_id")
        REFERENCES "teams"("id"),

    FOREIGN KEY("away_team_id")
        REFERENCES "teams"("id")
);
