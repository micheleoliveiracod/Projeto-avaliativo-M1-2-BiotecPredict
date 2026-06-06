"""
Módulo de banco de dados.

Fornece:
- database: Configuração do SQLAlchemy
- repository: Repository pattern para acesso a dados
"""

from .database import Base, SessionLocal, engine, get_db, init_db

__all__ = [
    "Base",
    "SessionLocal",
    "engine",
    "get_db",
    "init_db",
]
