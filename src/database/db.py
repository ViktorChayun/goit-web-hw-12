from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DB_URL = "postgresql+psycopg2://postgres:567234@localhost:5432/goit_hw11"
engine = create_engine(SQLALCHEMY_DB_URL)

# для створення фабрики сесій, яка використовується для створення сесій для взаємодії з базою даних
# autoflush - це режим, коли будь-які зміни, які ви вносите в об'єкти сесії, автоматично відправляються в базу --> вимкнено
# сесія не буде авто комітити і не буде автоматично скидати зміни в базу даних
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# це залежність, яка повертає сесію з використанням фабрики SessionLocal
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
