from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuration de l'application"""
    database_url: str = "sqlite:///./security_learning.db"
    secret_key: str = "I-YX8WPwNnSM2NYy3tLN_Xq9Y79RNWAtKIhON9iUKFI"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()

# Configuration de la base de données SQLite
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # Nécessaire pour SQLite avec FastAPI
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Générateur de session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Créer toutes les tables"""
    from models import (
        Base, Utilisateur, Cours, Exercice, Question, Note,
        Image, Video, Paragraphe
    )
    Base.metadata.create_all(bind=engine)
