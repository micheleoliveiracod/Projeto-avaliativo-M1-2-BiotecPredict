#!/usr/bin/env python3
"""
Script para configurar automação com os números reais das issues
Atualiza milestones, adiciona ao projeto e cria branches
"""

import subprocess
import sys
from typing import List, Tuple

REPO = "micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict"
PROJECT_ID = "7"

# Mapeamento REAL de Issues (números reais do GitHub)
ISSUE_MAPPING = {
    202: {"branch": "feature/sqlalchemy-models", "milestone": "Sprint 1 - Backend"},
    203: {"branch": "feature/pydantic-schemas", "milestone": "Sprint 1 - Backend"},
    204: {"branch": "feature/upload-endpoint", "milestone": "Sprint 1 - Backend"},
    205: {"branch": "feature/query-endpoints", "milestone": "Sprint 1 - Backend"},
    206: {"branch": "feature/backend-unit-tests", "milestone": "Sprint 1 - Backend"},
    207: {"branch": "feature/home-upload-page", "milestone": "Sprint 2 - Frontend"},
    208: {"branch": "feature/dashboard-kpis", "milestone": "Sprint 2 - Frontend"},
    209: {"branch": "feature/batch-table", "milestone": "Sprint 2 - Frontend"},
    210: {"branch": "feature/api-integration", "milestone": "Sprint 2 - Frontend"},
    211: {"branch": "feature/frontend-e2e-tests", "milestone": "Sprint 2 - Frontend"},
    212: {"branch": "feature/compliance-score-engine", "milestone": "Sprint 3 - ML"},
    213: {"branch": "feature/ml-pipeline-randomforest", "milestone": "Sprint 3 - ML"},
    214: {"branch": "feature/model-training", "milestone": "Sprint 3 - ML"},
    215: {"branch": "feature/ml-analytics-page", "milestone": "Sprint 3 - ML"},
    216: {"branch": "feature/ml-tests", "milestone": "Sprint 3 - ML"},
    217: {"branch": "feature/backend-pytest-coverage", "milestone": "Sprint 4 - Testes"},
    218: {"branch": "feature/frontend-vitest-coverage", "milestone": "Sprint 4 - Testes"},
    219: {"branch": "feature/postman-integration-tests", "milestone": "Sprint 4 - Testes"},
    220: {"branch": "feature/cypress-e2e-tests", "milestone": "Sprint 4 - Testes"},
    221: {"branch": "feature/coverage-validation", "milestone": "Sprint 4 - Testes"},
    222: {"branch": "feature/swagger-documentation", "milestone": "Sprint 5 - Documentação"},
    223: {"branch": "feature/dev-guides", "milestone": "Sprint 5 - Documentação"},
    224: {"branch": "feature/data-validation-scripts", "milestone": "Sprint 5 - Documentação"},
    225: {"branch": "feature/compliance-validation-scripts", "milestone": "Sprint 5 - Documentação"},
    226: {"branch": "release/v1.0.0", "milestone": "Sprint 5 - Documentação"},
    227: {"branch": "chore/create-scripts-automation", "milestone": "Sprint 0 - Setup"},
    228: {"branch": "chore/create-templates", "milestone": "Sprint 0 - Setup"},
    229: {"branch": "chore/configure-workflows", "milestone": "Sprint 0 - Setup"},
    230: {"branch": "chore/create-steering-docs", "milestone": "Sprint 0 - Setup"},
    231: {"branch": "chore/create-directory-structure", "milestone": "Sprint 0 - Setup"},
    234: {"branch": "chore/entrega-final", "milestone": "Entrega Final"},
    235: {"branch": "feature/data-quality-validation", "milestone": "Fase 7 - Validação de Dados"},
    236: {"branch": "feature/prompt-logging-system", "milestone": "Fase 8 - Prompt Logging"},
    237: {"branch": "feature/ai-powered-cicd", "milestone": "Fase 9 - CI/CD com IA"},
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
        print(f"  ⚠️  Issue #{issue_number}: {output[:80]}")
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
        if "already" in output.lower():
            print(f"  ℹ️  Issue #{issue_number}: já estava no projeto")
            return True
        print(f"  ⚠️  Issue #{issue_number}: {output[:80]}")
        return False

def main():
    """Executa configuração automática"""
    print_header("BIOTECPREDICT: Configurando Automação de Issues")
    
    print(f"Configurando {len(ISSUE_MAPPING)} issues...")
    print()
    
    success_count = 0
    error_count = 0
    
    for issue_number, mapping in sorted(ISSUE_MAPPING.items()):
        milestone = mapping["milestone"]
        
        print(f"🔧 Configurando Issue #{issue_number}...")
        
        # Atualizar milestone
        if update_issue_milestone(issue_number, milestone):
            success_count += 1
        else:
            error_count += 1
        
        # Adicionar ao projeto
        add_issue_to_project(issue_number)
    
    # Resumo final
    print_header("Configuração Completa!")
    
    print(f"✅ Issues configuradas com sucesso: {success_count}/{len(ISSUE_MAPPING)}")
    if error_count > 0:
        print(f"❌ Erros: {error_count}")
    print()
    
    print("📊 Resumo da Configuração:")
    print(f"  • Total de issues: {len(ISSUE_MAPPING)}")
    print(f"  • Issues com milestone: {success_count}")
    print(f"  • Issues adicionadas ao projeto: {success_count}")
    print()
    
    print("✅ Automação configurada com sucesso!")
    print()
    
    print("🌐 Acessar projeto:")
    print("  https://github.com/users/micheleoliveiracod/projects/7")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print()
        print("⚠️  Operação cancelada pelo usuário")
        print()
        sys.exit(0)
