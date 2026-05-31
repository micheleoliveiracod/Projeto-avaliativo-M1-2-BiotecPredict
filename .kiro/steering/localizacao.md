# Localização e Configuração Regional - BiotecPredict

Documento que define as configurações de idioma, timezone e localização para todo o projeto BiotecPredict.

---

## 🌍 Configurações Globais

### Idioma
- **Idioma Padrão**: Português Brasileiro (pt-BR)
- **Escopo**: Toda documentação, issues, PRs, commits, comentários de código
- **Exceção**: Código-fonte pode conter comentários em inglês se necessário para clareza técnica

### Timezone
- **Timezone Padrão**: America/Sao_Paulo (Brasília)
- **UTC Offset**: UTC-3 (sem horário de verão)
- **Aplicação**: Todos os timestamps, agendamentos, relatórios

### Localização
- **País**: Brasil
- **Capital**: Brasília
- **Formato de Data**: DD/MM/YYYY
- **Formato de Hora**: HH:mm:ss
- **Formato DateTime**: DD/MM/YYYY HH:mm:ss

---

## 📋 Aplicação em Diferentes Áreas

### GitHub Issues

**Idioma**: Português Brasileiro

**Templates de Issues**:
- 🐛 Relatório de Bug
- 🚀 Solicitação de Funcionalidade
- 📚 Documentação
- 🔧 Manutenção
- 💬 Questão Geral

### Pull Requests

**Idioma**: Português Brasileiro

**Estrutura de PR**:
```markdown
## Contexto
Por que essa mudança é necessária?

## O que foi feito
- Item 1
- Item 2

## Como testar
1. Passo 1
2. Passo 2

## Dependências
Closes #123

## Referências
- `.kiro/steering/tech.md`
```

### Commits

**Convenção**: Conventional Commits em Português

**Tipos**:
- `feat`: nova funcionalidade
- `fix`: correção de bug
- `docs`: documentação
- `chore`: manutenção
- `refactor`: refatoração
- `test`: testes
- `style`: formatação
- `perf`: performance
- `ci`: CI/CD

### Branches

**Convenção**: GitFlow em Português

**Tipos de Branch**:
- `feature/nome-da-funcionalidade` - Nova funcionalidade
- `bugfix/descricao-do-ajuste` - Correção de bug
- `hotfix/descricao-do-problema` - Correção urgente
- `release/vX.Y.Z` - Preparação de release
- `chore/descricao-da-tarefa` - Manutenção
- `docs/descricao-da-documentacao` - Documentação

---

## ⏰ Agendamentos de Workflows

Todos os workflows são agendados para horário de Brasília (UTC-3).

### Segunda-feira (Dia de Relatórios)

| Horário | Workflow | Descrição |
|---------|----------|-----------|
| 12:00 | Relatório de Progresso | Métricas de progresso do projeto |
| 13:00 | Análise de Velocidade | Análise de velocidade do time |
| 14:00 | Dashboard de Métricas | Dashboard completo de métricas |

---

## 📝 Documentação

### Formato de Data em Documentos
```
Formato: DD de MMMM de YYYY

Exemplos:
- 24 de Maio de 2026
- 31 de Dezembro de 2025
- 01 de Janeiro de 2026
```

### Formato de Hora em Documentos
```
Formato: HH:mm:ss (Brasília - UTC-3)

Exemplos:
- 14:35:22 (Brasília - UTC-3)
- 09:15:00 (Brasília - UTC-3)
- 23:59:59 (Brasília - UTC-3)
```

### Timestamps em Logs
```
Formato: YYYY-MM-DD HH:mm:ss

Exemplos:
- 2026-05-24 14:35:22
- 2026-05-27 00:45:18
- 2026-05-26 22:01:37
```

---

## 🔧 Configuração Técnica

### Python (log_prompt.py)
```python
import pytz

def get_brasilia_timestamp() -> str:
    """Gera timestamp em horário de Brasília."""
    tz = pytz.timezone("America/Sao_Paulo")
    now = datetime.now(tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")
```

### GitHub Actions (Workflows)
```yaml
# Converter para timezone de Brasília
- name: Gerar relatório
  run: |
    now=$(date -u +%s)
    brasilia_date=$(TZ='America/Sao_Paulo' date -d @$now +%Y-%m-%d)
```

### JavaScript (Node.js)
```javascript
// Converter para timezone de Brasília
const brasiliaTz = new Date(now.toLocaleString('pt-BR', { 
  timeZone: 'America/Sao_Paulo' 
}));
const date = brasiliaTz.toISOString().split('T')[0];
```

---

## ✅ Checklist de Localização

Ao criar novo conteúdo, verificar:

- [ ] Idioma: Português Brasileiro
- [ ] Timezone: America/Sao_Paulo (UTC-3)
- [ ] Formato de data: DD/MM/YYYY
- [ ] Formato de hora: HH:mm:ss
- [ ] Commits: Conventional Commits em português
- [ ] Issues: Títulos e descrições em português
- [ ] PRs: Contexto e descrição em português
- [ ] Branches: Nomes em português (kebab-case)
- [ ] Documentação: Português Brasileiro
- [ ] Comentários: Português Brasileiro
- [ ] Timestamps: YYYY-MM-DD HH:mm:ss (Brasília)

---

**Versão**: 1.0.0  
**Data**: 27 de Maio de 2026  
**Status**: ✅ Localização Configurada  
**Timezone**: America/Sao_Paulo (UTC-3)  
**Idioma**: Português Brasileiro (pt-BR)
