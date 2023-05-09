import sqlite3


class UserDB:
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def get_user(self, username):
        query = "SELECT * FROM users WHERE username = ?"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()

    def create_user(self, username, password):
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        self.cursor.execute(query, (username, password))
        self.conn.commit()

    def update_password(self, username, new_password):
        query = "UPDATE users SET password = ? WHERE username = ?"
        self.cursor.execute(query, (new_password, username))
        self.conn.commit()

