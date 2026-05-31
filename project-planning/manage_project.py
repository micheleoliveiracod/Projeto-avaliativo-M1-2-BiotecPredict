#!/usr/bin/env python3
"""
Script interativo para gerenciar o GitHub Project Board do BiotecPredict
Oferece menu com opções para:
- Criar labels, milestones e issues
- Adicionar issues ao projeto
- Sincronizar status
- Gerar relatórios
"""

import subprocess
import sys
import os

REPO = "micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict"
PROJECT_ID = "7"
PROJECT_URL = "https://github.com/users/micheleoliveiracod/projects/7"

def print_header(title: str):
    """Exibe cabeçalho formatado"""
    print()
    print("╔" + "="*78 + "╗")
    print("║" + title.center(78) + "║")
    print("╚" + "="*78 + "╝")
    print()

def print_menu():
    """Exibe menu principal"""
    print_header("BIOTECPREDICT: Gerenciador de Projeto")
    print("Escolha uma opção:")
    print()
    print("  1️⃣  Criar labels, milestones e 30 issues")
    print("  2️⃣  Adicionar todas as issues ao projeto")
    print("  3️⃣  Criar apenas Sprint 0 (5 issues)")
    print("  4️⃣  Listar todas as issues")
    print("  5️⃣  Abrir projeto no navegador")
    print("  6️⃣  Verificar status do projeto")
    print("  0️⃣  Sair")
    print()

def run_script(script_name: str):
    """Executa um script Python"""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    if not os.path.exists(script_path):
        print(f"❌ Erro: Script {script_name} não encontrado")
        return False
    
    try:
        subprocess.run([sys.executable, script_path], check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao executar {script_name}")
        return False

def create_all_issues():
    """Opção 1: Criar labels, milestones e 30 issues"""
    print_header("Criando Labels, Milestones e 30 Issues")
    print("Isso vai criar:")
    print("  • 19 labels")
    print("  • 6 milestones (Sprint 0-5)")
    print("  • 30 issues (5 por sprint)")
    print()
    
    confirm = input("Deseja continuar? (s/n): ").lower()
    if confirm != 's':
        print("❌ Operação cancelada")
        return
    
    print()
    run_script("create_all_issues.py")

def add_issues_to_project():
    """Opção 2: Adicionar todas as issues ao projeto"""
    print_header("Adicionando Issues ao Projeto")
    print("Isso vai:")
    print("  • Buscar todas as issues do repositório")
    print("  • Adicionar cada uma ao projeto")
    print("  • Exibir relatório final")
    print()
    
    confirm = input("Deseja continuar? (s/n): ").lower()
    if confirm != 's':
        print("❌ Operação cancelada")
        return
    
    print()
    run_script("add_issues_to_project.py")

def create_sprint0():
    """Opção 3: Criar apenas Sprint 0"""
    print_header("Criando 5 Issues do Sprint 0")
    print("Isso vai criar apenas as issues do Sprint 0:")
    print("  • setup: estruturar repositório")
    print("  • setup: configurar banco de dados")
    print("  • setup: configurar FastAPI")
    print("  • setup: configurar React")
    print("  • setup: criar issues e milestones")
    print()
    
    confirm = input("Deseja continuar? (s/n): ").lower()
    if confirm != 's':
        print("❌ Operação cancelada")
        return
    
    print()
    run_script("create_sprint0_issues.py")

def list_issues():
    """Opção 4: Listar todas as issues"""
    print_header("Listando Todas as Issues")
    
    cmd = [
        "gh", "issue", "list",
        "--repo", REPO,
        "--state", "all",
        "--limit", "100"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro: {e}")

def open_project():
    """Opção 5: Abrir projeto no navegador"""
    print_header("Abrindo Projeto no Navegador")
    print(f"URL: {PROJECT_URL}")
    print()
    
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

def check_project_status():
    """Opção 6: Verificar status do projeto"""
    print_header("Status do Projeto")
    
    # Contar issues
    cmd = [
        "gh", "issue", "list",
        "--repo", REPO,
        "--state", "all",
        "--limit", "100",
        "--json", "number"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        import json
        issues = json.loads(result.stdout)
        
        print(f"📊 Estatísticas do Projeto:")
        print()
        print(f"  Total de issues: {len(issues)}")
        print(f"  Projeto: {PROJECT_URL}")
        print()
        
        # Contar por milestone
        cmd_milestone = [
            "gh", "issue", "list",
            "--repo", REPO,
            "--state", "all",
            "--limit", "100",
            "--json", "milestone"
        ]
        
        result_milestone = subprocess.run(cmd_milestone, capture_output=True, text=True, check=True)
        milestones_data = json.loads(result_milestone.stdout)
        
        milestone_counts = {}
        for issue in milestones_data:
            milestone = issue.get("milestone", {})
            if milestone:
                title = milestone.get("title", "Sem milestone")
                milestone_counts[title] = milestone_counts.get(title, 0) + 1
        
        if milestone_counts:
            print("  Issues por Sprint:")
            for sprint, count in sorted(milestone_counts.items()):
                print(f"    • {sprint}: {count} issues")
        else:
            print("  ⚠️  Nenhuma issue com milestone encontrada")
        
        print()
        print("✅ Status verificado com sucesso")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro: {e}")
    except Exception as e:
        print(f"❌ Erro ao processar dados: {e}")

def main():
    """Loop principal do menu"""
    while True:
        print_menu()
        
        choice = input("Opção: ").strip()
        
        if choice == "1":
            create_all_issues()
        elif choice == "2":
            add_issues_to_project()
        elif choice == "3":
            create_sprint0()
        elif choice == "4":
            list_issues()
        elif choice == "5":
            open_project()
        elif choice == "6":
            check_project_status()
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
