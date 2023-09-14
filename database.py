import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("snake_scores.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS scores (nickname TEXT, score INT)''')
        self.conn.commit()

    def get_top_scores(self):
        top_scores = self.cursor.execute('''SELECT nickname, score FROM scores ORDER BY score DESC LIMIT 5''').fetchall()
        return top_scores

    def insert_score(self, nickname, score):
        self.cursor.execute("INSERT INTO scores (nickname, score) VALUES (?, ?)", (nickname, score))
        self.conn.commit()