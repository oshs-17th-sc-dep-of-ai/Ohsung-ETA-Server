import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    
    def create_posts_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                              post_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                              board_id  INT NOT NULL,
                              user_id   INT NOT NULL,
                              likes     INT DEFAULT 0,
                              dislikes  INT DEFAULT 0,
                              title     TEXT NOT NULL,
                              content   TEXT NOT NULL,
                              posted_at DATETIME NOT NULL
                              );''')
        self.conn.commit()

    def create_users_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                              user_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                              username TEXT UNIQUE NOT NULL,
                              password TEXT NOT NULL
                              );''')
        self.conn.commit()

    # board
    def write_post(self, board_id, user_id, title, content):
        self.cursor.execute("INSERT INTO posts (board_id, user_id, title, content, posted_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)", (board_id, user_id, title, content))
        self.conn.commit()

    def get_popular_posts(self, board_id):
        self.cursor.execute("SELECT * FROM posts WHERE board_id = ? ORDER BY likes DESC", (board_id))
        return self.cursor.fetchall()
    
    def like_post(self, post_id):
        self.cursor.execute("UPDATE posts SET likes = likes + 1 WHERE post_id = ?", (post_id))
        self.conn.commit()

    def dislike_post(self, post_id):
        self.cursor.execute("UPDATE posts SET dislikes = dislikes + 1 WHERE post_id = ?", (post_id))
        self.conn.commit()

    def get_post_by_id(self, board_id, post_id):
        self.cursor.execute("SELECT * FROM posts WHERE board_id = ? AND post_id = ?", (board_id, post_id))
        post = self.cursor.fetchone()
        if post:
            return {
                "post_id": post[0],
                "board_id": post[1],
                "user_id": post[2],
                "likes": post[3],
                "dislikes": post[4],
                "title": post[5],
                "content": post[6],
                "posted_at": post[7]
            }
        else:
            return None

    def update_post(self, board_id, post_id, title, content):
        self.cursor.execute("UPDATE posts SET title = ?, content = ? WHERE board_id = ? AND post_id = ?", (title, content, board_id, post_id))
        if self.cursor.rowcount > 0:
            self.conn.commit()

    def delete_post(self, board_id, post_id):
        self.cursor.execute("DELETE FROM posts WHERE board_id = ? AND post_id = ?", (board_id, post_id))
        if self.cursor.rowcount > 0:
            self.conn.commit()

    # user
    def register_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError: # 무결성 검사
            return None

    def authenticate_user(self, username, password):
        self.cursor.execute("SELECT user_id FROM users WHERE username = ? AND password = ?", (username, password))
        user = self.cursor.fetchone()
        if user:
            return user[0]
        else:
            return None

    def update_user_profile(self, user_id, new_username, new_password):
        if new_username and new_password:
            self.cursor.execute("UPDATE users SET username = ?, password = ? WHERE user_id = ?", (new_username, new_password, user_id))
        elif new_username:
            self.cursor.execute("UPDATE users SET username = ? WHERE user_id = ?", (new_username, user_id))
        elif new_password:
            self.cursor.execute("UPDATE users SET password = ? WHERE user_id = ?", (new_password, user_id))
        else:
            return False

        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        else:
            return False
    def get_user_profile(self, user_id):
        self.cursor.execute("SELECT username FROM users WHERE user_id = ?", (user_id))
        user = self.cursor.fetchone()
        if user:
            return {"username": user[0]}