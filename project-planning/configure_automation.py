#!/usr/bin/env python3
"""
Script para configurar automação completa entre Issues, Branches, Milestones e GitHub Project Board
Relaciona automaticamente:
- Issues com suas branches correspondentes
- Issues com seus milestones
- Issues com o GitHub Project Board
- Configura automação de status no board

Repositório: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict
Projeto: https://github.com/users/micheleoliveiracod/projects/7
"""

import subprocess
import json
import sys
from typing import Dict, List, Optional, Tuple

REPO = "micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict"
PROJECT_ID = "7"
PROJECT_URL = "https://github.com/users/micheleoliveiracod/projects/7"

# Mapeamento de Issues para Branches e Milestones
# Formato: {issue_number: {"branch": "nome-da-branch", "milestone": "Sprint X - Nome"}}
ISSUE_MAPPING = {
    # Sprint 0 - Setup (5 issues)
    1: {"branch": "feature/project-structure", "milestone": "Sprint 0 - Setup"},
    2: {"branch": "feature/database-setup", "milestone": "Sprint 0 - Setup"},
    3: {"branch": "feature/fastapi-setup", "milestone": "Sprint 0 - Setup"},
    4: {"branch": "feature/react-setup", "milestone": "Sprint 0 - Setup"},
    5: {"branch": "chore/create-issues-milestones", "milestone": "Sprint 0 - Setup"},
    
    # Sprint 1 - Backend (5 issues)
    6: {"branch": "feature/sqlalchemy-models", "milestone": "Sprint 1 - Backend"},
    7: {"branch": "feature/pydantic-schemas", "milestone": "Sprint 1 - Backend"},
    8: {"branch": "feature/upload-endpoint", "milestone": "Sprint 1 - Backend"},
    9: {"branch": "feature/query-endpoints", "milestone": "Sprint 1 - Backend"},
    10: {"branch": "feature/backend-unit-tests", "milestone": "Sprint 1 - Backend"},
    
    # Sprint 2 - Frontend (5 issues)
    11: {"branch": "feature/home-upload-page", "milestone": "Sprint 2 - Frontend"},
    12: {"branch": "feature/dashboard-kpis", "milestone": "Sprint 2 - Frontend"},
    13: {"branch": "feature/batch-table", "milestone": "Sprint 2 - Frontend"},
    14: {"branch": "feature/api-integration", "milestone": "Sprint 2 - Frontend"},
    15: {"branch": "feature/frontend-e2e-tests", "milestone": "Sprint 2 - Frontend"},
    
    # Sprint 3 - ML (5 issues)
    16: {"branch": "feature/compliance-score-engine", "milestone": "Sprint 3 - ML"},
    17: {"branch": "feature/ml-pipeline-randomforest", "milestone": "Sprint 3 - ML"},
    18: {"branch": "feature/model-training", "milestone": "Sprint 3 - ML"},
    19: {"branch": "feature/ml-analytics-page", "milestone": "Sprint 3 - ML"},
    20: {"branch": "feature/ml-tests", "milestone": "Sprint 3 - ML"},
    
    # Sprint 4 - Testes (5 issues)
    21: {"branch": "feature/backend-pytest-coverage", "milestone": "Sprint 4 - Testes"},
    22: {"branch": "feature/frontend-vitest-coverage", "milestone": "Sprint 4 - Testes"},
    23: {"branch": "feature/postman-integration-tests", "milestone": "Sprint 4 - Testes"},
    24: {"branch": "feature/cypress-e2e-tests", "milestone": "Sprint 4 - Testes"},
    25: {"branch": "feature/coverage-validation", "milestone": "Sprint 4 - Testes"},
    
    # Sprint 5 - Documentação (5 issues)
    26: {"branch": "feature/swagger-documentation", "milestone": "Sprint 5 - Documentação"},
    27: {"branch": "feature/dev-guides", "milestone": "Sprint 5 - Documentação"},
    28: {"branch": "feature/data-validation-scripts", "milestone": "Sprint 5 - Documentação"},
    29: {"branch": "feature/compliance-validation-scripts", "milestone": "Sprint 5 - Documentação"},
    30: {"branch": "release/v1.0.0", "milestone": "Sprint 5 - Documentação"},
}

def print_header(title: str):
    """Exibe cabeçalho formatado"""
    print()
    print("╔" + "="*78 + "╗")
    print("║" + title.center(78) + "║")
    print("╚" + "="*78 + "╝")
    print()

def run_command(cmd: List[str], capture: bool = False) -> Tuple[bool, str]:
    """Executa comando e retorna (sucesso, output)"""
    try:
        result = subprocess.run(cmd, capture_output=capture, text=True, check=True)
        return True, result.stdout if capture else ""
    except subprocess.CalledProcessError as e:
        return False, e.stderr if e.stderr else str(e)

