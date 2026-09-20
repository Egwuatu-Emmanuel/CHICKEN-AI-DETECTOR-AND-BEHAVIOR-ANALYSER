import sqlite3
from datetime import datetime

from .config import DATABASE_DIR


class Database:
    def __init__(self):
        self.database_path = DATABASE_DIR / "poultry.db"

        self.connection = sqlite3.connect(
            self.database_path
        )

        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chicken_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chicken_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                x REAL NOT NULL,
                y REAL NOT NULL,
                distance REAL NOT NULL,
                speed REAL NOT NULL
            )
            """
        )

        self.connection.commit()

    def save_activity(
        self,
        chicken_id,
        x,
        y,
        distance,
        speed
    ):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO chicken_activity
            (
                chicken_id,
                timestamp,
                x,
                y,
                distance,
                speed
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                chicken_id,
                datetime.now().isoformat(),
                x,
                y,
                distance,
                speed
            )
        )

        self.connection.commit()

    def close(self):
        self.connection.close()