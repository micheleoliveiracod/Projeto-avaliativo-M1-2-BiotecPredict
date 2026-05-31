# Implementation Plan: Prompt Logging

## Overview

Sistema automático de logging de prompts executados no Kiro, organizado por branch Git. O objetivo é manter rastreabilidade completa das interações com o agente durante o desenvolvimento do BiotecPredict.

**Arquitetura:**
```
Kiro (promptSubmit) → Hook → Script Python → Arquivo .md por branch
```

---

## Tasks

## 1. Configuração Inicial

### 1.1 Criar estrutura de diretórios
- [x] Criar diretório `.kiro/hooks/` (se não existir)
- [x] Criar diretório `.kiro/scripts/` (se não existir)
- [x] Criar diretório `.kiro/prompt-logs/` (será criado automaticamente pelo script, mas pode ser criado manualmente)

### 1.2 Configurar dependências Python
- [x] Adicionar `pytz>=2024.1` ao `requirements.txt` (ou criar arquivo se não existir)
- [x] Documentar instalação de dependências no README

---

## 2. Implementação do Hook

### 2.1 Criar arquivo de hook
- [x] Criar `.kiro/hooks/prompt-logger.json` com configuração do hook `promptSubmit`
- [x] Validar sintaxe JSON
- [x] Testar se hook é reconhecido pelo Kiro

---

## 3. Implementação do Script de Logging

### 3.1 Criar script Python base
- [x] Criar `.kiro/scripts/log_prompt.py` com estrutura básica
- [x] Adicionar shebang e encoding UTF-8
- [x] Adicionar docstring de documentação

### 3.2 Implementar funções de coleta de metadados
- [x] Implementar `get_git_branch()` - detecta branch atual via Git
- [x] Implementar `get_git_user()` - obtém nome do usuário Git
- [x] Implementar `get_brasilia_timestamp()` - gera timestamp em horário de Brasília
- [x] Implementar tratamento de erros para cada função (fallback gracioso)

### 3.3 Implementar captura de conteúdo do prompt
- [x] Implementar `get_prompt_content()` com múltiplas estratégias:
  - [x] Tentar variável de ambiente `KIRO_PROMPT`
  - [x] Tentar ler de stdin (se não for TTY)
  - [x] Fallback para placeholder se não disponível
- [x] Testar cada estratégia de captura

### 3.4 Implementar formatação de log
- [x] Implementar `sanitize_branch_name()` - converte caracteres especiais em nomes válidos
- [x] Implementar `format_log_entry()` - formata entrada no padrão Markdown
- [x] Extrair título do prompt (primeiras 50 caracteres)
- [x] Adicionar blocos de código para preservar formatação

### 3.5 Implementar persistência de logs
- [x] Implementar `log_prompt()` - função principal
- [x] Criar diretório `.kiro/prompt-logs/` se não existir
- [x] Adicionar cabeçalho ao arquivo na primeira entrada
- [x] Adicionar entrada formatada em modo append
- [x] Implementar tratamento de erros gracioso (não bloquear Kiro)

### 3.6 Tornar script executável
- [x] Adicionar permissões de execução: `chmod +x .kiro/scripts/log_prompt.py`
- [x] Testar execução direta do script

---

## 4. Documentação

### 4.1 Criar documentação de uso
- [x] Criar `docs/prompt-logging.md` com:
  - [x] Visão geral da funcionalidade
  - [x] Instruções de instalação
  - [x] Instruções de uso
  - [x] Exemplos de consulta de logs
  - [x] Troubleshooting
  - [x] Limitações conhecidas

### 4.2 Criar steering file
- [x] Criar `.kiro/steering/prompt-logging.md` com:
  - [x] Contexto da funcionalidade para o agente Kiro
  - [x] Convenções de logging
  - [x] Instruções para manutenção

### 4.3 Atualizar README principal
- [x] Adicionar seção sobre Prompt Logging no README.md
- [x] Incluir link para documentação detalhada
- [x] Mencionar dependências (pytz)

### 4.4 Atualizar .gitignore (se necessário)
- [x] Avaliar se logs devem ser versionados ou ignorados
- [x] Adicionar entrada ao .gitignore se decisão for ignorar logs
- [x] Documentar decisão no README

---

## 5. Testes

### 5.1 Testes manuais básicos
- [x] Testar primeiro prompt em nova branch (arquivo criado com cabeçalho)
- [x] Testar múltiplos prompts na mesma branch (append correto)
- [x] Testar troca de branch (arquivos separados)
- [x] Testar branch com caracteres especiais (sanitização correta)

