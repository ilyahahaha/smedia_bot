# SMedia Bot

Интерактивный user bot на основе Pyrogram.

### Используемый стэк:

- Python 3.11
- PostgreSQL (asyncpg driver)
- Pyrogram
- SQLAlchemy
- Alembic
- APScheduler

------------

### Особенности реализации

- Применен Alembic для миграций измений базы данных
- Используемый планировщик сохраняет задачи в базу данных, что гарантирует выполнение задач даже после внеплановой
  остановки бота."
- CLI для выполнения полезных функций и запуска бота
- Возможность повторно прогнать воронку, даже после получения триггера на остановку
