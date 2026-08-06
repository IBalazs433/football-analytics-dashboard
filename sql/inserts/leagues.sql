INSERT OR IGNORE INTO leagues(
    code,
    name,
    country_id
)
SELECT
    :league_code,
    :league_name,
    countries.id
FROM countries
WHERE countries.name = :country;
