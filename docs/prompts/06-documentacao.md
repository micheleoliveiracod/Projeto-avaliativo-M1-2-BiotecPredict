# Prompts — Etapa 6: Documentação Técnica com IA

Prompts utilizados para gerar documentação técnica automática (docstrings, Swagger, README).

---

## Prompt 6.1 — Docstrings automáticas no backend

**Padrão aplicado:** Role-based + Few-shot  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Branch:** `feature/swagger-documentation`  
**Data:** 2026-05-28

### Prompt original

```
Como desenvolvedor Python senior especialista em documentação técnica,
Quero que você adicione docstrings completas em todos os módulos do BiotecPredict,
Para que o Swagger/OpenAPI seja gerado automaticamente pelo FastAPI.

Formato esperado para functions:
def upload_csv(file: UploadFile, db: Session) -> BatchResponse:
    """
    Upload de arquivo CSV com dados de sensores.

    Processa o arquivo através do pipeline:
    1. Parse CSV
    2. Validação de ranges
    3. Limpeza de dados
    4. Persistência no banco

    Args:
        file: Arquivo CSV multipart
        db: Sessão do banco de dados (injetada)

    Returns:
        BatchResponse com ID do batch criado

    Raises:
        HTTPException 400: CSV inválido ou sem linhas válidas
        HTTPException 500: Erro interno de processamento
    """

Módulos a documentar:
- backend/api/routes/ (todos os endpoints)
- backend/services/ (todos os métodos públicos)
- backend/processors/ (todos os métodos estáticos)

Restrições:
- Docstrings em português
- Incluir exemplos de entrada/saída nos endpoints principais
- Tags OpenAPI coerentes com os grupos de funcionalidade
```

### Resultado obtido

Docstrings adicionadas em todos os módulos. Swagger disponível em `/docs` e `/redoc` automaticamente via FastAPI. Tags organizadas por funcionalidade: `batches`, `compliance`, `predictions`, `health`.

---

## Prompt 6.2 — Diagrama de arquitetura em Mermaid

**Padrão aplicado:** Role-based  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-28

### Prompt original

```
Como arquiteto de software,
Quero que você gere um diagrama de arquitetura do BiotecPredict em formato Mermaid,
Para incluir no README.md e tornar a arquitetura visualmente clara.

Componentes a incluir:
- Frontend React (Upload, Dashboard)
- API FastAPI (routes, services, repositories)
- SQLite
- Pipeline ML (RandomForest)
- GitHub Actions CI/CD

Mostre o fluxo de dados: CSV upload → processamento → ML → resposta ao frontend
```

### Resultado obtido

Diagrama Mermaid gerado e integrado ao README.md na seção de arquitetura. Mostra o fluxo completo desde o upload do CSV até a resposta com compliance score e predição de risco.

---

## Prompt 6.3 — Padronização de nomenclatura de branches e issues

**Padrão aplicado:** Role-based  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-24

### Prompt original

```
Como desenvolvedor fullstack senior,
Quero que você padronize a nomenclatura de branches e issues conforme gitflow.md,
Para manter consistência em toda a documentação e automações.

O que você não deve fazer:
- Não crie nenhum arquivo desnecessário
- Não modifique arquivos além dos citados
- Não altere a estrutura de pastas existente
```

### Resultado obtido

Nomenclatura padronizada: `feature/`, `chore/`, `docs/`, `release/`, `test/` com nomes descritivos em kebab-case. Templates de issues atualizados para refletir o padrão.
