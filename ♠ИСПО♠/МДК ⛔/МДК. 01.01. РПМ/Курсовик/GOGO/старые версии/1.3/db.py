import sqlite3
import datetime
import logging

DATABASE_FILE = 'python_learning_bot.db'

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Ошибка при подключении к базе данных: {e}")
        return None

def create_user(conn, user_id):
    sql = ''' INSERT INTO users(user_id) VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    conn.commit()
    return cur.lastrowid


def add_question(conn, user_id, topic, question, answer):
    sql = ''' INSERT INTO questions(user_id, topic, question, answer) VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (user_id, topic, question, answer))
    conn.commit()
    return cur.lastrowid

# ... (добавить функции для получения вопросов, проверки ответов и т.д.) ...

def init_db():
    conn = create_connection()
    if conn is None:
        return

    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                topic TEXT,
                question TEXT,
                answer TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка создания таблиц: {e}")
    finally:
        conn.close()

init_db()