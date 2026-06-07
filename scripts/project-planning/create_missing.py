#!/usr/bin/env python3
"""
Script para criar automaticamente os 3 milestones + 4 issues + 3 labels + 4 branches faltantes no GitHub
Repositório: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict
Projeto: https://github.com/users/micheleoliveiracod/projects/7

Milestones a criar (3 total):
- Fase 7 - Validação de Dados
- Fase 8 - Prompt Logging
- Fase 9 - CI/CD com IA

Issues a criar (4 total):
- #31: Entrega Final (Milestone: Entrega Final - já existe)
- #32: Validação de Dados (Milestone: Fase 7 - Validação de Dados)
- #33: Prompt Logging (Milestone: Fase 8 - Prompt Logging)
- #34: CI/CD com IA (Milestone: Fase 9 - CI/CD com IA)

Funcionalidades:
- Cria 3 milestones faltantes (Fase 7, 8, 9)
- Cria 3 labels faltantes (entrega-final, logging, ci)
- Cria 4 issues com templates estruturados
- Cria 4 branches correspondentes
- Adiciona issues ao projeto board
- Exibe progresso e relatório final

IMPORTANTE: Verifica se milestones já existem antes de criar (evita duplicatas).
"""

import subprocess
import json
import sys
from typing import List, Dict, Optional

# Configurações
REPO = "micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict"
PROJECT_ID = "7"
PROJECT_URL = "https://github.com/users/micheleoliveiracod/projects/7"

# Definição dos 3 milestones faltantes
MISSING_MILESTONES = [
    {
        "title": "Fase 7 - Validação de Dados",
        "description": "Implementação de scripts de validação de qualidade de dados e rastreabilidade completa"
    },
    {
        "title": "Fase 8 - Prompt Logging",
        "description": "Implementação completa do sistema de logging de prompts com rastreabilidade de todas as interações com IA"
    },
    {
        "title": "Fase 9 - CI/CD com IA",
        "description": "Implementação de workflows CI/CD avançados com geração automática de testes e documentação via IA"
    }
]

