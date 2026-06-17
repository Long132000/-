import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
from datetime import datetime

# ------------------- КОНСТАНТЫ -------------------
DB_NAME = "database.db"
IMAGES_DIR = "images"
PLACEHOLDER = os.path.join(IMAGES_DIR, "picture.png")
MAX_IMAGE_SIZE = (80, 80)  # Маленькие фото в таблице

# ------------------- БАЗА ДАННЫХ -------------------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Создаёт таблицы и заполняет данными."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Пользователи
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('guest','client','manager','admin'))
        )
    ''')

    # Категории
    cur.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Поставщики
    cur.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Товары
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
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
        )
    ''')

    # Заказы
    cur.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('новый','в обработке','готов к выдаче','выдан','отменён')),
            pickup_address TEXT NOT NULL,
            order_date TEXT NOT NULL,
            delivery_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
        )
    ''')

    # Состав заказа
    cur.execute('''
        CREATE TABLE IF NOT EXISTS order_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            price_at_order REAL NOT NULL CHECK(price_at_order >= 0),
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
        )
    ''')

    # ---------- ЗАПОЛНЯЕМ ДАННЫМИ ----------
    
    # Пользователи
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        users = [
            ('admin', 'admin', 'Администратор Системы', 'admin'),
            ('manager', 'manager', 'Менеджер Петров И.И.', 'manager'),
            ('client', 'client', 'Клиент Иванов А.А.', 'client'),
        ]
        cur.executemany(
            "INSERT INTO users (login, password, full_name, role) VALUES (?, ?, ?, ?)",
            users
        )

    # Категории
    cur.execute("SELECT COUNT(*) FROM categories")
    if cur.fetchone()[0] == 0:
        categories = ['Конструкторы', 'Мягкие игрушки', 'Настольные игры', 'Машинки', 'Куклы']
        for cat in categories:
            cur.execute("INSERT INTO categories (name) VALUES (?)", (cat,))

    # Поставщики
    cur.execute("SELECT COUNT(*) FROM suppliers")
    if cur.fetchone()[0] == 0:
        suppliers = ['ООО "Мир игрушек"', 'ИП Смирнов', 'ЗАО "Детский мир"', 'ООО "Игрушка-Плюс"']
        for sup in suppliers:
            cur.execute("INSERT INTO suppliers (name) VALUES (?)", (sup,))

    # Товары
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        cur.execute("SELECT id, name FROM categories")
        cat_map = {row['name']: row['id'] for row in cur.fetchall()}
        cur.execute("SELECT id, name FROM suppliers")
        sup_map = {row['name']: row['id'] for row in cur.fetchall()}

        products = [
            ('LEGO City Пожарная станция', 'Набор для строительства пожарной станции', cat_map.get('Конструкторы', 1), 'LEGO', sup_map.get('ООО "Мир игрушек"', 1), 2999.99, 'шт', 15, 10, None),
            ('Мягкий мишка Тедди', 'Коричневый медвежонок, высота 40 см', cat_map.get('Мягкие игрушки', 2), 'Teddy&Co', sup_map.get('ИП Смирнов', 2), 1200.00, 'шт', 7, 5, None),
            ('Монополия', 'Классическая настольная игра', cat_map.get('Настольные игры', 3), 'Hasbro', sup_map.get('ЗАО "Детский мир"', 3), 2500.00, 'шт', 3, 0, None),
            ('Радиоуправляемая машинка', 'Внедорожник на пульте', cat_map.get('Машинки', 4), 'RC Toys', sup_map.get('ООО "Игрушка-Плюс"', 4), 4500.00, 'шт', 2, 20, None),
            ('Кукла Барби', 'С аксессуарами', cat_map.get('Куклы', 5), 'Mattel', sup_map.get('ЗАО "Детский мир"', 3), 1800.00, 'шт', 5, 18, None),
        ]
        for p in products:
            cur.execute('''
                INSERT INTO products (name, description, category_id, manufacturer, supplier_id, price, unit, quantity, discount, photo_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', p)

    # Заказы
    cur.execute("SELECT COUNT(*) FROM orders")
    if cur.fetchone()[0] == 0:
        cur.execute("SELECT id FROM users WHERE role='client' LIMIT 1")
        client_row = cur.fetchone()
        if client_row:
            client_id = client_row['id']
            now = datetime.now().isoformat()
            cur.execute('''
                INSERT INTO orders (order_number, user_id, status, pickup_address, order_date, delivery_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('ORD-001', client_id, 'готов к выдаче', 'ул. Ленина, д.5, пункт выдачи', now, None))
            
            cur.execute("SELECT last_insert_rowid()")
            order_id = cur.fetchone()[0]
            cur.execute("SELECT id, price FROM products LIMIT 2")
            for prod in cur.fetchall():
                cur.execute('''
                    INSERT INTO order_details (order_id, product_id, quantity, price_at_order)
                    VALUES (?, ?, ?, ?)
                ''', (order_id, prod['id'], 1, prod['price']))

    conn.commit()
    conn.close()

# ------------------- ИЗОБРАЖЕНИЯ -------------------
def resize_image(image_path, size=MAX_IMAGE_SIZE):
    """Открывает изображение и изменяет размер."""
    try:
        img = Image.open(image_path)
        img.thumbnail(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки: {image_path} - {e}")
        return get_placeholder_image()

def get_placeholder_image():
    """Возвращает изображение-заглушку."""
    if os.path.exists(PLACEHOLDER):
        try:
            img = Image.open(PLACEHOLDER)
            img.thumbnail(MAX_IMAGE_SIZE, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except:
            pass
    # Если заглушки нет, создаём серый квадрат
    img = Image.new('RGB', MAX_IMAGE_SIZE, color='lightgray')
    return ImageTk.PhotoImage(img)

def save_uploaded_image(file_path):
    """Сохраняет изображение в папку images."""
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ('.png', '.jpg', '.jpeg', '.bmp', '.gif'):
        ext = '.png'
    dest = os.path.join(IMAGES_DIR, f"prod_{timestamp}{ext}")
    try:
        img = Image.open(file_path)
        img.thumbnail(MAX_IMAGE_SIZE, Image.LANCZOS)
        img.save(dest)
        return dest
    except Exception as e:
        raise Exception(f"Не удалось сохранить изображение: {e}")

def delete_old_image(path):
    """Удаляет файл изображения."""
    if path and os.path.exists(path) and path != PLACEHOLDER:
        try:
            os.remove(path)
        except:
            pass

# ------------------- ГЛАВНОЕ ПРИЛОЖЕНИЕ -------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Вход в систему")
        self.root.geometry("400x300")
        self.root.minsize(400, 300)
        self.root.resizable(True, True)

        self.current_user = None
        init_database()
        self.show_login_window()

    def show_login_window(self):
        self.clear_window()
        self.root.title("Вход в систему")
        self.root.geometry("400x300")

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Логин:").grid(row=0, column=0, sticky='w', pady=5)
        login_entry = ttk.Entry(frame, width=30)
        login_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Пароль:").grid(row=1, column=0, sticky='w', pady=5)
        pass_entry = ttk.Entry(frame, width=30, show='*')
        pass_entry.grid(row=1, column=1, pady=5)

        def do_login():
            login = login_entry.get().strip()
            password = pass_entry.get().strip()
            if not login or not password:
                messagebox.showerror("Ошибка", "Введите логин и пароль")
                return
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT id, login, full_name, role FROM users WHERE login=? AND password=?",
                (login, password)
            )
            user = cur.fetchone()
            conn.close()
            if user:
                self.current_user = dict(user)
                self.show_main_window()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")

        def guest_login():
            self.current_user = {'id': 0, 'login': 'guest', 'full_name': 'Гость', 'role': 'guest'}
            self.show_main_window()

        ttk.Button(frame, text="Войти", command=do_login).grid(row=2, column=0, pady=10)
        ttk.Button(frame, text="Войти как гость", command=guest_login).grid(row=2, column=1, pady=10)

        self.root.bind('<Return>', lambda e: do_login())

    def show_main_window(self):
        self.clear_window()
        role = self.current_user['role']
        self.root.title(f"Главная – {self.current_user['full_name']} ({role})")
        self.root.geometry("1100x700")

        # Верхняя панель
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(top_frame, text=f"👤 {self.current_user['full_name']}").pack(side=tk.LEFT)
        ttk.Button(top_frame, text="🚪 Выйти", command=self.logout).pack(side=tk.RIGHT)

        # Вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Товары
        self.products_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.products_frame, text="📦 Товары")
        self.init_products_tab(role)

        # Заказы (для менеджера и админа)
        if role in ('manager', 'admin'):
            self.orders_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.orders_frame, text="📋 Заказы")
            self.init_orders_tab(role)

    def logout(self):
        self.current_user = None
        self.show_login_window()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ------------------- ТОВАРЫ -------------------
    def init_products_tab(self, role):
        for child in self.products_frame.winfo_children():
            child.destroy()

        # Верхняя панель с фильтрами
        top_frame = ttk.Frame(self.products_frame)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        if role in ('manager', 'admin'):
            # Поиск
            ttk.Label(top_frame, text="🔍 Поиск:").grid(row=0, column=0, padx=2)
            search_var = tk.StringVar()
            search_entry = ttk.Entry(top_frame, textvariable=search_var, width=20)
            search_entry.grid(row=0, column=1, padx=2)

            # Фильтр по поставщику
            ttk.Label(top_frame, text="Поставщик:").grid(row=0, column=2, padx=2)
            conn = get_db_connection()
            suppliers = [row['name'] for row in conn.execute("SELECT name FROM suppliers ORDER BY name")]
            conn.close()
            filter_var = tk.StringVar(value="Все поставщики")
            filter_combo = ttk.Combobox(top_frame, textvariable=filter_var, 
                                       values=["Все поставщики"] + suppliers, 
                                       state="readonly", width=20)
            filter_combo.grid(row=0, column=3, padx=2)

            # Сортировка по цене
            ttk.Label(top_frame, text="Цена:").grid(row=0, column=4, padx=2)
            sort_price_var = tk.StringVar(value="Без сортировки")
            sort_price_combo = ttk.Combobox(top_frame, textvariable=sort_price_var,
                                           values=["Без сортировки", "По возрастанию", "По убыванию"],
                                           state="readonly", width=14)
            sort_price_combo.grid(row=0, column=5, padx=2)

            # Сортировка по количеству
            ttk.Label(top_frame, text="Кол-во:").grid(row=0, column=6, padx=2)
            sort_qty_var = tk.StringVar(value="Без сортировки")
            sort_qty_combo = ttk.Combobox(top_frame, textvariable=sort_qty_var,
                                         values=["Без сортировки", "По возрастанию", "По убыванию"],
                                         state="readonly", width=14)
            sort_qty_combo.grid(row=0, column=7, padx=2)

            # Обновление в реальном времени
            def on_filter_change(*args):
                self.refresh_products_tree(
                    role, 
                    search_var.get(), 
                    filter_var.get(), 
                    sort_price_var.get(), 
                    sort_qty_var.get()
                )
            
            search_var.trace('w', on_filter_change)
            filter_var.trace('w', on_filter_change)
            sort_price_var.trace('w', on_filter_change)
            sort_qty_var.trace('w', on_filter_change)

            if role == 'admin':
                btn_add = ttk.Button(top_frame, text="➕ Добавить товар", command=self.open_add_product_window)
                btn_add.grid(row=0, column=8, padx=10)
                
                # Кнопка обновления
                btn_refresh = ttk.Button(top_frame, text="🔄 Обновить", 
                                        command=lambda: self.refresh_products_tree(role, search_var.get(), filter_var.get(), sort_price_var.get(), sort_qty_var.get()))
                btn_refresh.grid(row=0, column=9, padx=5)
        else:
            ttk.Label(top_frame, text="📦 Просмотр товаров (без фильтрации)").pack()

        # ✅ ИСПОЛЬЗУЕМ ФРЕЙМ С ПРОКРУТКОЙ ДЛЯ КАРТОЧЕК ТОВАРОВ (ВМЕСТО TREEVIEW)
        # Создаём Canvas с прокруткой для отображения товаров
        canvas_frame = ttk.Frame(self.products_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Хранилище для изображений
        self.product_images = {}
        
        # Загружаем данные
        self.refresh_products_tree(role, '', 'Все поставщики', 'Без сортировки', 'Без сортировки')

    def refresh_products_tree(self, role, search_text, filter_supplier, sort_price, sort_qty):
        """Обновляет отображение товаров (карточками с фото)."""
        # Очищаем старые карточки
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Очищаем старые изображения
        self.product_images = {}

        # Строим запрос
        query = """
            SELECT p.id, p.name, p.description, p.price, p.unit, p.quantity, p.discount, p.photo_path,
                   c.name as category_name, s.name as supplier_name, p.manufacturer
            FROM products p
            JOIN categories c ON p.category_id = c.id
            JOIN suppliers s ON p.supplier_id = s.id
            WHERE 1=1
        """
        params = []

        # Поиск
        if search_text:
            search = f"%{search_text}%"
            query += " AND (p.name LIKE ? OR p.description LIKE ? OR p.manufacturer LIKE ? OR c.name LIKE ? OR s.name LIKE ?)"
            params.extend([search, search, search, search, search])

        # Фильтр по поставщику
        if filter_supplier != "Все поставщики":
            query += " AND s.name = ?"
            params.append(filter_supplier)

        # Сортировка
        if sort_price == "По возрастанию":
            query += " ORDER BY p.price ASC"
        elif sort_price == "По убыванию":
            query += " ORDER BY p.price DESC"

        if sort_qty != "Без сортировки":
            if sort_price == "Без сортировки":
                query += " ORDER BY p.quantity " + ("ASC" if sort_qty == "По возрастанию" else "DESC")
            else:
                query += ", p.quantity " + ("ASC" if sort_qty == "По возрастанию" else "DESC")

        if sort_price == "Без сортировки" and sort_qty == "Без сортировки":
            query += " ORDER BY p.id"

        # Получаем данные
        conn = get_db_connection()
        rows = conn.execute(query, params).fetchall()
        conn.close()

        print(f"📊 Загружено товаров: {len(rows)}")

        # Создаём карточки для каждого товара
        for row in rows:
            card = self.create_product_card(row)
            card.pack(fill=tk.X, padx=5, pady=5)

    def create_product_card(self, row):
        """Создаёт карточку товара с фото."""
        card = ttk.Frame(self.scrollable_frame, relief=tk.RAISED, borderwidth=1)
        
        # Определяем цвет фона
        bg_color = 'white'
        if row['quantity'] == 0:
            bg_color = 'lightblue'
        elif row['discount'] > 17:
            bg_color = '#FFDEAD'
        
        card.configure(style='Card.TFrame')
        
        # Фрейм для фото
        photo_frame = ttk.Frame(card)
        photo_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Загружаем фото
        photo_path = row['photo_path']
        if photo_path and os.path.exists(photo_path):
            photo_img = resize_image(photo_path)
        else:
            photo_img = get_placeholder_image()
        
        # Сохраняем ссылку
        img_id = f"img_{row['id']}"
        self.product_images[img_id] = photo_img
        
        # Отображаем фото
        photo_label = ttk.Label(photo_frame, image=photo_img)
        photo_label.pack()
        
        # Фрейм для информации
        info_frame = ttk.Frame(card)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Название (жирное)
        name_label = ttk.Label(info_frame, text=row['name'], font=('Arial', 12, 'bold'))
        name_label.pack(anchor='w')
        
        # Категория и поставщик
        cat_label = ttk.Label(info_frame, text=f"🏷️ {row['category_name']} | {row['supplier_name']}")
        cat_label.pack(anchor='w')
        
        # Цена
        price = row['price']
        discount = row['discount']
        if discount > 0:
            final_price = price * (1 - discount/100)
            price_frame = ttk.Frame(info_frame)
            price_frame.pack(anchor='w')
            old_price = ttk.Label(price_frame, text=f"{price:.2f} ₽", foreground='red', font=('Arial', 10, 'overstrike'))
            old_price.pack(side=tk.LEFT)
            new_price = ttk.Label(price_frame, text=f" {final_price:.2f} ₽", foreground='black', font=('Arial', 11, 'bold'))
            new_price.pack(side=tk.LEFT)
            discount_label = ttk.Label(info_frame, text=f"Скидка: {discount:.0f}%", foreground='green')
            discount_label.pack(anchor='w')
        else:
            price_label = ttk.Label(info_frame, text=f"💰 {price:.2f} ₽", font=('Arial', 11))
            price_label.pack(anchor='w')
        
        # Количество
        qty_label = ttk.Label(info_frame, text=f"📦 В наличии: {row['quantity']} {row['unit'] or 'шт'}")
        qty_label.pack(anchor='w')
        
        # Описание (если есть)
        if row['description']:
            desc_label = ttk.Label(info_frame, text=f"📝 {row['description'][:100]}...", wraplength=300)
            desc_label.pack(anchor='w')
        
        # Для администратора - кнопки редактирования и удаления
        if self.current_user and self.current_user['role'] == 'admin':
            btn_frame = ttk.Frame(card)
            btn_frame.pack(side=tk.RIGHT, padx=5, pady=5)
            
            edit_btn = ttk.Button(btn_frame, text="✏️", width=3, 
                                 command=lambda: self.open_edit_product_window(row['id']))
            edit_btn.pack(side=tk.TOP, pady=2)
            
            del_btn = ttk.Button(btn_frame, text="🗑️", width=3,
                                command=lambda: self.delete_product(row['id']))
            del_btn.pack(side=tk.TOP, pady=2)
        
        return card

    def delete_product(self, product_id):
        """Удаляет товар."""
        if not messagebox.askyesno("Подтверждение", f"Удалить товар #{product_id}?"):
            return
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Проверяем, есть ли товар в заказах
        cur.execute("SELECT COUNT(*) FROM order_details WHERE product_id=?", (product_id,))
        if cur.fetchone()[0] > 0:
            messagebox.showerror("Ошибка", "Товар присутствует в заказах, удалить нельзя")
            conn.close()
            return
        
        # Получаем путь к фото
        cur.execute("SELECT photo_path FROM products WHERE id=?", (product_id,))
        row = cur.fetchone()
        photo_path = row['photo_path'] if row else None
        
        # Удаляем товар
        cur.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        conn.close()
        
        # Удаляем фото
        if photo_path:
            delete_old_image(photo_path)
        
        messagebox.showinfo("Успех", "✅ Товар удалён")
        
        # Обновляем список
        self.refresh_products_tree(
            self.current_user['role'], 
            '', 
            'Все поставщики', 
            'Без сортировки', 
            'Без сортировки'
        )

    def open_add_product_window(self):
        """Открывает окно добавления товара."""
        if self.current_user['role'] != 'admin':
            return
        EditProductWindow(self.root, self, None)

    def open_edit_product_window(self, product_id):
        """Открывает окно редактирования товара."""
        if self.current_user['role'] != 'admin':
            return
        if hasattr(self, 'edit_window') and self.edit_window and self.edit_window.winfo_exists():
            messagebox.showwarning("Внимание", "Окно редактирования уже открыто")
            return
        self.edit_window = EditProductWindow(self.root, self, product_id)

    # ------------------- ЗАКАЗЫ -------------------
    def init_orders_tab(self, role):
        for child in self.orders_frame.winfo_children():
            child.destroy()

        top_frame = ttk.Frame(self.orders_frame)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        if role == 'admin':
            ttk.Button(top_frame, text="➕ Добавить заказ", command=self.open_add_order_window).pack(side=tk.LEFT, padx=5)

        # Фрейм для таблицы
        tree_frame = ttk.Frame(self.orders_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ('id', 'order_number', 'user', 'status', 'pickup_address', 'order_date', 'delivery_date')
        self.orders_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        self.orders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.orders_tree.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.orders_tree.configure(yscrollcommand=v_scroll.set)

        h_scroll = ttk.Scrollbar(self.orders_frame, orient=tk.HORIZONTAL, command=self.orders_tree.xview)
        h_scroll.pack(fill=tk.X, padx=5)
        self.orders_tree.configure(xscrollcommand=h_scroll.set)

        # Заголовки
        self.orders_tree.heading('id', text='ID')
        self.orders_tree.heading('order_number', text='Артикул заказа')
        self.orders_tree.heading('user', text='Клиент')
        self.orders_tree.heading('status', text='Статус')
        self.orders_tree.heading('pickup_address', text='Адрес выдачи')
        self.orders_tree.heading('order_date', text='Дата заказа')
        self.orders_tree.heading('delivery_date', text='Дата доставки')

        # Ширина колонок
        self.orders_tree.column('id', width=50, anchor='center')
        self.orders_tree.column('order_number', width=120)
        self.orders_tree.column('user', width=150)
        self.orders_tree.column('status', width=120)
        self.orders_tree.column('pickup_address', width=200)
        self.orders_tree.column('order_date', width=150)
        self.orders_tree.column('delivery_date', width=150)

        if role == 'admin':
            self.orders_tree.bind('<Double-1>', self.on_order_double_click)

        self.refresh_orders_tree(role)

    def refresh_orders_tree(self, role):
        """Обновляет таблицу заказов."""
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        conn = get_db_connection()
        query = """
            SELECT o.id, o.order_number, o.status, o.pickup_address, o.order_date, o.delivery_date,
                   u.full_name as user_name
            FROM orders o
            JOIN users u ON o.user_id = u.id
            ORDER BY o.id DESC
        """
        rows = conn.execute(query).fetchall()
        conn.close()

        for row in rows:
            values = (
                row['id'],
                row['order_number'],
                row['user_name'],
                row['status'],
                row['pickup_address'],
                row['order_date'],
                row['delivery_date'] or ''
            )
            self.orders_tree.insert('', tk.END, values=values)

    def on_order_double_click(self, event):
        """Двойной клик по заказу."""
        selected = self.orders_tree.selection()
        if not selected:
            return
        item = selected[0]
        order_id = self.orders_tree.item(item, 'values')[0]
        self.open_edit_order_window(int(order_id))

    def open_add_order_window(self):
        """Открывает окно добавления заказа."""
        if self.current_user['role'] != 'admin':
            return
        EditOrderWindow(self.root, self, None)

    def open_edit_order_window(self, order_id):
        """Открывает окно редактирования заказа."""
        if self.current_user['role'] != 'admin':
            return
        if hasattr(self, 'edit_order_window') and self.edit_order_window and self.edit_order_window.winfo_exists():
            messagebox.showwarning("Внимание", "Окно редактирования заказа уже открыто")
            return
        self.edit_order_window = EditOrderWindow(self.root, self, order_id)

# ------------------- ОКНО РЕДАКТИРОВАНИЯ ТОВАРА -------------------
class EditProductWindow(tk.Toplevel):
    def __init__(self, parent, app, product_id=None):
        super().__init__(parent)
        self.app = app
        self.product_id = product_id
        self.title("Редактирование товара" if product_id else "Добавление товара")
        self.geometry("550x700")
        self.minsize(450, 500)
        self.resizable(True, True)
        self.grab_set()

        self.name_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.manufacturer_var = tk.StringVar()
        self.supplier_var = tk.StringVar()
        self.price_var = tk.DoubleVar()
        self.unit_var = tk.StringVar()
        self.quantity_var = tk.IntVar()
        self.discount_var = tk.DoubleVar()
        self.photo_path_var = tk.StringVar()

        if product_id:
            self.load_product_data()
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas со скроллом для полей
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Поля
        row = 0
        
        if self.product_id:
            ttk.Label(scrollable_frame, text="ID товара:").grid(row=row, column=0, sticky='w', pady=5)
            ttk.Label(scrollable_frame, text=str(self.product_id), foreground='gray').grid(row=row, column=1, sticky='w', pady=5)
            row += 1

        ttk.Label(scrollable_frame, text="Наименование:*").grid(row=row, column=0, sticky='w', pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.name_var, width=40).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Описание:").grid(row=row, column=0, sticky='w', pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.desc_var, width=40).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Категория:*").grid(row=row, column=0, sticky='w', pady=5)
        conn = get_db_connection()
        categories = [row['name'] for row in conn.execute("SELECT name FROM categories ORDER BY name")]
        conn.close()
        self.category_combo = ttk.Combobox(scrollable_frame, textvariable=self.category_var, 
                                          values=categories, state="readonly", width=37)
        self.category_combo.grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Производитель:").grid(row=row, column=0, sticky='w', pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.manufacturer_var, width=40).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Поставщик:*").grid(row=row, column=0, sticky='w', pady=5)
        conn = get_db_connection()
        suppliers = [row['name'] for row in conn.execute("SELECT name FROM suppliers ORDER BY name")]
        conn.close()
        self.supplier_combo = ttk.Combobox(scrollable_frame, textvariable=self.supplier_var, 
                                          values=suppliers, state="readonly", width=37)
        self.supplier_combo.grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Цена:*").grid(row=row, column=0, sticky='w', pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.price_var, width=40).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Единица измерения:").grid(row=row, column=0, sticky='w', pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.unit_var, width=40).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Количество на складе:*").grid(row=row, column=0, sticky='w', pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.quantity_var, width=40).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Действующая скидка (%):").grid(row=row, column=0, sticky='w', pady=5)
        ttk.Entry(scrollable_frame, textvariable=self.discount_var, width=40).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(scrollable_frame, text="Фото товара:").grid(row=row, column=0, sticky='w', pady=5)
        photo_frame = ttk.Frame(scrollable_frame)
        photo_frame.grid(row=row, column=1, pady=5, sticky='w')
        self.photo_label = ttk.Label(photo_frame)
        self.photo_label.pack(side=tk.LEFT)
        ttk.Button(photo_frame, text="📁 Выбрать фото", command=self.choose_photo).pack(side=tk.LEFT, padx=5)
        row += 1

        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="💾 Сохранить", command=self.save_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Отмена", command=self.destroy).pack(side=tk.LEFT, padx=5)

        if self.product_id and self.photo_path_var.get():
            self.update_photo_preview()

    def load_product_data(self):
        conn = get_db_connection()
        row = conn.execute('''
            SELECT p.*, c.name as cat_name, s.name as sup_name
            FROM products p
            JOIN categories c ON p.category_id = c.id
            JOIN suppliers s ON p.supplier_id = s.id
            WHERE p.id = ?
        ''', (self.product_id,)).fetchone()
        conn.close()
        if not row:
            messagebox.showerror("Ошибка", "Товар не найден")
            self.destroy()
            return

        self.name_var.set(row['name'])
        self.desc_var.set(row['description'] or '')
        self.category_var.set(row['cat_name'])
        self.manufacturer_var.set(row['manufacturer'] or '')
        self.supplier_var.set(row['sup_name'])
        self.price_var.set(row['price'])
        self.unit_var.set(row['unit'] or '')
        self.quantity_var.set(row['quantity'])
        self.discount_var.set(row['discount'])
        self.photo_path_var.set(row['photo_path'] or '')

    def choose_photo(self):
        file_path = filedialog.askopenfilename(
            title="Выберите фото товара",
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.photo_path_var.set(file_path)
            self.update_photo_preview()

    def update_photo_preview(self):
        path = self.photo_path_var.get()
        if path and os.path.exists(path):
            img = resize_image(path)
        else:
            img = get_placeholder_image()
        self.photo_label.config(image=img)
        self.photo_label.image = img

    def save_product(self):
        """Сохраняет товар."""
        try:
            name = self.name_var.get().strip()
            if not name:
                raise ValueError("Наименование товара обязательно")
            
            description = self.desc_var.get().strip()
            
            category = self.category_var.get().strip()
            if not category:
                raise ValueError("Выберите категорию")
            
            manufacturer = self.manufacturer_var.get().strip()
            
            supplier = self.supplier_var.get().strip()
            if not supplier:
                raise ValueError("Выберите поставщика")
            
            price = self.price_var.get()
            if price < 0:
                raise ValueError("Цена не может быть отрицательной")
            
            unit = self.unit_var.get().strip()
            
            quantity = self.quantity_var.get()
            if quantity < 0:
                raise ValueError("Количество не может быть отрицательным")
            
            discount = self.discount_var.get()
            if discount < 0 or discount > 100:
                raise ValueError("Скидка должна быть от 0 до 100")
                
        except tk.TclError as e:
            messagebox.showerror("Ошибка", f"Проверьте правильность введённых данных: {e}")
            return
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            return

        conn = get_db_connection()
        cur = conn.cursor()
        
        # Получаем ID категории
        cur.execute("SELECT id FROM categories WHERE name=?", (category,))
        cat_row = cur.fetchone()
        if not cat_row:
            messagebox.showerror("Ошибка", f"Категория '{category}' не найдена")
            conn.close()
            return
        category_id = cat_row['id']

        # Получаем ID поставщика
        cur.execute("SELECT id FROM suppliers WHERE name=?", (supplier,))
        sup_row = cur.fetchone()
        if not sup_row:
            messagebox.showerror("Ошибка", f"Поставщик '{supplier}' не найден")
            conn.close()
            return
        supplier_id = sup_row['id']

        # Обработка фото
        photo_path = self.photo_path_var.get().strip()
        saved_photo = None
        old_photo = None

        if photo_path and os.path.exists(photo_path):
            if not photo_path.startswith(IMAGES_DIR):
                try:
                    saved_photo = save_uploaded_image(photo_path)
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось сохранить изображение: {e}")
                    conn.close()
                    return
            else:
                saved_photo = photo_path

        # Если это редактирование, получаем старое фото
        if self.product_id:
            row = conn.execute("SELECT photo_path FROM products WHERE id=?", (self.product_id,)).fetchone()
            old_photo = row['photo_path'] if row else None

        try:
            if self.product_id:
                # Обновление
                cur.execute('''
                    UPDATE products
                    SET name=?, description=?, category_id=?, manufacturer=?, supplier_id=?,
                        price=?, unit=?, quantity=?, discount=?, photo_path=?
                    WHERE id=?
                ''', (
                    name, description, category_id, manufacturer, 
                    supplier_id, price, unit, quantity, discount, 
                    saved_photo, self.product_id
                ))
                message = "Товар обновлён"
            else:
                # Вставка
                cur.execute('''
                    INSERT INTO products (name, description, category_id, manufacturer, supplier_id, 
                                         price, unit, quantity, discount, photo_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    name, description, category_id, manufacturer, 
                    supplier_id, price, unit, quantity, discount, saved_photo
                ))
                message = "Товар добавлен"

            conn.commit()
            
            # Удаляем старое фото, если оно было заменено
            if old_photo and saved_photo and old_photo != saved_photo:
                delete_old_image(old_photo)

            messagebox.showinfo("Успех", f"✅ {message}")
            
            # Обновляем таблицу
            self.app.refresh_products_tree(
                self.app.current_user['role'], 
                '', 
                'Все поставщики', 
                'Без сортировки', 
                'Без сортировки'
            )
            self.destroy()
            
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка БД", f"Ошибка при сохранении: {e}")
        finally:
            conn.close()

# ------------------- ОКНО РЕДАКТИРОВАНИЯ ЗАКАЗА -------------------
class EditOrderWindow(tk.Toplevel):
    def __init__(self, parent, app, order_id=None):
        super().__init__(parent)
        self.app = app
        self.order_id = order_id
        self.title("Редактирование заказа" if order_id else "Добавление заказа")
        self.geometry("450x400")
        self.minsize(400, 350)
        self.resizable(True, True)
        self.grab_set()

        self.order_number_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.delivery_var = tk.StringVar()

        if order_id:
            self.load_order_data()
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        row = 0
        
        if self.order_id:
            ttk.Label(main_frame, text="ID заказа:").grid(row=row, column=0, sticky='w', pady=5)
            ttk.Label(main_frame, text=str(self.order_id), foreground='gray').grid(row=row, column=1, sticky='w', pady=5)
            row += 1

        ttk.Label(main_frame, text="Артикул заказа:*").grid(row=row, column=0, sticky='w', pady=5)
        entry = ttk.Entry(main_frame, textvariable=self.order_number_var, width=30)
        entry.grid(row=row, column=1, pady=5)
        if self.order_id:
            entry.config(state='readonly')
        row += 1

        ttk.Label(main_frame, text="Статус заказа:*").grid(row=row, column=0, sticky='w', pady=5)
        statuses = ['новый', 'в обработке', 'готов к выдаче', 'выдан', 'отменён']
        self.status_combo = ttk.Combobox(main_frame, textvariable=self.status_var, 
                                        values=statuses, state="readonly", width=27)
        self.status_combo.grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(main_frame, text="Адрес пункта выдачи:*").grid(row=row, column=0, sticky='w', pady=5)
        ttk.Entry(main_frame, textvariable=self.address_var, width=30).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(main_frame, text="Дата заказа (ГГГГ-ММ-ДД):*").grid(row=row, column=0, sticky='w', pady=5)
        ttk.Entry(main_frame, textvariable=self.date_var, width=30).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(main_frame, text="Дата доставки (ГГГГ-ММ-ДД):").grid(row=row, column=0, sticky='w', pady=5)
        ttk.Entry(main_frame, textvariable=self.delivery_var, width=30).grid(row=row, column=1, pady=5)
        row += 1

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="💾 Сохранить", command=self.save_order).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Отмена", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def load_order_data(self):
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM orders WHERE id=?", (self.order_id,)).fetchone()
        conn.close()
        if not row:
            messagebox.showerror("Ошибка", "Заказ не найден")
            self.destroy()
            return
        self.order_number_var.set(row['order_number'])
        self.status_var.set(row['status'])
        self.address_var.set(row['pickup_address'])
        self.date_var.set(row['order_date'])
        self.delivery_var.set(row['delivery_date'] or '')

    def save_order(self):
        try:
            order_number = self.order_number_var.get().strip()
            if not order_number:
                raise ValueError("Артикул заказа обязателен")
            status = self.status_var.get().strip()
            if not status:
                raise ValueError("Выберите статус")
            address = self.address_var.get().strip()
            if not address:
                raise ValueError("Адрес обязателен")
            order_date = self.date_var.get().strip()
            if not order_date:
                raise ValueError("Дата заказа обязательна")
            delivery_date = self.delivery_var.get().strip() or None
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            return

        conn = get_db_connection()
        cur = conn.cursor()

        if self.order_id:
            cur.execute('''
                UPDATE orders
                SET status=?, pickup_address=?, order_date=?, delivery_date=?
                WHERE id=?
            ''', (status, address, order_date, delivery_date, self.order_id))
        else:
            cur.execute("SELECT id FROM users WHERE role='client' LIMIT 1")
            user_row = cur.fetchone()
            if not user_row:
                messagebox.showerror("Ошибка", "Нет клиентов в системе")
                conn.close()
                return
            user_id = user_row['id']
            cur.execute('''
                INSERT INTO orders (order_number, user_id, status, pickup_address, order_date, delivery_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (order_number, user_id, status, address, order_date, delivery_date))

        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", "✅ Заказ сохранён")
        self.app.refresh_orders_tree(self.app.current_user['role'])
        self.destroy()

# ------------------- ЗАПУСК -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()