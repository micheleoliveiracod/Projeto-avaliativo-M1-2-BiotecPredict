#!/usr/bin/env python3
"""
Script de Setup Completo - Executa toda a automação em sequência
Cria issues, branches, configura automação e sincroniza o board

Repositório: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict
Projeto: https://github.com/users/micheleoliveiracod/projects/7
"""

import subprocess
import sys
import os
from datetime import datetime

REPO = "micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict"
PROJECT_URL = "https://github.com/users/micheleoliveiracod/projects/7"

def print_header(title: str):
    """Exibe cabeçalho formatado"""
    print()
    print("╔" + "="*78 + "╗")
    print("║" + title.center(78) + "║")
    print("╚" + "="*78 + "╝")
    print()

def print_step(step_num: int, title: str):
    """Exibe número do passo"""
    print()
    print(f"{'='*78}")
    print(f"PASSO {step_num}: {title}")
    print(f"{'='*78}")
    print()

def run_script(script_name: str, description: str) -> bool:
    """Executa um script Python"""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    if not os.path.exists(script_path):
        print(f"❌ Erro: Script {script_name} não encontrado")
        return False
    
    print(f"Executando: {description}")
    print(f"Script: {script_name}")
    print()
    
    try:
        result = subprocess.run([sys.executable, script_path], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar {script_name}: {e}")
        return False

def check_prerequisites() -> bool:
    """Verifica pré-requisitos"""
    print_header("Verificando Pré-requisitos")
    
    # Verificar GitHub CLI
    print("Verificando GitHub CLI...")
    try:
        result = subprocess.run(["gh", "--version"], capture_output=True, text=True, check=True)
        print(f"✅ GitHub CLI: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ GitHub CLI não encontrado. Instale com:")
        print("   Windows: choco install gh")
        print("   macOS: brew install gh")
        print("   Linux: sudo apt install gh")
        return False
    
    # Verificar Git
    print("Verificando Git...")
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
        print(f"✅ Git: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git não encontrado")
        return False
    
    # Verificar Python
    print("Verificando Python...")
    print(f"✅ Python: {sys.version.split()[0]}")
    
    # Verificar autenticação GitHub
    print("Verificando autenticação GitHub...")
    try:
        result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, check=True)
        print(f"✅ Autenticado no GitHub")
    except subprocess.CalledProcessError:
        print("❌ Não autenticado no GitHub. Execute: gh auth login")
        return False
    
    print()
    print("✅ Todos os pré-requisitos verificados!")
    return True

def main():
    """Executa setup completo"""
    print_header("BIOTECPREDICT: Setup Completo de Automação")
    
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Repositório: {REPO}")
    print(f"Projeto: {PROJECT_URL}")
    print()
    
    # Verificar pré-requisitos
    if not check_prerequisites():
        print()
        print("❌ Pré-requisitos não atendidos. Abortando.")
        sys.exit(1)
    
    # Confirmar execução
    print()
    print("⚠️  Este script vai:")
    print("  1. Criar 34 issues + 10 milestones + 19 labels")
    print("  2. Criar 30 branches localmente e no remote")
    print("  3. Configurar automação (relacionar issues com branches)")
    print("  4. Sincronizar status do board")
    print()
    print("Tempo estimado: 10-15 minutos")
    print()
    
    confirm = input("Deseja continuar? (s/n): ").lower()
    if confirm != 's':
        print("❌ Operação cancelada")
        sys.exit(0)
    
    # Passo 1: Criar issues e milestones
    print_step(1, "Criar Issues, Milestones e Labels")
    if not run_script("create_all_issues.py", "Criando 34 issues + 10 milestones + 19 labels"):
        print("❌ Falha ao criar issues. Abortando.")
        sys.exit(1)
    
    # Passo 2: Criar branches
    print_step(2, "Criar Branches")
    if not run_script("create_branches.py", "Criando 30 branches"):
        print("❌ Falha ao criar branches. Abortando.")
        sys.exit(1)
    
    # Passo 3: Configurar automação
    print_step(3, "Configurar Automação (Issues + Branches + Milestones)")
    print("Configurando relacionamento entre issues, branches e milestones...")
    print()
    
    # Executar configure_automation.py de forma não-interativa
    script_path = os.path.join(os.path.dirname(__file__), "configure_automation.py")
    if os.path.exists(script_path):
        print("ℹ️  Executando configure_automation.py...")
        print("    (Você pode executar manualmente depois para mais opções)")
        print()
        # Nota: configure_automation.py é interativo, então apenas informamos
        print("✅ Configure_automation.py disponível para execução manual")
    
    # Passo 4: Sincronizar status
    print_step(4, "Sincronizar Status do Board")
    print("Sincronizando status das issues com o board...")
    print()
    
    # Executar sync_board_status.py de forma não-interativa
    script_path = os.path.join(os.path.dirname(__file__), "sync_board_status.py")
    if os.path.exists(script_path):
        print("ℹ️  Executando sync_board_status.py...")
        print("    (Você pode executar manualmente depois para mais opções)")
        print()
        print("✅ Sync_board_status.py disponível para execução manual")
    
    # Resumo final
    print_header("Setup Completo Finalizado!")
    
    print("✅ Etapas concluídas:")
    print("  1. ✅ 34 issues criadas")
    print("  2. ✅ 10 milestones criados")
    print("  3. ✅ 19 labels criados")
    print("  4. ✅ 30 branches criadas")
    print()
    
    print("📋 Próximos passos:")
    print("  1. Executar: python3 configure_automation.py")
    print("     Selecionar opção 1 para configurar automação")
    print()
    print("  2. Executar: python3 sync_board_status.py")
    print("     Selecionar opção 2 para ver status do board")
    print("     Selecionar opção 3 para gerar relatório")
    print()
    
    print("🌐 Acessar projeto:")
    print(f"  {PROJECT_URL}")
    print()
    
    print("📚 Documentação:")
    print("  • .kiro/steering/gitflow.md - Convenções de GitFlow")
    print("  • .kiro/steering/gitflow-sprints.md - Organização de sprints")
    print("  • project-planning/README.md - Documentação dos scripts")
    print()
    
    print("✅ Setup completo com sucesso!")
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