# Definição das 4 issues faltantes
MISSING_ISSUES = [
    {
        "number": 31,
        "title": "chore: entrega final e apresentação do projeto",
        "milestone": "Entrega Final",
        "labels": ["chore", "entrega-final", "sprint-final"],
        "branch": "chore/entrega-final-apresentacao",
        "body": """## Descrição

Consolidar projeto, preparar apresentação e entregar para avaliação.

## Checklist de Atividades

- [ ] Revisar todos os 9 requisitos de entrega (M01-M09)
- [ ] Verificar README.md com todos os requisitos
- [ ] Validar vídeo de apresentação (máx 10 min)
- [ ] Confirmar GitHub Board com automação completa
- [ ] Validar todas as 30 issues + 4 milestones adicionais
- [ ] Testar deploy local com Docker Compose
- [ ] Gerar relatório final de cobertura de testes (≥ 70%)
- [ ] Documentar análise crítica de uso de IA
- [ ] Preparar apresentação executiva
- [ ] Fazer commit final e tag v1.0.0

## Critérios de Aceitação

- [ ] Todos os 9 requisitos de entrega atendidos
- [ ] Projeto 100% funcional
- [ ] Documentação completa
- [ ] Vídeo publicado no YouTube
- [ ] Pronto para avaliação

## Branch

`chore/entrega-final-apresentacao`
"""
    },
    {
        "number": 32,
        "title": "feat(validation): implementar validação completa de dados",
        "milestone": "Fase 7 - Validação de Dados",
        "labels": ["backend", "validation", "feat", "sprint-5"],
        "branch": "feature/data-quality-validation",
        "body": """## Descrição

Criar suite completa de validação de qualidade de dados e rastreabilidade.

## Checklist de Atividades

- [ ] Criar validate_data.py com validação de ranges
- [ ] Implementar detecção de outliers e anomalias
- [ ] Criar validate_compliance.py para validação de scores
- [ ] Implementar rastreabilidade de origem dos dados
- [ ] Gerar relatórios versionados em backend/reports/
- [ ] Adicionar logging completo de validações
- [ ] Criar testes para scripts de validação
- [ ] Documentar processo de validação

## Critérios de Aceitação

- [ ] Scripts de validação funcionando
- [ ] Relatórios gerados corretamente
- [ ] Rastreabilidade implementada
- [ ] Testes passando

## Branch

`feature/data-quality-validation`
"""
    },
    {
        "number": 33,
        "title": "feat(logging): implementar sistema de prompt logging",
        "milestone": "Fase 8 - Prompt Logging",
        "labels": ["backend", "logging", "feat", "sprint-0"],
        "branch": "feature/prompt-logging-system",
        "body": """## Descrição

Criar sistema automático de logging de prompts com rastreabilidade de todas as interações com IA.

## Checklist de Atividades

- [ ] Criar hook Kiro para captura de prompts (promptSubmit)
- [ ] Implementar script log_prompt.py
- [ ] Configurar armazenamento em .kiro/prompt-logs/
- [ ] Implementar filtro de prompts triviais
- [ ] Adicionar timestamp em horário de Brasília (UTC-3)
- [ ] Criar estrutura de metadados obrigatória
- [ ] Implementar versionamento de logs
- [ ] Criar documentação de convenções de logging
- [ ] Adicionar análise de prompts bem-sucedidos

## Critérios de Aceitação

- [ ] Sistema de logging funcionando
- [ ] Prompts capturados automaticamente
- [ ] Logs organizados por branch
- [ ] Documentação completa

## Branch

`feature/prompt-logging-system`
"""
    },
    {
        "number": 34,
        "title": "feat(ci-cd): implementar workflows CI/CD com IA",
        "milestone": "Fase 9 - CI/CD com IA",
        "labels": ["ci", "automation", "feat", "sprint-4"],
        "branch": "feature/ai-powered-cicd",
        "body": """## Descrição

Criar workflows GitHub Actions com geração automática de testes e documentação via IA.

## Checklist de Atividades

- [ ] Criar workflow ai-test-generation.yml
- [ ] Implementar geração automática de testes com IA
- [ ] Criar workflow docs-generation.yml
- [ ] Implementar geração automática de documentação
- [ ] Criar workflow metrics-dashboard.yml
- [ ] Implementar análise de métricas do projeto
- [ ] Criar workflow progress-report.yml
- [ ] Implementar relatórios semanais de progresso
- [ ] Criar workflow velocity-analysis.yml
- [ ] Implementar análise de velocidade do time
- [ ] Documentar workflows e triggers

## Critérios de Aceitação

- [ ] Todos os workflows funcionando
- [ ] Testes gerados automaticamente
- [ ] Documentação atualizada automaticamente
- [ ] Relatórios gerados semanalmente

## Branch

`feature/ai-powered-cicd`
"""
    }
]

# Definição dos 4 labels faltantes
MISSING_LABELS = [
    {
        "name": "entrega-final",
        "color": "8B008B",
        "description": "Requisitos de entrega final"
    },
    {
        "name": "logging",
        "color": "20C997",
        "description": "Sistema de logging e rastreamento"
    },
    {
        "name": "ci",
        "color": "17A2B8",
        "description": "CI/CD e automação"
    }
]

