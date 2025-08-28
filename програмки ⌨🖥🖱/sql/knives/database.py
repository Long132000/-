import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('client', 'manager', 'admin')),
            blocked INTEGER DEFAULT 0
        )
    ''')

    # Таблица корзины (исправлено)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('pending', 'completed', 'canceled')),
            order_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')

    # Таблица категорий
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    # Таблица товаров
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category_id INTEGER NOT NULL,
            stock INTEGER NOT NULL,
            image_path TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    ''')

    # Тестовые данные
    test_users = [
        ('client@test.com', '256', 'client'),
        ('manager@test.com', '256', 'manager'),
        ('admin@test.com', '256', 'admin')
    ]

    # Добавление категорий
    categories = ['Кухонные', 'Охотничьи', 'Туристические']
    for cat in categories:
        cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (cat,))

    # Добавление пользователей
    for email, pwd, role in test_users:
        cursor.execute('''
            INSERT OR IGNORE INTO users (email, password_hash, role)
            VALUES (?, ?, ?)
        ''', (email, hash_password(pwd), role))

    # Добавление товаров
    cursor.execute('''
        INSERT OR IGNORE INTO products (name, price, category_id, stock)
        VALUES 
            ('Нож шеф-повара', 2500, 1, 10),
            ('Охотничий нож', 4500, 2, 5),
            ('Туристический нож', 1500, 3, 8)
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()