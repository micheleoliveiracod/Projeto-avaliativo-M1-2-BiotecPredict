#!/usr/bin/env python3
"""
Script para criar labels, milestones e 30 issues do BiotecPredict no GitHub
Repositório: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict

Segue exatamente as convenções do gitflow.md e gitflow-sprints.md
"""

import subprocess
import sys

REPO = "micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict"

# Labels conforme gitflow.md - Seção "Labels Recomendados"
LABELS = [
    {"name": "backend", "color": "1d76db", "description": "Alterações no backend Python/FastAPI"},
    {"name": "frontend", "color": "28a745", "description": "Alterações no frontend React"},
    {"name": "ml", "color": "6f42c1", "description": "Alterações em machine learning"},
    {"name": "database", "color": "fd7e14", "description": "Alterações no banco de dados"},
    {"name": "api", "color": "0052cc", "description": "Alterações na API REST"},
    {"name": "testing", "color": "ffc107", "description": "Testes e cobertura"},
    {"name": "documentation", "color": "6c757d", "description": "Documentação"},
    {"name": "bug", "color": "dc3545", "description": "Correção de bugs"},
    {"name": "feat", "color": "17a2b8", "description": "Novas funcionalidades"},
    {"name": "chore", "color": "e2e3e5", "description": "Tarefas de manutenção"},
    {"name": "setup", "color": "0e8a16", "description": "Configuração inicial do projeto"},
    {"name": "business-logic", "color": "f9d0c4", "description": "Lógica de negócio"},
    {"name": "validation", "color": "c5def5", "description": "Validação e qualidade"},
    {"name": "sprint-0", "color": "0e8a16", "description": "Issues do Sprint 0"},
    {"name": "sprint-1", "color": "28a745", "description": "Issues do Sprint 1"},
    {"name": "sprint-2", "color": "1d76db", "description": "Issues do Sprint 2"},
    {"name": "sprint-3", "color": "6f42c1", "description": "Issues do Sprint 3"},
    {"name": "sprint-4", "color": "fd7e14", "description": "Issues do Sprint 4"},
    {"name": "sprint-5", "color": "dc3545", "description": "Issues do Sprint 5"},
]

# Milestones dos 6 sprints
MILESTONES = [
    {"title": "Sprint 0 - Setup", "description": "Setup e gerenciamento do projeto"},
    {"title": "Sprint 1 - Backend", "description": "Backend + API + Modelos"},
    {"title": "Sprint 2 - Frontend", "description": "Frontend + Dashboard"},
    {"title": "Sprint 3 - ML", "description": "ML + Compliance + Predição"},
    {"title": "Sprint 4 - Testes", "description": "Testes + Cobertura"},
    {"title": "Sprint 5 - Documentação", "description": "Documentação + Validação + Deploy"},
]

