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

# Caminho absoluto e único do banco, ancorado neste arquivo (não no cwd de quem
# invoca o processo) — evita que "uvicorn backend.main:app" gere um .db num lugar
# e "cd backend && python main.py" gere outro. Em produção/Docker, DATABASE_URL
# é sempre definida via variável de ambiente (ver deploy/docker-compose.yml) e
# sobrepõe este default.
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/db/
_DEFAULT_DB_PATH = os.path.join(_BASE_DIR, "..", "data", "Biotecpredict.db")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{_DEFAULT_DB_PATH}"
)

# Garante que a pasta do arquivo SQLite exista antes de abrir a conexão
# (sqlite3 não cria diretórios pai sozinho)
if DATABASE_URL.startswith("sqlite:///") and DATABASE_URL not in ("sqlite:///:memory:",):
    db_dir = os.path.dirname(DATABASE_URL.replace("sqlite:///", "", 1))
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

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
