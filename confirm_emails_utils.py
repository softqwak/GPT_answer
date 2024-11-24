Для реализации подтверждения регистрации по email в FastAPI потребуется отправить пользователю письмо со ссылкой, содержащей уникальный токен. Когда пользователь перейдёт по ссылке, сервер проверит токен и активирует аккаунт. Вот подробный процесс:

### 1. Настройка почтового сервиса

Для отправки писем нужно подключить SMTP-сервер, например, Gmail, SendGrid или другой почтовый сервис. Ниже представлен пример с использованием Gmail.

#### Установка зависимостей
Для отправки почты можно использовать библиотеку `aiosmtplib` для асинхронной отправки писем. Установите её с помощью команды:
```bash
pip install aiosmtplib
```

### 2. Настройка FastAPI для отправки писем с токеном

Создадим структуру для подтверждения регистрации по email. 

#### Шаг 1: Настройка токенов
Для токенов используем библиотеку `itsdangerous`, чтобы генерировать и проверять токены:
```bash
pip install itsdangerous
```

##### Генерация токенов
В отдельном модуле создадим функцию для создания токенов.

```python
# token_utils.py
from itsdangerous import URLSafeTimedSerializer

SECRET_KEY = "your-secret-key"  # лучше хранить в .env

def generate_confirmation_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt="email-confirmation-salt")

def confirm_token(token: str, expiration=3600) -> str:
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt="email-confirmation-salt",
            max_age=expiration
        )
    except Exception as e:
        return None
    return email
```

#### Шаг 2: Настройка отправки email

```python
# email_utils.py
import aiosmtplib
from email.message import EmailMessage

async def send_confirmation_email(recipient_email: str, token: str):
    msg = EmailMessage()
    msg["Subject"] = "Подтверждение регистрации"
    msg["From"] = "your-email@gmail.com"
    msg["To"] = recipient_email

    confirmation_url = f"http://localhost:8000/confirm?token={token}"
    msg.set_content(f"Перейдите по ссылке, чтобы подтвердить регистрацию: {confirmation_url}")

    # Отправка через SMTP Gmail
    await aiosmtplib.send(
        msg,
        hostname="smtp.gmail.com",
        port=587,
        username="your-email@gmail.com",
        password="your-email-password",
        start_tls=True,
    )
```

#### Шаг 3: Регистрация пользователя и отправка письма

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.email_utils import send_confirmation_email
from app.token_utils import generate_confirmation_token, confirm_token

app = FastAPI()

class User(BaseModel):
    email: EmailStr
    password: str

# Временное хранилище для пользователей
fake_users_db = {}

@app.post("/register")
async def register(user: User):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    token = generate_confirmation_token(user.email)
    await send_confirmation_email(user.email, token)
    
    fake_users_db[user.email] = {"email": user.email, "password": user.password, "is_active": False}
    return {"message": "Проверьте вашу почту для подтверждения регистрации"}

@app.get("/confirm")
async def confirm_email(token: str):
    email = confirm_token(token)
    if not email or email not in fake_users_db:
        raise HTTPException(status_code=400, detail="Недействительный или истекший токен")

    fake_users_db[email]["is_active"] = True
    return {"message": "Регистрация подтверждена! Теперь вы можете войти."}
```

### Краткое объяснение кода

1. **Генерация токена:** `generate_confirmation_token` генерирует токен на основе email.
2. **Отправка письма:** `send_confirmation_email` отправляет письмо с подтверждением на указанный email.
3. **Маршрут регистрации:** `/register` сохраняет пользователя в базе и отправляет токен на email.
4. **Маршрут подтверждения:** `/confirm` принимает токен, проверяет его, активирует пользователя.

### Примечания

- Убедитесь, что ваш SMTP-сервер и данные конфиденциальности настроены правильно.
- В реальном проекте используйте ORM для работы с базой данных и сохранения пользователей.
- Не забудьте заменить значения `SECRET_KEY`, `your-email@gmail.com`, и `your-email-password` на реальные данные, а также хранить их безопасно, например, в `.env` файле.