# Prompts — Etapa 3: Refatoração com Suporte de IA

Refatoração documentada com critério SOLID, prompt utilizado, estado anterior e resultado obtido.

---

## Refatoração 1 — Aplicação do Princípio Open/Closed no BatchService

**Critério técnico:** SOLID — Open/Closed Principle  
**Padrão de prompt:** Role-based + Chain of Thought  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Branch:** `feature/refatoracao-ia`  
**Data:** 2026-05-27

---

### Código ANTES da refatoração

```python
# batch_service.py — versão original (violação OCP)
class BatchService:
    @staticmethod
    def calculate_compliance(rows):
        score = 100.0
        for row in rows:
            # lógica de temperatura
            if row['temperature'] < 30 or row['temperature'] > 40:
                score -= 10
            # lógica de pH
            if row['ph'] < 6.8 or row['ph'] > 7.4:
                score -= 10
            # lógica de O2
            if row['dissolved_oxygen'] < 80:
                score -= 15
            # lógica de pressão
            if row['pressure'] < 0.8 or row['pressure'] > 1.2:
                score -= 10
            # lógica de agitação
            if row['agitator_speed'] < 200 or row['agitator_speed'] > 300:
                score -= 5
        return max(0.0, score)
```

**Problema:** Para adicionar uma nova regra de compliance era necessário modificar o `BatchService` — violação do Open/Closed Principle. Além disso, sem separação de responsabilidades, impossível testar cada regra individualmente.

---

### Prompt de refatoração

```
Como engenheiro de software especialista em princípios SOLID,
Quero que você refatore o método calculate_compliance do BatchService,
Para que novas regras de compliance possam ser adicionadas sem modificar a classe existente.

Código atual:
[código acima]

Aplique o princípio Open/Closed:
- Crie uma abstração ComplianceRule com método evaluate(row) → penalty
- Implemente cada regra como classe separada
- O ComplianceService recebe uma lista de regras e as aplica
- Novas regras são adicionadas criando novas classes, sem tocar no service

Restrições:
- Mantenha compatibilidade com a interface atual
- Cada regra deve ter nome descritivo e penalty documentada
- Use dataclasses ou Protocol para a abstração
```

---

### Código DEPOIS da refatoração

```python
# compliance_service.py — versão refatorada (OCP aplicado)
from dataclasses import dataclass
from typing import Protocol, List

class ComplianceRule(Protocol):
    def evaluate(self, row: dict) -> float:
        ...

@dataclass
class TemperatureRule:
    min_val: float = 30.0
    max_val: float = 40.0
    penalty: float = 10.0

    def evaluate(self, row: dict) -> float:
        t = row.get('temperature', 0)
        return self.penalty if not (self.min_val <= t <= self.max_val) else 0.0

@dataclass
class PhRule:
    min_val: float = 6.8
    max_val: float = 7.4
    penalty: float = 10.0

    def evaluate(self, row: dict) -> float:
        ph = row.get('ph', 0)
        return self.penalty if not (self.min_val <= ph <= self.max_val) else 0.0

# ... demais regras

class ComplianceService:
    DEFAULT_RULES: List[ComplianceRule] = [
        TemperatureRule(), PhRule(), OxygenRule(), PressureRule(), AgitatorRule()
    ]

    @classmethod
    def calculate_score(cls, rows: list, rules=None) -> float:
        rules = rules or cls.DEFAULT_RULES
        if not rows:
            return 0.0
        total_penalty = sum(
            rule.evaluate(row) for row in rows for rule in rules
        )
        avg_penalty = total_penalty / len(rows)
        return round(max(0.0, 100.0 - avg_penalty), 2)
```

---

### Avaliação do resultado

✅ Cada regra é testável de forma independente  
✅ Novas regras são adicionadas sem modificar `ComplianceService`  
✅ Configuração de regras injetável (útil para testes)  
⚠️ A IA inicialmente usou herança em vez de Protocol — corrigido para composição via Protocol (mais pythônico e flexível)
