import unittest
import sqlite3
from userdb import UserDB

class UserDBTests(unittest.TestCase):

    def setUp(self):
        # Ініціалізуємо тестову базу даних або створимо її в пам'яті
        self.conn = sqlite3.connect(":memory:")
        self.db = UserDB()
        self.db.conn = self.conn
        self.db.create_table()

    def tearDown(self):
        # Закриваємо з'єднання з базою даних
        self.conn.close()

    def test_create_user(self):
        # Перевіряємо додавання користувача
        self.db.create_user("john_doe", "password", "john@example.com")
        user = self.db.get_user("john_doe")
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "john_doe")
        self.assertEqual(user[2], "password")
        self.assertEqual(user[3], "john@example.com")

    def test_update_password(self):
        # Додаємо користувача
        self.db.create_user("jane_smith", "password123", "jane@example.com")

        # Перевіряємо зміну пароля користувача
        self.db.update_password("jane_smith", "new_password")
        user = self.db.get_user("jane_smith")
        self.assertEqual(user[2], "new_password")

    def test_add_post(self):
        # Додаємо пост
        self.db.add_post("john_doe", "Hello World", "This is my first post!")

        # Перевіряємо, що пост був доданий
        posts = self.db.get_user_posts("john_doe")
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0][1], "john_doe")
        self.assertEqual(posts[0][2], "Hello World")
        self.assertEqual(posts[0][3], "This is my first post!")

    def test_add_comment(self):
        # Додаємо коментар
        self.db.add_comment(1, "jane_smith", "Great post!")

        # Перевіряємо, що коментар був доданий
        comments = self.db.get_post_comments_by_id(1)
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0][1], 1)
        self.assertEqual(comments[0][2], "jane_smith")
        self.assertEqual(comments[0][3], "Great post!")

    def test_get_user_by_post_id(self):
        # Додаємо пост
        self.db.add_post("john_doe", "Hello World", "This is my first post!")

        # Отримуємо автора посту
        author = self.db.get_user_by_post_id(1)
        self.assertEqual(author[0][0], "john_doe")

    def test_get_user_posts(self):
        # Додаємо пости для користувача
        self.db.add_post("john_doe", "Post 1", "Content 1")
        self.db.add_post("john_doe", "Post 2", "Content 2")

        # Отримуємо пости користувача
        posts = self.db.get_user_posts("john_doe")
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0][1], "john_doe")
        self.assertEqual(posts[0][2], "Post 1")
        self.assertEqual(posts[0][3], "Content 1")
        self.assertEqual(posts[1][1], "john_doe")
        self.assertEqual(posts[1][2], "Post 2")
        self.assertEqual(posts[1][3], "Content 2")

    def test_get_post_comments_by_id(self):
        # Додаємо коментарі до посту
        self.db.add_comment(1, "jane_smith", "Comment 1")
        self.db.add_comment(1, "john_doe", "Comment 2")

        # Отримуємо коментарі до посту
        comments = self.db.get_post_comments_by_id(1)
        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0][1], 1)
        self.assertEqual(comments[0][2], "jane_smith")
        self.assertEqual(comments[0][3], "Comment 1")
        self.assertEqual(comments[1][1], 1)
        self.assertEqual(comments[1][2], "john_doe")
        self.assertEqual(comments[1][3], "Comment 2")

    def test_create_table(self):
        # Переконуємося, що таблиці існують
        tables = self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = [table[0] for table in tables]
        self.assertIn("users", table_names)
        self.assertIn("posts", table_names)
        self.assertIn("comments", table_names)

if __name__ == '__main__':
    unittest.main()