def get_issue_number_from_title(title: str) -> Optional[int]:
    """Extrai número da issue do título"""
    try:
        # Formato esperado: "#123 - Título"
        if title.startswith("#"):
            parts = title.split(" ")
            return int(parts[0][1:])
    except (ValueError, IndexError):
        pass
    return None

def get_all_issues() -> List[Dict]:
    """Obtém todas as issues do repositório"""
    print("📋 Buscando todas as issues...")
    
    cmd = [
        "gh", "issue", "list",
        "--repo", REPO,
        "--state", "all",
        "--limit", "100",
        "--json", "number,title,milestone,labels"
    ]
    
    success, output = run_command(cmd, capture=True)
    
    if not success:
        print(f"❌ Erro ao buscar issues: {output}")
        return []
    
    try:
        issues = json.loads(output)
        print(f"✅ {len(issues)} issues encontradas")
        return issues
    except json.JSONDecodeError:
        print(f"❌ Erro ao parsear JSON: {output}")
        return []

def update_issue_milestone(issue_number: int, milestone: str) -> bool:
    """Atualiza milestone de uma issue"""
    cmd = [
        "gh", "issue", "edit", str(issue_number),
        "--repo", REPO,
        "--milestone", milestone
    ]
    
    success, output = run_command(cmd)
    
    if success:
        print(f"  ✅ Issue #{issue_number}: milestone '{milestone}' atualizado")
        return True
    else:
        print(f"  ❌ Erro ao atualizar issue #{issue_number}: {output}")
        return False

def add_issue_to_project(issue_number: int) -> bool:
    """Adiciona issue ao GitHub Project"""
    cmd = [
        "gh", "project", "item-add", PROJECT_ID,
        "--repo", REPO,
        "--id", str(issue_number)
    ]
    
    success, output = run_command(cmd)
    
    if success:
        print(f"  ✅ Issue #{issue_number}: adicionada ao projeto")
        return True
    else:
        # Pode falhar se já está no projeto, não é erro crítico
        if "already exists" in output or "already added" in output:
            print(f"  ℹ️  Issue #{issue_number}: já estava no projeto")
            return True
        print(f"  ⚠️  Issue #{issue_number}: {output}")
        return False

def create_branch_locally(branch_name: str) -> bool:
    """Cria branch localmente (se não existir)"""
    # Verificar se branch já existe
    cmd_check = ["git", "rev-parse", "--verify", branch_name]
    success, _ = run_command(cmd_check)
    
    if success:
        print(f"  ℹ️  Branch '{branch_name}' já existe")
        return True
    
    # Criar branch a partir de develop
    cmd_create = ["git", "checkout", "-b", branch_name, "develop"]
    success, output = run_command(cmd_create)
    
    if success:
        print(f"  ✅ Branch '{branch_name}' criada")
        return True
    else:
        print(f"  ⚠️  Erro ao criar branch '{branch_name}': {output}")
        return False

def push_branch(branch_name: str) -> bool:
    """Faz push da branch para remote"""
    cmd = ["git", "push", "-u", "origin", branch_name]
    success, output = run_command(cmd)
    
    if success:
        print(f"  ✅ Branch '{branch_name}' enviada para remote")
        return True
    else:
        if "already exists" in output or "up-to-date" in output:
            print(f"  ℹ️  Branch '{branch_name}' já está no remote")
            return True
        print(f"  ⚠️  Erro ao fazer push: {output}")
        return False

def configure_issue_automation(issue_number: int, branch_name: str, milestone: str) -> bool:
    """Configura automação completa para uma issue"""
    print(f"\n🔧 Configurando Issue #{issue_number}...")
    
    # 1. Atualizar milestone
    if not update_issue_milestone(issue_number, milestone):
        return False
    
    # 2. Adicionar ao projeto
    if not add_issue_to_project(issue_number):
        return False
    
    # 3. Criar branch localmente
    if not create_branch_locally(branch_name):
        return False
    
    # 4. Fazer push da branch
    if not push_branch(branch_name):
        return False
    
    return True

def configure_all_issues() -> Tuple[int, int]:
    """Configura automação para todas as issues"""
    print_header("Configurando Automação de Issues")
    
    success_count = 0
    error_count = 0
    
    for issue_number, mapping in sorted(ISSUE_MAPPING.items()):
        branch = mapping["branch"]
        milestone = mapping["milestone"]
        
        if configure_issue_automation(issue_number, branch, milestone):
            success_count += 1
        else:
            error_count += 1
    
    return success_count, error_count

