#!/usr/bin/env python3
"""
Script para atualizar as 5 issues do Sprint 0 para o novo formato
- Sprint 0 agora tem apenas 1 branch: chore/sprint-0-setup-gerenciamento-projeto
- Todas as 5 issues são do tipo chore/
- Sem código de backend/frontend
- Sem testes CI/CD

Repositório: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict
"""

import subprocess
import json
import sys

REPO = "micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict"

# 5 Issues do Sprint 0 - Novo Formato
SPRINT0_ISSUES = [
    {
        "title": "chore: criar estrutura de diretórios base",
        "labels": ["setup", "chore", "sprint-0"],
        "milestone": "Sprint 0 - Setup",
        "body": """## Contexto
Criar estrutura de diretórios conforme `.kiro/steering/structure.md`

## Escopo
- Criar diretórios backend (api/, processors/, services/, models/, schemas/, db/, ml/, scripts/, reports/, tests/) com .gitkeep
- Criar diretórios frontend (src/, components/, pages/, services/, hooks/, utils/) com .gitkeep
- Criar diretórios .kiro/ (.kiro/hooks/, .kiro/scripts/, .kiro/specs/, .kiro/steering/)
- Criar diretórios .github/ (.github/workflows/, .github/issue_template/)
- Criar diretórios scripts/ para automação
- Criar arquivos README.md em diretórios principais
- Configurar .gitignore para Python e React
- Criar arquivos iniciais (requirements.txt, package.json)

## Critérios de Aceitação
- [ ] Estrutura de diretórios criada conforme especificação
- [ ] Todos os .gitkeep presentes
- [ ] Todos os .gitignore configurados corretamente

## Branch
chore/sprint-0-setup-gerenciamento-projeto

## Notas
- Sprint 0 usa apenas 1 branch única para todos os commits
- Sem código de backend/frontend
- Sem testes CI/CD"""
    },
    {
        "title": "chore: criar documentação estratégica em .kiro/steering/",
        "labels": ["setup", "chore", "documentation", "sprint-0"],
        "milestone": "Sprint 0 - Setup",
        "body": """## Contexto
Criar steering files com contexto permanente do projeto

## Escopo
- Criar tech.md (stack tecnológica)
- Criar structure.md (estrutura do projeto)
- Criar requirements.md (requisitos funcionais)
- Criar product.md (visão do produto)
- Criar gitflow.md (fluxo Git e sprints)
- Criar ci-cd.md (workflows GitHub Actions)
- Criar compliance.md (conformidade e rastreabilidade)
- Criar deploy.md (instruções de deploy)
- Criar localizacao.md (timezone e idioma)

## Critérios de Aceitação
- [ ] Todos os steering files criados
- [ ] Documentação completa e consistente
- [ ] Referências cruzadas funcionando

## Branch
chore/sprint-0-setup-gerenciamento-projeto

## Notas
- Steering files fornecem contexto permanente ao agente Kiro
- Documentação estratégica do projeto"""
    },
    {
        "title": "chore: configurar workflows GitHub Actions",
        "labels": ["setup", "chore", "ci-cd", "sprint-0"],
        "milestone": "Sprint 0 - Setup",
        "body": """## Contexto
Criar workflows CI/CD que disparam apenas em Sprint 1+

## Escopo
- Criar ci.yml (lint + testes para feature/*, bugfix/*, hotfix/*)
- Criar release-lint.yml (lint only para release/*)
- Criar cd.yml (deploy em main)
- Criar project-automation.yml (automação de board)
- Criar progress-report.yml (relatório semanal)
- Criar velocity-analysis.yml (análise de velocidade)
- Criar metrics-dashboard.yml (dashboard de métricas)
- Criar docs-generation.yml (geração de docs)
- Criar ai-test-generation.yml (geração de testes com IA)
- **Garantir que Sprint 0 (chore/*) NÃO dispara CI/CD de testes**

## Critérios de Aceitação
- [ ] Todos os workflows criados
- [ ] Workflows testados e funcionando
- [ ] Sprint 0 não dispara testes CI/CD

## Branch
chore/sprint-0-setup-gerenciamento-projeto

## Notas
- Sprint 0 não dispara testes CI/CD
- Testes começam em Sprint 1 com branches feature/*"""
    },
    {
        "title": "chore: criar templates de issues e PRs",
        "labels": ["setup", "chore", "sprint-0"],
        "milestone": "Sprint 0 - Setup",
        "body": """## Contexto
Criar templates estruturados para issues e PRs

## Escopo
- Criar bug_report.yml
- Criar feature.yml
- Criar chore.yml
- Criar documentation.yml
- Criar general.yml
- Criar pull_request_template.md
- Criar config.yml para templates
- Adicionar labels padrão

## Critérios de Aceitação
- [ ] Todos os templates criados
- [ ] Templates testados no GitHub
- [ ] Labels configurados

## Branch
chore/sprint-0-setup-gerenciamento-projeto

## Notas
- Templates padronizam criação de issues e PRs
- Melhoram qualidade da documentação"""
    },
    {
        "title": "chore: criar scripts de automação e hooks Kiro",
        "labels": ["setup", "chore", "automation", "sprint-0"],
        "milestone": "Sprint 0 - Setup",
        "body": """## Contexto
Criar scripts Python e hooks Kiro para automação

## Escopo
- Criar log_prompt.py (logging de prompts)
- Criar create_all_issues.py (criação de issues)
- Criar create_branches.py (criação de branches)
- Criar manage_project.py (gerenciamento de projeto)
- Criar hooks Kiro (prompt-logger.json, generate-tests.json, etc)
- Criar README.md em scripts/
- Criar README.md em .kiro/hooks/
- Testar scripts localmente

## Critérios de Aceitação
- [ ] Todos os scripts criados e funcionando
- [ ] Hooks Kiro configurados
- [ ] Documentação de scripts completa

## Branch
chore/sprint-0-setup-gerenciamento-projeto

## Notas
- Scripts automatizam tarefas repetitivas
- Hooks Kiro integram IA no desenvolvimento"""
    },
]


