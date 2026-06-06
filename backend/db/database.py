"""
Configuração do banco de dados SQLAlchemy.

Fornece:
- Base: Classe base para todos os modelos
- engine: Engine do SQLAlchemy
- SessionLocal: Factory de sessões
- get_db: Dependency injection para FastAPI
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

# Configurar URL do banco de dados
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./biotecpredict.db"
)

# Criar engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Criar factory de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar classe base para modelos
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection para obter sessão do banco de dados.
    
    Yields:
        Session: Sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializar banco de dados criando todas as tabelas."""
    Base.metadata.create_all(bind=engine)
