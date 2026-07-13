from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings


# Block to connect to the database using psycopg2 (commented out)

# while True:
#     try:
#         connection = psycopg2.connect(
#             host="localhost",
#             database="social_media",
#             user="postgres",
#             password="nesttutorial2026",
#             cursor_factory=RealDictCursor
#         )
#         cursor = connection.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Error while connecting to PostgreSQL", error)
#         time.sleep(3)




DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(DATABASE_URL, echo=True)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base() 