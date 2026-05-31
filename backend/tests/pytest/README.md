# Testes Pytest - BiotecPredict

Guia completo de testes unitários e integração com pytest.

## 📋 Estrutura

```
pytest/
├── README.md                      # Este arquivo
├── conftest.py                    # Fixtures compartilhadas
├── unit/                          # Testes unitários
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_schemas.py
│   ├── test_schemas_base.py
│   ├── test_processors.py
│   └── test_validators.py
├── integration/                   # Testes de integração
│   ├── __init__.py
│   ├── test_routes.py
│   ├── test_batch_service.py
│   ├── test_compliance_service.py
│   └── test_ml_service.py
├── repositories/                  # Testes de repositórios
│   ├── __init__.py
│   ├── test_batch_repository.py
│   ├── test_sensor_reading_repository.py
│   └── test_prediction_repository.py
├── database/                      # Testes de banco de dados
│   ├── __init__.py
│   └── test_database.py
├── error_handling/                # Testes de tratamento de erros
│   ├── __init__.py
│   └── test_error_handling.py
├── health/                        # Testes de saúde
│   ├── __init__.py
│   └── test_health.py
└── fixtures/                      # Fixtures customizadas
    ├── __init__.py
    ├── batch_fixtures.py
    ├── sensor_fixtures.py
    └── prediction_fixtures.py
```

## 🚀 Início Rápido

### Instalar dependências
```bash
cd backend
pip install -r requirements.txt
```

### Executar todos os testes
```bash
pytest tests/pytest/ -v
```

### Executar com cobertura
```bash
pytest tests/pytest/ --cov=backend --cov-report=html --cov-report=term
```

## 📊 Testes por Categoria

### Testes Unitários (`unit/`)

Testes de componentes individuais sem dependências externas.

#### test_models.py
- Testes dos modelos SQLAlchemy
- Validação de campos
- Relacionamentos entre modelos
- Métodos `to_dict()` e `__repr__()`

**Executar:**
```bash
pytest tests/pytest/unit/test_models.py -v
```

#### test_schemas.py
- Testes dos schemas Pydantic
- Validação de entrada/saída
- Conversão de tipos

**Executar:**
```bash
pytest tests/pytest/unit/test_schemas.py -v
```

#### test_schemas_base.py
- Testes de schemas base
- Validações customizadas

**Executar:**
```bash
pytest tests/pytest/unit/test_schemas_base.py -v
```

#### test_processors.py
- Testes do processador CSV
- Parsing de dados
- Validação de formato

**Executar:**
```bash
pytest tests/pytest/unit/test_processors.py -v
```

#### test_validators.py
- Testes de validadores
- Validação de ranges
- Detecção de anomalias

**Executar:**
```bash
pytest tests/pytest/unit/test_validators.py -v
```

### Testes de Integração (`integration/`)

Testes que envolvem múltiplos componentes.

#### test_routes.py
- Testes dos endpoints da API
- Validação de requisições/respostas
- Códigos de status HTTP

**Executar:**
```bash
pytest tests/pytest/integration/test_routes.py -v
```

#### test_batch_service.py
- Testes do serviço de batches
- CRUD de batches
- Processamento de dados

**Executar:**
```bash
pytest tests/pytest/integration/test_batch_service.py -v
```

#### test_compliance_service.py
- Testes do serviço de compliance score
- Cálculo de scores
- Classificações (ACCEPTABLE/WARNING/CRITICAL)

**Executar:**
```bash
pytest tests/pytest/integration/test_compliance_service.py -v
```

#### test_ml_service.py
- Testes do serviço de ML
- Predições
- Confidence scores

**Executar:**
```bash
pytest tests/pytest/integration/test_ml_service.py -v
```

### Testes de Repositórios (`repositories/`)

Testes da camada de acesso a dados.

#### test_batch_repository.py
- Testes CRUD de batches
- Queries customizadas
- Relacionamentos

**Executar:**
```bash
pytest tests/pytest/repositories/test_batch_repository.py -v
```

#### test_sensor_reading_repository.py
- Testes CRUD de leituras de sensores
- Queries por batch
- Filtros por timestamp

**Executar:**
```bash
pytest tests/pytest/repositories/test_sensor_reading_repository.py -v
```

#### test_prediction_repository.py
- Testes CRUD de predições
- Queries por batch
- Histórico de predições

**Executar:**
```bash
pytest tests/pytest/repositories/test_prediction_repository.py -v
```

### Testes de Banco de Dados (`database/`)

Testes de configuração e operações do banco.

#### test_database.py
- Testes de conexão
- Migrations
- Operações CRUD

**Executar:**
```bash
pytest tests/pytest/database/test_database.py -v
```

### Testes de Tratamento de Erros (`error_handling/`)

Testes de cenários de erro.

#### test_error_handling.py
- Testes de exceções
- Tratamento de erros
- Mensagens de erro

**Executar:**
```bash
pytest tests/pytest/error_handling/test_error_handling.py -v
```

### Testes de Saúde (`health/`)

Testes de health checks.

