#!/usr/bin/env python3
"""
Script para adicionar automaticamente todas as 30 issues ao GitHub Project Board
Repositório: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict
Projeto: https://github.com/users/micheleoliveiracod/projects/7

Funcionalidades:
- Busca todas as issues do repositório
- Adiciona cada issue ao projeto automaticamente
- Move issues para a coluna "Todo" (padrão)
- Exibe progresso e relatório final
- Trata erros graciosamente
"""

import subprocess
import json
import sys
from typing import List, Dict, Optional

# Configurações
REPO = "micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict"
PROJECT_ID = "7"  # ID do projeto: https://github.com/users/micheleoliveiracod/projects/7
PROJECT_URL = "https://github.com/users/micheleoliveiracod/projects/7"

# Mapeamento de sprints para colunas do projeto
SPRINT_TO_COLUMN = {
    "Sprint 0 - Setup": "Todo",
    "Sprint 1 - Backend": "Todo",
    "Sprint 2 - Frontend": "Todo",
    "Sprint 3 - ML": "Todo",
    "Sprint 4 - Testes": "Todo",
    "Sprint 5 - Documentação": "Todo",
}

class GitHubProjectManager:
    """Gerenciador de issues e projeto GitHub"""
    
    def __init__(self, repo: str, project_id: str):
        self.repo = repo
        self.project_id = project_id
        self.issues = []
        self.added_count = 0
        self.failed_count = 0
        self.already_added_count = 0
    
    def get_all_issues(self) -> List[Dict]:
        """Busca todas as issues do repositório"""
        print("🔍 Buscando todas as issues do repositório...")
        print()
        
        cmd = [
            "gh", "issue", "list",
            "--repo", self.repo,
            "--state", "all",
            "--limit", "100",
            "--json", "number,title,milestone"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.issues = json.loads(result.stdout)
            print(f"✅ {len(self.issues)} issues encontradas")
            print()
            return self.issues
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao buscar issues: {e}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao parsear JSON: {e}")
            sys.exit(1)
    
    def add_issue_to_project(self, issue_number: int, issue_title: str) -> bool:
        """Adiciona uma issue ao projeto"""
        cmd = [
            "gh", "project", "item-add",
            self.project_id,
            "--owner", "micheleoliveiracod",
            "--url", f"https://github.com/{self.repo}/issues/{issue_number}"
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            # Verifica se é erro de "já adicionada"
            if "already added" in str(e.stderr).lower() or "already exists" in str(e.stderr).lower():
                return None  # Já estava adicionada
            print(f"  ❌ Erro ao adicionar: {e.stderr}")
            return False
    
    def set_issue_status(self, issue_number: int, status: str = "Todo") -> bool:
        """Define o status da issue no projeto (coluna)"""
        cmd = [
            "gh", "project", "item-edit",
            self.project_id,
            "--owner", "micheleoliveiracod",
            "--id", str(issue_number),
            "--field", "Status",
            "--value", status
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError:
            # Falha silenciosa - pode ser que o campo não exista
            return False
    
    def add_all_issues_to_project(self):
        """Adiciona todas as issues ao projeto"""
        print("="*80)
        print("📋 ADICIONANDO ISSUES AO PROJETO")
        print("="*80)
        print()
        
        if not self.issues:
            print("❌ Nenhuma issue encontrada. Execute get_all_issues() primeiro.")
            return
        
        print(f"Adicionando {len(self.issues)} issues ao projeto...")
        print()
        
        for idx, issue in enumerate(self.issues, 1):
            issue_number = issue.get("number")
            issue_title = issue.get("title", "Sem título")
            milestone = issue.get("milestone", {})
            milestone_title = milestone.get("title") if milestone else "Sem milestone"
            
            # Truncar título para exibição
            display_title = issue_title[:60] + "..." if len(issue_title) > 60 else issue_title
            
            print(f"[{idx}/{len(self.issues)}] #{issue_number} - {display_title}")
            print(f"  Milestone: {milestone_title}")
            
            # Adicionar issue ao projeto
            result = self.add_issue_to_project(issue_number, issue_title)
            
            if result is True:
                print(f"  ✅ Adicionada ao projeto")
                self.added_count += 1
            elif result is None:
                print(f"  ℹ️  Já estava no projeto")
                self.already_added_count += 1
            else:
                print(f"  ❌ Falha ao adicionar")
                self.failed_count += 1
            
            print()
        
        self.print_summary()
    
    def print_summary(self):
        """Exibe resumo final"""
        print("="*80)
        print("📊 RESUMO FINAL")
        print("="*80)
        print()
        print(f"✅ Issues adicionadas: {self.added_count}")
        print(f"ℹ️  Issues já no projeto: {self.already_added_count}")
        print(f"❌ Falhas: {self.failed_count}")
        print(f"📈 Total processado: {len(self.issues)}")
        print()
        
        if self.added_count == len(self.issues):
            print("🎉 SUCESSO! Todas as issues foram adicionadas ao projeto!")
        elif self.added_count + self.already_added_count == len(self.issues):
            print("✅ SUCESSO! Todas as issues estão no projeto!")
        else:
            print(f"⚠️  {self.failed_count} issues falharam. Verifique os logs acima.")
        
        print()
        print("Próximos passos:")
        print(f"1. Acesse o projeto: {PROJECT_URL}")
        print("2. Verifique se todas as issues estão visíveis")
        print("3. Configure as colunas do projeto (se necessário)")
        print("4. Inicie o Sprint 0")
        print()

def main():
    """Função principal"""
    print()
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  BIOTECPREDICT: Adicionar Issues ao GitHub Project Board".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    print()
    
    # Verificar se gh CLI está instalado
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ERRO: GitHub CLI (gh) não está instalado ou não está no PATH")
        print()
        print("Para instalar:")
        print("  Windows: choco install gh")
        print("  Mac: brew install gh")
        print("  Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md")
        print()
        sys.exit(1)
    
    # Verificar autenticação
    try:
        subprocess.run(["gh", "auth", "status"], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("❌ ERRO: Não autenticado no GitHub")
        print()
        print("Para autenticar:")
        print("  gh auth login")
        print()
        sys.exit(1)
    
    # Criar gerenciador e executar
    manager = GitHubProjectManager(REPO, PROJECT_ID)
    
    # Buscar todas as issues
    manager.get_all_issues()
    
    # Adicionar todas ao projeto
    manager.add_all_issues_to_project()

if __name__ == "__main__":
    main()
