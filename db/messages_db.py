import sqlite3
import os


class db:
    _db_instance = None

    def __new__(cls, *args, **kwargs):
        if cls._db_instance is None:
            cls._db_instance = super().__new__(cls)
            return cls._db_instance
        else:
            return cls._db_instance

    def __init__(self):
        if not os.path.exists('./db/messages.db'):
            with open('./db/messages.db', 'x'):
                pass
        if not hasattr(self, 'connection'):
            self.connection = sqlite3.connect("./db/messages.db")
        if not hasattr(self, 'cursor'):
            self.cursor = self.connection.cursor()

    def setup_db(self):
        cur = self.cursor
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS messages (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            sender TEXT NOT NULL,
                            message TEXT NOT NULL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )
                    """)

    def show_messages(self):
        cur = self.cursor
        res = cur.execute("SELECT * FROM messages;")
        return res.fetchall()

    def add_message(self, message, user):
        con = self.connection
        cur = self.cursor
        cur.execute(f"INSERT INTO messages (sender, message) VALUES ('{user}', '{message}');")
        con.commit()

    def drop_db(self):
        con = self.connection
        cur = self.cursor
        cur.execute("DROP TABLE messages;")
        con.commit()
        con.close()
