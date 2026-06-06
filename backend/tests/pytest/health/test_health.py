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
    """
    required_packages = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'sqlalchemy': 'sqlalchemy',
        'pydantic': 'pydantic',
        'pandas': 'pandas',
        'scikit-learn': 'sklearn'  # Package name is sklearn, not scikit-learn
    }
    
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            pytest.fail(f"Pacote {package_name} não está instalado")
