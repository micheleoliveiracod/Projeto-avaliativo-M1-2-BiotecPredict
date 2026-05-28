# Configuração Manual do GitHub Project Board

## 📋 Objetivo

Adicionar as 30 issues ao Project Board e configurar automação.

## 🔗 Links Importantes

- **Project Board:** https://github.com/users/micheleoliveiracod/projects/7
- **Repositório:** https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict
- **Issues:** https://github.com/micheleoliveiracod/Projeto-avaliativo-M1-2-BiotecPredict/issues

## 📝 Issues a Adicionar (30 total)

### Sprint 0 (5 issues)
- #227 setup: estruturar repositorio e diretorios base
- #228 setup: configurar banco de dados PostgreSQL e ORM
- #229 setup: configurar FastAPI e endpoints base
- #230 setup: configurar React e estrutura de componentes
- #231 setup: criar issues e milestones do projeto

### Sprint 1 (5 issues)
- #202 feat(backend): implementar modelos SQLAlchemy
- #203 feat(backend): criar schemas Pydantic
- #204 feat(api): criar endpoint POST /upload
- #205 feat(api): criar endpoints GET de consulta
- #206 test(backend): implementar testes unitários

### Sprint 2 (5 issues)
- #207 feat(frontend): criar página Home com upload
- #208 feat(frontend): criar Dashboard com KPIs
- #209 feat(frontend): criar tabela de batches
- #210 feat(frontend): integração com API backend
- #211 test(frontend): implementar testes E2E

### Sprint 3 (5 issues)
- #212 feat(ml): implementar Compliance Score Engine
- #213 feat(ml): criar ML Pipeline com RandomForest
- #214 feat(ml): treinar modelo com dataset Kaggle
- #215 feat(frontend): criar página ML Analytics
- #216 test(ml): implementar testes de ML

### Sprint 4 (5 issues)
- #217 test(backend): testes unitários com pytest
- #218 test(frontend): testes unitários com Vitest
- #219 test(api): testes de integração com Postman
- #220 test(e2e): testes E2E com Cypress
- #221 test(coverage): validação de cobertura e relatórios

### Sprint 5 (5 issues)
- #222 docs: documentação de API com Swagger
- #223 docs: guias de desenvolvimento
- #224 feat(validation): scripts de validação de dados
- #225 feat(validation): scripts de validação de compliance
- #226 chore: deploy em produção e entrega final

## 🚀 Passo 1: Adicionar Issues ao Project Board

### Opção A: Adicionar Manualmente (Recomendado)

1. Acesse o Project Board: https://github.com/users/micheleoliveiracod/projects/7

2. Clique no botão **"Add item"** ou **"+"** no canto superior direito

3. Selecione **"Add issues from repository"**

4. Na caixa de busca, digite cada issue:
   - `#202` e pressione Enter
   - `#203` e pressione Enter
   - ... continue até `#231`

5. Ou use a busca por label:
   - Busque por `sprint-0` para adicionar todas do Sprint 0
   - Busque por `sprint-1` para adicionar todas do Sprint 1
   - ... continue para todos os sprints

### Opção B: Adicionar via Bulk (Mais Rápido)

1. Acesse o Project Board

2. Clique em **"Add item"**

3. Cole a seguinte lista de issues:
   ```
   #202 #203 #204 #205 #206
   #207 #208 #209 #210 #211
   #212 #213 #214 #215 #216
   #217 #218 #219 #220 #221
   #222 #223 #224 #225 #226
   #227 #228 #229 #230 #231
   ```

4. Pressione Enter para adicionar todas

## 🎯 Passo 2: Configurar Colunas do Board

1. Acesse o Project Board

2. Clique em **"Settings"** (engrenagem no canto superior direito)

3. Vá para **"Columns"** ou **"Fields"**

4. Configure as colunas padrão:
   - **Todo** (padrão)
   - **In Progress**
   - **In Review**
   - **Done**

5. Ou customize conforme necessário para seu workflow

## ⚙️ Passo 3: Ativar Automação

### Automação de Issues

1. Acesse o Project Board

2. Clique em **"Settings"** (engrenagem)

3. Vá para **"Automation"** ou **"Workflows"**

4. Ative as seguintes automações:

   **Auto-add to project:**
   - Quando: Issue é criada
   - Ação: Adicionar ao projeto automaticamente
   - Coluna: Todo

   **Auto-move to In Progress:**
   - Quando: Issue é atribuída
   - Ação: Mover para "In Progress"

   **Auto-move to In Review:**
   - Quando: Pull Request é criado
   - Ação: Mover para "In Review"

   **Auto-move to Done:**
   - Quando: Issue é fechada
   - Ação: Mover para "Done"

### Automação de Pull Requests

1. Vá para **"Automation"** no Project Board

2. Ative:
   - **Auto-add PRs:** Quando PR é criado, adicionar ao projeto
   - **Auto-move PR:** Quando PR é mergeado, mover para "Done"

## 📊 Passo 4: Verificar Configuração

1. Acesse o Project Board: https://github.com/users/micheleoliveiracod/projects/7

2. Verifique se:
   - ✅ Todas as 30 issues estão no board
   - ✅ As colunas estão configuradas
   - ✅ A automação está ativa
   - ✅ As issues estão distribuídas por sprint

## 🎉 Próximos Passos

1. ✅ Adicionar 30 issues ao Project Board
2. ✅ Configurar colunas
3. ✅ Ativar automação
4. ⏳ Iniciar Sprint 0 com as 5 issues

## 📝 Notas

- As issues já possuem labels de sprint (`sprint-0`, `sprint-1`, etc.)
- As issues já possuem milestones configurados
- A automação ajudará a manter o board atualizado automaticamente
- Você pode customizar as colunas e automação conforme necessário

## 🆘 Troubleshooting

**Problema:** Issues não aparecem no board
- **Solução:** Verifique se o repositório está vinculado ao projeto

**Problema:** Automação não funciona
- **Solução:** Verifique as permissões do projeto e do repositório

**Problema:** Não consigo adicionar issues
- **Solução:** Verifique se você tem permissão de escrita no projeto

## 📞 Suporte

Para mais informações sobre GitHub Projects, consulte:
- https://docs.github.com/en/issues/planning-and-tracking-with-projects
- https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project
