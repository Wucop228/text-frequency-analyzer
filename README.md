# text-frequency-analyzer

Сервис для анализа текстовых файлов. Принимает файл, собирает статистику по словоформам с лемматизацией (pymorphy3) и выдает резуьтат в excel

## Как работает

1. Пользователь загружает файл через POST /public/report/export
2. Создаётся запись в БД и запускается фоновая задача
3. Анализатор читает файл построчно, считает частоту словоформ
4. Результат записывается в excel

## Стек

- Python 3.12, FastAPI, async SQLAlchemy, PostgreSQL, Alembic
- pymorphy3 — морфологический анализ
- openpyxl — генерация Excel
- Docker, docker-compose
- Loguru — логирование

## Запуск

```bash
cp .env.example .env

make build     # Сборка и запуск
make migrate   # Миграции
make logs      # Логи
```

## API
 
```bash
# Загрузка файла
curl -X POST http://localhost:8000/public/report/export -F "file=@text.txt"
 
# Статус отчёта 
curl http://localhost:8000/public/report/{id}
 
# Скачать отчёт
curl http://localhost:8000/public/report/{id}/download -o report.xlsx
```