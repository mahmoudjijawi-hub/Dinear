/**
 * cart.js — منطق السلة والتفاعل مع المنيو
 */

// حالة السلة: { productId: { id, name, price, quantity } }
let cart = {};

// عناصر DOM
const cartItemsEl = document.getElementById('cartItems');
const cartCountEl = document.getElementById('cartCount');
const cartTotalEl = document.getElementById('cartTotal');
const confirmBtn = document.getElementById('confirmOrderBtn');
const cartEmptyEl = document.getElementById('cartEmpty');

// عناصر الموبايل
const cartMobileBar = document.getElementById('cartMobileBar');
const cartMobileToggle = document.getElementById('cartMobileToggle');
const cartCountMobile = document.getElementById('cartCountMobile');
const cartTotalMobile = document.getElementById('cartTotalMobile');
const cartItemsMobile = document.getElementById('cartItemsMobile');
const confirmBtnMobile = document.getElementById('confirmOrderBtnMobile');

// المودال
const orderModal = document.getElementById('orderModal');
const modalSummary = document.getElementById('modalOrderSummary');
const newOrderBtn = document.getElementById('newOrderBtn');
const toastError = document.getElementById('toastError');

// ===== تهيئة الأحداث =====
document.addEventListener('DOMContentLoaded', () => {
    initProductCards();
    initCategoryTabs();
    initCartButtons();
    initMobileCart();
    initModal();
});

/** ربط أحداث بطاقات المنتجات */
function initProductCards() {
    document.querySelectorAll('.product-card').forEach(card => {
        const productId = card.dataset.productId;
        const addBtn = card.querySelector('[data-action="add"]');
        const qtyControl = card.querySelector('[data-action="quantity"]');
        const decreaseBtn = card.querySelector('[data-action="decrease"]');
        const increaseBtn = card.querySelector('[data-action="increase"]');

        addBtn.addEventListener('click', () => {
            const name = card.querySelector('.product-name').textContent;
            const price = parseFloat(card.querySelector('.product-price').textContent.replace('$', ''));
            addToCart(productId, name, price);
            showQuantityControl(card);
        });

        decreaseBtn.addEventListener('click', () => {
            updateQuantity(productId, -1, card);
        });

        increaseBtn.addEventListener('click', () => {
            updateQuantity(productId, 1, card);
        });
    });
}

/** تبويبات الأقسام — تمرير سلس */
function initCategoryTabs() {
    const tabs = document.querySelectorAll('.category-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            const target = document.getElementById(tab.dataset.target);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // تحديث التبويب النشط عند التمرير
    const sections = document.querySelectorAll('.menu-section');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                tabs.forEach(tab => {
                    tab.classList.toggle('active', tab.dataset.target === id);
                });
            }
        });
    }, { rootMargin: '-100px 0px -60% 0px' });

    sections.forEach(section => observer.observe(section));
}

/** أزرار تأكيد الطلب */
function initCartButtons() {
    confirmBtn.addEventListener('click', placeOrder);
    confirmBtnMobile.addEventListener('click', placeOrder);
}

/** توسيع/طي سلة الموبايل */
function initMobileCart() {
    cartMobileToggle.addEventListener('click', () => {
        cartMobileBar.classList.toggle('expanded');
    });
}

/** زر طلب جديد */
function initModal() {
    newOrderBtn.addEventListener('click', () => {
        resetCart();
        orderModal.classList.remove('active');
    });

    orderModal.addEventListener('click', (e) => {
        if (e.target === orderModal) {
            orderModal.classList.remove('active');
        }
    });
}

// ===== منطق السلة =====

function addToCart(productId, name, price) {
    if (cart[productId]) {
        cart[productId].quantity++;
    } else {
        cart[productId] = { id: productId, name, price, quantity: 1 };
    }
    renderCart();
}

