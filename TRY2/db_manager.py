import sqlite3
import json
from datetime import datetime

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trends (
                    id TEXT PRIMARY KEY,
                    trends TEXT,
                    timestamp TEXT,
                    ip_address TEXT
                )
            ''')

    def insert_trend(self, trend_data):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO trends (id, trends, timestamp, ip_address)
                VALUES (?, ?, ?, ?)
            ''', (
                trend_data['id'],
                json.dumps(trend_data['trends']),
                trend_data['timestamp'],
                trend_data['ip_address']
            ))

    def get_all_trends(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM trends')
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'trends': json.loads(row[1]),
                    'timestamp': row[2],
                    'ip_address': row[3]
                }
                for row in rows
            ]

