INSERT OR IGNORE INTO seasons(
    league_id,
    season
)
SELECT
    leagues.id,
    :season
FROM leagues
WHERE leagues.code = :league_code 
    AND leagues.country_id = (SELECT id FROM countries WHERE name = :country);