# 30 Issues (5 por sprint) conforme gitflow-sprints.md
ISSUES = [
    # Sprint 0 - Setup (5 issues)
    {
        "title": "setup: estruturar repositorio e diretorios base",
        "labels": ["setup", "backend", "frontend", "sprint-0"],
        "milestone": "Sprint 0 - Setup",
        "body": """## Contexto
Criar estrutura de diretorios conforme steering/structure.md

## Escopo
- Criar diretorios backend (api/, processors/, services/, models/, schemas/, db/, ml/, scripts/, reports/, tests/)
- Criar diretorios frontend (src/components/, src/pages/, src/services/, src/hooks/, src/utils/)
- Criar arquivos README.md em diretorios principais
- Configurar .gitignore para Python e React
- Criar arquivos iniciais (requirements.txt, package.json)

## Criterios de Aceite
- [ ] Estrutura de diretorios criada conforme especificacao
- [ ] Projeto pode ser inicializado localmente
- [ ] Todos os .gitignore configurados corretamente

## Branch
feature/project-structure"""
    },
    {
        "title": "setup: configurar banco de dados PostgreSQL e ORM",
        "labels": ["setup", "database", "backend", "sprint-0"],
        "milestone": "Sprint 0 - Setup",
        "body": """## Contexto
Configurar SQLAlchemy e conexao com PostgreSQL

## Escopo
- Criar modelos SQLAlchemy (Batch, SensorReading, Prediction)
- Implementar repository pattern
- Configurar conexao com SQLite (dev) e PostgreSQL (prod)
- Criar migrations iniciais
- Implementar funcoes CRUD basicas

## Criterios de Aceite
- [ ] Modelos SQLAlchemy funcionando
- [ ] Conexao com banco de dados testada
- [ ] Migrations executadas com sucesso

## Branch
feature/database-setup"""
    },
    {
        "title": "setup: configurar FastAPI e endpoints base",
        "labels": ["setup", "backend", "api", "sprint-0"],
        "milestone": "Sprint 0 - Setup",
        "body": """## Contexto
Configurar FastAPI com estrutura base

## Escopo
- Criar main.py com FastAPI app
- Configurar CORS e middleware
- Criar estrutura de rotas (api/routes/)
- Implementar health check endpoint
- Configurar documentacao Swagger

## Criterios de Aceite
- [ ] FastAPI rodando localmente
- [ ] Swagger acessivel em /docs
- [ ] Health check respondendo

## Branch
feature/fastapi-setup"""
    },
    {
        "title": "setup: configurar React e estrutura de componentes",
        "labels": ["setup", "frontend", "sprint-0"],
        "milestone": "Sprint 0 - Setup",
        "body": """## Contexto
Configurar React com Vite e estrutura base

## Escopo
- Criar projeto React com Vite
- Configurar TailwindCSS
- Criar estrutura de componentes base
- Configurar roteamento (React Router)
- Criar servico de API (Axios)

## Criterios de Aceite
- [ ] React rodando localmente
- [ ] Componentes base criados
- [ ] Roteamento funcionando

## Branch
feature/react-setup"""
    },
    {
        "title": "setup: criar issues e milestones do projeto",
        "labels": ["setup", "chore", "sprint-0"],
        "milestone": "Sprint 0 - Setup",
        "body": """## Contexto
Criar todas as 30 issues e 6 milestones no GitHub

## Escopo
- Criar 6 milestones (Sprint 0-5)
- Criar 30 issues (5 por sprint)
- Adicionar labels apropriadas
- Configurar GitHub Project Board
- Adicionar issues ao board

## Criterios de Aceite
- [ ] Todas as 30 issues criadas
- [ ] Milestones configurados
- [ ] Board Kanban funcional

## Branch
chore/create-issues-milestones"""
    },
    # Sprint 1 - Backend (5 issues)
    {
        "title": "feat(backend): implementar modelos SQLAlchemy",
        "labels": ["backend", "database", "feat", "sprint-1"],
        "milestone": "Sprint 1 - Backend",
        "body": """## Contexto
Criar modelos SQLAlchemy para Batch, SensorReading e Prediction

## Escopo
- Criar modelo Batch com campos: id, upload_date, status, compliance_score, risk_prediction
- Criar modelo SensorReading com campos: temperature, ph, dissolved_oxygen, pressure, agitator_speed
- Criar modelo Prediction com campos: model_version, prediction_timestamp, confidence_score
- Implementar relacionamentos entre modelos
- Adicionar validações e constraints

## Critérios de Aceite
- [ ] Modelos criados e testados
- [ ] Relacionamentos funcionando
- [ ] Migrations executadas

## Branch
`feature/sqlalchemy-models`"""
    },
    {
        "title": "feat(backend): criar schemas Pydantic",
        "labels": ["backend", "api", "feat", "sprint-1"],
        "milestone": "Sprint 1 - Backend",
        "body": """## Contexto
Criar schemas Pydantic para validação de entrada/saída

## Escopo
- Criar schema BatchCreate para upload
- Criar schema BatchResponse para retorno
- Criar schema SensorReadingSchema
- Criar schema PredictionSchema
- Adicionar validações customizadas

## Critérios de Aceite
- [ ] Schemas validando corretamente
- [ ] Documentação Swagger atualizada
- [ ] Testes de validação passando

## Branch
`feature/pydantic-schemas`"""
    },
    {
        "title": "feat(api): criar endpoint POST /upload",
        "labels": ["backend", "api", "feat", "sprint-1"],
        "milestone": "Sprint 1 - Backend",
        "body": """## Contexto
Implementar endpoint para upload de arquivo CSV

## Escopo
- Criar rota POST /api/v1/upload
- Implementar validação de arquivo CSV
- Processar dados do CSV
- Persistir batch no banco
- Retornar ID do batch criado

## Critérios de Aceite
- [ ] Endpoint respondendo corretamente
- [ ] Arquivo CSV processado
- [ ] Batch persistido no banco

## Branch
`feature/upload-endpoint`"""
    },
    {
        "title": "feat(api): criar endpoints GET de consulta",
        "labels": ["backend", "api", "feat", "sprint-1"],
        "milestone": "Sprint 1 - Backend",
        "body": """## Contexto
Implementar endpoints para consultar batches e resultados

## Escopo
- Criar rota GET /api/v1/batches (listar todos)
- Criar rota GET /api/v1/batch/{id} (detalhes)
- Criar rota GET /api/v1/prediction/{batch_id}
- Criar rota GET /api/v1/compliance/{batch_id}
- Implementar filtros e paginação

## Critérios de Aceite
- [ ] Todos os endpoints respondendo
- [ ] Dados retornados corretamente
- [ ] Filtros funcionando

## Branch
`feature/query-endpoints`"""
    },
    {
        "title": "test(backend): implementar testes unitários",
        "labels": ["backend", "testing", "sprint-1"],
        "milestone": "Sprint 1 - Backend",
        "body": """## Contexto
Criar testes unitários com pytest

## Escopo
- Criar testes para modelos
- Criar testes para schemas
- Criar testes para endpoints
- Criar testes para services
- Atingir cobertura mínima de 70%

## Critérios de Aceite
- [ ] Testes passando
- [ ] Cobertura ≥ 70%
- [ ] Sem warnings

## Branch
`feature/backend-unit-tests`"""
    },
    # Sprint 2 - Frontend (5 issues)
    {
        "title": "feat(frontend): criar página Home com upload",
        "labels": ["frontend", "feat", "sprint-2"],
        "milestone": "Sprint 2 - Frontend",
        "body": """## Contexto
Implementar página inicial com interface de upload de CSV

## Escopo
- Criar componente UploadCard
- Implementar drag-and-drop
- Validar arquivo CSV
- Chamar API de upload
- Exibir feedback de sucesso/erro

## Critérios de Aceite
- [ ] Upload funcionando
- [ ] Validação de arquivo
- [ ] Feedback ao usuário

## Branch
`feature/home-upload-page`"""
    },
    {
        "title": "feat(frontend): criar Dashboard com KPIs",
        "labels": ["frontend", "feat", "sprint-2"],
        "milestone": "Sprint 2 - Frontend",
        "body": """## Contexto
Implementar dashboard com visualização de KPIs

## Escopo
- Criar componente Dashboard
- Exibir compliance score
- Exibir predição de risco
- Criar gráficos com Recharts
- Implementar atualização em tempo real

## Critérios de Aceite
- [ ] Dashboard renderizando
- [ ] Gráficos exibindo dados
- [ ] Dados atualizando

## Branch
`feature/dashboard-kpis`"""
    },
    {
        "title": "feat(frontend): criar tabela de batches",
        "labels": ["frontend", "feat", "sprint-2"],
        "milestone": "Sprint 2 - Frontend",
        "body": """## Contexto
Implementar tabela com histórico de batches

## Escopo
- Criar componente BatchTable
- Listar todos os batches
- Implementar filtros (data, status, score)
- Implementar paginação
- Adicionar link para detalhes

## Critérios de Aceite
- [ ] Tabela exibindo batches
- [ ] Filtros funcionando
- [ ] Paginação implementada

## Branch
`feature/batch-table`"""
    },
    {
        "title": "feat(frontend): integração com API backend",
        "labels": ["frontend", "api", "feat", "sprint-2"],
        "milestone": "Sprint 2 - Frontend",
        "body": """## Contexto
Integrar frontend com endpoints da API

## Escopo
- Criar serviço de API (Axios)
- Implementar chamadas para todos os endpoints
- Adicionar tratamento de erros
- Implementar loading states
- Adicionar cache de dados

## Critérios de Aceite
- [ ] Todas as chamadas funcionando
- [ ] Erros tratados
- [ ] Loading states visíveis

## Branch
`feature/api-integration`"""
    },
    {
        "title": "test(frontend): implementar testes E2E",
        "labels": ["frontend", "testing", "sprint-2"],
        "milestone": "Sprint 2 - Frontend",
        "body": """## Contexto
Criar testes E2E com Cypress

## Escopo
- Criar testes de upload
- Criar testes de dashboard
- Criar testes de tabela
- Criar testes de filtros
- Atingir cobertura mínima de 70%

## Critérios de Aceite
- [ ] Testes passando
- [ ] Cobertura ≥ 70%
- [ ] Sem warnings

## Branch
`feature/frontend-e2e-tests`"""
    },
    # Sprint 3 - ML (5 issues)
    {
        "title": "feat(ml): implementar Compliance Score Engine",
        "labels": ["backend", "business-logic", "feat", "sprint-3"],
        "milestone": "Sprint 3 - ML",
        "body": """## Contexto
Criar engine para cálculo de compliance score

## Escopo
- Implementar regras de validação por sensor
- Calcular score 0-100
- Classificar em ACCEPTABLE/WARNING/CRITICAL
- Adicionar rastreabilidade de cálculos
- Criar testes de validação

## Critérios de Aceite
- [ ] Score calculado corretamente
- [ ] Classificação correta
- [ ] Rastreabilidade implementada

## Branch
`feature/compliance-score-engine`"""
    },
    {
        "title": "feat(ml): criar ML Pipeline com RandomForest",
        "labels": ["backend", "business-logic", "feat", "sprint-3"],
        "milestone": "Sprint 3 - ML",
        "body": """## Contexto
Implementar pipeline de ML com RandomForestClassifier

## Escopo
- Criar pipeline de preprocessamento
- Implementar RandomForestClassifier
- Configurar features (Temperature, pH, DO, Pressure, Agitator Speed)
- Implementar predição
- Adicionar confidence score

## Critérios de Aceite
- [ ] Pipeline funcionando
- [ ] Predições geradas
- [ ] Confidence score calculado

## Branch
`feature/ml-pipeline-randomforest`"""
    },
    {
        "title": "feat(ml): treinar modelo com dataset Kaggle",
        "labels": ["backend", "business-logic", "feat", "sprint-3"],
        "milestone": "Sprint 3 - ML",
        "body": """## Contexto
Treinar modelo com dataset Kaggle

## Escopo
- Carregar dataset Kaggle
- Preparar dados (train/test split)
- Treinar RandomForestClassifier
- Validar acurácia (≥ 80%)
- Salvar modelo treinado

## Critérios de Aceite
- [ ] Modelo treinado
- [ ] Acurácia ≥ 80%
- [ ] Modelo persistido

## Branch
`feature/model-training`"""
    },
    {
        "title": "feat(frontend): criar página ML Analytics",
        "labels": ["frontend", "feat", "sprint-3"],
        "milestone": "Sprint 3 - ML",
        "body": """## Contexto
Criar página com análises de ML

## Escopo
- Criar componente MLAnalytics
- Exibir predição de risco
- Exibir confidence score
- Criar gráficos de distribuição
- Adicionar histórico de predições

## Critérios de Aceite
- [ ] Página renderizando
- [ ] Dados exibindo
- [ ] Gráficos funcionando

## Branch
`feature/ml-analytics-page`"""
    },
    {
        "title": "test(ml): implementar testes de ML",
        "labels": ["backend", "testing", "sprint-3"],
        "milestone": "Sprint 3 - ML",
        "body": """## Contexto
Criar testes para compliance score e ML

## Escopo
- Testes de compliance score
- Testes de predição
- Testes de confidence score
- Testes de edge cases
- Atingir cobertura mínima de 70%

## Critérios de Aceite
- [ ] Testes passando
- [ ] Cobertura ≥ 70%
- [ ] Sem warnings

## Branch
`feature/ml-tests`"""
    },
    # Sprint 4 - Testes (5 issues)
    {
        "title": "test(backend): testes unitários com pytest",
        "labels": ["backend", "testing", "sprint-4"],
        "milestone": "Sprint 4 - Testes",
        "body": """## Contexto
Expandir testes unitários backend para 70% cobertura

## Escopo
- Adicionar testes para todos os services
- Adicionar testes para processors
- Adicionar testes para validators
- Gerar relatório de cobertura
- Atingir 70% de cobertura

## Critérios de Aceite
- [ ] Cobertura ≥ 70%
- [ ] Testes passando
- [ ] Relatório gerado

## Branch
`feature/backend-pytest-coverage`"""
    },
    {
        "title": "test(frontend): testes unitários com Vitest",
        "labels": ["frontend", "testing", "sprint-4"],
        "milestone": "Sprint 4 - Testes",
        "body": """## Contexto
Expandir testes unitários frontend para 70% cobertura

## Escopo
- Adicionar testes para componentes
- Adicionar testes para hooks
- Adicionar testes para services
- Gerar relatório de cobertura
- Atingir 70% de cobertura

## Critérios de Aceite
- [ ] Cobertura ≥ 70%
- [ ] Testes passando
- [ ] Relatório gerado

## Branch
`feature/frontend-vitest-coverage`"""
    },
    {
        "title": "test(api): testes de integração com Postman",
        "labels": ["backend", "api", "testing", "sprint-4"],
        "milestone": "Sprint 4 - Testes",
        "body": """## Contexto
Criar testes de integração com Postman/Newman

## Escopo
- Criar collection Postman
- Adicionar testes para todos os endpoints
- Configurar environment variables
- Executar testes com Newman
- Gerar relatórios

## Critérios de Aceite
- [ ] Testes passando
- [ ] Todos os endpoints testados
- [ ] Relatórios gerados

## Branch
`feature/postman-integration-tests`"""
    },
    {
        "title": "test(e2e): testes E2E com Cypress",
        "labels": ["frontend", "testing", "sprint-4"],
        "milestone": "Sprint 4 - Testes",
        "body": """## Contexto
Expandir testes E2E com Cypress

## Escopo
- Criar testes de fluxo completo
- Adicionar testes de responsividade
- Adicionar testes de performance
- Gerar relatórios
- Atingir cobertura mínima

## Critérios de Aceite
- [ ] Testes passando
- [ ] Fluxos completos testados
- [ ] Relatórios gerados

## Branch
`feature/cypress-e2e-tests`"""
    },
    {
        "title": "test(coverage): validação de cobertura e relatórios",
        "labels": ["testing", "sprint-4"],
        "milestone": "Sprint 4 - Testes",
        "body": """## Contexto
Validar cobertura total e gerar relatórios

## Escopo
- Consolidar cobertura backend + frontend
- Gerar relatório consolidado
- Validar cobertura ≥ 70%
- Criar dashboard de cobertura
- Documentar resultados

## Critérios de Aceite
- [ ] Cobertura total ≥ 70%
- [ ] Relatórios gerados
- [ ] Dashboard acessível

## Branch
`feature/coverage-validation`"""
    },
    # Sprint 5 - Documentação (5 issues)
    {
        "title": "docs: documentação de API com Swagger",
        "labels": ["documentation", "backend", "sprint-5"],
        "milestone": "Sprint 5 - Documentação",
        "body": """## Contexto
Criar documentação completa da API com Swagger

## Escopo
- Documentar todos os endpoints
- Adicionar exemplos de requisição/resposta
- Documentar schemas
- Adicionar autenticação (se aplicável)
- Gerar OpenAPI spec

## Critérios de Aceite
- [ ] Swagger acessível em /docs
- [ ] Todos os endpoints documentados
- [ ] Exemplos funcionando

## Branch
`feature/swagger-documentation`"""
    },
    {
        "title": "docs: guias de desenvolvimento",
        "labels": ["documentation", "sprint-5"],
        "milestone": "Sprint 5 - Documentação",
        "body": """## Contexto
Criar guias de desenvolvimento

## Escopo
- Criar guia de setup local
- Criar guia de arquitetura
- Criar guia de contribuição
- Criar guia de deployment
- Adicionar troubleshooting

## Critérios de Aceite
- [ ] Guias completos
- [ ] Exemplos funcionando
- [ ] Fácil de seguir

## Branch
`feature/dev-guides`"""
    },
    {
        "title": "feat(validation): scripts de validação de dados",
        "labels": ["backend", "validation", "feat", "sprint-5"],
        "milestone": "Sprint 5 - Documentação",
        "body": """## Contexto
Criar scripts para validação de qualidade de dados

## Escopo
- Criar validate_data.py
- Validar ranges de sensores
- Detectar outliers
- Gerar relatórios
- Adicionar logging

## Critérios de Aceite
- [ ] Script funcionando
- [ ] Validações corretas
- [ ] Relatórios gerados

## Branch
`feature/data-validation-scripts`"""
    },
    {
        "title": "feat(validation): scripts de validação de compliance",
        "labels": ["backend", "validation", "feat", "sprint-5"],
        "milestone": "Sprint 5 - Documentação",
        "body": """## Contexto
Criar scripts para validação de compliance score

## Escopo
- Criar validate_compliance.py
- Validar cálculos de score
- Verificar classificações
- Gerar relatórios
- Adicionar rastreabilidade

## Critérios de Aceite
- [ ] Script funcionando
- [ ] Validações corretas
- [ ] Relatórios gerados

## Branch
`feature/compliance-validation-scripts`"""
    },
    {
        "title": "chore: deploy em produção e entrega final",
        "labels": ["chore", "sprint-5"],
        "milestone": "Sprint 5 - Documentação",
        "body": """## Contexto
Deploy final em produção e entrega do projeto

## Escopo
- Preparar ambiente de produção
- Executar migrations
- Deploy da aplicação
- Testes de smoke
- Documentar processo de deploy

## Critérios de Aceite
- [ ] Aplicação em produção
- [ ] Testes passando
- [ ] Documentação completa

## Branch
`release/v1.0.0`"""
    },
]

