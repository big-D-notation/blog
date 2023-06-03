import unittest
from unittest.mock import Mock
from userdb import UserDB


class UserDBTests(unittest.TestCase):
    def setUp(self):
        self.db = UserDB()
        self.db.cursor = Mock()

    def test_get_user(self):
        # Мокуємо виклик execute та повертаємо дані
        self.db.cursor.fetchone.return_value = (1, "john_doe", "password", "john@example.com")

        # Викликаємо метод get_user
        user = self.db.get_user("john_doe")

        # Перевіряємо, що execute було викликано з правильними аргументами
        self.db.cursor.execute.assert_called_once_with("SELECT * FROM users WHERE username = ?", ("john_doe",))

        # Перевіряємо, що метод повернув очікуваний результат
        self.assertEqual(user, (1, "john_doe", "password", "john@example.com"))

    def test_create_user(self):
    # Мокуємо виклик execute
        self.db.cursor.execute.return_value = None

        # Викликаємо метод create_user
        self.db.create_user("jane_smith", "password123", "jane@example.com")

        # Перевіряємо, що execute було викликано з правильними аргументами
        self.db.cursor.execute.assert_called_once_with(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            ("jane_smith", "password123", "jane@example.com")
        )

        # Перевіряємо, що коміт був викликаний
        self.db.conn.commit.assert_called_once()

    def test_add_post(self):
        # Мокуємо виклик execute
        self.db.cursor.execute.return_value = None

        # Викликаємо метод add_post
        self.db.add_post("john_doe", "Hello World", "This is my first post!")

        # Перевіряємо, що execute було викликано з правильними аргументами
        self.db.cursor.execute.assert_called_once_with("INSERT INTO posts (username, title, content) VALUES (?, ?, ?)",
                                                      ("john_doe", "Hello World", "This is my first post!"))

        # Перевіряємо, що коміт був викликаний
        self.db.conn.commit.assert_called_once()

    def test_get_user_posts(self):
        # Мокуємо виклик execute та повертаємо дані
        self.db.cursor.fetchall.return_value = [(1, "john_doe", "Hello World", "This is my first post!")]

        # Викликаємо метод get_user_posts
        posts = self.db.get_user_posts("john_doe")

        # Перевіряємо, що execute було викликано з правильними аргументами
        self.db.cursor.execute.assert_called_once_with("SELECT * FROM posts WHERE username = ?", ("john_doe",))

        # Перевіряємо, що метод повернув очікуваний результат
        self.assertEqual(posts, [(1, "john_doe", "Hello World", "This is my first post!")])

if __name__ == '__main__':
    unittest.main()