def run_command(cmd):
    """Executar comando e retornar output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.returncode
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return None, 1


def get_sprint0_issue_numbers():
    """Obter números das 5 primeiras issues (Sprint 0)"""
    cmd = f'gh issue list --repo {REPO} --limit 5 --json number --jq ".[].number"'
    output, code = run_command(cmd)
    
    if code != 0:
        print(f"❌ Erro ao listar issues: {output}")
        return []
    
    try:
        numbers = [int(line.strip()) for line in output.split('\n') if line.strip()]
        return numbers
    except Exception as e:
        print(f"❌ Erro ao parsear números de issues: {e}")
        return []


def update_issue(issue_number, title, labels, body):
    """Atualizar uma issue existente"""
    print(f"\n📝 Atualizando issue #{issue_number}...")
    
    # Atualizar título
    cmd = f'gh issue edit {issue_number} --repo {REPO} --title "{title}"'
    output, code = run_command(cmd)
    if code != 0:
        print(f"❌ Erro ao atualizar título: {output}")
        return False
    
    # Atualizar labels
    labels_str = " ".join(labels)
    cmd = f'gh issue edit {issue_number} --repo {REPO} --add-label "{labels_str}"'
    output, code = run_command(cmd)
    if code != 0:
        print(f"⚠️  Aviso ao adicionar labels: {output}")
    
    # Atualizar body (descrição)
    # Salvar body em arquivo temporário para evitar problemas com caracteres especiais
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(body)
        temp_file = f.name
    
    cmd = f'gh issue edit {issue_number} --repo {REPO} --body-file "{temp_file}"'
    output, code = run_command(cmd)
    
    import os
    os.unlink(temp_file)
    
    if code != 0:
        print(f"❌ Erro ao atualizar descrição: {output}")
        return False
    
    print(f"✅ Issue #{issue_number} atualizada com sucesso!")
    return True


def main():
    """Função principal"""
    print("=" * 70)
    print("🔄 ATUALIZANDO ISSUES DO SPRINT 0")
    print("=" * 70)
    print(f"\nRepositório: {REPO}")
    print(f"Total de issues a atualizar: {len(SPRINT0_ISSUES)}")
    
    # Obter números das 5 primeiras issues
    issue_numbers = get_sprint0_issue_numbers()
    
    if not issue_numbers or len(issue_numbers) < 5:
        print(f"\n❌ Erro: Esperado 5 issues, encontrado {len(issue_numbers)}")
        print("Certifique-se de que as 5 issues do Sprint 0 já foram criadas")
        return 1
    
    print(f"\n✅ Encontradas {len(issue_numbers)} issues do Sprint 0")
    print(f"   Números: {issue_numbers}")
    
    # Atualizar cada issue
    success_count = 0
    for i, issue_number in enumerate(issue_numbers):
        issue_data = SPRINT0_ISSUES[i]
        if update_issue(
            issue_number,
            issue_data["title"],
            issue_data["labels"],
            issue_data["body"]
        ):
            success_count += 1
    
    print("\n" + "=" * 70)
    print(f"✅ ATUALIZAÇÃO CONCLUÍDA: {success_count}/{len(SPRINT0_ISSUES)} issues atualizadas")
    print("=" * 70)
    
    if success_count == len(SPRINT0_ISSUES):
        print("\n🎉 Todas as issues do Sprint 0 foram atualizadas com sucesso!")
        print("\nPróximos passos:")
        print("1. Verificar as issues no GitHub")
        print("2. Começar Sprint 0 com branch: chore/sprint-0-setup-gerenciamento-projeto")
        print("3. Fazer commits nesta branch única")
        print("4. Fazer squash merge em develop")
        return 0
    else:
        print(f"\n⚠️  {len(SPRINT0_ISSUES) - success_count} issues falharam na atualização")
        return 1


if __name__ == "__main__":
    sys.exit(main())
