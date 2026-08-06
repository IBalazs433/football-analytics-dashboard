"""
This script creates the football database and initializes it with the schema defined in the schema.sql file.
"""

from config.settings import SQL_DIR, DATA_DIR

import sqlite3


def main():
    database_path = DATA_DIR / "football.db"
    schema_path = SQL_DIR / "schema.sql"

    conn = sqlite3.connect(database_path)
    conn.executescript(schema_path.read_text())

    conn.close()
    print("Database created successfully.")


if __name__ == "__main__":
    main()
