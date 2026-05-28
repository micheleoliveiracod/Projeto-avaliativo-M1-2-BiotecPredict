# Documentação do Sistema de Prompt Logging

## Visão Geral

### O que é o Sistema de Prompt Logging?

O **Sistema de Prompt Logging** é um mecanismo automático de rastreabilidade que captura e registra todos os prompts executados no Kiro durante o desenvolvimento do BiotecPredict. O sistema funciona de forma transparente, sem interferir no fluxo de trabalho do desenvolvedor, e organiza os logs por branch Git para facilitar a navegação e análise histórica.

### Por que é Importante?

A rastreabilidade completa das interações com o agente de IA é fundamental para:

- **Auditoria e Conformidade**: Manter registro documentado de todas as decisões e instruções fornecidas ao agente durante o desenvolvimento
- **Reprodutibilidade**: Permitir que qualquer desenvolvedor entenda o contexto e as decisões que levaram a uma implementação específica
- **Análise de Qualidade**: Avaliar a efetividade das instruções e identificar padrões de uso do agente
- **Documentação Viva**: Criar um histórico executável que complementa a documentação técnica tradicional
- **Aprendizado Contínuo**: Analisar prompts bem-sucedidos para melhorar futuras interações com o agente

### Como Funciona

O sistema opera através de um fluxo simples e automático:

```
Desenvolvedor submete prompt no Kiro
        ↓
Hook "promptSubmit" é disparado
        ↓
Script Python coleta metadados (usuário, branch, timestamp)
        ↓
Prompt é registrado em arquivo .md por branch
        ↓
Arquivo é versionado no Git automaticamente
```

Cada branch Git tem seu próprio arquivo de log (`main.md`, `develop.md`, `feature-auth.md`, etc.), permitindo rastreabilidade granular de quem fez o quê e quando.

### Características Principais

#### 1. **Captura Automática**
- Nenhuma ação manual necessária
- Funciona transparentemente em background
- Não interfere no fluxo de desenvolvimento

#### 2. **Organização por Branch**
- Cada branch tem seu próprio arquivo de log
- Facilita análise de trabalho específico
- Mantém histórico separado por contexto

#### 3. **Metadados Completos**
- Responsável (nome do usuário Git)
- Branch de origem
- Data e hora em horário de Brasília (UTC-3)
- Conteúdo completo do prompt

#### 4. **Rastreabilidade Versionada**
- Logs são versionados no Git
- Histórico completo preservado
- Facilita code reviews e análise histórica

#### 5. **Filtros Inteligentes**
- Prompts triviais são automaticamente filtrados
- Apenas interações significativas são registradas
- Reduz ruído nos logs

### Estrutura de Armazenamento

Os logs são organizados em uma estrutura simples e intuitiva:

```
.kiro/prompt-logs/
├── main.md                    # Logs da branch main
├── develop.md                 # Logs da branch develop
├── feature-compliance.md      # Logs de feature branches
├── bugfix-validation.md       # Logs de bugfix branches
├── release-v1.0.0.md         # Logs de release branches
└── chore-setup.md            # Logs de chore branches
```

Cada arquivo segue um formato padronizado com:
- Título do prompt
- Responsável (usuário Git)
- Branch de origem
- Data e hora (Brasília)
- Conteúdo completo do prompt

### Benefícios para o Projeto

#### Para Desenvolvedores
- Consultar histórico de decisões e instruções
- Entender contexto de implementações anteriores
- Reutilizar prompts bem-sucedidos
- Aprender com padrões de uso do agente

#### Para Revisores de Código
- Entender intenção por trás de mudanças
- Validar que instruções foram seguidas corretamente
- Identificar se houve desvios de requisitos
- Facilitar discussões em code reviews

#### Para Gestão de Projeto
- Rastrear uso de IA no desenvolvimento
- Medir efetividade do agente
- Identificar gargalos ou dificuldades
- Documentar decisões arquiteturais

#### Para Análise Crítica de IA
- Avaliar qualidade de código gerado
- Comparar código manual vs gerado por IA
- Identificar limitações do agente
- Fundamentar recomendações para uso futuro

### Integração com Fluxo de Trabalho

O sistema se integra perfeitamente ao fluxo Git Flow do projeto:

```
1. Criar branch (feature/*, bugfix/*, etc)
   ↓
2. Submeter prompts no Kiro
   ↓ (Automático: prompts são registrados em .kiro/prompt-logs/<branch>.md)
   ↓
3. Fazer commits e push
   ↓
4. Abrir Pull Request
   ↓
5. Revisor pode consultar logs da branch para entender contexto
   ↓
6. Merge em develop/main
   ↓
7. Logs permanecem versionados no Git para referência futura
```

### Conformidade e Segurança

- **Sem dados sensíveis**: Logs contêm apenas prompts e metadados, nunca senhas ou tokens
- **Acesso controlado**: Logs são versionados no repositório Git com controle de acesso padrão
- **Transparência**: Todos os desenvolvedores podem consultar logs de qualquer branch
- **Auditoria**: Histórico completo preservado para conformidade regulatória

### Próximos Passos

Para começar a usar o sistema:

1. **Verificar instalação**: Confirmar que hook e script estão em `.kiro/hooks/` e `.kiro/scripts/`
2. **Submeter prompts**: Usar normalmente o Kiro; logs são capturados automaticamente
3. **Consultar logs**: Acessar `.kiro/prompt-logs/<branch>.md` para revisar histórico
4. **Integrar em code reviews**: Referenciar logs ao revisar PRs

---

**Versão**: 0.1.0  
**Data**: 27 de Maio de 2026  
**Status**: ✅ Visão Geral Documentada


## Instruções de Instalação

### Pré-requisitos

Antes de instalar o sistema de prompt logging, certifique-se de que você possui:

#### 1. **Python 3.8+**
O script de logging é escrito em Python e requer Python 3.8 ou superior.

**Verificar versão instalada:**
```bash
python --version
# ou
python3 --version
```

**Se não tiver Python instalado:**
- Windows: Baixe em https://www.python.org/downloads/
- Mac: `brew install python3`
- Linux: `sudo apt-get install python3`

#### 2. **Git**
O sistema depende de Git para identificar a branch atual e versionar os logs.

**Verificar se Git está instalado:**
```bash
git --version
```

**Se não tiver Git instalado:**
- Windows: Baixe em https://git-scm.com/download/win
- Mac: `brew install git`
- Linux: `sudo apt-get install git`

#### 3. **Kiro**
O sistema funciona através de hooks do Kiro. Certifique-se de que o Kiro está configurado no seu projeto.

**Verificar se Kiro está configurado:**
```bash
ls -la .kiro/
# Deve existir o diretório .kiro/ com subdiretórios hooks/, scripts/, specs/, etc.
```

### Passo 1: Instalar Dependência Python (pytz)

O script de logging utiliza a biblioteca `pytz` para converter timestamps para o horário de Brasília (UTC-3).

**Instalar pytz:**
```bash
pip install pytz
# ou
pip3 install pytz
```

**Verificar instalação:**
```bash
python -c "import pytz; print(pytz.__version__)"
```

Se o comando acima retornar um número de versão, a instalação foi bem-sucedida.

### Passo 2: Verificar Estrutura de Diretórios

O sistema requer que os seguintes diretórios e arquivos existam:

**Estrutura esperada:**
```
.kiro/
├── hooks/
│   └── prompt-logger.json          # Hook de captura de prompts
├── scripts/
│   └── log_prompt.py               # Script de logging
└── prompt-logs/                    # Diretório para armazenar logs
    ├── main.md
    ├── develop.md
    └── (outros arquivos de log por branch)
```

**Verificar se os arquivos existem:**
```bash
# Windows
if exist ".kiro\hooks\prompt-logger.json" echo "Hook encontrado"
if exist ".kiro\scripts\log_prompt.py" echo "Script encontrado"
if exist ".kiro\prompt-logs" echo "Diretório de logs encontrado"

# Mac/Linux
ls -la .kiro/hooks/prompt-logger.json
ls -la .kiro/scripts/log_prompt.py
ls -la .kiro/prompt-logs/
```

Se algum arquivo ou diretório estiver faltando, consulte a seção "Troubleshooting" abaixo.

### Passo 3: Verificar Configuração do Hook

O hook `prompt-logger.json` deve estar configurado para interceptar o evento `promptSubmit` do Kiro.

**Conteúdo esperado do hook:**
```json
{
  "name": "Prompt Logger",
  "version": "1.0.0",
  "when": {
    "type": "promptSubmit"
  },
  "then": {
    "type": "runCommand",
    "command": "python .kiro/scripts/log_prompt.py"
  }
}
```

**Verificar conteúdo do hook:**
```bash
# Windows
type .kiro\hooks\prompt-logger.json

# Mac/Linux
cat .kiro/hooks/prompt-logger.json
```

Se o conteúdo estiver diferente, atualize o arquivo com a configuração acima.

### Passo 4: Verificar Permissões do Script

O script `log_prompt.py` deve ter permissões de execução.

**Verificar permissões (Mac/Linux):**
```bash
ls -la .kiro/scripts/log_prompt.py
# Deve mostrar algo como: -rwxr-xr-x (com 'x' para execução)
```

**Conceder permissões de execução (Mac/Linux):**
```bash
chmod +x .kiro/scripts/log_prompt.py
```

**Windows:** Permissões são gerenciadas automaticamente; nenhuma ação necessária.

### Passo 5: Testar a Instalação

Para verificar se o sistema está funcionando corretamente, execute um teste simples:

#### Teste 1: Verificar Estrutura
```bash
# Verificar se todos os arquivos existem
python .kiro/scripts/log_prompt.py --check
```

Se o comando retornar "OK", a estrutura está correta.

#### Teste 2: Criar Log de Teste
```bash
# Criar um log de teste manualmente
python .kiro/scripts/log_prompt.py --test
```

Isso deve criar uma entrada de teste no arquivo de log da branch atual.

#### Teste 3: Verificar Arquivo de Log
```bash
# Verificar se o arquivo de log foi criado
# Windows
type .kiro\prompt-logs\<branch-atual>.md

# Mac/Linux
cat .kiro/prompt-logs/<branch-atual>.md
```

Você deve ver uma entrada com:
- Título do prompt
- Responsável (seu usuário Git)
- Branch
- Data/hora em horário de Brasília
- Conteúdo do prompt

### Passo 6: Integração com Fluxo de Trabalho

Após verificar que a instalação está funcionando, o sistema está pronto para uso automático.

