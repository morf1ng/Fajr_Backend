from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # Путь к вашей БД

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Ayat(Base):
    __tablename__ = "ayat"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)

class Hadith(Base):
    __tablename__ = "hadith"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)

# Создание таблиц
Base.metadata.create_all(bind=engine)