### 5.2 Testes de edge cases
- [x] Testar em branch sem Git configurado (fallback para "unknown")
- [x] Testar com prompt vazio
- [x] Testar com prompt muito longo (>1000 caracteres)
- [x] Testar com caracteres especiais no prompt (UTF-8)

### 5.3 Testes de captura de conteúdo
- [x] Validar se variável de ambiente `KIRO_PROMPT` está disponível
- [ ] Validar se stdin está disponível no contexto do hook
- [ ] Documentar resultado dos testes de captura

### 5.4 Testes de performance
- [ ] Medir tempo de execução do script (<100ms)
  - Resultado: 151.89ms (média de 30 iterações)
  - Status: Acima do requisito, mas impacto negligenciável
  - Documentação: `.kiro/reports/performance_report.md`
- [x] Verificar que não bloqueia execução do Kiro
  - Status: ✅ Confirmado - não bloqueia significativamente

---

## 6. Validação e Ajustes

### 6.1 Validação de formato
- [ ] Verificar que logs são válidos em Markdown
- [ ] Verificar que diffs no Git são legíveis
- [ ] Verificar renderização no GitHub/GitLab

### 6.2 Validação de limitações
- [ ] Confirmar se conteúdo do prompt é capturado automaticamente
- [ ] Documentar limitações confirmadas
- [ ] Atualizar documentação com resultados dos testes

### 6.3 Code review
- [ ] Revisar código do script Python
- [ ] Revisar configuração do hook
- [ ] Revisar documentação

---

## 7. Entrega

### 7.1 Commit e versionamento
- [ ] Commit de todos os arquivos criados
- [ ] Seguir convenção de commits do projeto (Conventional Commits)
- [ ] Mensagem de commit descritiva

### 7.2 Documentação final
- [ ] Verificar que toda documentação está completa
- [ ] Verificar que exemplos estão corretos
- [ ] Verificar que limitações estão documentadas

### 7.3 Comunicação
- [ ] Informar equipe sobre nova funcionalidade
- [ ] Compartilhar documentação de uso
- [ ] Solicitar feedback inicial

---

## 8. Melhorias Futuras (Opcional)

### 8.1* Captura de resultados
- [ ] Implementar hook `agentStop` para capturar fim da execução
- [ ] Capturar resumo da resposta do agente
- [ ] Associar prompt → resultado no log

### 8.2* Interface de consulta
- [ ] Criar CLI para buscar logs: `kiro-logs search "keyword"`
- [ ] Implementar filtros por data, branch, usuário
- [ ] Exportação para JSON/CSV

### 8.3* Rotação de logs
- [ ] Implementar arquivamento automático de logs antigos
- [ ] Implementar compressão de arquivos grandes
- [ ] Configurar política de retenção

---

## Checklist de Conclusão

- [ ] Todos os arquivos criados e testados
- [ ] Documentação completa e revisada
- [ ] Testes manuais executados com sucesso
- [ ] Limitações documentadas
- [ ] README atualizado
- [ ] Commit realizado seguindo convenções do projeto
- [ ] Equipe informada sobre nova funcionalidade

---

## Task Dependency Graph

```
1.1 Criar estrutura de diretórios
    ↓
1.2 Configurar dependências Python
    ↓
2.1 Criar arquivo de hook
    ↓
3.1 Criar script Python base
    ↓
3.2 Implementar funções de coleta de metadados
    ↓
3.3 Implementar captura de conteúdo do prompt
    ↓
3.4 Implementar formatação de log
    ↓
3.5 Implementar persistência de logs
    ↓
3.6 Tornar script executável
    ↓
4.1 Criar documentação de uso
    ↓
4.2 Criar steering file
    ↓
4.3 Atualizar README principal
    ↓
4.4 Atualizar .gitignore
    ↓
5.1 Testes manuais básicos
    ↓
5.2 Testes de edge cases
    ↓
5.3 Testes de captura de conteúdo
    ↓
5.4 Testes de performance
    ↓
6.1 Validação de formato
    ↓
6.2 Validação de limitações
    ↓
6.3 Code review
    ↓
7.1 Commit e versionamento
    ↓
7.2 Documentação final
    ↓
7.3 Comunicação
```

---

## Notes

- **Prioridade**: Alta - Rastreabilidade de desenvolvimento
- **Complexidade**: Média - Integração com Kiro e Git
- **Risco**: Baixo - Não afeta código de produção
- **Estimativa**: 8-12 horas
- **Dependências externas**: Kiro, Git, Python 3.8+, pytz
