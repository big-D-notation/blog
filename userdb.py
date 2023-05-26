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
            password TEXT NOT NULL,
            email TEXT NOT NULL
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

        query = """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

        query = """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            comment TEXT NOT NULL
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def get_user(self, username):
        query = "SELECT * FROM users WHERE username = ?"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()

    def create_user(self, username, password, email):
        query = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
        self.cursor.execute(query, (username, password, email))
        self.conn.commit()

    def update_password(self, username, new_password):
        query = "UPDATE users SET password = ? WHERE username = ?"
        self.cursor.execute(query, (new_password, username))
        self.conn.commit()

    def add_post(self, username, title, content):
        query = "INSERT INTO posts (username, title, content) VALUES (?, ?, ?)"
        self.cursor.execute(query, (username, title, content))
        self.conn.commit()

    def add_comment(self, post_id, username, comment):
        query = "INSERT INTO comments (post_id, username, comment) VALUES (?, ?, ?)"
        self.cursor.execute(query, (post_id, username, comment))
        self.conn.commit()

    def get_user_posts(self, username):
        query = "SELECT * FROM posts WHERE username = ?"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchall()

    def get_post_comments_by_id(self, post_id):
        query = "SELECT * FROM comments WHERE post_id = ?"
        self.cursor.execute(query, (post_id,))
        return self.cursor.fetchall()

    def get_user_by_post_id(self, post_id):
        query = "SELECT username FROM posts WHERE id = ?"
        self.cursor.execute(query, (post_id,))
        return self.cursor.fetchall()
        
        