INSERT OR IGNORE INTO teams(
    name,
    country_id
)
SELECT
    DISTINCT AwayTeam,
    (SELECT id FROM countries WHERE name = :country)
FROM staging;
