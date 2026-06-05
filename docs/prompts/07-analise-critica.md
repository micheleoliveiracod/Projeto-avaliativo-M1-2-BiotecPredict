# Prompts — Etapa 7: Análise Crítica de Saídas da IA

Casos documentados em que a saída da IA foi identificada como incorreta ou insuficiente, com descrição do problema, correção aplicada e lição aprendida.

---

## Caso 1 — CI/CD configurado para todas as branches (problema crítico)

**Etapa:** Pipeline CI/CD  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-28  
**Gravidade:** Alta — quebrava todos os PRs de feature

### Problema identificado

O workflow `ci.yml` gerado pela IA configurou o trigger para rodar em **todas as branches**:

```yaml
# VERSÃO INCORRETA gerada pela IA
on:
  push:
    branches: ['**']  # todas as branches
  pull_request:
    branches: ['**']
```

O job `backend-tests` precisava de um serviço PostgreSQL configurado. Quando rodava em branches de feature que ainda não tinham o backend configurado, **todos os testes falhavam com erro de conexão**, bloqueando os PRs de avançar.

### Diagnóstico

A IA interpretou "CI/CD completo" como "rodar em tudo", sem considerar que branches de feature podem estar em estado incompleto durante o desenvolvimento.

### Correção aplicada

```yaml
# VERSÃO CORRIGIDA
on:
  push:
    branches: [develop]
    paths-ignore:
      - 'docs/**'
      - '.kiro/steering/**'
      - '*.md'
  pull_request:
    branches: [develop, main]
```

Restrito a `develop` para pushes, e para PRs direcionados a `develop` ou `main`. Branches de feature não disparam o CI completo, apenas o `release-lint.yml` quando o PR vai para `main`.

### Lição aprendida

Prompts para CI/CD precisam especificar explicitamente **em quais branches** o workflow deve rodar e **por quê**. A IA tende a gerar configurações "máximas" sem considerar o ciclo de vida real do desenvolvimento.

---

## Caso 2 — Microsserviços propostos para um projeto de escopo reduzido

**Etapa:** Arquitetura  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-24  
**Gravidade:** Média — aumentaria complexidade desnecessariamente

### Problema identificado

Ao solicitar a arquitetura do sistema, a IA propôs uma arquitetura de **microsserviços com Docker Swarm**:

```
Serviço de Upload (porta 8001)
Serviço de ML (porta 8002)
Serviço de Compliance (porta 8003)
API Gateway (porta 80)
Message Queue (RabbitMQ)
```

### Diagnóstico

O prompt não especificou restrições de escopo e prazo. A IA generalizou para "melhor prática em produção" sem considerar que o objetivo é uma aplicação demonstrável de escopo acadêmico.

### Correção aplicada

Prompt refinado com restrições explícitas:

```
Restrições de escopo:
- Projeto acadêmico com prazo de 2 semanas
- Time de 1 desenvolvedor
- Objetivo: demonstrar funcionalidades, não escalar para produção
- Monolito modular é suficiente e preferível
```

Resultado: arquitetura simplificada para monolito FastAPI com módulos internos bem separados.

### Lição aprendida

Para decisões arquiteturais, sempre incluir restrições de **escopo, prazo e tamanho do time** no prompt. Sem essas restrições, a IA propõe soluções de nível enterprise que são inadequadas para projetos menores.

---

## Caso 3 — Testes unitários com dependência desnecessária de banco de dados

**Etapa:** Testes automatizados  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-27  
**Gravidade:** Média — testes lentos e frágeis

### Problema identificado

A IA gerou testes para `CSVProcessor` e `DataValidator` usando fixtures que criavam uma sessão real de banco de dados:

```python
# VERSÃO INCORRETA gerada pela IA
def test_csv_processor(db_session):  # fixture com PostgreSQL real
    processor = CSVProcessor(db=db_session)  # desnecessário
    result = processor.process(csv_content)
    assert len(result) > 0
```

Os processors são classes de processamento puro — **não precisam de banco de dados**. Isso tornava os testes unitários dependentes de infraestrutura externa.

### Diagnóstico

A IA reutilizou a fixture `db_session` em todos os testes por consistência, sem avaliar se cada módulo realmente precisava dela.

### Correção aplicada

```python
# VERSÃO CORRIGIDA
def test_csv_processor_valid_content():
    # Sem fixture de banco — teste puro de lógica
    content = "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n36.5,7.2,85.0,1.0,250"
    result = CSVProcessor.process(content)
    assert len(result) == 1
    assert result[0]['temperature'] == 36.5
```

### Lição aprendida

No prompt de geração de testes, especificar explicitamente: **"testes de lógica pura não devem usar fixtures de banco de dados"**. A IA precisa de instrução explícita para distinguir testes unitários de testes de integração.
