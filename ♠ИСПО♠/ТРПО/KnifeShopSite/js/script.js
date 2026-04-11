// Загрузка товаров
let products = [];
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// Загрузка данных из JSON
async function loadProducts() {
    try {
        const response = await fetch('data/knives.json');
        products = await response.json();
        displayProducts(products);
        updateCartCount();
    } catch (error) {
        console.error('Ошибка загрузки товаров:', error);
    }
}

// Отображение товаров
function displayProducts(productsToShow) {
    const container = document.getElementById('products-container');
    if (!container) return;

    container.innerHTML = productsToShow.map(product => `
        <div class="product-card">
            <h3>${product.name}</h3>
            <p class="category">${product.category}</p>
            <p class="price">${product.price.toLocaleString()} ₽</p>
            <p>${product.description}</p>
            <button class="btn btn-primary" onclick="addToCart(${product.id})">
                В корзину
            </button>
        </div>
    `).join('');
}

// Добавление в корзину
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({ ...product, quantity: 1 });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    alert(`${product.name} добавлен в корзину!`);
}

// Обновление счётчика корзины
function updateCartCount() {
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);
    const countElement = document.getElementById('cart-count');
    if (countElement) {
        countElement.textContent = count;
    }
}

// Фильтрация и сортировка
if (document.getElementById('category-filter')) {
    document.getElementById('category-filter').addEventListener('change', filterAndSort);
    document.getElementById('sort-select').addEventListener('change', filterAndSort);
}

function filterAndSort() {
    const category = document.getElementById('category-filter').value;
    const sortBy = document.getElementById('sort-select').value;
    
    let filtered = category === 'all' 
        ? [...products] 
        : products.filter(p => p.category === category);
    
    if (sortBy === 'price-asc') {
        filtered.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price-desc') {
        filtered.sort((a, b) => b.price - a.price);
    }
    
    displayProducts(filtered);
}

// Загрузка при старте
if (window.location.pathname.includes('catalog')) {
    loadProducts();
}

// Обновление счётчика на всех страницах
updateCartCount();

// Отображение корзины
if (window.location.pathname.includes('cart')) {
    displayCart();
}

function displayCart() {
    const container = document.getElementById('cart-items');
    const totalElement = document.getElementById('cart-total');
    
    if (cart.length === 0) {
        container.innerHTML = '<p>Корзина пуста</p>';
        totalElement.innerHTML = '';
        return;
    }
    
    let total = 0;
    container.innerHTML = cart.map((item, index) => {
        total += item.price * item.quantity;
        return `
            <div class="cart-item">
                <h3>${item.name}</h3>
                <p>Цена: ${item.price.toLocaleString()} ₽</p>
                <p>
                    Количество: 
                    <input type="number" min="1" value="${item.quantity}" 
                           onchange="updateQuantity(${index}, this.value)">
                </p>
                <p>Сумма: ${(item.price * item.quantity).toLocaleString()} ₽</p>
                <button class="btn btn-danger" onclick="removeFromCart(${index})">Удалить</button>
            </div>
        `;
    }).join('');
    
    totalElement.innerHTML = `<h2>Итого: ${total.toLocaleString()} ₽</h2>`;
}

function updateQuantity(index, newQuantity) {
    const quantity = parseInt(newQuantity);
    if (quantity > 0) {
        cart[index].quantity = quantity;
        localStorage.setItem('cart', JSON.stringify(cart));
        displayCart();
        updateCartCount();
    }
}

function removeFromCart(index) {
    cart.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    displayCart();
    updateCartCount();
}

function checkout() {
    if (cart.length === 0) {
        alert('Корзина пуста!');
        return;
    }
    alert('Заказ оформлен! Спасибо за покупку!');
    cart = [];
    localStorage.setItem('cart', JSON.stringify(cart));
    displayCart();
    updateCartCount();
}