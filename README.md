1. `docker-compose up -d` - поднять PostgreSQL с помощью Docker
2. `poetry shell` - вход в виртуальное окружение
3. `poetry install` - установка зависимостей
4. `python src/manage.py migrate` - выполнить миграции
5. `python src/manage.py clickhouse_migrate` - выполнить миграции в clickhouse
6. `python src/manage.py runserver` - запуск сервера для разработки на http://localhost:8000
7. `pre-commit install` - установить pre commit hook
8. `pre-commit run -a` - запуск линтеров вручную