function updateQuantity(productId, delta, card) {
    if (!cart[productId]) return;

    cart[productId].quantity += delta;

    if (cart[productId].quantity <= 0) {
        delete cart[productId];
        hideQuantityControl(card);
    } else {
        card.querySelector('.quantity-value').textContent = cart[productId].quantity;
    }

    renderCart();
}

function showQuantityControl(card) {
    card.querySelector('.add-to-cart-btn').style.display = 'none';
    const qtyControl = card.querySelector('.quantity-control');
    qtyControl.classList.add('active');
    qtyControl.querySelector('.quantity-value').textContent = cart[card.dataset.productId].quantity;
}

function hideQuantityControl(card) {
    card.querySelector('.add-to-cart-btn').style.display = 'flex';
    card.querySelector('.quantity-control').classList.remove('active');
}

/** عرض السلة */
function renderCart() {
    const items = Object.values(cart);
    const totalItems = items.reduce((sum, i) => sum + i.quantity, 0);
    const totalPrice = items.reduce((sum, i) => sum + i.price * i.quantity, 0);

    // تحديث العداد والمجموع
    cartCountEl.textContent = totalItems;
    cartTotalEl.textContent = formatPrice(totalPrice);
    cartCountMobile.textContent = totalItems;
    cartTotalMobile.textContent = formatPrice(totalPrice);

    const hasItems = totalItems > 0;
    confirmBtn.disabled = !hasItems;
    confirmBtnMobile.disabled = !hasItems;

    // عرض العناصر
    if (!hasItems) {
        cartEmptyEl.style.display = 'block';
        cartItemsEl.querySelectorAll('.cart-item').forEach(el => el.remove());
        cartItemsMobile.innerHTML = '<p class="cart-empty">سلتك فارغة</p>';
        return;
    }

    cartEmptyEl.style.display = 'none';

    const html = items.map(item => `
        <div class="cart-item">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-detail">${item.quantity} × ${formatPrice(item.price)}</div>
            </div>
            <div class="cart-item-subtotal">${formatPrice(item.price * item.quantity)}</div>
        </div>
    `).join('');

    // تحديث السلة الجانبية
    cartItemsEl.querySelectorAll('.cart-item').forEach(el => el.remove());
    cartItemsEl.insertAdjacentHTML('beforeend', html);

    // تحديث سلة الموبايل
    cartItemsMobile.innerHTML = html;
}

function formatPrice(amount) {
    return '$' + amount.toFixed(2);
}

// ===== تأكيد الطلب =====

async function placeOrder() {
    const items = Object.values(cart).map(item => ({
        product_id: parseInt(item.id),
        quantity: item.quantity,
    }));

    if (items.length === 0) return;

    confirmBtn.disabled = true;
    confirmBtnMobile.disabled = true;

    try {
        const response = await fetch(PLACE_ORDER_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN,
            },
            body: JSON.stringify({ items }),
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || 'حدث خطأ أثناء إرسال الطلب');
        }

        showOrderModal(data);
    } catch (error) {
        showError(error.message);
        confirmBtn.disabled = false;
        confirmBtnMobile.disabled = false;
    }
}

function showOrderModal(data) {
    const itemsHtml = data.items.map(item => `
        <div class="modal-order-item">
            <span>${item.name} × ${item.quantity}</span>
            <span>$${item.subtotal}</span>
        </div>
    `).join('');

    modalSummary.innerHTML = itemsHtml + `
        <div class="modal-order-total">
            <span>المجموع الكلي</span>
            <span>$${data.total}</span>
        </div>
    `;

    orderModal.classList.add('active');
}

function showError(message) {
    toastError.textContent = message;
    toastError.classList.add('show');
    setTimeout(() => toastError.classList.remove('show'), 4000);
}

/** إعادة تعيين السلة */
function resetCart() {
    cart = {};
    renderCart();

    document.querySelectorAll('.product-card').forEach(card => {
        hideQuantityControl(card);
    });
}
