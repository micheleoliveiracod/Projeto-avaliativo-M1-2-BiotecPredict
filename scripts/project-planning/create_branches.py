#!/usr/bin/env python3
"""
Script para criar branches automaticamente no GitHub seguindo GitFlow
Repositório: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict

Este script cria as 30 branches (5 por sprint) após a conclusão dos sprints,
seguindo as convenções do GitFlow e o escopo do projeto BiotecPredict.
"""

import subprocess
import sys
import os

REPO = "micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict"
REPO_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Definição das 30 branches (5 por sprint)
BRANCHES = {
    "Sprint 0 - Setup": [
        "feature/project-structure",
        "feature/database-setup",
        "feature/fastapi-setup",
        "feature/react-setup",
        "chore/create-issues-milestones",
    ],
    "Sprint 1 - Backend": [
        "feature/sqlalchemy-models",
        "feature/pydantic-schemas",
        "feature/upload-endpoint",
        "feature/query-endpoints",
        "feature/backend-unit-tests",
    ],
    "Sprint 2 - Frontend": [
        "feature/home-upload-page",
        "feature/dashboard-kpis",
        "feature/batch-table",
        "feature/api-integration",
        "feature/frontend-e2e-tests",
    ],
    "Sprint 3 - ML": [
        "feature/compliance-score-engine",
        "feature/ml-pipeline-randomforest",
        "feature/model-training",
        "feature/ml-analytics-page",
        "feature/ml-tests",
    ],
    "Sprint 4 - Testes": [
        "feature/backend-pytest-coverage",
        "feature/frontend-vitest-coverage",
        "feature/postman-integration-tests",
        "feature/cypress-e2e-tests",
        "feature/coverage-validation",
    ],
    "Sprint 5 - Documentação": [
        "feature/swagger-documentation",
        "feature/dev-guides",
        "feature/data-validation-scripts",
        "feature/compliance-validation-scripts",
        "release/v1.0.0",
    ],
}

def check_git_installed():
    """Verifica se Git está instalado"""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_repo_exists():
    """Verifica se o repositório local existe"""
    return os.path.isdir(os.path.join(REPO_PATH, ".git"))

def create_branch_local(branch_name):
    """Cria uma branch localmente"""
    try:
        # Verificar se branch já existe
        result = subprocess.run(
            ["git", "branch", "-a"],
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            check=True
        )
        
        if branch_name in result.stdout:
            return {"success": False, "error": "Branch já existe"}
        
        # Criar branch a partir de develop
        subprocess.run(
            ["git", "checkout", "develop"],
            cwd=REPO_PATH,
            capture_output=True,
            check=True
        )
        
        subprocess.run(
            ["git", "pull", "origin", "develop"],
            cwd=REPO_PATH,
            capture_output=True,
            check=True
        )
        
        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            cwd=REPO_PATH,
            capture_output=True,
            check=True
        )
        
        return {"success": True}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e)}

def push_branch_remote(branch_name):
    """Faz push da branch para o repositório remoto"""
    try:
        subprocess.run(
            ["git", "push", "-u", "origin", branch_name],
            cwd=REPO_PATH,
            capture_output=True,
            check=True
        )
        return {"success": True}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e)}

def create_branches_for_sprint(sprint_name, branches):
    """Cria todas as branches de um sprint"""
    print(f"\n📦 Criando branches do {sprint_name}...")
    print()
    
    results = []
    for branch in branches:
        print(f"  Criando branch: {branch}")
        
        # Criar branch localmente
        result_local = create_branch_local(branch)
        if not result_local["success"]:
            print(f"    ❌ Erro local: {result_local['error']}")
            results.append({"branch": branch, "success": False})
            continue
        
        # Fazer push para remote
        result_remote = push_branch_remote(branch)
        if not result_remote["success"]:
            print(f"    ❌ Erro ao fazer push: {result_remote['error']}")
            results.append({"branch": branch, "success": False})
            continue
        
        print(f"    ✅ Branch criada e enviada")
        results.append({"branch": branch, "success": True})
    
    return results

def cleanup_branches():
    """Volta para develop e limpa branches locais"""
    try:
        subprocess.run(
            ["git", "checkout", "develop"],
            cwd=REPO_PATH,
            capture_output=True,
            check=True
        )
        print("\n✅ Voltado para branch develop")
    except subprocess.CalledProcessError as e:
        print(f"\n⚠️  Erro ao voltar para develop: {e}")

def main():
    print("="*80)
    print("🚀 BIOTECPREDICT: Criando 30 branches (5 por sprint)")
    print("="*80)
    print()
    
    # Verificações iniciais
    if not check_git_installed():
        print("❌ Git não está instalado!")
        sys.exit(1)
    
    if not check_repo_exists():
        print("❌ Repositório local não encontrado!")
        print(f"   Esperado em: {REPO_PATH}")
        sys.exit(1)
    
    print("✅ Git instalado")
    print(f"✅ Repositório encontrado em: {REPO_PATH}")
    print()
    
    # Criar branches por sprint
    all_results = []
    for sprint_name, branches in BRANCHES.items():
        results = create_branches_for_sprint(sprint_name, branches)
        all_results.extend(results)
    
    # Limpeza
    cleanup_branches()
    
    # Resumo
    print()
    print("="*80)
    success_count = sum(1 for r in all_results if r["success"])
    total_count = len(all_results)
    print(f"✅ {success_count}/{total_count} branches criadas com sucesso")
    print("="*80)
    print()
    
    if success_count == total_count:
        print("🎉 Todas as branches foram criadas e enviadas para o repositório remoto!")
        print()
        print("Próximos passos:")
        print("1. Verificar branches no GitHub")
        print("2. Configurar proteção de branches (se necessário)")
        print("3. Iniciar desenvolvimento nos sprints")
        print()
        print("Convenção de branches:")
        print("  - feature/<nome> : Novas funcionalidades")
        print("  - chore/<nome>   : Tarefas de manutenção")
        print("  - release/v<ver> : Preparação de release")
    else:
        print("⚠️  Algumas branches falharam ao ser criadas.")
        print("   Verifique os erros acima e tente novamente.")
        sys.exit(1)

if __name__ == "__main__":
    main()