def create_label(label_data):
    """Cria uma label no GitHub"""
    cmd = [
        "gh", "label", "create",
        label_data["name"],
        "--repo", REPO,
        "--color", label_data["color"],
        "--description", label_data["description"],
        "--force"
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {"success": True}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e)}

def create_milestone(milestone_data):
    """Cria um milestone no GitHub"""
    cmd = [
        "gh", "milestone", "create",
        "--repo", REPO,
        "--title", milestone_data["title"],
        "--description", milestone_data["description"]
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {"success": True}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e)}

def create_issue(title, labels, body, milestone):
    """Cria uma issue no GitHub"""
    cmd = ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", body]
    for label in labels:
        cmd.extend(["--label", label])
    cmd.extend(["--milestone", milestone])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {"success": True, "url": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e)}

def main():
    print("="*80)
    print("� BIOTECPREDICT: Criando labels, milestones e 30 issues")
    print("="*80)
    print()
    
    # Criar labels
    print("🏷️  Criando 19 labels...")
    print()
    for label in LABELS:
        result = create_label(label)
        if result["success"]:
            print(f"  ✅ {label['name']}")
        else:
            print(f"  ⚠️  {label['name']} (pode já existir)")
    print()
    
    # Criar milestones
    print("📅 Criando 6 milestones...")
    print()
    for milestone in MILESTONES:
        result = create_milestone(milestone)
        if result["success"]:
            print(f"  ✅ {milestone['title']}")
        else:
            print(f"  ⚠️  {milestone['title']} (pode já existir)")
    print()
    
    # Criar issues
    print("📝 Criando 30 issues...")
    print()
    
    success_count = 0
    for idx, issue in enumerate(ISSUES, 1):
        print(f"[{idx}/30] {issue['title']}")
        result = create_issue(issue['title'], issue['labels'], issue['body'], issue['milestone'])
        if result["success"]:
            print(f"  ✅ Criada")
            success_count += 1
        else:
            print(f"  ❌ Erro: {result['error']}")
    
    print()
    print("="*80)
    print(f"✅ {success_count}/30 issues criadas com sucesso")
    print("="*80)
    print()
    
    if success_count == len(ISSUES):
        print("🎉 Todas as issues foram criadas com sucesso!")
        print()
        print("Próximos passos:")
        print("1. Verificar issues no GitHub")
        print("2. Configurar GitHub Project Board")
        print("3. Iniciar Sprint 0")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
