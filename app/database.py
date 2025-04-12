from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Замените на ваши данные для подключения к базе данных
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/cor"

# Создаем движок подключения
engine = create_engine(DATABASE_URL)

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем локальную сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Попробуем подключиться
try:
    with engine.connect() as connection:
        print("Подключение успешно!")
except Exception as e:
    print(f"Ошибка подключения: {e}")