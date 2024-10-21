# Класс для работы с базой данных
import sqlite3
class Database:
    def __init__(self):
        self.connection = sqlite3.connect('game_scores.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY,
                name TEXT,
                score INTEGER )
        ''')
        self.connection.commit()

    def add_score(self, name, score):
        self.cursor.execute('INSERT INTO scores (name, score) VALUES (?, ?)', (name, score))
        self.connection.commit()

    def get_top_scores(self):
        self.cursor.execute('SELECT name, round(score,2) FROM scores ORDER BY score DESC LIMIT 5')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()