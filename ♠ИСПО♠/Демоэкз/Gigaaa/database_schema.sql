-- ============================================
-- СКРИПТ БАЗЫ ДАННЫХ
-- Создан: 2026-06-19 22:22:44
-- ============================================

CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('guest','client','manager','admin'))
        );

CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );

CREATE TABLE suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );

CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category_id INTEGER NOT NULL,
            manufacturer TEXT,
            supplier_id INTEGER NOT NULL,
            price REAL NOT NULL CHECK(price >= 0),
            unit TEXT,
            quantity INTEGER NOT NULL CHECK(quantity >= 0),
            discount REAL DEFAULT 0 CHECK(discount >= 0 AND discount <= 100),
            photo_path TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE RESTRICT
        );

CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('новый','в обработке','готов к выдаче','выдан','отменён')),
            pickup_address TEXT NOT NULL,
            order_date TEXT NOT NULL,
            delivery_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
        );

CREATE TABLE order_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            price_at_order REAL NOT NULL CHECK(price_at_order >= 0),
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
        );

