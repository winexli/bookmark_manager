import sqlite3
from typing import List, Optional
from contextlib import contextmanager
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str = "bookmarks.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        from database.schema import SCHEMA_QUERIES
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for query in SCHEMA_QUERIES:
                cursor.execute(query)
            conn.commit()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()