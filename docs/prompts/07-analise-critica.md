# Prompts — Etapa 7: Análise Crítica de Saídas da IA

Casos documentados em que a saída da IA foi identificada como incorreta ou insuficiente, com descrição do problema, correção aplicada e lição aprendida.

---

## Caso 1 — CI/CD configurado para todas as branches (problema crítico)

**Etapa:** Pipeline CI/CD  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-28  
**Gravidade:** Alta — quebrava todos os PRs de feature

### Problema identificado

O workflow `ci.yml` gerado pela IA configurou o trigger para rodar em **todas as branches**:

```yaml
# VERSÃO INCORRETA gerada pela IA
on:
  push:
    branches: ['**']  # todas as branches
  pull_request:
    branches: ['**']
```

O job `backend-tests` precisava de um serviço SQLite configurado. Quando rodava em branches de feature que ainda não tinham o backend configurado, **todos os testes falhavam com erro de conexão**, bloqueando os PRs de avançar.

### Diagnóstico

A IA interpretou "CI/CD completo" como "rodar em tudo", sem considerar que branches de feature podem estar em estado incompleto durante o desenvolvimento.

### Correção aplicada

```yaml
# VERSÃO CORRIGIDA
on:
  push:
    branches: [develop]
    paths-ignore:
      - 'docs/**'
      - '.kiro/steering/**'
      - '*.md'
  pull_request:
    branches: [develop, main]
```

Restrito a `develop` para pushes, e para PRs direcionados a `develop` ou `main`. Branches de feature não disparam o CI completo, apenas o `release-lint.yml` quando o PR vai para `main`.

### Lição aprendida

Prompts para CI/CD precisam especificar explicitamente **em quais branches** o workflow deve rodar e **por quê**. A IA tende a gerar configurações "máximas" sem considerar o ciclo de vida real do desenvolvimento.

---

## Caso 2 — Microsserviços propostos para um projeto de escopo reduzido

**Etapa:** Arquitetura  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-24  
**Gravidade:** Média — aumentaria complexidade desnecessariamente

### Problema identificado

Ao solicitar a arquitetura do sistema, a IA propôs uma arquitetura de **microsserviços com Docker Swarm**:

```
Serviço de Upload (porta 8001)
Serviço de ML (porta 8002)
Serviço de Compliance (porta 8003)
API Gateway (porta 80)
Message Queue (RabbitMQ)
```

### Diagnóstico

O prompt não especificou restrições de escopo e prazo. A IA generalizou para "melhor prática em produção" sem considerar que o objetivo é uma aplicação demonstrável de escopo acadêmico.

### Correção aplicada

Prompt refinado com restrições explícitas:

```
Restrições de escopo:
- Projeto acadêmico com prazo de 2 semanas
- Time de 1 desenvolvedor
- Objetivo: demonstrar funcionalidades, não escalar para produção
- Monolito modular é suficiente e preferível
```

Resultado: arquitetura simplificada para monolito FastAPI com módulos internos bem separados.

### Lição aprendida

Para decisões arquiteturais, sempre incluir restrições de **escopo, prazo e tamanho do time** no prompt. Sem essas restrições, a IA propõe soluções de nível enterprise que são inadequadas para projetos menores.

---

## Caso 3 — Testes unitários com dependência desnecessária de banco de dados

**Etapa:** Testes automatizados  
**Ferramenta:** Kiro (Claude Haiku 4.5)  
**Data:** 2026-05-27  
**Gravidade:** Média — testes lentos e frágeis

### Problema identificado

A IA gerou testes para `CSVProcessor` e `DataValidator` usando fixtures que criavam uma sessão real de banco de dados:

```python
# VERSÃO INCORRETA gerada pela IA
def test_csv_processor(db_session):  # fixture com SQLite real
    processor = CSVProcessor(db=db_session)  # desnecessário
    result = processor.process(csv_content)
    assert len(result) > 0
```

Os processors são classes de processamento puro — **não precisam de banco de dados**. Isso tornava os testes unitários dependentes de infraestrutura externa.

### Diagnóstico

A IA reutilizou a fixture `db_session` em todos os testes por consistência, sem avaliar se cada módulo realmente precisava dela.

### Correção aplicada

```python
# VERSÃO CORRIGIDA
def test_csv_processor_valid_content():
    # Sem fixture de banco — teste puro de lógica
    content = "temperature,ph,dissolved_oxygen,pressure,agitator_speed\n36.5,7.2,85.0,1.0,250"
    result = CSVProcessor.process(content)
    assert len(result) == 1
    assert result[0]['temperature'] == 36.5
```

### Lição aprendida

No prompt de geração de testes, especificar explicitamente: **"testes de lógica pura não devem usar fixtures de banco de dados"**. A IA precisa de instrução explícita para distinguir testes unitários de testes de integração.

---

## Caso 4 — Corrupção de nome de arquivo Unicode ao renomear via shell

**Etapa:** Organização de documentação  
**Ferramenta:** Claude Code (Claude Sonnet 4.6)  
**Data:** 2026-06-06  
**Gravidade:** Baixa — não afetou código de produção, mas gerou um arquivo com nome diferente do pedido, exigindo detecção e correção manual

### Problema identificado

Ao pedir para renomear `docs/considerções-sobre-IAs.rmd` para `.md`, a IA executou o comando pelo shell Bash:

```bash
mv "docs/considerções-sobre-IAs.rmd" "docs/considerções-sobre-IAs.md"
```

O comando reportou sucesso, e um `ls` logo em seguida até exibiu o nome esperado na tela. Mas o arquivo realmente gravado em disco ficou com um nome **diferente do solicitado**: `consideracao-sobre-IAs.md` — os caracteres "ç" e "õ" foram trocados por "c" e "cao" (não apenas acentos removidos: as letras mudaram).

### Diagnóstico

Os bytes UTF-8 do nome do arquivo (contendo "ç"/"õ") foram corrompidos ao passar pelo shell Bash/MSYS emulado no Windows — um mismatch de code page entre a ferramenta de shell e o sistema de arquivos NTFS. A confirmação só veio ao inspecionar os bytes reais do nome com `Get-ChildItem` + conversão para códigos numéricos no PowerShell, que revelou caracteres ASCII puros gravados em disco (`c-o-n-s-i-d-e-r-a-c-a-o`), não os caracteres acentuados do pedido original. Ou seja: a IA reportou sucesso e mostrou o nome "certo" no terminal, mas o resultado real estava errado — um erro silencioso.

### Correção aplicada

```powershell
# Renomear novamente, agora via PowerShell nativo (Unicode-safe no Windows)
Rename-Item -Path "consideracao-sobre-IAs.md" -NewName "considerções-sobre-IAs.md"
```

O `Rename-Item` do PowerShell preserva corretamente os caracteres Unicode do nome original — diferente do `mv` rodando em emulação Bash/MSYS no Windows.

### Lição aprendida

Em ambiente Windows, operações com nomes de arquivo contendo acentos/Unicode devem usar ferramentas nativas (PowerShell `Rename-Item`/`Move-Item`, ou ferramentas dedicadas de leitura/escrita) em vez de comandos de shell Bash/MSYS — que podem corromper a codificação dos argumentos **silenciosamente**, sem erro, sem aviso, e até exibindo o nome "correto" no terminal logo depois. Sempre vale conferir o resultado real (bytes do nome, não só a saída do comando) quando a operação envolve caracteres não-ASCII.
