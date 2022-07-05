from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:" \
                          f"{os.getenv('POSTGRES_PASSWORD', 'postgres')}" \
                          f"@db:5432/{os.getenv('POSTGRES_DB', 'fastapiauth')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
