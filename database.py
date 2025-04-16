import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_name: str = "hay.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self) -> None:
        """Create the donations table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS donations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    donor_name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date DATE NOT NULL,
                    note TEXT
                )
            ''')
            conn.commit()

    def get_all_donations(self) -> List[Dict]:
        """Retrieve all donations from the database."""
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM donations ORDER BY date DESC')
            return [dict(row) for row in cursor.fetchall()]

    def get_donations_by_year(self, year: int) -> List[Dict]:
        """Retrieve donations for a specific year."""
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM donations 
                WHERE strftime('%Y', date) = ? 
                ORDER BY date DESC
            ''', (str(year),))
            return [dict(row) for row in cursor.fetchall()]

    def get_available_years(self) -> List[int]:
        """Get all years that have donation records."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT strftime('%Y', date) as year 
                FROM donations 
                ORDER BY year DESC
            ''')
            return [int(row[0]) for row in cursor.fetchall()]

    def add_donation(self, donor_name: str, amount: float, date: str, note: str = "") -> int:
        """Add a new donation to the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO donations (donor_name, amount, date, note)
                VALUES (?, ?, ?, ?)
            ''', (donor_name, amount, date, note))
            conn.commit()
            return cursor.lastrowid

    def update_donation(self, donation_id: int, donor_name: str, amount: float, 
                       date: str, note: str = "") -> bool:
        """Update an existing donation."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE donations 
                    SET donor_name = ?, amount = ?, date = ?, note = ?
                    WHERE id = ?
                ''', (donor_name, amount, date, note, donation_id))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False

    def delete_donation(self, donation_id: int) -> bool:
        """Delete a donation from the database."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM donations WHERE id = ?', (donation_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False 