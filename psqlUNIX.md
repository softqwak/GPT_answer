Чтобы настроить FastAPI приложение на сервере Selectel с PostgreSQL и asyncpg, выполните следующие шаги:

1. **Установите PostgreSQL**:
   На сервере Selectel установите PostgreSQL:
   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   ```

2. **Создайте базу данных и пользователя**:
   Войдите в PostgreSQL и настройте базу данных и пользователя:
   ```bash
   sudo -i -u postgres
   psql
   ```
   Затем создайте базу данных и пользователя:
   ```sql
   CREATE DATABASE your_database_name;
   CREATE USER your_user_name WITH PASSWORD 'your_password';
   ALTER ROLE your_user_name SET client_encoding TO 'utf8';
   ALTER ROLE your_user_name SET default_transaction_isolation TO 'read committed';
   ALTER ROLE your_user_name SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_user_name;
   ```
   После этого выйдите из PostgreSQL:
   ```sql
   \q
   exit
   ```

3. **Установите зависимости проекта на сервере**:
   Если вы еще не установили зависимости FastAPI, asyncpg и другие библиотеки, сделайте это:
   ```bash
   pip install fastapi asyncpg databases psycopg2
   ```

4. **Настройте переменные окружения**:
   Создайте файл `.env` на сервере и укажите параметры подключения к базе данных, например:
   ```dotenv
   DATABASE_URL=postgresql+asyncpg://your_user_name:your_password@localhost/your_database_name
   ```

5. **Запустите FastAPI приложение**:
   Убедитесь, что FastAPI приложение на сервере использует переменные окружения для подключения к базе данных. Для запуска используйте команду Uvicorn:
   ```bash
   uvicorn your_app_name:app --host 0.0.0.0 --port 8000
   ```

6. **Настройте firewall и доступы**:
   Проверьте, открыт ли порт для доступа к вашему FastAPI приложению, и настройте его при необходимости.

Эти шаги помогут вам настроить FastAPI приложение на сервере для работы с PostgreSQL через asyncpg.