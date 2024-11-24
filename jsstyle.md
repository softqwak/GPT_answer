Вот пример структуры и подхода для написания "правильного" фронтенд-кода на чистом JavaScript для небольшого проекта. Основные принципы:

- **Читабельность**: Код должен быть понятен, с логичным разделением задач.
- **Модульность**: Логика разбивается на отдельные функции/модули.
- **Универсальность**: Код должен быть переиспользуемым.
- **Обработка ошибок**: Всегда проверяйте, что запросы или действия успешны.

---

### Пример структуры кода
#### 1. **Конфигурация**
Создайте файл с общими настройками:
```javascript
// config.js
const API_BASE_URL = 'https://example.com/api';

export const endpoints = {
  getMerch: `${API_BASE_URL}/merch`,
  getTickets: `${API_BASE_URL}/tickets`,
  createOrder: `${API_BASE_URL}/order`,
};
```

---

#### 2. **Функция для работы с API**
Централизованная логика для запросов к серверу:
```javascript
// api.js
export async function fetchData(url, options = {}) {
  try {
    const response = await fetch(url, {
      credentials: 'include', // Для работы с куками
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Fetch error:', error);
    alert('Произошла ошибка. Попробуйте снова.');
    throw error;
  }
}
```

---

#### 3. **Реализация функциональности**
**Добавление товаров в корзину:**
```javascript
// cart.js
let cart = []; // Локальное хранилище корзины

export function addToCart(item) {
  cart.push(item);
  console.log('Cart updated:', cart);
  renderCart();
}

export function removeFromCart(itemId) {
  cart = cart.filter(item => item.id !== itemId);
  console.log('Cart updated:', cart);
  renderCart();
}

function renderCart() {
  const cartContainer = document.querySelector('#cart-items');
  cartContainer.innerHTML = '';
  cart.forEach(item => {
    const itemElement = document.createElement('div');
    itemElement.textContent = `${item.name} — ${item.price} руб.`;
    cartContainer.appendChild(itemElement);
  });
}
```

---

#### 4. **Работа с DOM**
**Динамическое отображение товаров:**
```javascript
// merch.js
import { fetchData } from './api.js';
import { endpoints } from './config.js';
import { addToCart } from './cart.js';

export async function renderMerch() {
  const merchContainer = document.querySelector('#merch-container');
  const merchItems = await fetchData(endpoints.getMerch);

  merchItems.forEach(item => {
    const itemElement = document.createElement('div');
    itemElement.classList.add('merch-item');
    itemElement.innerHTML = `
      <h3>${item.name}</h3>
      <p>${item.price} руб.</p>
      <button data-id="${item.id}">Добавить в корзину</button>
    `;

    itemElement.querySelector('button').addEventListener('click', () => {
      addToCart(item);
    });

    merchContainer.appendChild(itemElement);
  });
}
```

---

#### 5. **Главный файл для инициализации**
```javascript
// app.js
import { renderMerch } from './merch.js';

document.addEventListener('DOMContentLoaded', () => {
  renderMerch();

  // Пример: другие функции, которые нужно запустить на старте
  // renderTickets();
  // setupProfile();
});
```

---

### Особенности кода
1. **Отделение логики и отображения**:
   - Логика работы с данными (API, корзина) отделена от манипуляций с DOM.

2. **Использование событий**:
   - Взаимодействие с пользователем (клики, ввод) реализовано через обработчики событий.

3. **Универсальность функций**:
   - Например, `fetchData` подходит для любых запросов, а не только для одного API.

4. **Модульность**:
   - Каждый файл отвечает за свою часть (API, корзина, отображение).

---

Если у вас уже есть конкретная задача, например, "как оформить корзину" или "как отправить заказ на сервер", могу предложить более конкретный пример.