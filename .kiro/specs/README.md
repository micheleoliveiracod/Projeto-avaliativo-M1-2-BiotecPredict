# Specs - BiotecPredict

Especificações técnicas e documentação de features do projeto.

## 📁 Estrutura

```
.kiro/specs/
├── requirements.md        # Requisitos funcionais e não-funcionais
├── design.md             # Design e arquitetura
├── tasks.md              # Tasks e checklist de implementação
├── prompt-logging/       # Spec de Prompt Logging (feature)
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
└── README.md             # Este arquivo
```

## 🎯 Propósito

Documentação técnica estruturada seguindo a metodologia Kiro:
- **Requirements**: O que precisa ser feito
- **Design**: Como será implementado
- **Tasks**: Checklist de execução

## 📋 Arquivos Principais

### `requirements.md`
Especificação de requisitos funcionais e não-funcionais do projeto.

**Conteúdo**:
- Requisitos funcionais (upload, processamento, ML, dashboard)
- Requisitos não-funcionais (performance, segurança, manutenibilidade)
- Critérios de aceitação

### `design.md`
Arquitetura e design técnico do projeto.

**Conteúdo**:
- Arquitetura geral (Clean Architecture + ETL distribuído)
- Componentes principais
- Fluxo de dados
- Padrões de design

### `tasks.md`
Checklist de tasks para implementação.

**Conteúdo**:
- Tasks por sprint
- Dependências entre tasks
- Critérios de conclusão
- Estimativas

## 📂 Features com Specs Próprias

### `prompt-logging/`

Especificação completa do sistema de Prompt Logging.

**Arquivos**:
- `requirements.md` - Requisitos do sistema de logging
- `design.md` - Design da arquitetura de logging
- `tasks.md` - Tasks de implementação

**Propósito**: Capturar e registrar automaticamente todos os prompts executados no Kiro, com rastreabilidade completa.

## 🔧 Como Usar

### Consultar Requisitos

```bash
# Ver requisitos gerais
cat .kiro/specs/requirements.md

# Ver requisitos de uma feature
cat .kiro/specs/prompt-logging/requirements.md
```

### Consultar Design

```bash
# Ver design geral
cat .kiro/specs/design.md

# Ver design de uma feature
cat .kiro/specs/prompt-logging/design.md
```

### Consultar Tasks

```bash
# Ver tasks gerais
cat .kiro/specs/tasks.md

# Ver tasks de uma feature
cat .kiro/specs/prompt-logging/tasks.md
```

## 📊 Fluxo de Desenvolvimento

```
Requirements (O que?)
    ↓
Design (Como?)
    ↓
Tasks (Checklist)
    ↓
Implementação
    ↓
Testes
    ↓
Entrega
```

## 🔐 Boas Práticas

✅ **Fazer**:
- Manter specs atualizadas com código
- Documentar decisões de design
- Usar specs como referência durante implementação
- Versionar specs junto com código

❌ **Não fazer**:
- Deixar specs desatualizadas
- Implementar sem consultar specs
- Deletar specs antigas (manter histórico)
- Modificar specs sem comunicar time

## 📚 Referências

- Metodologia Kiro: `.kiro/steering/`
- Git Flow: `.kiro/steering/gitflow.md`
- Estrutura do Projeto: `.kiro/steering/structure.md`
- Requisitos Gerais: `.kiro/steering/requirements.md`

---

**Versão**: 1.0.0  
**Status**: ✅ Ativo  
**Última Atualização**: 2026-05-27
