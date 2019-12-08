import sqlite3

class DBService:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._connect()

    def _connect(self):
        if not self.db_name:
            raise Exception('no database specified')
        self.conn = sqlite3.connect('msuspider.db')
        self.cursor = self.conn.cursor()

    def get_texts(self):
        if not self.cursor:
            raise Exception('connect to database first')
        return self.cursor.execute("SELECT * FROM texts").fetchall()