#### test_health.py
- Testes de endpoints de saúde
- Status da aplicação
- Verificação de dependências

**Executar:**
```bash
pytest tests/pytest/health/test_health.py -v
```

## 🔧 Fixtures

### Fixtures Compartilhadas (`conftest.py`)

```python
@pytest.fixture
def db_session():
    """Sessão de banco de dados para testes."""
    # Setup
    # Yield
    # Teardown

@pytest.fixture
def client():
    """Cliente FastAPI para testes."""
    # Setup
    # Yield
    # Teardown

@pytest.fixture
def sample_batch():
    """Batch de exemplo."""
    return Batch(status="PROCESSING")

@pytest.fixture
def sample_sensor_reading(sample_batch):
    """Leitura de sensor de exemplo."""
    return SensorReading(
        batch_id=sample_batch.id,
        temperature=25.0,
        ph=7.0,
        dissolved_oxygen=75.0,
        pressure=5.0,
        agitator_speed=250
    )

@pytest.fixture
def sample_prediction(sample_batch):
    """Predição de exemplo."""
    return Prediction(
        batch_id=sample_batch.id,
        model_version="v1.0.0",
        confidence_score=0.92,
        risk_level="LOW"
    )
```

### Fixtures Customizadas (`fixtures/`)

#### batch_fixtures.py
- Fixtures de batches com diferentes estados
- Batches com dados válidos/inválidos

#### sensor_fixtures.py
- Fixtures de leituras de sensores
- Dados em diferentes ranges

#### prediction_fixtures.py
- Fixtures de predições
- Diferentes níveis de confiança

## 📊 Cobertura de Testes

### Mínimo Requerido
- **70%** de cobertura geral
- **80%** de cobertura de código crítico

### Gerar Relatório
```bash
pytest tests/pytest/ --cov=backend --cov-report=html --cov-report=term
```

### Visualizar Relatório
```bash
# Windows
start htmlcov/index.html

# Mac/Linux
open htmlcov/index.html
```

## 🎯 Markers

### Usar Markers
```python
@pytest.mark.unit
def test_something():
    pass

@pytest.mark.integration
def test_something_else():
    pass

@pytest.mark.slow
def test_slow_operation():
    pass

@pytest.mark.skip(reason="Não implementado")
def test_not_implemented():
    pass
```

### Executar com Markers
```bash
# Apenas testes unitários
pytest tests/pytest/ -m "unit" -v

# Apenas testes de integração
pytest tests/pytest/ -m "integration" -v

# Excluir testes lentos
pytest tests/pytest/ -m "not slow" -v
```

## 🔍 Debugging

### Modo Verbose
```bash
pytest tests/pytest/ -v
```

### Modo Very Verbose
```bash
pytest tests/pytest/ -vv
```

### Mostrar Prints
```bash
pytest tests/pytest/ -s
```

### Parar no Primeiro Erro
```bash
pytest tests/pytest/ -x
```

### Parar após N Erros
```bash
pytest tests/pytest/ --maxfail=3
```

### Debugger
```bash
pytest tests/pytest/ --pdb
```

### Último Traceback
```bash
pytest tests/pytest/ --tb=short
```

## 📝 Convenções

### Nomes de Testes
```python
# ✅ Bom
def test_batch_creation_with_valid_data():
    pass

def test_batch_creation_fails_with_invalid_status():
    pass

# ❌ Ruim
def test_batch():
    pass

def test_1():
    pass
```

### Estrutura de Testes (AAA)
```python
def test_something():
    # Arrange - Preparar dados
    batch = Batch(status="PROCESSING")
    
    # Act - Executar ação
    result = batch.to_dict()
    
    # Assert - Verificar resultado
    assert result["status"] == "PROCESSING"
```

### Docstrings
```python
def test_batch_creation():
    """Test creating a Batch instance."""
    # Implementação
```

## 🚨 Troubleshooting

### Testes falhando
```bash
# Executar com traceback completo
pytest tests/pytest/ --tb=long

# Executar teste específico
pytest tests/pytest/unit/test_models.py::TestBatchModel::test_batch_creation -v
```

### Banco de dados não encontrado
```bash
# Verificar se banco está configurado
python -c "from backend.db.database import engine; engine.connect()"
```

### Imports falhando
```bash
# Adicionar backend ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/pytest/ -v
```

### Fixtures não encontradas
```bash
# Verificar conftest.py
pytest tests/pytest/ --fixtures
```

## 📚 Referências

- [pytest Documentation](https://docs.pytest.org/)
- [pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [pytest Markers](https://docs.pytest.org/en/stable/how-to-use-pytest-marks.html)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/faq/testing.html)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)

## ✅ Checklist

- [ ] Todos os testes passam
- [ ] Cobertura ≥ 70%
- [ ] Sem warnings
- [ ] Fixtures reutilizáveis
- [ ] Testes documentados
- [ ] CI/CD validando

---

**Versão**: 1.0.0  
**Data**: 31 de Maio de 2026  
**Status**: ✅ Guia de Testes Pytest Completo
