Если куки создаются в браузере только при возвращении обычного словаря (`dict`), а в других случаях — нет, это может быть связано с тем, как вы возвращаете ответ в FastAPI. 

### Проблема

Когда вы возвращаете **обычный словарь** в FastAPI (например, через `return {"key": "value"}`), FastAPI автоматически создает стандартный HTTP-ответ с кодом состояния `200 OK` и отправляет его в браузер. Однако, когда вы пытаетесь использовать другие типы ответов, такие как `JSONResponse` или другие, важно правильно настроить ответы, чтобы гарантировать установку кук в браузере.

### Почему это происходит?

1. **JSONResponse**:
   Когда вы используете `JSONResponse`, это специфичный класс ответа, который устанавливает заголовки `Content-Type: application/json`. Это не всегда работает в контексте куки, если не указать их явно.
   
2. **Другие типы ответов**:
   В ответах типа `HTMLResponse`, `RedirectResponse` или `JSONResponse` необходимо явно установить куки, как это сделано в примере:

   ```python
   response.set_cookie("key", "value", max_age=3600, httponly=True)
   ```

### Как решить эту проблему?

Чтобы куки устанавливались правильно, необходимо использовать **явное создание ответа**, например, через `JSONResponse`, `HTMLResponse`, или `RedirectResponse`, а не просто возвращать словарь.

#### Пример 1: Использование `JSONResponse`

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/login")
async def login():
    # Логика аутентификации пользователя (например, проверка пароля)
    response = JSONResponse(content={"message": "User logged in"})
    response.set_cookie(key="session_id", value="your_session_id", httponly=True, max_age=3600)
    return response
```

#### Пример 2: Использование `HTMLResponse`

Если вы хотите вернуть HTML-страницу и при этом установить куки:

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/home")
async def home():
    response = HTMLResponse(content="<html><body><h1>Home Page</h1></body></html>")
    response.set_cookie(key="session_id", value="your_session_id", httponly=True, max_age=3600)
    return response
```

#### Пример 3: Использование `RedirectResponse`

Если вы хотите перенаправить пользователя и при этом установить куки:

```python
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/redirect")
async def redirect():
    response = RedirectResponse(url="/home")
    response.set_cookie(key="session_id", value="your_session_id", httponly=True, max_age=3600)
    return response
```

### Важные моменты:

- **`response.set_cookie`** должен быть вызван на объекте ответа, например, на объекте `JSONResponse`, `HTMLResponse` или `RedirectResponse`.
- Убедитесь, что вы не забываете передавать куки в правильном контексте, например, при работе с куками для сессий или аутентификации.
- Если вы работаете с **CORS**, убедитесь, что ваш сервер правильно настроен на работу с кук (например, `credentials: 'include'` на фронтенде).
- Используйте **`httponly=True`**, если вы хотите, чтобы кука была доступна только через HTTP-запросы, а не через JavaScript, что повышает безопасность.

### Пример с фронтендом

На стороне клиента, например, при отправке формы с помощью `fetch`, указывайте `credentials: 'include'`:

```javascript
async function loginUser() {
    const formData = new FormData(document.getElementById("loginForm"));
    const data = Object.fromEntries(formData.entries());

    const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
        credentials: "include", // Включаем передачу куки с запросом
    });

    const result = await response.json();
    console.log(result.message); // Успешная регистрация
}
```

### Заключение

Чтобы куки точно устанавливались в браузере, всегда используйте явное создание ответа с установкой куки, например через `JSONResponse`, `HTMLResponse`, или `RedirectResponse`. Просто возвращение словаря не гарантирует создание куки в браузере, поскольку это не приводит к созданию полноценного ответа с нужными заголовками.