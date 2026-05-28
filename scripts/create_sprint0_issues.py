#!/usr/bin/env python3
"""
Script para criar APENAS as 5 issues do Sprint 0 que faltam
Verifica se a issue ja existe antes de criar (evita duplicatas)
"""

import subprocess
import sys

REPO = "micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict"

# 5 Issues do Sprint 0 que faltam
SPRINT0_ISSUES = [
    {
        "title": "setup: estruturar repositorio e diretorios base",
        "labels": ["setup", "backend", "frontend", "sprint-0"],
        "milestone": "Fase 0 - Setup Inicial",
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
        "milestone": "Fase 0 - Setup Inicial",
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
        "milestone": "Fase 0 - Setup Inicial",
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
        "milestone": "Fase 0 - Setup Inicial",
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
        "milestone": "Fase 0 - Setup Inicial",
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
]

def issue_exists(title):
    """Verifica se uma issue com este titulo ja existe"""
    cmd = [
        "gh", "issue", "list",
        "--repo", REPO,
        "--search", f'"{title}"',
        "--state", "all",
        "--limit", "100"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # Se encontrou algo, a issue existe
        return len(result.stdout.strip()) > 0
    except subprocess.CalledProcessError:
        return False

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
    print("BIOTECPREDICT: Criando 5 issues do Sprint 0 (sem duplicatas)")
    print("="*80)
    print()
    
    print("Verificando quais issues ja existem...")
    print()
    
    existing_count = 0
    new_count = 0
    
    for idx, issue in enumerate(SPRINT0_ISSUES, 1):
        title = issue['title']
        print(f"[{idx}/5] {title}")
        
        if issue_exists(title):
            print(f"  ⚠️  JA EXISTE - Pulando")
            existing_count += 1
        else:
            print(f"  Criando...")
            result = create_issue(title, issue['labels'], issue['body'], issue['milestone'])
            if result["success"]:
                print(f"  ✅ Criada com sucesso")
                new_count += 1
            else:
                print(f"  ❌ Erro: {result['error']}")
    
    print()
    print("="*80)
    print(f"Resultado: {new_count} novas issues criadas, {existing_count} ja existiam")
    print("="*80)
    print()
    
    if new_count > 0:
        print(f"✅ {new_count} issues do Sprint 0 foram criadas com sucesso!")
    
    if existing_count > 0:
        print(f"ℹ️  {existing_count} issues ja existiam (nao foram duplicadas)")
    
    print()
    print("Proximos passos:")
    print("1. Verificar todas as 30 issues no GitHub")
    print("2. Configurar GitHub Project Board")
    print("3. Iniciar Sprint 0")

if __name__ == "__main__":
    main()
