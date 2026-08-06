INSERT OR IGNORE INTO teams(
    name,
    country_id
)
SELECT 
    DISTINCT HomeTeam,
    (SELECT id FROM countries WHERE name = :country)
FROM staging;
