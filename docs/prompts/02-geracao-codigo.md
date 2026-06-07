# Prompts — Etapa 2: Geração de Código (3 Ciclos)

Ciclos completos de geração e refinamento do código principal com suporte de IA.

---

## Ciclo 1 — Geração Inicial (Abordagem Ampla)

**Padrão aplicado:** Chain of Thought  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Branch:** `feature/geracao-codigo-ia`  
**Data:** 2026-05-25

### Prompt original (v1.0)

```
Como desenvolvedor Python senior especialista em FastAPI e Clean Architecture,
Quero que você implemente o backend completo do BiotecPredict,
Para que o sistema processe uploads de CSV com dados de sensores industriais.

Pense passo a passo:
1. Primeiro, identifique as entidades do domínio (Batch, SensorReading, Prediction)
2. Depois, defina os modelos SQLAlchemy para cada entidade
3. Em seguida, crie os schemas Pydantic para validação
4. Implemente os repositórios com padrão Repository
5. Crie os services com a lógica de negócio
6. Por fim, exponha os endpoints FastAPI

Restrições:
- Use SQLAlchemy 2.0 com session typing
- Pydantic v2 com model_config
- Separação clara entre camadas (models / schemas / repositories / services / routes)
- Sem lógica de negócio nas routes
```

### Código gerado (v1.0 — problema identificado)

A IA gerou todos os modelos, schemas, repositories e routes em um único arquivo `main.py` com mais de 800 linhas, misturando todas as camadas.

### Problema identificado

Violação do princípio Single Responsibility — arquivo monolítico impossível de testar e manter.

---

## Ciclo 2 — Refinamento: Separação de Camadas

**Padrão aplicado:** Chain of Thought + Role-based  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-25

### Prompt de refinamento (v2.0)

```
O código anterior violou o princípio SRP ao concentrar tudo em main.py.

Como arquiteto de software especialista em Clean Architecture,
Quero que você refatore o código separando em módulos independentes,
Para que cada arquivo tenha uma única responsabilidade.

Estrutura esperada:
backend/
  models/       ← apenas modelos SQLAlchemy
  schemas/      ← apenas schemas Pydantic
  db/
    repository/ ← apenas acesso a dados
  services/     ← apenas lógica de negócio
  api/routes/   ← apenas endpoints HTTP
  processors/   ← apenas processamento de dados (CSV, validação, limpeza)

Regras:
- Routes não importam models diretamente (só via services)
- Services não importam routes
- Cada módulo tem seu __init__.py com exports explícitos
```

### Resultado (v2.0)

Estrutura modular implementada com separação clara entre camadas. Cada módulo testável de forma independente.

---

## Ciclo 3 — Refinamento: Pipeline de Processamento CSV

**Padrão aplicado:** Few-shot  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-26

### Prompt de refinamento (v3.0)

```
Como engenheiro de dados especialista em processamento de dados industriais,
Quero que você implemente o pipeline de processamento de CSV do BiotecPredict,
Para que os dados de sensores sejam validados e limpos antes de persistir.

Exemplo de entrada CSV:
temperature,ph,dissolved_oxygen,pressure,agitator_speed
36.5,7.2,85.3,1.02,250
42.1,6.8,91.0,1.05,260

Regras de negócio:
- temperatura: 30–40°C (fora = WARNING)
- pH: 6.8–7.4 (fora = WARNING)
- O₂ dissolvido: 80–100% (fora = CRITICAL se < 70%)
- pressão: 0.8–1.2 bar
- agitação: 200–300 RPM

Pipeline esperado (3 etapas):
1. CSVProcessor.process(content) → List[Dict]
2. DataValidator.validate_batch(rows) → (valid_rows, errors)
3. DataCleaner.clean(rows) → (cleaned_rows, warnings)

Mostre um exemplo de cada etapa com input e output esperado.
```

### Resultado (v3.0)

Pipeline implementado em `backend/processors/` com 3 classes independentes, cada uma testável unitariamente. Regras de negócio documentadas nos docstrings.