**Próximas ações:**
1. Submeter um prompt no Kiro normalmente
2. O hook será disparado automaticamente
3. O prompt será registrado em `.kiro/prompt-logs/<branch-atual>.md`
4. Fazer commit e push dos logs junto com o código

**Exemplo de fluxo:**
```bash
# 1. Criar branch
git checkout -b feature/nova-funcionalidade

# 2. Submeter prompts no Kiro (automático: logs são capturados)

# 3. Fazer commit
git add .
git commit -m "feat: implementa nova funcionalidade"

# 4. Fazer push
git push -u origin feature/nova-funcionalidade

# 5. Logs estão versionados em .kiro/prompt-logs/feature-nova-funcionalidade.md
```

---

## Troubleshooting

### Problema 1: "ModuleNotFoundError: No module named 'pytz'"

**Causa:** A biblioteca `pytz` não está instalada.

**Solução:**
```bash
pip install pytz
# ou
pip3 install pytz
```

**Verificar instalação:**
```bash
python -c "import pytz; print('OK')"
```

### Problema 2: "Hook não está sendo disparado"

**Causa:** O hook pode não estar configurado corretamente ou o Kiro não está reconhecendo-o.

**Solução:**
1. Verificar se o arquivo `.kiro/hooks/prompt-logger.json` existe
2. Verificar se o conteúdo do hook está correto (veja Passo 3)
3. Reiniciar o Kiro
4. Verificar logs de erro do Kiro

**Verificar logs do Kiro:**
```bash
# Logs geralmente estão em:
# Windows: %APPDATA%\Kiro\logs\
# Mac/Linux: ~/.kiro/logs/
```

### Problema 3: "Arquivo de log não está sendo criado"

**Causa:** O script pode não ter permissões de execução ou o diretório `.kiro/prompt-logs/` não existe.

**Solução:**
1. Verificar se o diretório `.kiro/prompt-logs/` existe
2. Se não existir, criar manualmente:
   ```bash
   mkdir -p .kiro/prompt-logs
   ```
3. Verificar permissões do script (veja Passo 4)
4. Executar teste manual:
   ```bash
   python .kiro/scripts/log_prompt.py --test
   ```

### Problema 4: "Timestamp está em horário incorreto"

**Causa:** A biblioteca `pytz` pode não estar configurada corretamente para o timezone de Brasília.

**Solução:**
1. Verificar se `pytz` está instalado corretamente
2. Verificar se o script está usando `America/Sao_Paulo` como timezone
3. Executar teste:
   ```bash
   python -c "import pytz; from datetime import datetime; tz = pytz.timezone('America/Sao_Paulo'); print(datetime.now(tz))"
   ```

### Problema 5: "Permissão negada ao executar script"

**Causa:** O script não tem permissões de execução (Mac/Linux).

**Solução:**
```bash
chmod +x .kiro/scripts/log_prompt.py
```

**Verificar permissões:**
```bash
ls -la .kiro/scripts/log_prompt.py
# Deve mostrar 'x' na coluna de permissões
```

### Problema 6: "Git não consegue identificar a branch"

**Causa:** O repositório Git pode não estar inicializado ou o script não consegue acessar informações do Git.

**Solução:**
1. Verificar se o repositório Git está inicializado:
   ```bash
   git status
   ```
2. Verificar se você está em uma branch válida:
   ```bash
   git branch
   ```
3. Se necessário, reinicializar o repositório:
   ```bash
   git init
   ```

### Problema 7: "Conteúdo do prompt não está sendo capturado"

**Causa:** Limitação conhecida do Kiro - nem sempre consegue expor o conteúdo completo do prompt via hooks.

**Solução:**
- Metadados (usuário, branch, timestamp) ainda são registrados
- Considerar captura manual se necessário
- Consultar a seção "Limitações Conhecidas" na documentação principal

---

## Verificação Final

Após completar todos os passos, execute este checklist para confirmar que a instalação está correta:

- [ ] Python 3.8+ instalado (`python --version`)
- [ ] Git instalado (`git --version`)
- [ ] Kiro configurado (diretório `.kiro/` existe)
- [ ] pytz instalado (`pip install pytz`)
- [ ] Diretório `.kiro/hooks/` existe
- [ ] Arquivo `.kiro/hooks/prompt-logger.json` existe e está configurado
- [ ] Diretório `.kiro/scripts/` existe
- [ ] Arquivo `.kiro/scripts/log_prompt.py` existe
- [ ] Diretório `.kiro/prompt-logs/` existe
- [ ] Script tem permissões de execução (Mac/Linux)
- [ ] Teste manual passou (`python .kiro/scripts/log_prompt.py --test`)
- [ ] Arquivo de log foi criado (`.kiro/prompt-logs/<branch>.md`)
- [ ] Entrada de teste está visível no arquivo de log

Se todos os itens estiverem marcados, a instalação foi bem-sucedida e o sistema está pronto para uso!

---

## Próximos Passos

Após a instalação bem-sucedida:

1. **Usar normalmente**: Submeter prompts no Kiro; logs são capturados automaticamente
2. **Consultar logs**: Acessar `.kiro/prompt-logs/<branch>.md` para revisar histórico
3. **Integrar em code reviews**: Referenciar logs ao revisar PRs
4. **Manter atualizado**: Fazer commit e push dos logs junto com o código

Para mais informações sobre como usar o sistema, consulte a seção "Visão Geral" acima.

---

**Versão**: 0.1.0  
**Data**: 27 de Maio de 2026  
**Status**: ✅ Instruções de Instalação Completas


## Instruções de Uso

### Visão Geral

Esta seção fornece instruções práticas para usar o sistema de prompt logging no dia a dia do desenvolvimento. O sistema funciona de forma automática, mas existem várias formas de consultar, buscar e integrar os logs ao seu fluxo de trabalho.

### 1. Submeter Prompts no Kiro (Captura Automática)

O sistema captura prompts automaticamente quando você os submete no Kiro. Nenhuma ação manual é necessária.

#### Fluxo Automático

```
1. Abrir Kiro
2. Digitar seu prompt
3. Pressionar Enter/Submit
   ↓ (Automático)
4. Hook "promptSubmit" é disparado
5. Script Python coleta metadados
6. Prompt é registrado em .kiro/prompt-logs/<branch-atual>.md
7. Arquivo é versionado no Git
```

#### Exemplo Prático

```
Você está na branch: feature/compliance-score
Você submete o prompt: "Implementar cálculo de compliance score com regras determinísticas"
   ↓ (Automático)
Prompt é registrado em: .kiro/prompt-logs/feature-compliance-score.md
```

#### O que é Capturado Automaticamente

- ✅ Título do prompt (primeiras palavras)
- ✅ Responsável (seu usuário Git)
- ✅ Branch atual
- ✅ Data e hora (Brasília - UTC-3)
- ✅ Conteúdo completo do prompt
- ✅ Timestamp em formato ISO (YYYY-MM-DD HH:mm:ss)

#### O que NÃO é Capturado

- ❌ Resposta do agente (planejado para fase futura)
- ❌ Prompts triviais (< 10 caracteres)
- ❌ Confirmações simples (sim, não, ok, yes, no)
- ❌ Comandos de navegação (next, back, continue)

**Justificativa:** Manter logs limpos e focados em interações significativas.

### 2. Visualizar Logs da Branch Atual

Para consultar os prompts registrados na sua branch atual, acesse o arquivo de log correspondente.

#### Método 1: Abrir Arquivo Diretamente

**Windows:**
```cmd
# Abrir no editor padrão
start .kiro\prompt-logs\<branch-atual>.md

# Ou abrir em editor específico
code .kiro\prompt-logs\<branch-atual>.md
```

**Mac/Linux:**
```bash
# Abrir no editor padrão
open .kiro/prompt-logs/<branch-atual>.md

# Ou abrir em editor específico
code .kiro/prompt-logs/<branch-atual>.md
```

#### Método 2: Visualizar no Terminal

**Windows:**
```cmd
type .kiro\prompt-logs\<branch-atual>.md
```

**Mac/Linux:**
```bash
cat .kiro/prompt-logs/<branch-atual>.md
```

#### Método 3: Visualizar Últimas Entradas

**Windows:**
```cmd
# Últimas 50 linhas
powershell -Command "Get-Content .kiro\prompt-logs\<branch-atual>.md -Tail 50"
```

**Mac/Linux:**
```bash
# Últimas 50 linhas
tail -n 50 .kiro/prompt-logs/<branch-atual>.md
```

#### Exemplo de Saída

```markdown
## Prompt: Implementar cálculo de compliance score
- Responsável: seu-usuario-git
- Branch: feature-compliance-score
- Data/hora: 2026-05-27 14:35:22 (Brasília - UTC-3)

### Prompt original
```
Implementar cálculo de Manufacturing Compliance Score com as seguintes regras:
- Temperature: 20-45°C (score 100 se dentro, 50 se fora)
- pH: 4.0-9.0 (score 100 se dentro, 50 se fora)
- Score final: média dos scores individuais
```

---

## Prompt: Criar testes unitários para compliance score
- Responsável: seu-usuario-git
- Branch: feature-compliance-score
- Data/hora: 2026-05-27 15:10:45 (Brasília - UTC-3)

### Prompt original
```
Criar testes unitários com pytest para a função de cálculo de compliance score.
Incluir testes para:
1. Valores dentro do range (score 100)
2. Valores fora do range (score 50)
3. Valores extremos (0, 100)
```
```

### 3. Visualizar Logs de Outras Branches

Para consultar prompts de outras branches (útil para entender contexto de features anteriores), acesse o arquivo de log da branch desejada.

#### Listar Todas as Branches com Logs

**Windows:**
```cmd
dir .kiro\prompt-logs\
```

**Mac/Linux:**
```bash
ls -la .kiro/prompt-logs/
```

#### Visualizar Log de Branch Específica

**Windows:**
```cmd
type .kiro\prompt-logs\feature-upload-csv.md
```

**Mac/Linux:**
```bash
cat .kiro/prompt-logs/feature-upload-csv.md
```

#### Exemplo: Consultar Logs de Feature Anterior

```bash
# Você está em: feature/ml-prediction
# Quer consultar logs de: feature/compliance-score

# Mac/Linux
cat .kiro/prompt-logs/feature-compliance-score.md

# Windows
type .kiro\prompt-logs\feature-compliance-score.md
```

**Benefício:** Entender como a feature anterior foi implementada e reutilizar padrões bem-sucedidos.

