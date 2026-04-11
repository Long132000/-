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
        <div class="product-card" onclick="showProductModal(${product.id})">
            <div class="product-image">
                🔪
            </div>
            <div class="product-info">
                <p class="category">${product.category}</p>
                <h3>${product.name}</h3>
                <p class="description">${product.description}</p>
                <p class="price">${product.price.toLocaleString()} ₽</p>
                <button class="btn btn-primary" onclick="event.stopPropagation(); addToCart(${product.id})">
                    В корзину
                </button>
            </div>
        </div>
    `).join('');
}

// Модальное окно товара
function showProductModal(productId) {
    const product = products.find(p => p.id === productId);
    
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h2>${product.name}</h2>
            <p class="category">${product.category}</p>
            <p class="price">${product.price.toLocaleString()} ₽</p>
            <p>${product.fullDescription}</p>
            <button class="btn btn-primary" onclick="addToCart(${product.id}); closeModal()">
                Добавить в корзину
            </button>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.remove();
    }
}

// Закрытие модального окна по клику вне его
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.remove();
    }
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
    
    // Анимация добавления
    const btn = event.target;
    btn.textContent = '✓ Добавлено!';
    btn.style.backgroundColor = '#27AE60';
    setTimeout(() => {
        btn.textContent = 'В корзину';
        btn.style.backgroundColor = '';
    }, 1000);
}

// Обновление счётчика корзины
function updateCartCount() {
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);
    const countElement = document.getElementById('cart-count');
    if (countElement) {
        countElement.textContent = count;
    }
}

// Поиск
if (document.getElementById('search-input')) {
    document.getElementById('search-input').addEventListener('input', filterAndSort);
}

// Фильтрация и сортировка
if (document.getElementById('category-filter')) {
    document.getElementById('category-filter').addEventListener('change', filterAndSort);
    document.getElementById('sort-select').addEventListener('change', filterAndSort);
}

function filterAndSort() {
    const searchTerm = document.getElementById('search-input')?.value.toLowerCase() || '';
    const category = document.getElementById('category-filter')?.value || 'all';
    const sortBy = document.getElementById('sort-select')?.value || 'default';
    
    let filtered = products.filter(p => {
        const matchesSearch = p.name.toLowerCase().includes(searchTerm) || 
                             p.description.toLowerCase().includes(searchTerm);
        const matchesCategory = category === 'all' || p.category === category;
        return matchesSearch && matchesCategory;
    });
    
    if (sortBy === 'price-asc') {
        filtered.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price-desc') {
        filtered.sort((a, b) => b.price - a.price);
    }
    
    displayProducts(filtered);
}

// Отображение корзины
if (window.location.pathname.includes('cart')) {
    displayCart();
}

function displayCart() {
    const container = document.getElementById('cart-items');
    const totalElement = document.getElementById('cart-total');
    
    if (!container) return;
    
    if (cart.length === 0) {
        container.innerHTML = '<p style="text-align: center; padding: 2rem;">🛒 Корзина пуста</p>';
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
                <p><strong>Сумма: ${(item.price * item.quantity).toLocaleString()} ₽</strong></p>
                <button class="btn btn-danger" onclick="removeFromCart(${index})">🗑️ Удалить</button>
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

// Оформление заказа
function showCheckoutForm() {
    if (cart.length === 0) {
        alert('Корзина пуста!');
        return;
    }
    
    const formHtml = `
        <div class="checkout-form">
            <h2>Оформление заказа</h2>
            <form onsubmit="submitOrder(event)">
                <div class="form-group">
                    <label>Имя *</label>
                    <input type="text" id="customer-name" required>
                </div>
                <div class="form-group">
                    <label>Телефон *</label>
                    <input type="tel" id="customer-phone" required>
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="customer-email">
                </div>
                <div class="form-group">
                    <label>Адрес доставки *</label>
                    <textarea id="customer-address" required></textarea>
                </div>
                <div class="form-group">
                    <label>Комментарий к заказу</label>
                    <textarea id="order-comment"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Подтвердить заказ</button>
                <button type="button" class="btn" onclick="cancelCheckout()">Отмена</button>
            </form>
        </div>
    `;
    
    const container = document.querySelector('.container');
    const existingForm = document.querySelector('.checkout-form');
    if (existingForm) existingForm.remove();
    
    document.getElementById('cart-items').insertAdjacentHTML('beforebegin', formHtml);
}

function submitOrder(event) {
    event.preventDefault();
    
    const orderData = {
        customer: {
            name: document.getElementById('customer-name').value,
            phone: document.getElementById('customer-phone').value,
            email: document.getElementById('customer-email').value,
            address: document.getElementById('customer-address').value,
            comment: document.getElementById('order-comment').value
        },
        items: cart,
        total: cart.reduce((sum, item) => sum + item.price * item.quantity, 0),
        orderDate: new Date().toISOString()
    };
    
    console.log('Заказ:', orderData);
    alert(`Спасибо за заказ, ${orderData.customer.name}!\nМы свяжемся с вами по телефону ${orderData.customer.phone} для подтверждения.`);
    
    cart = [];
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    
    window.location.href = 'index.html';
}

function cancelCheckout() {
    document.querySelector('.checkout-form')?.remove();
}

// Загрузка при старте
if (window.location.pathname.includes('catalog')) {
    loadProducts();
}

// Обновление счётчика на всех страницах
updateCartCount();