class GitHubIssueCreator:
    """Criador de issues, labels e branches no GitHub"""
    
    def __init__(self, repo: str, project_id: str):
        self.repo = repo
        self.project_id = project_id
        self.created_issues = []
        self.created_labels = []
        self.created_branches = []
        self.created_milestones = []
        self.failed_issues = []
        self.failed_labels = []
        self.failed_branches = []
        self.failed_milestones = []
    
    def create_milestone(self, milestone: Dict) -> bool:
        """Cria um milestone no repositório"""
        cmd = [
            "gh", "api",
            f"repos/{self.repo}/milestones",
            "-f", f"title={milestone['title']}",
            "-f", f"description={milestone['description']}"
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            error_msg = str(e.stderr).lower()
            if "already exists" in error_msg or "validation failed" in error_msg:
                # Milestone já existe
                return True
            print(f"  ❌ Erro ao criar milestone: {e.stderr}")
            return False
    
    def create_label(self, label: Dict) -> bool:
        """Cria um label no repositório"""
        cmd = [
            "gh", "label", "create",
            "--repo", self.repo,
            "--name", label['name'],
            "--color", label['color'],
            "--description", label['description']
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            error_msg = str(e.stderr).lower()
            if "already exists" in error_msg:
                # Label já existe
                return True
            print(f"  ❌ Erro ao criar label: {e.stderr}")
            return False
    def create_issue(self, issue: Dict, milestone_title: Optional[str]) -> Optional[int]:
        """Cria uma issue no repositório"""
        cmd = [
            "gh", "issue", "create",
            "--repo", self.repo,
            "--title", issue['title'],
            "--body", issue['body'],
        ]
        
        # Adicionar labels (sem validação - deixar falhar silenciosamente se não existir)
        if issue.get('labels'):
            for label in issue['labels']:
                cmd.extend(["--label", label])
        
        # Adicionar milestone por título
        if milestone_title:
            cmd.extend(["--milestone", milestone_title])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            # Extrair número da issue da URL retornada
            # Formato: https://github.com/user/repo/issues/123
            if "issues/" in result.stdout:
                issue_number = int(result.stdout.split("issues/")[-1].strip())
                return issue_number
        except subprocess.CalledProcessError as e:
            # Tentar criar sem labels se falhar
            if "label" in str(e.stderr).lower():
                print(f"  ⚠️  Aviso: Alguns labels não existem, criando issue sem eles")
                cmd_no_labels = [
                    "gh", "issue", "create",
                    "--repo", self.repo,
                    "--title", issue['title'],
                    "--body", issue['body'],
                ]
                if milestone_title:
                    cmd_no_labels.extend(["--milestone", milestone_title])
                
                try:
                    result = subprocess.run(cmd_no_labels, capture_output=True, text=True, check=True)
                    if "issues/" in result.stdout:
                        issue_number = int(result.stdout.split("issues/")[-1].strip())
                        return issue_number
                except subprocess.CalledProcessError as e2:
                    print(f"  ❌ Erro ao criar issue (sem labels): {e2.stderr}")
            else:
                print(f"  ❌ Erro ao criar issue: {e.stderr}")
        
        return None
    
    def add_issue_to_project(self, issue_number: int) -> bool:
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
            if "already added" in str(e.stderr).lower():
                return True  # Já estava adicionada
            print(f"  ❌ Erro ao adicionar ao projeto: {e.stderr}")
            return False
    
    def create_branch(self, branch_name: str) -> bool:
        """Cria uma branch a partir de develop"""
        cmd = [
            "git", "checkout", "-b", branch_name, "origin/develop"
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=self.repo)
            return True
        except subprocess.CalledProcessError as e:
            error_msg = str(e.stderr).lower()
            if "already exists" in error_msg or "fatal: a branch named" in error_msg:
                # Branch já existe
                return True
            print(f"  ❌ Erro ao criar branch: {e.stderr}")
            return False
    
    def create_all_milestones(self):
        """Cria todos os milestones faltantes"""
        print("="*80)
        print("🎯 CRIANDO MILESTONES FALTANTES")
        print("="*80)
        print()
        
        for idx, milestone in enumerate(MISSING_MILESTONES, 1):
            print(f"[{idx}/{len(MISSING_MILESTONES)}] Criando milestone: {milestone['title']}")
            
            if self.create_milestone(milestone):
                print(f"  ✅ Milestone criado")
                self.created_milestones.append(milestone['title'])
            else:
                print(f"  ❌ Falha ao criar milestone")
                self.failed_milestones.append(milestone['title'])
            
            print()
    
    def create_all_labels(self):
        """Cria todos os labels faltantes"""
        print("="*80)
        print("🏷️  CRIANDO LABELS FALTANTES")
        print("="*80)
        print()
        
        for idx, label in enumerate(MISSING_LABELS, 1):
            print(f"[{idx}/{len(MISSING_LABELS)}] Criando label: {label['name']}")
            
            if self.create_label(label):
                print(f"  ✅ Label criado")
                self.created_labels.append(label['name'])
            else:
                print(f"  ❌ Falha ao criar label")
                self.failed_labels.append(label['name'])
            
            print()
    def create_all_issues(self):
        """Cria todas as issues faltantes"""
        print("="*80)
        print("📝 CRIANDO ISSUES FALTANTES")
        print("="*80)
        print()
        
        for idx, issue in enumerate(MISSING_ISSUES, 1):
            print(f"[{idx}/{len(MISSING_ISSUES)}] #{issue['number']} - {issue['title']}")
            
            # Usar título do milestone diretamente
            milestone_title = issue['milestone']
            
            # Criar issue
            issue_number = self.create_issue(issue, milestone_title)
            
            if issue_number:
                print(f"  ✅ Issue criada (#{issue_number})")
                
                # Adicionar ao projeto
                if self.add_issue_to_project(issue_number):
                    print(f"  ✅ Adicionada ao projeto")
                    self.created_issues.append({
                        "number": issue_number,
                        "title": issue['title'],
                        "milestone": issue['milestone'],
                        "branch": issue['branch']
                    })
                else:
                    print(f"  ⚠️  Falha ao adicionar ao projeto")
                    self.created_issues.append({
                        "number": issue_number,
                        "title": issue['title'],
                        "milestone": issue['milestone'],
                        "branch": issue['branch']
                    })
            else:
                print(f"  ❌ Falha ao criar issue")
                self.failed_issues.append(issue['title'])
            
            print()
    
    def create_all_branches(self):
        """Cria todas as branches faltantes"""
        print("="*80)
        print("🌿 CRIANDO BRANCHES FALTANTES")
        print("="*80)
        print()
        
        for idx, issue in enumerate(MISSING_ISSUES, 1):
            branch_name = issue['branch']
            print(f"[{idx}/{len(MISSING_ISSUES)}] Criando branch: {branch_name}")
            
            if self.create_branch(branch_name):
                print(f"  ✅ Branch criada")
                self.created_branches.append(branch_name)
            else:
                print(f"  ❌ Falha ao criar branch")
                self.failed_branches.append(branch_name)
            
            print()
    
    def print_summary(self):
        """Exibe resumo final"""
        print("="*80)
        print("📊 RESUMO FINAL")
        print("="*80)
        print()
        
        print(f"✅ Milestones criados: {len(self.created_milestones)}")
        for milestone in self.created_milestones:
            print(f"   - {milestone}")
        print()
        
        print(f"✅ Labels criados: {len(self.created_labels)}")
        for label in self.created_labels:
            print(f"   - {label}")
        print()
        
        print(f"✅ Issues criadas: {len(self.created_issues)}")
        for i in self.created_issues:
            print(f"   - #{i['number']}: {i['title']} ({i['milestone']})")
        print()
        
        print(f"✅ Branches criadas: {len(self.created_branches)}")
        for branch in self.created_branches:
            print(f"   - {branch}")
        print()
        
        if self.failed_milestones:
            print(f"❌ Milestones falhados: {len(self.failed_milestones)}")
            for milestone in self.failed_milestones:
                print(f"   - {milestone}")
            print()
        
        if self.failed_labels:
            print(f"❌ Labels falhados: {len(self.failed_labels)}")
            for label in self.failed_labels:
                print(f"   - {label}")
            print()
        
        if self.failed_issues:
            print(f"❌ Issues falhadas: {len(self.failed_issues)}")
            for i in self.failed_issues:
                print(f"   - {i}")
            print()
        
        if self.failed_branches:
            print(f"❌ Branches falhadas: {len(self.failed_branches)}")
            for branch in self.failed_branches:
                print(f"   - {branch}")
            print()
        
        if not self.failed_milestones and not self.failed_labels and not self.failed_issues and not self.failed_branches:
            print("🎉 SUCESSO! Todos os 3 milestones, 3 labels, 4 issues e 4 branches foram criados!")
        else:
            total_failed = len(self.failed_milestones) + len(self.failed_labels) + len(self.failed_issues) + len(self.failed_branches)
            print(f"⚠️  {total_failed} itens falharam.")
        
        print()
        print("Próximos passos:")
        print(f"1. Acesse o projeto: {PROJECT_URL}")
        print("2. Verifique se todos os 3 milestones foram criados")
        print("3. Verifique se todas as 4 issues estão visíveis")
        print("4. Confirme que os 3 labels foram criados")
        print("5. Verifique se as 4 branches foram criadas localmente")
        print("6. Faça push das branches: git push -u origin <branch-name>")
        print("7. Inicie o Sprint 1")
        print()

def main():
    """Função principal"""
    print()
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  BIOTECPREDICT: Criar 4 Issues Faltantes".center(78) + "║")
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
    creator = GitHubIssueCreator(REPO, PROJECT_ID)
    
    # Criar milestones
    creator.create_all_milestones()
    
    # Criar labels
    creator.create_all_labels()
    
    # Criar issues
    creator.create_all_issues()
    
    # Criar branches
    creator.create_all_branches()
    
    # Exibir resumo
    creator.print_summary()

if __name__ == "__main__":
    main()