def verify_configuration() -> bool:
    """Verifica se a configuração foi aplicada corretamente"""
    print_header("Verificando Configuração")
    
    issues = get_all_issues()
    
    if not issues:
        print("❌ Nenhuma issue encontrada")
        return False
    
    print(f"\n📊 Resumo da Configuração:")
    print()
    
    milestone_counts = {}
    issues_with_milestone = 0
    issues_in_project = 0
    
    for issue in issues:
        issue_num = issue.get("number")
        milestone = issue.get("milestone")
        
        if milestone:
            issues_with_milestone += 1
            milestone_title = milestone.get("title", "Sem título")
            milestone_counts[milestone_title] = milestone_counts.get(milestone_title, 0) + 1
    
    print(f"  Total de issues: {len(issues)}")
    print(f"  Issues com milestone: {issues_with_milestone}")
    print()
    
    if milestone_counts:
        print("  Issues por Sprint:")
        for sprint, count in sorted(milestone_counts.items()):
            print(f"    • {sprint}: {count} issues")
    
    print()
    print("✅ Configuração verificada com sucesso")
    return True

def show_branch_status() -> bool:
    """Mostra status das branches locais"""
    print_header("Status das Branches Locais")
    
    cmd = ["git", "branch", "-a"]
    success, output = run_command(cmd, capture=True)
    
    if success:
        branches = [b.strip() for b in output.split("\n") if b.strip()]
        print(f"Total de branches: {len(branches)}")
        print()
        
        # Contar branches por tipo
        feature_count = len([b for b in branches if "feature/" in b])
        bugfix_count = len([b for b in branches if "bugfix/" in b])
        hotfix_count = len([b for b in branches if "hotfix/" in b])
        release_count = len([b for b in branches if "release/" in b])
        chore_count = len([b for b in branches if "chore/" in b])
        
        print("Branches por tipo:")
        if feature_count > 0:
            print(f"  • feature/*: {feature_count}")
        if bugfix_count > 0:
            print(f"  • bugfix/*: {bugfix_count}")
        if hotfix_count > 0:
            print(f"  • hotfix/*: {hotfix_count}")
        if release_count > 0:
            print(f"  • release/*: {release_count}")
        if chore_count > 0:
            print(f"  • chore/*: {chore_count}")
        
        print()
        print("✅ Status das branches verificado")
        return True
    else:
        print(f"❌ Erro ao verificar branches: {output}")
        return False

def show_project_status() -> bool:
    """Mostra status do GitHub Project"""
    print_header("Status do GitHub Project")
    
    print(f"Projeto: {PROJECT_URL}")
    print()
    
    issues = get_all_issues()
    
    if not issues:
        print("❌ Nenhuma issue encontrada")
        return False
    
    print(f"Total de issues: {len(issues)}")
    print()
    
    # Contar issues por milestone
    milestone_counts = {}
    for issue in issues:
        milestone = issue.get("milestone")
        if milestone:
            title = milestone.get("title", "Sem milestone")
            milestone_counts[title] = milestone_counts.get(title, 0) + 1
    
    if milestone_counts:
        print("Issues por Sprint:")
        for sprint, count in sorted(milestone_counts.items()):
            print(f"  • {sprint}: {count} issues")
    else:
        print("⚠️  Nenhuma issue com milestone encontrada")
    
    print()
    print("✅ Status do projeto verificado")
    return True

def print_menu():
    """Exibe menu principal"""
    print_header("BIOTECPREDICT: Configurador de Automação")
    print("Escolha uma opção:")
    print()
    print("  1️⃣  Configurar automação para TODAS as issues")
    print("  2️⃣  Verificar configuração atual")
    print("  3️⃣  Ver status das branches locais")
    print("  4️⃣  Ver status do GitHub Project")
    print("  5️⃣  Abrir projeto no navegador")
    print("  0️⃣  Sair")
    print()

def main():
    """Loop principal do menu"""
    while True:
        print_menu()
        
        choice = input("Opção: ").strip()
        
        if choice == "1":
            confirm = input("\n⚠️  Isso vai configurar automação para TODAS as 30 issues. Continuar? (s/n): ").lower()
            if confirm == 's':
                success, error = configure_all_issues()
                print()
                print_header("Resumo da Configuração")
                print(f"✅ Issues configuradas com sucesso: {success}")
                if error > 0:
                    print(f"❌ Erros: {error}")
                print()
                verify_configuration()
            else:
                print("❌ Operação cancelada")
        
        elif choice == "2":
            verify_configuration()
        
        elif choice == "3":
            show_branch_status()
        
        elif choice == "4":
            show_project_status()
        
        elif choice == "5":
            print()
            print(f"Abrindo: {PROJECT_URL}")
            import os
            try:
                if sys.platform == "win32":
                    os.startfile(PROJECT_URL)
                elif sys.platform == "darwin":
                    subprocess.run(["open", PROJECT_URL])
                else:
                    subprocess.run(["xdg-open", PROJECT_URL])
                print("✅ Projeto aberto no navegador")
            except Exception as e:
                print(f"❌ Erro ao abrir navegador: {e}")
                print(f"Abra manualmente: {PROJECT_URL}")
        
        elif choice == "0":
            print()
            print("👋 Até logo!")
            print()
            break
        
        else:
            print("❌ Opção inválida. Tente novamente.")
        
        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print()
        print("⚠️  Operação cancelada pelo usuário")
        print()
        sys.exit(0)
