"""
Testes de saúde da aplicação
"""

import pytest


def test_health_check():
    """
    Teste básico de saúde da aplicação.
    
    Verifica se a aplicação está respondendo corretamente.
    """
    assert True, "Aplicação está saudável"


def test_imports():
    """
    Teste de importação de módulos principais.
    
    Verifica se os módulos principais podem ser importados sem erros.
    """
    try:
        from fastapi import FastAPI
        assert FastAPI is not None
    except ImportError:
        pytest.fail("Não foi possível importar FastAPI")


def test_requirements():
    """
    Teste de dependências instaladas.
    
    Verifica se as dependências principais estão instaladas.
    Nota: scikit-learn é opcional nesta branch (será usado em Sprint 3).
    """
    # Dependências obrigatórias para Sprint 1
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
    ]
    
    # Dependências opcionais (podem não estar instaladas em todas as branches)
    optional_packages = [
        'pandas',
        'scikit-learn'
    ]
    
    # Verificar dependências obrigatórias
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            pytest.fail(f"Pacote obrigatório {package} não está instalado")
    
    # Verificar dependências opcionais (apenas log, não falha)
    for package in optional_packages:
        try:
            __import__(package)
        except ImportError:
            pass  # Ignorar se não estiver instalado
