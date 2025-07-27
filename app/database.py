from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


# SQLAlCHEMY_DATABASE_URL='postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.databse_port}/{settings.database_name}'
# engine=create_engine(SQLAlCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# print("connet")

# Base=declarative_base()



# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



# # while True:    # run until it get connected it not directly jump to below apis if connection is      failed it will wait for 2 seconds and try again 

# #     try:
# #         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='1234', cursor_factory=RealDictCursor)
# #         cursor=conn.cursor()
# #         print("connected with DB")
# #         break

# #     except Exception as error:
# #         print("connection is failed")
# #         print("error:",error)
# #         time.sleep(2)


# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print("connet")

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()