### **Запуск Backend'a**

1. `docker-compose up -d` - поднять PostgreSQL с помощью Docker
2. `poetry shell` - вход в виртуальное окружение
3. `poetry install` - установка зависимостей
4. `python src/manage.py migrate` - выполнить миграции
5. `python src/manage.py clickhouse_migrate` - выполнить миграции в clickhouse
6. `python src/manage.py create_mview` - создать материализованное представление для подсчета количества посетителей
   счетчика по дням
7. `python src/manage.py runserver` - запуск сервера для разработки на http://localhost:8000
8. `pre-commit install` - установить pre commit hook
9. `pre-commit run -a` - запуск линтеров вручную

### **Запуск Frontend'a**
1. `cd src/frontend` - перейти в папку фронтенда
2. `npm ci` - установить зависимости
3. `npm run watch` - сборка для разработки
4. `npm run build` - сборка для продакшена

### **Работа с ClickHouse**
1. `python src/manage.py clickhouse_group_tables` - группировка данных в таблице
