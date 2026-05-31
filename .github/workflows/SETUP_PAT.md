# Configuração do Personal Access Token (PAT) para Automação de Projeto

## ⚠️ Problema Identificado

O erro `Could not resolve to a ProjectV2 with the number 7` ocorre porque o `GITHUB_TOKEN` padrão **não tem permissão** para acessar ProjectV2.

## ✅ Solução: Criar um Personal Access Token (PAT)

### Passo 1: Criar o PAT

1. Acesse: https://github.com/settings/tokens
2. Clique em **"Generate new token"** → **"Generate new token (classic)"**
3. Preencha os dados:
   - **Token name:** `ADD_TO_PROJECT_PAT`
   - **Expiration:** Escolha um período (recomendado: 90 dias ou "No expiration")
   - **Scopes:** Selecione:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `project` (Full control of projects)
     - ✅ `read:user` (Read user profile data)

4. Clique em **"Generate token"**
5. **Copie o token** (você não conseguirá vê-lo novamente!)

### Passo 2: Adicionar o Token aos Secrets do Repositório

1. Acesse: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/settings/secrets/actions
2. Clique em **"New repository secret"**
3. Preencha:
   - **Name:** `ADD_TO_PROJECT_PAT`
   - **Secret:** Cole o token que você copiou
4. Clique em **"Add secret"**

### Passo 3: Verificar a Configuração

O workflow agora usará:
```yaml
github-token: ${{ secrets.ADD_TO_PROJECT_PAT }}
```

Em vez de:
```yaml
github-token: ${{ secrets.GITHUB_TOKEN }}
```

## 📋 Checklist

- [ ] Acessei https://github.com/settings/tokens
- [ ] Criei um novo token com nome `ADD_TO_PROJECT_PAT`
- [ ] Selecionei os scopes: `repo`, `project`, `read:user`
- [ ] Copiei o token
- [ ] Acessei https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/settings/secrets/actions
- [ ] Criei um novo secret com nome `ADD_TO_PROJECT_PAT`
- [ ] Colei o token no secret
- [ ] Cliquei em "Add secret"

## 🧪 Teste

Após configurar o PAT:

1. Abra uma nova PR ou modifique uma existente
2. Acesse: https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/actions
3. Procure pelo workflow "Project Automation"
4. Verifique se o job "Add Issue/PR to Project" passou ✅

## 🔒 Segurança

- ✅ O token é armazenado de forma segura no GitHub
- ✅ O token é mascarado nos logs (aparece como `***`)
- ✅ O token só é acessível pelo workflow
- ✅ Você pode revogar o token a qualquer momento em https://github.com/settings/tokens

## 📝 Workflow Atualizado

O arquivo `.github/workflows/project-automation.yml` foi atualizado para usar:

```yaml
jobs:
  add-to-project:
    name: Add Issue/PR to Project
    runs-on: ubuntu-latest
    steps:
      - name: Add to project
        uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/users/micheleoliveiracod/projects/7
          github-token: ${{ secrets.ADD_TO_PROJECT_PAT }}
```

## ✅ Resultado Esperado

Após configurar o PAT:
- ✅ PRs serão adicionadas automaticamente ao quadro do projeto
- ✅ Issues serão adicionadas automaticamente ao quadro do projeto
- ✅ Sem erros de permissão
- ✅ Workflow executará com sucesso

---

**Commit:** 071fd39  
**Mensagem:** fix(automation): usar ADD_TO_PROJECT_PAT em vez de GITHUB_TOKEN para acessar ProjectV2  
**Status:** ⏳ Aguardando configuração do PAT
