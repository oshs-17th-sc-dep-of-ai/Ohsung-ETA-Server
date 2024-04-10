import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                              post_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                              board_id  INT NOT NULL,
                              user_id   INT NOT NULL,
                              likes     INT DEFAULT 0,
                              dislikes  INT DEFAULT 0,
                              title     TEXT NOT NULL,
                              content   TEXT NOT NULL,
                              posted_at DATETIME NOT NULL,
                              );''')
        self.conn.commit()

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