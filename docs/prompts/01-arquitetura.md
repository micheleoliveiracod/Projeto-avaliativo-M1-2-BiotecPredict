# Prompts — Etapa 1: Arquitetura e Especificação

Prompts utilizados para planejar a arquitetura do BiotecPredict com suporte de IA.

---

## Prompt 1.1 — Definição do domínio e visão do produto

**Padrão aplicado:** Role-based + Chain of Thought  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-24

### Prompt original

```
Como especialista em produtos de software para indústria biofarmacêutica,
Quero que você defina o domínio e a visão do produto BiotecPredict,
Para que possamos planejar a arquitetura com responsabilidades claras.

Contexto:
- Dados de sensores industriais (temperatura, pH, O₂ dissolvido, pressão, agitação)
- Dataset: Big Data – Biopharmaceutical Manufacturing (Kaggle)
- Objetivo: calcular compliance score + prever risco com ML

Atividades:
1. Descreva o problema que o produto resolve
2. Liste as funcionalidades principais (mínimo 2)
3. Defina os componentes arquiteturais necessários
4. Justifique as decisões tecnológicas

O que você não deve fazer:
- Não crie código ainda
- Não proponha features fora do escopo industrial
```

### Resultado obtido

Definição do produto BiotecPredict como plataforma SaaS de manufatura preditiva com:
- Componente de cálculo de **Manufacturing Compliance Score** (regras determinísticas)
- Componente de **predição de risco** via RandomForestClassifier
- Arquitetura em camadas: API (FastAPI) → Services → Repositories → Database (SQLite)

### Avaliação crítica

A IA propôs inicialmente uma arquitetura de microsserviços com Docker Swarm. **Refinamento aplicado:** simplificado para monolito modular (mais adequado ao escopo do projeto e ao prazo).

---

## Prompt 1.2 — Planejamento da stack tecnológica

**Padrão aplicado:** Role-based + Few-shot  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-24

### Prompt original

```
Como desenvolvedor fullstack senior especialista em Python e React,
Quero que você defina a stack tecnológica do BiotecPredict,
Para que todas as decisões estejam documentadas e justificadas.

Restrições:
- Backend: Python (obrigatório)
- Frontend: React + TypeScript (obrigatório)
- ML: scikit-learn (obrigatório)
- Banco: SQLite (obrigatório)

Formato esperado (exemplo):
| Tecnologia | Papel | Justificativa |
| FastAPI    | API   | Performance async, Swagger automático |

O que você não deve fazer:
- Não use tecnologias fora das restrições acima
- Não proponha bancos NoSQL
```

### Resultado obtido

Stack definida: FastAPI 0.104 + React 18 + SQLite 15 + scikit-learn 1.3 + pytest + Vitest + Cypress + GitHub Actions.

---

## Prompt 1.3 — Unificação de sprints e gitflow

**Padrão aplicado:** Role-based  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-24

### Prompt original

```
Como especialista em gestão de produtos com experiência em metodologias ágeis,
Quero que você unifique as informações do arquivo sprint.md com o gitflow.md,
atualize os templates de issues e os scripts de criação,
Para ter uma estrutura de sprints consistente e automações funcionando corretamente.

Atividades:
1. Adicione as informações do sprint.md no gitflow.md sem remover nada existente
2. Atualize os arquivos .yml dentro de .github/issue_template/
3. Atualize os scripts dentro de scripts/ para refletir o fluxo de criação de issues

O que você não deve fazer:
- Não crie nenhum arquivo desnecessário
- Não modifique arquivos além dos citados
```

### Resultado obtido

Gitflow unificado com sprints (Sprint 0 ao 5 + Entrega Final), templates de issues atualizados, scripts de automação criados em `scripts/project-planning/`.
