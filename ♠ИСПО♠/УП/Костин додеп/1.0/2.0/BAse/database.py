import sqlite3
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

# Таблица пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password_hash TEXT,
        role TEXT,
        status TEXT DEFAULT 'active'
    )
''')

# Таблица категорий
cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
''')

# Таблица товаров
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        category_id INTEGER,
        stock INTEGER,
        image_path TEXT,
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    )
''')

# Таблица корзины
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
''')

# Таблица заказов
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        status TEXT,
        order_date TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
''')

# Таблица позиций заказа
cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
''')

# Добавим категории (если пусто)
cursor.execute("SELECT COUNT(*) FROM categories")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO categories (name) VALUES (?)",
                       [("Кухонные",), ("Охотничьи",), ("Коллекционные",), ("Туристические",)])

# Добавим пользователей (если пусто)
cursor.execute("SELECT COUNT(*) FROM users")
if cursor.fetchone()[0] == 0:
    cursor.executemany(
        "INSERT INTO users (email, password_hash, role, status) VALUES (?, ?, ?, ?)",
        [
            ("client@example.com", hash_password("1234"), "client", "active"),
            ("manager@example.com", hash_password("1234"), "manager", "active"),
            ("admin@example.com", hash_password("1234"), "admin", "active"),
        ]
    )

# Добавим тестовые товары (если пусто)
cursor.execute("SELECT COUNT(*) FROM products")
if cursor.fetchone()[0] == 0:
    # Получаем id категорий
    cursor.execute("SELECT category_id, name FROM categories")
    categories = {name: cid for cid, name in cursor.fetchall()}

    products = [
        ("Шеф-нож Samura", 2500, categories["Кухонные"], 10, ""),
        ("Охотничий нож Медведь", 4500, categories["Охотничьи"], 5, ""),
        ("Коллекционный нож Katana Mini", 12000, categories["Коллекционные"], 2, ""),
        ("Туристический нож Gerber", 3800, categories["Туристические"], 7, ""),
    ]

    cursor.executemany(
        "INSERT INTO products (name, price, category_id, stock, image_path) VALUES (?, ?, ?, ?, ?)",
        products
    )

conn.commit()
conn.close()

print("База данных успешно создана и заполнена тестовыми данными.")