### 4. Buscar Logs por Palavra-Chave

Para encontrar prompts específicos em um arquivo de log, use comandos de busca.

#### Buscar em Log da Branch Atual

**Windows (PowerShell):**
```powershell
Select-String -Path ".kiro\prompt-logs\<branch-atual>.md" -Pattern "palavra-chave"
```

**Mac/Linux:**
```bash
grep "palavra-chave" .kiro/prompt-logs/<branch-atual>.md
```

#### Buscar em Todos os Logs

**Windows (PowerShell):**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "palavra-chave"
```

**Mac/Linux:**
```bash
grep -r "palavra-chave" .kiro/prompt-logs/
```

#### Exemplos Práticos

**Buscar prompts sobre "compliance":**
```bash
# Mac/Linux
grep -i "compliance" .kiro/prompt-logs/*.md

# Windows
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "compliance"
```

**Buscar prompts sobre "teste":**
```bash
# Mac/Linux
grep -i "teste" .kiro/prompt-logs/*.md

# Windows
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "teste"
```

**Buscar prompts de um usuário específico:**
```bash
# Mac/Linux
grep "Responsável: seu-usuario" .kiro/prompt-logs/*.md

# Windows
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "Responsável: seu-usuario"
```

#### Buscar com Contexto

**Mac/Linux (mostrar 5 linhas antes e depois):**
```bash
grep -B 5 -A 5 "palavra-chave" .kiro/prompt-logs/<branch>.md
```

**Windows (PowerShell):**
```powershell
Select-String -Path ".kiro\prompt-logs\<branch>.md" -Pattern "palavra-chave" -Context 5,5
```

### 5. Integrar Logs em Code Reviews

Os logs são ferramentas poderosas para code reviews. Use-os para entender o contexto e validar que as instruções foram seguidas.

#### Passo 1: Revisor Acessa o Log da Branch

Quando revisar uma PR, consulte o arquivo de log da branch correspondente:

```bash
# Você está revisando PR da branch: feature/ml-prediction
# Consulte o log:
cat .kiro/prompt-logs/feature-ml-prediction.md
```

#### Passo 2: Entender o Contexto

Leia os prompts para entender:
- Qual era a intenção original
- Quais requisitos foram solicitados
- Quais decisões arquiteturais foram tomadas
- Quais padrões foram seguidos

#### Passo 3: Validar Implementação

Compare o código com os prompts:
- ✅ O código implementa o que foi solicitado?
- ✅ Os padrões foram seguidos?
- ✅ Os requisitos foram atendidos?
- ✅ Há desvios não documentados?

#### Passo 4: Comentar na PR

Referencie os logs em seus comentários:

```markdown
## Comentário de Review

Consultei o log de prompts desta branch (.kiro/prompt-logs/feature-ml-prediction.md) 
e identifiquei que o prompt solicitava:

> "Implementar RandomForestClassifier com features: Temperature, pH, Dissolved Oxygen, Pressure, Agitator Speed"

Porém, no código vejo que apenas 3 features estão sendo utilizadas. 
Isso é intencional ou foi um desvio?

Referência: Prompt de 2026-05-27 14:35:22
```

#### Exemplo Completo de Code Review com Logs

```markdown
## Code Review - feature/ml-prediction

### Contexto (baseado em .kiro/prompt-logs/feature-ml-prediction.md)

O desenvolvedor solicitou ao Kiro:
1. Implementar RandomForestClassifier
2. Usar 5 features específicas
3. Retornar predição com confiança
4. Adicionar testes unitários

### Validação

- ✅ RandomForestClassifier implementado corretamente
- ✅ Todas as 5 features estão sendo utilizadas
- ✅ Confiança é retornada na resposta
- ✅ Testes unitários cobrem casos principais
- ⚠️ Faltam testes para edge cases (valores extremos)

### Sugestões

Adicionar testes para:
- Valores mínimos (0)
- Valores máximos (100)
- Valores nulos

Referência: Prompts em .kiro/prompt-logs/feature-ml-prediction.md
```

### 6. Melhores Práticas para Usar o Sistema

#### 1. **Fazer Commits Regulares dos Logs**

Os logs devem ser versionados junto com o código:

```bash
# Após submeter prompts e fazer alterações
git add .kiro/prompt-logs/
git commit -m "docs: adiciona prompts de implementação da feature"
git push
```

#### 2. **Referenciar Logs em Commits**

Quando fazer commit de código gerado por IA, referencie o log:

```bash
git commit -m "feat(ml): implementa RandomForestClassifier

Implementação baseada em prompts registrados em:
.kiro/prompt-logs/feature-ml-prediction.md

Prompts de 2026-05-27 14:35:22 e 2026-05-27 15:10:45"
```

#### 3. **Consultar Logs Antes de Iniciar Feature**

Antes de começar uma nova feature, consulte logs de features similares:

```bash
# Você vai implementar "feature/data-validation"
# Consulte logs de features anteriores:
cat .kiro/prompt-logs/feature-data-cleaner.md
cat .kiro/prompt-logs/feature-csv-processor.md
```

**Benefício:** Reutilizar padrões bem-sucedidos e evitar repetir erros.

#### 4. **Usar Logs para Documentação**

Inclua referências aos logs na documentação técnica:

```markdown
## Implementação de Compliance Score

Para entender como esta feature foi desenvolvida, consulte:
- Prompts: `.kiro/prompt-logs/feature-compliance-score.md`
- Commits: `git log --grep="compliance"`
- PR: #15

### Decisões Arquiteturais

As decisões foram baseadas em prompts registrados em:
- 2026-05-27 14:35:22 - Definição de regras
- 2026-05-27 15:10:45 - Implementação de testes
```

#### 5. **Manter Logs Limpos**

Não edite manualmente os arquivos de log. Deixe o sistema gerenciar automaticamente:

```bash
# ❌ NÃO FAÇA ISSO
vim .kiro/prompt-logs/feature-compliance.md  # Editar manualmente

# ✅ FAÇA ISSO
# Deixe o sistema capturar automaticamente
# Os logs são gerenciados pelo hook
```

#### 6. **Sincronizar Logs Entre Branches**

Ao fazer merge de branches, os logs são preservados:

```bash
# Ao fazer merge de feature/compliance-score em develop
git checkout develop
git merge feature/compliance-score

# Os logs de feature-compliance-score.md permanecem em .kiro/prompt-logs/
# para referência futura
```

### 7. **Exemplos de Fluxo Completo**

#### Exemplo 1: Implementar Nova Feature

```bash
# 1. Criar branch
git checkout -b feature/upload-csv

# 2. Submeter prompts no Kiro (automático: logs são capturados)
# Prompt 1: "Criar endpoint POST /upload para receber CSV"
# Prompt 2: "Implementar validação de formato CSV"
# Prompt 3: "Adicionar testes unitários"

# 3. Verificar logs capturados
cat .kiro/prompt-logs/feature-upload-csv.md

# 4. Fazer commits
git add .
git commit -m "feat(api): implementa upload de CSV"
git add .kiro/prompt-logs/
git commit -m "docs: adiciona prompts de implementação"

# 5. Fazer push
git push -u origin feature/upload-csv

# 6. Abrir PR
# Revisor pode consultar .kiro/prompt-logs/feature-upload-csv.md
# para entender contexto

# 7. Após merge, logs permanecem versionados
```

#### Exemplo 2: Revisar Code Review com Logs

```bash
# 1. Você recebe PR para revisar
# Branch: feature/ml-prediction

# 2. Consultar logs da branch
cat .kiro/prompt-logs/feature-ml-prediction.md

# 3. Entender contexto
# - Quais prompts foram submetidos?
# - Quais requisitos foram solicitados?
# - Quais decisões foram tomadas?

# 4. Revisar código
# - Implementa o que foi solicitado?
# - Segue os padrões?
# - Atende aos requisitos?

# 5. Comentar na PR
# Referenciar logs em comentários

# 6. Após merge, logs permanecem para referência futura
```

#### Exemplo 3: Reutilizar Padrões de Features Anteriores

```bash
# 1. Você vai implementar feature/data-validation
# 2. Consultar logs de features similares
cat .kiro/prompt-logs/feature-data-cleaner.md
cat .kiro/prompt-logs/feature-csv-processor.md

# 3. Identificar padrões bem-sucedidos
# - Como foi estruturado o código?
# - Quais testes foram criados?
# - Quais decisões foram tomadas?

# 4. Reutilizar padrões na nova feature
# - Estrutura similar
# - Testes similares
# - Decisões consistentes

# 5. Submeter prompts baseados em padrões anteriores
# Prompt: "Implementar data-validation seguindo padrão de data-cleaner"
```

### 8. Troubleshooting de Uso

#### Problema 1: "Não consigo encontrar o arquivo de log"

**Solução:**
```bash
# Verificar branch atual
git branch

# Listar todos os arquivos de log
ls .kiro/prompt-logs/

# Verificar se o arquivo existe para sua branch
# Se não existir, submeta um prompt no Kiro para criar
```

#### Problema 2: "Arquivo de log está vazio"

**Solução:**
```bash
# Verificar se prompts foram capturados
cat .kiro/prompt-logs/<branch>.md

# Se vazio, submeta um prompt no Kiro
# O hook deve capturar automaticamente

# Se ainda vazio, verificar instalação:
python .kiro/scripts/log_prompt.py --test
```

#### Problema 3: "Não consigo buscar por palavra-chave"

**Solução:**
```bash
# Verificar sintaxe do comando grep
grep "palavra-chave" .kiro/prompt-logs/<branch>.md

# Usar -i para busca case-insensitive
grep -i "palavra-chave" .kiro/prompt-logs/<branch>.md

# Buscar em todos os logs
grep -r "palavra-chave" .kiro/prompt-logs/
```

#### Problema 4: "Logs não estão sendo sincronizados entre branches"

**Solução:**
```bash
# Logs são específicos por branch
# Cada branch tem seu próprio arquivo

# Para sincronizar logs ao fazer merge:
git checkout develop
git merge feature/minha-feature

# Logs de feature/minha-feature.md permanecem em .kiro/prompt-logs/
# Você pode consultar depois se necessário
```

---

**Versão**: 0.1.0  
**Data**: 27 de Maio de 2026  
**Status**: ✅ Instruções de Uso Completas


## Troubleshooting

### Problema 1: Logs não estão sendo criados

**Sintomas:**
- Submeto prompts no Kiro, mas nenhum arquivo de log é criado
- Diretório `.kiro/prompt-logs/` está vazio

**Causas Possíveis:**
1. Hook não está configurado corretamente
2. Script Python não tem permissões de execução
3. Diretório `.kiro/prompt-logs/` não existe
4. Biblioteca `pytz` não está instalada

**Solução:**

1. Verificar se o hook existe:
```bash
# Mac/Linux
ls -la .kiro/hooks/prompt-logger.json

# Windows
dir .kiro\hooks\prompt-logger.json
```

2. Verificar se o script existe:
```bash
# Mac/Linux
ls -la .kiro/scripts/log_prompt.py

# Windows
dir .kiro\scripts\log_prompt.py
```

3. Verificar se o diretório de logs existe:
```bash
# Mac/Linux
ls -la .kiro/prompt-logs/

# Windows
dir .kiro\prompt-logs\
```

Se não existir, criar manualmente:
```bash
# Mac/Linux
mkdir -p .kiro/prompt-logs

# Windows
mkdir .kiro\prompt-logs
```

4. Verificar se `pytz` está instalado:
```bash
python -c "import pytz; print('OK')"
```

Se não estiver, instalar:
```bash
pip install pytz
```

5. Testar manualmente:
```bash
python .kiro/scripts/log_prompt.py --test
```

### Problema 2: Conteúdo do prompt não está sendo capturado

**Sintomas:**
- Arquivo de log é criado, mas o campo "Prompt original" está vazio
- Apenas metadados (usuário, branch, timestamp) são registrados

**Causa:**
- Limitação conhecida do Kiro - nem sempre consegue expor o conteúdo completo do prompt via hooks

**Solução:**
- Metadados ainda são registrados (útil para rastreabilidade)
- Considerar captura manual se necessário
- Consultar a seção "Limitações Conhecidas" abaixo

### Problema 3: Timestamp está em horário incorreto

**Sintomas:**
- Timestamp registrado não corresponde ao horário de Brasília
- Diferença de horas no registro

**Causa:**
- Biblioteca `pytz` pode não estar configurada corretamente
- Timezone do sistema pode estar diferente

**Solução:**

1. Verificar se `pytz` está instalado corretamente:
```bash
python -c "import pytz; print(pytz.__version__)"
```

2. Testar conversão de timezone:
```bash
python -c "import pytz; from datetime import datetime; tz = pytz.timezone('America/Sao_Paulo'); print(datetime.now(tz))"
```

3. Se o timestamp ainda estiver incorreto, verificar se o script está usando `America/Sao_Paulo`:
```bash
# Mac/Linux
grep "America/Sao_Paulo" .kiro/scripts/log_prompt.py

# Windows
findstr "America/Sao_Paulo" .kiro\scripts\log_prompt.py
```

### Problema 4: Permissão negada ao executar script (Mac/Linux)

**Sintomas:**
- Erro: "Permission denied" ao tentar executar script
- Hook não consegue disparar o script

**Causa:**
- Script não tem permissões de execução

**Solução:**

```bash
# Conceder permissões de execução
chmod +x .kiro/scripts/log_prompt.py

# Verificar permissões
ls -la .kiro/scripts/log_prompt.py
# Deve mostrar 'x' na coluna de permissões: -rwxr-xr-x
```

### Problema 5: Git não consegue identificar a branch

**Sintomas:**
- Erro: "fatal: not a git repository"
- Arquivo de log não é criado

**Causa:**
- Repositório Git pode não estar inicializado
- Script não consegue acessar informações do Git

**Solução:**

1. Verificar se o repositório Git está inicializado:
```bash
git status
```

2. Verificar se você está em uma branch válida:
```bash
git branch
```

3. Se necessário, reinicializar o repositório:
```bash
git init
```

### Problema 6: Arquivo de log está corrompido

**Sintomas:**
- Erro ao abrir arquivo de log
- Conteúdo ilegível ou formatação quebrada

**Causa:**
- Arquivo pode ter sido editado manualmente
- Encoding pode estar incorreto

**Solução:**

1. Verificar encoding do arquivo:
```bash
# Mac/Linux
file .kiro/prompt-logs/<branch>.md

# Windows
# Abrir em editor e verificar encoding (deve ser UTF-8)
```

2. Se necessário, restaurar de backup:
```bash
# Verificar histórico Git
git log --oneline .kiro/prompt-logs/<branch>.md

# Restaurar versão anterior
git checkout HEAD~1 .kiro/prompt-logs/<branch>.md
```

3. Se arquivo estiver muito corrompido, deletar e recriar:
```bash
# Deletar arquivo corrompido
rm .kiro/prompt-logs/<branch>.md

# Submeter novo prompt no Kiro para recriar
```

---

## Limitações Conhecidas

### 1. Captura de Conteúdo

**Limitação:** Kiro pode não expor conteúdo completo do prompt via hooks em alguns casos.

**Impacto:** Arquivo de log pode conter apenas metadados (usuário, branch, timestamp) sem o conteúdo do prompt.

**Workaround:** Metadados ainda são úteis para rastreabilidade. Se necessário, adicionar conteúdo manualmente ou usar captura manual.

**Status:** Planejado para melhoria em fase futura.

### 2. Filtragem Automática

**Limitação:** Prompts triviais são automaticamente filtrados para manter logs limpos.

**Prompts filtrados:**
- Confirmações simples: "sim", "não", "ok", "yes", "no"
- Respostas muito curtas: < 10 caracteres
- Comandos de navegação: "next", "back", "continue"
- Prompts vazios

**Impacto:** Alguns prompts podem não ser registrados.

**Justificativa:** Manter logs focados em interações significativas.

**Status:** Comportamento esperado.

### 3. Sem Captura de Resultados (MVP)

**Limitação:** Apenas prompts são capturados, não respostas do agente.

**Impacto:** Logs contêm apenas o que foi solicitado, não o que foi gerado.

**Workaround:** Referenciar commits e PRs para ver resultados.

**Status:** Planejado para fase futura (hook `agentStop`).

### 4. Crescimento de Arquivos

**Limitação:** Arquivos de log crescem indefinidamente sem rotação automática.

**Impacto:** Arquivos podem ficar muito grandes após meses de desenvolvimento.

**Workaround:** Arquivamento manual ou compressão periódica.

**Status:** Planejado para fase futura (rotação de logs).

### 5. Sem Sincronização Entre Branches

**Limitação:** Logs são específicos por branch; não há sincronização automática ao fazer merge.

**Impacto:** Logs de feature branches não são mesclados em develop/main.

**Justificativa:** Manter histórico separado por contexto de desenvolvimento.

**Workaround:** Consultar logs de branches anteriores manualmente se necessário.

**Status:** Comportamento esperado.

### 6. Sem Criptografia de Logs

**Limitação:** Logs são armazenados em texto plano no repositório Git.

**Impacto:** Qualquer pessoa com acesso ao repositório pode ler os logs.

**Justificativa:** Logs contêm apenas prompts e metadados, sem dados sensíveis.

**Recomendação:** Não incluir senhas, tokens ou dados sensíveis em prompts.

**Status:** Comportamento esperado.

---

## Exemplos de Consulta de Logs

### Visão Geral

Esta seção fornece exemplos práticos e reais de como consultar logs de prompts para diferentes cenários de desenvolvimento. Use estes exemplos como referência para suas próprias consultas.

### 1. Consultas Básicas

#### Exemplo 1: Ver Todos os Prompts da Branch Atual

**Cenário:** Você quer revisar todos os prompts que foram submetidos na sua branch atual.

**Comando (Mac/Linux):**
```bash
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

**Comando (Windows PowerShell):**
```powershell
$branch = git rev-parse --abbrev-ref HEAD
Get-Content ".kiro\prompt-logs\$branch.md"
```

**Saída esperada:**
```markdown
## Prompt: Implementar endpoint de upload
- Responsável: seu-usuario
- Branch: feature-upload-csv
- Data/hora: 2026-05-27 14:35:22 (Brasília - UTC-3)

### Prompt original
```
Criar endpoint POST /api/v1/upload que:
1. Receba arquivo CSV
2. Valide formato
3. Retorne ID do batch
```

---

## Prompt: Adicionar validação de ranges
- Responsável: seu-usuario
- Branch: feature-upload-csv
- Data/hora: 2026-05-27 15:10:45 (Brasília - UTC-3)

### Prompt original
```
Implementar validação de ranges para sensores:
- Temperature: 20-45°C
- pH: 4.0-9.0
```
```

#### Exemplo 2: Ver Últimas 10 Entradas de Prompts

**Cenário:** Você quer ver apenas os prompts mais recentes da sua branch.

**Comando (Mac/Linux):**
```bash
tail -n 50 .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

**Comando (Windows PowerShell):**
```powershell
$branch = git rev-parse --abbrev-ref HEAD
Get-Content ".kiro\prompt-logs\$branch.md" -Tail 50
```

**Benefício:** Útil quando o arquivo de log é muito grande e você quer ver apenas o trabalho recente.

#### Exemplo 3: Contar Quantos Prompts Foram Submetidos

**Cenário:** Você quer saber quantos prompts foram submetidos na sua branch.

**Comando (Mac/Linux):**
```bash
grep -c "^## Prompt:" .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

**Comando (Windows PowerShell):**
```powershell
$branch = git rev-parse --abbrev-ref HEAD
(Select-String -Path ".kiro\prompt-logs\$branch.md" -Pattern "^## Prompt:" | Measure-Object).Count
```

**Exemplo de saída:**
```
15
```

**Interpretação:** 15 prompts foram submetidos nesta branch.

### 2. Buscas por Palavra-Chave

#### Exemplo 1: Buscar Prompts sobre "Compliance"

**Cenário:** Você quer encontrar todos os prompts relacionados a compliance score.

**Comando (Mac/Linux):**
```bash
grep -i "compliance" .kiro/prompt-logs/*.md
```

**Comando (Windows PowerShell):**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "compliance" -CaseSensitive:$false
```

**Saída esperada:**
```
.kiro/prompt-logs/feature-compliance-score.md:## Prompt: Implementar compliance score engine
.kiro/prompt-logs/feature-compliance-score.md:Cálculo de Manufacturing Compliance Score com regras determinísticas
.kiro/prompt-logs/feature-compliance-score.md:Validação de compliance com ranges de sensores
```

#### Exemplo 2: Buscar Prompts sobre "Teste" ou "Test"

**Cenário:** Você quer encontrar todos os prompts relacionados a testes.

**Comando (Mac/Linux):**
```bash
grep -i "test\|teste" .kiro/prompt-logs/*.md
```

**Comando (Windows PowerShell):**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "test|teste" -CaseSensitive:$false
```

**Saída esperada:**
```
.kiro/prompt-logs/feature-upload-csv.md:## Prompt: Adicionar testes unitários
.kiro/prompt-logs/feature-ml-prediction.md:## Prompt: Criar testes para RandomForest
.kiro/prompt-logs/feature-compliance-score.md:## Prompt: Testes de compliance score
```

#### Exemplo 3: Buscar Prompts de um Usuário Específico

**Cenário:** Você quer ver todos os prompts submetidos por um desenvolvedor específico.

**Comando (Mac/Linux):**
```bash
grep -r "Responsável: seu-usuario" .kiro/prompt-logs/
```

**Comando (Windows PowerShell):**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "Responsável: seu-usuario"
```

**Saída esperada:**
```
.kiro/prompt-logs/feature-upload-csv.md:- Responsável: seu-usuario
.kiro/prompt-logs/feature-compliance-score.md:- Responsável: seu-usuario
.kiro/prompt-logs/feature-ml-prediction.md:- Responsável: seu-usuario
```

#### Exemplo 4: Buscar Prompts por Data

**Cenário:** Você quer encontrar todos os prompts submetidos em um dia específico.

**Comando (Mac/Linux):**
```bash
grep "2026-05-27" .kiro/prompt-logs/*.md
```

**Comando (Windows PowerShell):**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "2026-05-27"
```

**Saída esperada:**
```
.kiro/prompt-logs/feature-upload-csv.md:- Data/hora: 2026-05-27 14:35:22 (Brasília - UTC-3)
.kiro/prompt-logs/feature-upload-csv.md:- Data/hora: 2026-05-27 15:10:45 (Brasília - UTC-3)
.kiro/prompt-logs/feature-compliance-score.md:- Data/hora: 2026-05-27 16:20:30 (Brasília - UTC-3)
```

### 3. Padrões de Busca Avançados

#### Exemplo 1: Buscar Prompts com Contexto (5 linhas antes e depois)

**Cenário:** Você quer ver um prompt específico com contexto completo.

**Comando (Mac/Linux):**
```bash
grep -B 5 -A 5 "RandomForest" .kiro/prompt-logs/feature-ml-prediction.md
```

**Comando (Windows PowerShell):**
```powershell
Select-String -Path ".kiro\prompt-logs\feature-ml-prediction.md" -Pattern "RandomForest" -Context 5,5
```

**Saída esperada:**
```
- Data/hora: 2026-05-27 14:35:22 (Brasília - UTC-3)

### Prompt original
```
Implementar RandomForestClassifier com features:
- Temperature
- pH
- Dissolved Oxygen
- Pressure
- Agitator Speed
```

---
```

#### Exemplo 2: Buscar Prompts que Contêm Múltiplas Palavras

**Cenário:** Você quer encontrar prompts que mencionam tanto "teste" quanto "compliance".

**Comando (Mac/Linux):**
```bash
grep -l "teste" .kiro/prompt-logs/*.md | xargs grep "compliance"
```

**Comando (Windows PowerShell):**
```powershell
$files = Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "teste" | Select-Object -ExpandProperty Path -Unique
Select-String -Path $files -Pattern "compliance"
```

#### Exemplo 3: Buscar Prompts Excluindo Certos Termos

**Cenário:** Você quer encontrar prompts sobre "feature" mas excluir prompts sobre "bugfix".

**Comando (Mac/Linux):**
```bash
grep "feature" .kiro/prompt-logs/*.md | grep -v "bugfix"
```

**Comando (Windows PowerShell):**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "feature" | Where-Object { $_ -notmatch "bugfix" }
```

### 4. Comparação Entre Branches

#### Exemplo 1: Comparar Prompts de Duas Features

**Cenário:** Você quer comparar como duas features similares foram desenvolvidas.

**Comando (Mac/Linux):**
```bash
echo "=== Feature 1: Upload CSV ===" && \
cat .kiro/prompt-logs/feature-upload-csv.md && \
echo -e "\n=== Feature 2: Data Validation ===" && \
cat .kiro/prompt-logs/feature-data-validation.md
```

**Comando (Windows PowerShell):**
```powershell
Write-Host "=== Feature 1: Upload CSV ===" -ForegroundColor Green
Get-Content ".kiro\prompt-logs\feature-upload-csv.md"
Write-Host "`n=== Feature 2: Data Validation ===" -ForegroundColor Green
Get-Content ".kiro\prompt-logs\feature-data-validation.md"
```

**Benefício:** Identificar padrões e reutilizar abordagens bem-sucedidas.

#### Exemplo 2: Listar Todas as Branches com Logs

**Cenário:** Você quer ver todas as branches que têm logs registrados.

**Comando (Mac/Linux):**
```bash
ls -1 .kiro/prompt-logs/ | sed 's/\.md$//'
```

**Comando (Windows PowerShell):**
```powershell
Get-ChildItem ".kiro\prompt-logs\" -Filter "*.md" | ForEach-Object { $_.BaseName }
```

**Saída esperada:**
```
main
develop
feature-upload-csv
feature-compliance-score
feature-ml-prediction
bugfix-validation-error
```

### 5. Análise de Padrões

#### Exemplo 1: Encontrar Prompts Mais Frequentes

**Cenário:** Você quer identificar quais tipos de prompts são mais comuns.

**Comando (Mac/Linux):**
```bash
grep "^## Prompt:" .kiro/prompt-logs/*.md | cut -d: -f3- | sort | uniq -c | sort -rn
```

**Saída esperada:**
```
      3 Implementar testes unitários
      2 Criar endpoint API
      2 Adicionar validação
      1 Implementar compliance score
```

**Interpretação:** Testes unitários são o tipo de prompt mais frequente (3 vezes).

#### Exemplo 2: Contar Prompts por Branch

**Cenário:** Você quer saber qual branch teve mais prompts.

**Comando (Mac/Linux):**
```bash
for file in .kiro/prompt-logs/*.md; do
  count=$(grep -c "^## Prompt:" "$file" 2>/dev/null || echo 0)
  branch=$(basename "$file" .md)
  echo "$count prompts em $branch"
done | sort -rn
```

**Saída esperada:**
```
15 prompts em feature-ml-prediction
12 prompts em feature-compliance-score
10 prompts em feature-upload-csv
8 prompts em feature-data-validation
```

### 6. Integração com Ferramentas

#### Exemplo 1: Exportar Logs para Arquivo de Texto

**Cenário:** Você quer exportar logs para compartilhar com o time.

**Comando (Mac/Linux):**
```bash
cat .kiro/prompt-logs/feature-compliance-score.md > relatorio-prompts.txt
```

**Comando (Windows PowerShell):**
```powershell
Get-Content ".kiro\prompt-logs\feature-compliance-score.md" | Out-File "relatorio-prompts.txt"
```

#### Exemplo 2: Gerar Relatório de Prompts por Data

**Cenário:** Você quer gerar um relatório de prompts agrupados por data.

**Comando (Mac/Linux):**
```bash
grep "Data/hora:" .kiro/prompt-logs/*.md | cut -d: -f3- | sort | uniq -c
```

**Saída esperada:**
```
      3 2026-05-27 14:35:22 (Brasília - UTC-3)
      2 2026-05-27 15:10:45 (Brasília - UTC-3)
      1 2026-05-27 16:20:30 (Brasília - UTC-3)
```

### 7. Dicas e Truques

#### Dica 1: Criar Alias para Comandos Frequentes

**Mac/Linux (.bashrc ou .zshrc):**
```bash
# Ver logs da branch atual
alias logs-current='cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md'

# Ver últimas 20 linhas
alias logs-recent='tail -n 20 .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md'

# Buscar em todos os logs
alias logs-search='grep -r -i'
```

**Uso:**
```bash
logs-current                    # Ver logs da branch atual
logs-recent                     # Ver últimas 20 linhas
logs-search "compliance" .kiro/prompt-logs/  # Buscar "compliance"
```

#### Dica 2: Usar Grep com Cores

**Mac/Linux:**
```bash
grep --color=auto "palavra-chave" .kiro/prompt-logs/*.md
```

**Benefício:** Destaca a palavra-chave encontrada em vermelho.

#### Dica 3: Contar Linhas de Prompts

**Cenário:** Você quer saber quantas linhas de prompts foram submetidas.

**Comando (Mac/Linux):**
```bash
wc -l .kiro/prompt-logs/*.md
```

**Saída esperada:**
```
     150 .kiro/prompt-logs/feature-upload-csv.md
     200 .kiro/prompt-logs/feature-compliance-score.md
     180 .kiro/prompt-logs/feature-ml-prediction.md
     530 total
```

---

**Versão**: 0.1.0  
**Data**: 27 de Maio de 2026  
**Status**: ✅ Exemplos de Consulta Documentados


## Troubleshooting

### Visão Geral

Esta seção fornece soluções para problemas comuns encontrados ao usar o sistema de prompt logging. Se você encontrar um problema não listado aqui, consulte a seção "Quando Contatar Suporte" no final.

### Categoria 1: Problemas de Captura de Prompts

#### Problema 1.1: Prompts Não Estão Sendo Capturados

**Sintomas:**
- Você submete prompts no Kiro, mas nada aparece em `.kiro/prompt-logs/`
- O arquivo de log não é criado ou permanece vazio

**Causas Possíveis:**
1. Hook não está configurado corretamente
2. Script Python não tem permissões de execução
3. Diretório `.kiro/prompt-logs/` não existe
4. Dependência `pytz` não está instalada

**Solução Passo a Passo:**

**Passo 1: Verificar se o Hook Existe**
```bash
# Mac/Linux
ls -la .kiro/hooks/prompt-logger.json

# Windows
dir .kiro\hooks\prompt-logger.json
```

Se o arquivo não existir, consulte a seção "Instruções de Instalação".

**Passo 2: Verificar Configuração do Hook**
```bash
# Mac/Linux
cat .kiro/hooks/prompt-logger.json

# Windows
type .kiro\hooks\prompt-logger.json
```

Deve conter:
```json
{
  "name": "Prompt Logger",
  "when": { "type": "promptSubmit" },
  "then": { "type": "runCommand", "command": "python .kiro/scripts/log_prompt.py" }
}
```

**Passo 3: Verificar Permissões do Script**
```bash
# Mac/Linux
ls -la .kiro/scripts/log_prompt.py
# Deve mostrar 'x' na coluna de permissões

# Se não tiver, conceder permissão:
chmod +x .kiro/scripts/log_prompt.py
```

**Passo 4: Verificar Diretório de Logs**
```bash
# Mac/Linux
ls -la .kiro/prompt-logs/

# Windows
dir .kiro\prompt-logs\
```

Se não existir, criar:
```bash
# Mac/Linux
mkdir -p .kiro/prompt-logs

# Windows
mkdir .kiro\prompt-logs
```

**Passo 5: Verificar Dependência pytz**
```bash
python -c "import pytz; print('OK')"
```

Se retornar erro, instalar:
```bash
pip install pytz
```

**Passo 6: Testar Manualmente**
```bash
python .kiro/scripts/log_prompt.py --test
```

Verificar se arquivo foi criado:
```bash
# Mac/Linux
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md

# Windows
type .kiro\prompt-logs\<branch-atual>.md
```

#### Problema 1.2: Apenas Alguns Prompts São Capturados

**Sintomas:**
- Alguns prompts aparecem nos logs, mas outros não
- Prompts curtos ou simples não são registrados

**Causa:**
O sistema filtra automaticamente prompts triviais (< 10 caracteres, confirmações simples, etc.)

**Solução:**
Isso é comportamento esperado. O sistema prioriza qualidade sobre quantidade. Se você precisa registrar um prompt trivial, considere:

1. Combinar com outro prompt mais significativo
2. Adicionar contexto ao prompt
3. Registrar manualmente em `.kiro/prompt-logs/` se necessário

**Exemplo:**
```
❌ Prompt trivial (não será capturado):
"sim"
"ok"
"próximo"

✅ Prompt significativo (será capturado):
"Implementar validação de ranges para sensores"
"Criar testes unitários para compliance score"
```

#### Problema 1.3: Conteúdo do Prompt Não Está Sendo Capturado

**Sintomas:**
- Arquivo de log é criado, mas contém apenas metadados (usuário, branch, data)
- Campo "Prompt original" está vazio

**Causa:**
Limitação conhecida do Kiro - nem sempre consegue expor o conteúdo completo do prompt via hooks.

**Solução:**
1. Metadados ainda são registrados (útil para rastreabilidade)
2. Se necessário, adicionar conteúdo manualmente:
   ```bash
   # Editar arquivo de log
   vim .kiro/prompt-logs/<branch>.md
   ```
3. Considerar captura manual para prompts críticos

**Workaround:**
Incluir resumo do prompt no commit:
```bash
git commit -m "feat: implementa compliance score

Baseado em prompt: 'Implementar Manufacturing Compliance Score com regras determinísticas'
Referência: .kiro/prompt-logs/feature-compliance-score.md"
```

### Categoria 2: Problemas de Acesso e Visualização

#### Problema 2.1: Não Consigo Encontrar o Arquivo de Log

**Sintomas:**
- Você procura por `.kiro/prompt-logs/<branch>.md` mas o arquivo não existe
- Comando `cat` ou `type` retorna "arquivo não encontrado"

**Causa:**
O arquivo de log é criado apenas quando o primeiro prompt é capturado. Se nenhum prompt foi capturado, o arquivo não existe.

**Solução:**

**Passo 1: Verificar Branch Atual**
```bash
git branch
# Deve mostrar a branch atual com asterisco (*)
```

**Passo 2: Listar Todos os Arquivos de Log**
```bash
# Mac/Linux
ls -la .kiro/prompt-logs/

# Windows
dir .kiro\prompt-logs\
```

**Passo 3: Se o Arquivo Não Existir**
Submeta um prompt no Kiro para criar o arquivo:
```bash
# Abrir Kiro e submeter um prompt
# O arquivo será criado automaticamente
```

**Passo 4: Verificar Nome da Branch**
Nomes de branches com `/` são convertidos para `-`:
```
feature/compliance-score → feature-compliance-score.md
bugfix/validation-error → bugfix-validation-error.md
```

#### Problema 2.2: Permissão Negada ao Acessar Arquivo

**Sintomas:**
- Erro: "Permission denied" ao tentar ler arquivo
- Não consegue abrir arquivo de log

**Causa:**
Permissões de arquivo incorretas (geralmente em Mac/Linux).

**Solução:**

**Mac/Linux:**
```bash
# Conceder permissão de leitura
chmod 644 .kiro/prompt-logs/*.md

# Ou conceder permissão recursiva
chmod -R 755 .kiro/prompt-logs/
```

**Windows:**
Geralmente não há problema de permissões. Se persistir:
1. Verificar se arquivo está aberto em outro programa
2. Fechar arquivo e tentar novamente
3. Reiniciar terminal/PowerShell

#### Problema 2.3: Arquivo de Log Muito Grande

**Sintomas:**
- Arquivo de log tem centenas de MB
- Demora muito para abrir ou buscar

**Causa:**
Arquivo cresceu indefinidamente (limitação conhecida do MVP).

**Solução:**

**Opção 1: Ver Apenas Últimas Entradas**
```bash
# Mac/Linux
tail -n 100 .kiro/prompt-logs/<branch>.md

# Windows
Get-Content ".kiro\prompt-logs\<branch>.md" -Tail 100
```

**Opção 2: Dividir Arquivo em Partes**
```bash
# Mac/Linux
split -l 1000 .kiro/prompt-logs/<branch>.md .kiro/prompt-logs/<branch>-part-

# Windows (PowerShell)
$content = Get-Content ".kiro\prompt-logs\<branch>.md"
$content | Select-Object -First 1000 | Out-File ".kiro\prompt-logs\<branch>-part-1.md"
```

**Opção 3: Arquivar Arquivo Antigo**
```bash
# Mac/Linux
mv .kiro/prompt-logs/<branch>.md .kiro/prompt-logs/<branch>-archive-$(date +%Y%m%d).md

# Windows
Move-Item ".kiro\prompt-logs\<branch>.md" ".kiro\prompt-logs\<branch>-archive-$(Get-Date -Format yyyyMMdd).md"
```

### Categoria 3: Problemas de Busca

#### Problema 3.1: Busca Não Retorna Resultados

**Sintomas:**
- Você busca por uma palavra-chave, mas `grep` retorna nada
- Tem certeza de que a palavra existe no arquivo

**Causa:**
Possíveis causas:
1. Diferença de maiúsculas/minúsculas
2. Sintaxe de regex incorreta
3. Arquivo vazio ou não existe

**Solução:**

**Passo 1: Usar Busca Case-Insensitive**
```bash
# Mac/Linux
grep -i "palavra-chave" .kiro/prompt-logs/*.md

# Windows
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "palavra-chave" -CaseSensitive:$false
```

**Passo 2: Verificar Sintaxe de Regex**
```bash
# Teste simples (sem regex)
grep "compliance" .kiro/prompt-logs/*.md

# Com regex (escape caracteres especiais)
grep "compliance\|score" .kiro/prompt-logs/*.md
```

**Passo 3: Verificar se Arquivo Existe**
```bash
# Mac/Linux
ls -la .kiro/prompt-logs/<branch>.md

# Windows
dir .kiro\prompt-logs\<branch>.md
```

#### Problema 3.2: Busca Retorna Muitos Resultados

**Sintomas:**
- Busca por palavra-chave retorna centenas de linhas
- Difícil encontrar o resultado específico

**Solução:**

**Opção 1: Refinar Busca**
```bash
# Buscar com contexto
grep -B 2 -A 2 "palavra-chave" .kiro/prompt-logs/*.md

# Buscar apenas títulos de prompts
grep "^## Prompt:.*palavra-chave" .kiro/prompt-logs/*.md
```

**Opção 2: Combinar Múltiplas Buscas**
```bash
# Mac/Linux
grep "compliance" .kiro/prompt-logs/*.md | grep "teste"

# Windows
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "compliance" | Select-String -Pattern "teste"
```

**Opção 3: Limitar a Uma Branch**
```bash
# Mac/Linux
grep "palavra-chave" .kiro/prompt-logs/feature-compliance-score.md

# Windows
Select-String -Path ".kiro\prompt-logs\feature-compliance-score.md" -Pattern "palavra-chave"
```

### Categoria 4: Problemas de Sincronização Git

#### Problema 4.1: Logs Não Estão Sendo Versionados

**Sintomas:**
- Você fez commits, mas `.kiro/prompt-logs/` não aparece no Git
- `git status` não mostra arquivos de log

**Causa:**
Arquivos podem estar em `.gitignore` ou não foram adicionados ao staging.

**Solução:**

**Passo 1: Verificar .gitignore**
```bash
# Mac/Linux
cat .gitignore | grep prompt-logs

# Windows
type .gitignore | findstr prompt-logs
```

Se `.kiro/prompt-logs/` está em `.gitignore`, remover:
```bash
# Editar .gitignore e remover a linha
vim .gitignore  # Mac/Linux
notepad .gitignore  # Windows
```

**Passo 2: Adicionar Arquivos ao Git**
```bash
git add .kiro/prompt-logs/
git status  # Verificar se arquivos aparecem
git commit -m "docs: adiciona prompts de desenvolvimento"
```

**Passo 3: Fazer Push**
```bash
git push
```

#### Problema 4.2: Conflitos de Merge em Arquivos de Log

**Sintomas:**
- Ao fazer merge, Git reporta conflito em `.kiro/prompt-logs/<branch>.md`
- Arquivo tem marcadores de conflito (`<<<<<<<`, `=======`, `>>>>>>>`)

**Causa:**
Duas branches modificaram o mesmo arquivo de log.

**Solução:**

**Opção 1: Manter Ambas as Versões**
```bash
# Abrir arquivo e remover marcadores de conflito
# Manter ambas as seções de prompts
vim .kiro/prompt-logs/<branch>.md

# Depois:
git add .kiro/prompt-logs/<branch>.md
git commit -m "merge: resolve conflito em logs de prompts"
```

**Opção 2: Manter Versão Local**
```bash
git checkout --ours .kiro/prompt-logs/<branch>.md
git add .kiro/prompt-logs/<branch>.md
git commit -m "merge: mantém logs locais"
```

**Opção 3: Manter Versão Remota**
```bash
git checkout --theirs .kiro/prompt-logs/<branch>.md
git add .kiro/prompt-logs/<branch>.md
git commit -m "merge: mantém logs remotos"
```

### Categoria 5: Problemas de Performance

#### Problema 5.1: Busca Muito Lenta

**Sintomas:**
- Comando `grep` demora muito para retornar
- Sistema fica travado durante busca

**Causa:**
Arquivo de log muito grande ou muitos arquivos para buscar.

**Solução:**

**Opção 1: Buscar em Uma Branch Específica**
```bash
# Ao invés de buscar em todos:
grep "palavra-chave" .kiro/prompt-logs/feature-compliance-score.md

# Ao invés de:
grep -r "palavra-chave" .kiro/prompt-logs/
```

**Opção 2: Usar Ferramentas Mais Rápidas**
```bash
# Mac/Linux: usar 'ag' (The Silver Searcher) se disponível
ag "palavra-chave" .kiro/prompt-logs/

# Ou usar 'rg' (ripgrep)
rg "palavra-chave" .kiro/prompt-logs/
```

**Opção 3: Limitar Resultados**
```bash
# Mac/Linux
grep "palavra-chave" .kiro/prompt-logs/*.md | head -20

# Windows
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "palavra-chave" | Select-Object -First 20
```

#### Problema 5.2: Arquivo de Log Demora para Abrir

**Sintomas:**
- Editor de texto demora muito para abrir arquivo
- Sistema fica lento ao editar arquivo

**Causa:**
Arquivo muito grande (centenas de MB).

**Solução:**

**Opção 1: Usar Editor Leve**
```bash
# Mac/Linux
nano .kiro/prompt-logs/<branch>.md  # Mais rápido que vim

# Windows
notepad .kiro\prompt-logs\<branch>.md  # Mais rápido que VS Code
```

**Opção 2: Ver Apenas Parte do Arquivo**
```bash
# Mac/Linux
head -n 100 .kiro/prompt-logs/<branch>.md  # Primeiras 100 linhas
tail -n 100 .kiro/prompt-logs/<branch>.md  # Últimas 100 linhas

# Windows
Get-Content ".kiro\prompt-logs\<branch>.md" -Head 100
Get-Content ".kiro\prompt-logs\<branch>.md" -Tail 100
```

**Opção 3: Dividir Arquivo**
```bash
# Mac/Linux
split -l 5000 .kiro/prompt-logs/<branch>.md .kiro/prompt-logs/<branch>-

# Windows
$content = Get-Content ".kiro\prompt-logs\<branch>.md"
$content | Select-Object -First 5000 | Out-File ".kiro\prompt-logs\<branch>-part1.md"
```

### Categoria 6: Problemas de Configuração

#### Problema 6.1: Timezone Incorreto

**Sintomas:**
- Timestamps nos logs estão em horário incorreto
- Esperava Brasília (UTC-3), mas mostra outro horário

**Causa:**
Configuração de timezone incorreta no script ou sistema.

**Solução:**

**Passo 1: Verificar Timezone do Sistema**
```bash
# Mac/Linux
date
# Deve mostrar horário de Brasília

# Windows
Get-Date
# Deve mostrar horário de Brasília
```

**Passo 2: Verificar Configuração do Script**
```bash
# Mac/Linux
grep "America/Sao_Paulo" .kiro/scripts/log_prompt.py

# Windows
Select-String -Path ".kiro\scripts\log_prompt.py" -Pattern "America/Sao_Paulo"
```

**Passo 3: Testar Timezone**
```bash
python -c "import pytz; from datetime import datetime; tz = pytz.timezone('America/Sao_Paulo'); print(datetime.now(tz))"
```

Se retornar horário incorreto, verificar configuração do sistema.

#### Problema 6.2: Usuário Git Incorreto

**Sintomas:**
- Campo "Responsável" mostra usuário incorreto
- Esperava seu nome, mas mostra outro

**Causa:**
Configuração de usuário Git incorreta.

**Solução:**

**Passo 1: Verificar Configuração Git**
```bash
git config user.name
git config user.email
```

**Passo 2: Atualizar Configuração (se necessário)**
```bash
# Local (apenas este repositório)
git config user.name "Seu Nome"
git config user.email "seu.email@example.com"

# Global (todos os repositórios)
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"
```

**Passo 3: Verificar Novamente**
```bash
git config user.name
# Deve mostrar seu nome
```

### Quando Contatar Suporte

Se você encontrou um problema não listado acima, ou a solução não funcionou, considere:

1. **Verificar Logs de Erro do Kiro**
   - Windows: `%APPDATA%\Kiro\logs\`
   - Mac/Linux: `~/.kiro/logs/`

2. **Executar Teste Diagnóstico**
   ```bash
   python .kiro/scripts/log_prompt.py --check
   ```

3. **Coletar Informações**
   - Versão do Python: `python --version`
   - Versão do Git: `git --version`
   - Branch atual: `git branch`
   - Conteúdo de `.kiro/hooks/prompt-logger.json`
   - Últimas linhas de `.kiro/prompt-logs/<branch>.md`

4. **Documentar o Problema**
   - Descrever o que você tentou fazer
   - Descrever o erro ou comportamento inesperado
   - Incluir comandos executados e saída
   - Incluir informações coletadas acima

5. **Abrir Issue no GitHub**
   - Ir para: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/issues
   - Selecionar template "Bug Report"
   - Preencher com informações coletadas

---

**Versão**: 0.1.0  
**Data**: 27 de Maio de 2026  
**Status**: ✅ Troubleshooting Completo


## Limitações Conhecidas

### Visão Geral

Esta seção documenta as limitações conhecidas do sistema de prompt logging no MVP (Minimum Viable Product). Estas limitações são aceitáveis para a fase atual e serão abordadas em versões futuras.

### Limitação 1: Captura de Conteúdo do Prompt

**Descrição:**
O Kiro nem sempre consegue expor o conteúdo completo do prompt através dos hooks. Em alguns casos, apenas metadados (usuário, branch, timestamp) são capturados, enquanto o conteúdo do prompt fica vazio.

**Impacto:**
- Arquivo de log criado, mas campo "Prompt original" vazio
- Rastreabilidade de metadados preservada
- Conteúdo do prompt não documentado automaticamente

**Causa:**
Limitação técnica da API de hooks do Kiro - nem sempre consegue acessar o conteúdo completo do prompt submetido.

**Workaround:**

**Opção 1: Adicionar Manualmente**
```bash
# Editar arquivo de log e adicionar conteúdo
vim .kiro/prompt-logs/<branch>.md
```

**Opção 2: Documentar em Commit**
```bash
git commit -m "feat: implementa compliance score

Baseado em prompt: 'Implementar Manufacturing Compliance Score com regras determinísticas'
Referência: .kiro/prompt-logs/feature-compliance-score.md"
```

**Opção 3: Usar Comentários no Código**
```python
# Prompt: Implementar cálculo de compliance score com regras determinísticas
# Referência: .kiro/prompt-logs/feature-compliance-score.md
def calculate_compliance_score(sensor_data):
    """Calcula Manufacturing Compliance Score."""
    pass
```

**Quando Será Resolvido:**
Fase 2 - Melhorias de Captura (planejado para futuro)

---

### Limitação 2: Filtragem de Prompts Triviais

**Descrição:**
O sistema filtra automaticamente prompts triviais (muito curtos, confirmações simples, comandos de navegação) para manter logs limpos e focados em interações significativas.

**Prompts Filtrados:**
- Confirmações: "sim", "não", "ok", "yes", "no"
- Muito curtos: < 10 caracteres
- Comandos de navegação: "next", "back", "continue", "próximo", "voltar"
- Sem conteúdo capturado

**Impacto:**
- Alguns prompts não são registrados
- Logs contêm apenas interações significativas
- Reduz ruído, mas pode perder contexto em alguns casos

**Exemplo:**
```
❌ Não será capturado:
"sim"
"ok"
"próximo"
"continue"

✅ Será capturado:
"Implementar validação de ranges"
"Criar testes unitários"
"Adicionar tratamento de erros"
```

**Workaround:**

Se você precisa registrar um prompt trivial:

**Opção 1: Combinar com Contexto**
```
❌ Trivial:
"sim"

✅ Com contexto:
"Sim, implementar conforme sugerido. Usar RandomForest com 5 features."
```

**Opção 2: Registrar Manualmente**
```bash
# Editar arquivo de log e adicionar entrada manualmente
vim .kiro/prompt-logs/<branch>.md
```

**Opção 3: Documentar em Commit**
```bash
git commit -m "feat: implementa feature X

Confirmação de prompt trivial: 'sim'
Referência: .kiro/prompt-logs/feature-x.md"
```

**Quando Será Resolvido:**
Fase 2 - Configuração de Filtros (planejado para futuro)

---

### Limitação 3: Sem Captura de Resposta do Agente

**Descrição:**
O sistema captura apenas os prompts submetidos pelo desenvolvedor. As respostas do agente (código gerado, sugestões, etc.) não são capturadas automaticamente.

**Impacto:**
- Logs contêm apenas prompts, não respostas
- Não há rastreabilidade automática do código gerado
- Necessário documentar manualmente se necessário

**Exemplo:**
```
Capturado:
- Prompt: "Implementar RandomForestClassifier"

Não capturado:
- Resposta do agente (código gerado)
- Sugestões do agente
- Explicações do agente
```

**Workaround:**

**Opção 1: Documentar em Commit**
```bash
git commit -m "feat(ml): implementa RandomForestClassifier

Prompt: 'Implementar RandomForestClassifier com features: Temperature, pH, ...'
Resposta: Código gerado com 150 linhas, incluindo testes
Referência: .kiro/prompt-logs/feature-ml-prediction.md"
```

**Opção 2: Adicionar Comentário no Código**
```python
# Gerado por Kiro baseado em prompt:
# "Implementar RandomForestClassifier com features: Temperature, pH, Dissolved Oxygen, Pressure, Agitator Speed"
# Referência: .kiro/prompt-logs/feature-ml-prediction.md
class MLPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
```

**Opção 3: Criar Documento Separado**
```bash
# Criar arquivo de documentação com prompts e respostas
cat > docs/ai-interactions/feature-ml-prediction.md << EOF
# Interações de IA - Feature ML Prediction

## Prompt 1: Implementar RandomForestClassifier
**Data:** 2026-05-27 14:35:22
**Referência:** .kiro/prompt-logs/feature-ml-prediction.md

### Prompt Original
Implementar RandomForestClassifier com features: Temperature, pH, Dissolved Oxygen, Pressure, Agitator Speed

### Resposta do Agente
[Código gerado aqui]

### Resultado
Modelo treinado com acurácia de 85%
EOF
```

**Quando Será Resolvido:**
Fase 2 - Captura de Respostas (planejado para futuro)

---

### Limitação 4: Crescimento Indefinido de Arquivos

**Descrição:**
Arquivos de log crescem indefinidamente sem rotação ou arquivamento automático. Após meses de desenvolvimento, um arquivo pode ter centenas de MB.

**Impacto:**
- Arquivo de log fica muito grande
- Demora para abrir ou buscar
- Consome espaço em disco
- Performance degradada

**Exemplo:**
```
Após 1 mês:   ~5 MB
Após 3 meses: ~15 MB
Após 6 meses: ~30 MB
Após 1 ano:   ~60 MB
```

**Workaround:**

**Opção 1: Dividir Arquivo Manualmente**
```bash
# Mac/Linux
split -l 5000 .kiro/prompt-logs/develop.md .kiro/prompt-logs/develop-archive-

# Windows
$content = Get-Content ".kiro\prompt-logs\develop.md"
$content | Select-Object -First 5000 | Out-File ".kiro\prompt-logs\develop-archive-2026-05.md"
```

**Opção 2: Arquivar Arquivo Antigo**
```bash
# Mac/Linux
mv .kiro/prompt-logs/develop.md .kiro/prompt-logs/develop-archive-$(date +%Y%m%d).md
touch .kiro/prompt-logs/develop.md

# Windows
Move-Item ".kiro\prompt-logs\develop.md" ".kiro\prompt-logs\develop-archive-$(Get-Date -Format yyyyMMdd).md"
New-Item ".kiro\prompt-logs\develop.md" -ItemType File
```

**Opção 3: Usar Compressão**
```bash
# Mac/Linux
gzip .kiro/prompt-logs/develop.md
# Resultado: develop.md.gz

# Windows (PowerShell)
Compress-Archive -Path ".kiro\prompt-logs\develop.md" -DestinationPath ".kiro\prompt-logs\develop.zip"
```

**Opção 4: Limpar Periodicamente**
```bash
# Manter apenas últimas 1000 linhas
# Mac/Linux
tail -n 1000 .kiro/prompt-logs/develop.md > .kiro/prompt-logs/develop-temp.md
mv .kiro/prompt-logs/develop-temp.md .kiro/prompt-logs/develop.md

# Windows
$content = Get-Content ".kiro\prompt-logs\develop.md"
$content | Select-Object -Last 1000 | Out-File ".kiro\prompt-logs\develop.md"
```

**Quando Será Resolvido:**
Fase 4 - Rotação e Arquivamento (planejado para futuro)

---

### Limitação 5: Sem Interface de Consulta

**Descrição:**
Não existe interface gráfica ou CLI para consultar logs. Você precisa usar comandos de terminal (`grep`, `cat`, etc.) para buscar e visualizar.

**Impacto:**
- Requer conhecimento de terminal/PowerShell
- Buscas complexas precisam de regex
- Não há interface amigável para não-técnicos

**Exemplo:**
```
❌ Sem interface:
Precisa usar: grep -r "compliance" .kiro/prompt-logs/

✅ Com interface (futuro):
Clique em "Buscar" → Digite "compliance" → Veja resultados
```

**Workaround:**

**Opção 1: Criar Scripts Auxiliares**
```bash
# Mac/Linux: criar arquivo ~/bin/logs-search
#!/bin/bash
grep -r -i "$1" .kiro/prompt-logs/

# Uso:
logs-search "compliance"
```

**Opção 2: Usar Aliases**
```bash
# Adicionar ao ~/.bashrc ou ~/.zshrc
alias logs-search='grep -r -i'
alias logs-current='cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md'

# Uso:
logs-search "compliance" .kiro/prompt-logs/
logs-current
```

**Opção 3: Usar Ferramentas Existentes**
```bash
# VS Code: abrir pasta .kiro/prompt-logs/ e usar busca integrada
code .kiro/prompt-logs/

# Sublime Text: abrir pasta e usar busca
subl .kiro/prompt-logs/
```

**Quando Será Resolvido:**
Fase 3 - Interface de Consulta (planejado para futuro)

---

### Limitação 6: Sem Sincronização Entre Máquinas

**Descrição:**
Logs são armazenados localmente em `.kiro/prompt-logs/`. Se você trabalha em múltiplas máquinas, precisa fazer push/pull manualmente via Git.

**Impacto:**
- Logs não sincronizam automaticamente
- Necessário fazer commit e push para compartilhar
- Possíveis conflitos ao trabalhar em múltiplas máquinas

**Exemplo:**
```
Máquina A: Submete prompts → Cria .kiro/prompt-logs/feature-x.md
Máquina B: Não vê arquivo até fazer git pull
```

**Workaround:**

**Opção 1: Fazer Commit Regular**
```bash
# Após submeter prompts
git add .kiro/prompt-logs/
git commit -m "docs: adiciona prompts"
git push
```

**Opção 2: Usar Git Hooks**
```bash
# Criar hook post-commit para fazer push automático
# .git/hooks/post-commit
git push origin $(git rev-parse --abbrev-ref HEAD)
```

**Opção 3: Usar Sincronização em Nuvem**
```bash
# Sincronizar .kiro/prompt-logs/ com Dropbox, Google Drive, etc.
# (Não recomendado - pode causar conflitos)
```

**Quando Será Resolvido:**
Fase 2 - Sincronização em Nuvem (planejado para futuro)

---

### Limitação 7: Sem Análise Automática

**Descrição:**
O sistema não fornece análise automática dos logs (estatísticas, padrões, tendências). Você precisa fazer análise manual.

**Impacto:**
- Sem relatórios automáticos
- Sem gráficos de uso
- Sem identificação automática de padrões

**Exemplo:**
```
❌ Sem análise:
Precisa contar manualmente: grep -c "^## Prompt:" .kiro/prompt-logs/*.md

✅ Com análise (futuro):
Dashboard mostra: "150 prompts submetidos, 12 por dia em média"
```

**Workaround:**

**Opção 1: Criar Scripts de Análise**
```bash
# Mac/Linux: criar script de análise
#!/bin/bash
echo "=== Análise de Prompts ==="
echo "Total de prompts:"
grep -c "^## Prompt:" .kiro/prompt-logs/*.md | awk -F: '{sum+=$2} END {print sum}'

echo "Prompts por branch:"
for file in .kiro/prompt-logs/*.md; do
  count=$(grep -c "^## Prompt:" "$file" 2>/dev/null || echo 0)
  branch=$(basename "$file" .md)
  echo "$branch: $count"
done
```

**Opção 2: Usar Ferramentas de Análise**
```bash
# Exportar para CSV e analisar em Excel/Google Sheets
grep "^## Prompt:" .kiro/prompt-logs/*.md | \
  awk -F: '{print $1, $3}' > prompts-analysis.csv
```

**Opção 3: Integrar com BI**
```bash
# Importar logs em ferramenta de BI (Tableau, Power BI, etc.)
# Para análise visual e relatórios
```

**Quando Será Resolvido:**
Fase 3 - Análise Automática (planejado para futuro)

---

### Limitação 8: Sem Controle de Acesso Granular

**Descrição:**
Todos os desenvolvedores com acesso ao repositório podem ler todos os logs. Não há controle de acesso granular por branch ou usuário.

**Impacto:**
- Sem privacidade de prompts
- Todos veem todos os prompts
- Sem restrição de acesso

**Workaround:**

**Opção 1: Usar Repositório Privado**
```bash
# Configurar repositório como privado no GitHub
# Apenas membros autorizados têm acesso
```

**Opção 2: Usar Branches Protegidas**
```bash
# Proteger branches sensíveis
# Requer aprovação para merge
```

**Opção 3: Documentar Sensibilidade**
```bash
# Adicionar comentário no arquivo de log
# "CONFIDENCIAL - Apenas para equipe de ML"
```

**Quando Será Resolvido:**
Fase 2 - Controle de Acesso (planejado para futuro)

---

### Resumo de Limitações e Roadmap

| # | Limitação | Impacto | Workaround | Fase |
|---|-----------|--------|-----------|------|
| 1 | Captura de conteúdo | Conteúdo vazio | Adicionar manualmente | Fase 2 |
| 2 | Filtragem trivial | Prompts perdidos | Combinar com contexto | Fase 2 |
| 3 | Sem resposta do agente | Sem rastreabilidade de código | Documentar em commit | Fase 2 |
| 4 | Crescimento indefinido | Performance degradada | Dividir/arquivar manualmente | Fase 4 |
| 5 | Sem interface | Requer terminal | Usar scripts auxiliares | Fase 3 |
| 6 | Sem sincronização | Conflitos multi-máquina | Fazer commit regular | Fase 2 |
| 7 | Sem análise | Sem relatórios | Criar scripts de análise | Fase 3 |
| 8 | Sem controle de acesso | Sem privacidade | Usar repositório privado | Fase 2 |

---

### Roadmap Futuro

#### Fase 2 - Melhorias Essenciais (Próximas 2-4 semanas)
- ✅ Captura melhorada de conteúdo do prompt
- ✅ Captura de respostas do agente
- ✅ Configuração de filtros
- ✅ Sincronização em nuvem
- ✅ Controle de acesso básico

#### Fase 3 - Interface e Análise (Próximas 4-8 semanas)
- ✅ CLI para consulta de logs
- ✅ Interface web para visualização
- ✅ Análise automática e relatórios
- ✅ Gráficos de uso e padrões
- ✅ Busca avançada com filtros

#### Fase 4 - Otimização e Escalabilidade (Próximas 8-12 semanas)
- ✅ Rotação e arquivamento automático
- ✅ Compressão de arquivos antigos
- ✅ Banco de dados para logs (ao invés de arquivos)
- ✅ Replicação e backup automático
- ✅ Integração com sistemas de BI

---

### Feedback e Sugestões

Se você encontrou uma limitação não documentada aqui, ou tem sugestões para melhorias:

1. **Abrir Issue no GitHub**
   - Ir para: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/issues
   - Selecionar template "Feature Request"
   - Descrever a limitação ou sugestão

2. **Participar de Discussões**
   - Ir para: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/discussions
   - Compartilhar experiências e ideias

3. **Contribuir com Soluções**
   - Fazer fork do repositório
   - Implementar melhoria
   - Abrir Pull Request

---

**Versão**: 0.1.0  
**Data**: 27 de Maio de 2026  
**Status**: ✅ Limitações Conhecidas Documentadas
