# Prompt Logging - Guia de Uso

## 📋 Visão Geral

O **Prompt Logging** é um sistema automático que registra todos os prompts executados no Kiro, organizados por branch Git. Isso permite rastreabilidade completa das interações durante o desenvolvimento, facilitando auditorias, code reviews e documentação viva do processo de desenvolvimento.

### Por que é importante?

- **Auditoria e Conformidade**: Registro documentado de todas as decisões e instruções ao agente
- **Reprodutibilidade**: Entender o contexto e decisões que levaram a uma implementação
- **Análise de Qualidade**: Avaliar efetividade das instruções e padrões de uso
- **Documentação Viva**: Histórico executável que complementa documentação técnica
- **Aprendizado Contínuo**: Analisar prompts bem-sucedidos para melhorar futuras interações

---

## 🚀 Início Rápido

### Instalação

1. **Instalar dependências Python:**
   ```bash
   pip install pytz
   ```

2. **Verificar estrutura de arquivos:**
   ```
   .kiro/
   ├── hooks/
   │   └── prompt-logger.json
   ├── scripts/
   │   └── log_prompt.py
   └── prompt-logs/
       ├── main.md
       ├── develop.md
       └── feature-*.md
   ```

3. **Reiniciar Kiro** (se necessário) para carregar o hook.

### Uso

**Automático!** Nenhuma ação manual é necessária. Prompts são registrados automaticamente quando você os submete ao Kiro.

```
1. Abrir Kiro
2. Digitar prompt
3. Pressionar Enter/Submit
   ↓ (Automático)
4. Hook dispara
5. Script coleta metadados
6. Prompt é registrado em .kiro/prompt-logs/<branch-atual>.md
```

---

## 📁 Estrutura de Logs

### Localização

Cada branch Git tem seu próprio arquivo de log:

```
.kiro/prompt-logs/
├── main.md                    # Logs da branch main
├── develop.md                 # Logs da branch develop
├── feature-auth.md            # Logs de feature/auth
├── feature-compliance.md      # Logs de feature/compliance
├── bugfix-validation.md       # Logs de bugfix/validation
└── release-v1.0.0.md         # Logs de release/v1.0.0
```

### Formato de Arquivo

Cada arquivo de log segue este padrão:

```markdown
# Prompt Logs: <branch-name>

Histórico de prompts executados no Kiro nesta branch.

---

## Prompt: <título extraído do prompt>
- Responsável: <nome do usuário Git>
- Branch: <nome-da-branch>
- Data/hora: YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)

### Prompt original
```
<conteúdo completo do prompt>
```

---

## Prompt: <próximo prompt>
...
```

### Exemplo Real

```markdown
# Prompt Logs: feature-compliance-score

Histórico de prompts executados no Kiro nesta branch.

---

## Prompt: Implementar Manufacturing Compliance Score Engine
- Responsável: Michele Oliveira
- Branch: feature-compliance-score
- Data/hora: 2026-05-29 14:35:22 (Brasília - UTC-3)

### Prompt original
```
Implementar o Manufacturing Compliance Score Engine que calcula um score de 0-100 baseado em regras determinísticas. O score deve classificar em ACCEPTABLE (80-100), WARNING (60-79) ou CRITICAL (0-59). Usar as variáveis: Temperature, pH, Dissolved Oxygen, Pressure, Agitator Speed.
```

---

## Prompt: Criar testes unitários para compliance score
- Responsável: Michele Oliveira
- Branch: feature-compliance-score
- Data/hora: 2026-05-29 15:12:45 (Brasília - UTC-3)

### Prompt original
```
Criar testes unitários com pytest para validar o cálculo do compliance score. Incluir testes para:
1. Score calculado corretamente
2. Classificação correta (ACCEPTABLE/WARNING/CRITICAL)
3. Tratamento de valores fora do range
4. Edge cases (valores nulos, zeros, máximos)
```

---
```

---

## 🔍 Como Consultar Logs

### Ver logs da branch atual

**Mac/Linux:**
```bash
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

**Windows PowerShell:**
```powershell
$branch = git rev-parse --abbrev-ref HEAD
Get-Content ".kiro\prompt-logs\$branch.md"
```

### Ver logs de uma branch específica

**Mac/Linux:**
```bash
cat .kiro/prompt-logs/feature-compliance-score.md
```

**Windows:**
```cmd
type .kiro\prompt-logs\feature-compliance-score.md
```

### Ver últimas entradas

**Mac/Linux:**
```bash
tail -n 50 .kiro/prompt-logs/feature-compliance-score.md
```

**Windows PowerShell:**
```powershell
Get-Content ".kiro\prompt-logs\feature-compliance-score.md" -Tail 50
```

### Buscar por palavra-chave

**Mac/Linux:**
```bash
grep -i "compliance" .kiro/prompt-logs/*.md
```

**Windows PowerShell:**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "compliance"
```

### Contar prompts por branch

**Mac/Linux:**
```bash
for file in .kiro/prompt-logs/*.md; do
  echo "$(basename $file): $(grep -c "## Prompt:" $file)"
done
```

**Windows PowerShell:**
```powershell
Get-ChildItem ".kiro\prompt-logs\*.md" | ForEach-Object {
  $count = (Select-String -Path $_.FullName -Pattern "## Prompt:" | Measure-Object).Count
  Write-Host "$($_.Name): $count"
}
```

---

## 📊 Exemplos de Uso

### Exemplo 1: Code Review com Contexto

Você está revisando uma PR de `feature/ml-prediction` e quer entender o contexto das decisões:

```bash
# Ver todos os prompts da feature
cat .kiro/prompt-logs/feature-ml-prediction.md

# Buscar prompts relacionados a "RandomForest"
grep -B 5 -A 10 "RandomForest" .kiro/prompt-logs/feature-ml-prediction.md
```

**Resultado:** Você vê exatamente quais instruções foram dadas ao Kiro para implementar o modelo, facilitando o code review.

### Exemplo 2: Documentação Viva

Você quer documentar como o compliance score foi implementado:

```bash
# Extrair prompts relacionados a compliance
grep -A 15 "Compliance Score" .kiro/prompt-logs/feature-compliance-score.md
```

**Resultado:** Você tem um histórico executável de como a funcionalidade foi desenvolvida.

### Exemplo 3: Análise de Padrões

Você quer entender quais tipos de prompts funcionam melhor:

```bash
# Contar prompts por desenvolvedor
grep "Responsável:" .kiro/prompt-logs/*.md | cut -d: -f3 | sort | uniq -c

# Ver prompts mais recentes
tail -n 100 .kiro/prompt-logs/develop.md | grep "## Prompt:"
```

**Resultado:** Você identifica padrões de sucesso e pode melhorar futuras interações.

---

## 🔎 Exemplos Avançados de Consulta de Logs

### 1. Visualizar Logs por Branch

#### Mac/Linux

**Ver logs da branch atual:**
```bash
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

**Ver logs de uma branch específica:**
```bash
cat .kiro/prompt-logs/feature-compliance-score.md
```

**Listar todas as branches com logs:**
```bash
ls -1 .kiro/prompt-logs/ | sed 's/.md$//'
```

**Contar prompts por branch:**
```bash
for file in .kiro/prompt-logs/*.md; do
  count=$(grep -c "## Prompt:" "$file" 2>/dev/null || echo 0)
  branch=$(basename "$file" .md)
  echo "$branch: $count prompts"
done | sort -t: -k2 -rn
```

#### Windows (PowerShell)

**Ver logs da branch atual:**
```powershell
$branch = git rev-parse --abbrev-ref HEAD
Get-Content ".kiro\prompt-logs\$branch.md"
```

**Ver logs de uma branch específica:**
```powershell
Get-Content ".kiro\prompt-logs\feature-compliance-score.md"
```

**Listar todas as branches com logs:**
```powershell
Get-ChildItem ".kiro\prompt-logs\*.md" | ForEach-Object { $_.BaseName }
```

**Contar prompts por branch:**
```powershell
Get-ChildItem ".kiro\prompt-logs\*.md" | ForEach-Object {
  $count = (Select-String -Path $_.FullName -Pattern "## Prompt:" | Measure-Object).Count
  Write-Host "$($_.BaseName): $count prompts"
} | Sort-Object -Descending
```

#### Windows (CMD)

**Ver logs da branch atual:**
```cmd
for /f "tokens=*" %%i in ('git rev-parse --abbrev-ref HEAD') do type .kiro\prompt-logs\%%i.md
```

**Ver logs de uma branch específica:**
```cmd
type .kiro\prompt-logs\feature-compliance-score.md
```

**Listar todas as branches com logs:**
```cmd
dir /b .kiro\prompt-logs\*.md
```

---

### 2. Buscar por Palavras-Chave

#### Mac/Linux

**Buscar palavra-chave em todos os logs:**
```bash
grep -r "compliance" .kiro/prompt-logs/
```

**Buscar com contexto (5 linhas antes e depois):**
```bash
grep -B 5 -A 5 "RandomForest" .kiro/prompt-logs/*.md
```

**Buscar case-insensitive:**
```bash
grep -i "authentication" .kiro/prompt-logs/*.md
```

**Buscar múltiplas palavras-chave (OR):**
```bash
grep -E "compliance|score|validation" .kiro/prompt-logs/*.md
```

**Buscar apenas títulos de prompts com palavra-chave:**
```bash
grep "## Prompt:.*compliance" .kiro/prompt-logs/*.md
```

**Contar ocorrências de palavra-chave:**
```bash
grep -c "API" .kiro/prompt-logs/*.md | grep -v ":0$"
```

#### Windows (PowerShell)

**Buscar palavra-chave em todos os logs:**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "compliance"
```

**Buscar com contexto (5 linhas antes e depois):**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "RandomForest" -Context 5,5
```

**Buscar case-insensitive:**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "authentication" -CaseSensitive:$false
```

**Buscar múltiplas palavras-chave (OR):**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "compliance|score|validation"
```

**Buscar apenas títulos de prompts com palavra-chave:**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "## Prompt:.*compliance"
```

**Contar ocorrências de palavra-chave:**
```powershell
Get-ChildItem ".kiro\prompt-logs\*.md" | ForEach-Object {
  $count = (Select-String -Path $_.FullName -Pattern "API" | Measure-Object).Count
  if ($count -gt 0) { Write-Host "$($_.Name): $count" }
}
```

#### Windows (CMD)

**Buscar palavra-chave em todos os logs:**
```cmd
findstr /s "compliance" .kiro\prompt-logs\*.md
```

**Buscar case-insensitive:**
```cmd
findstr /i /s "authentication" .kiro\prompt-logs\*.md
```

---

### 3. Filtrar por Data/Usuário

#### Mac/Linux

**Ver prompts de um usuário específico:**
```bash
grep -A 10 "Responsável: Michele Oliveira" .kiro/prompt-logs/*.md
```

**Ver prompts de uma data específica:**
```bash
grep "2026-05-29" .kiro/prompt-logs/*.md
```

**Ver prompts de um período (entre datas):**
```bash
grep -E "2026-05-2[89]|2026-05-30" .kiro/prompt-logs/*.md
```

**Ver prompts de um usuário em uma branch específica:**
```bash
grep -A 10 "Responsável: Michele Oliveira" .kiro/prompt-logs/feature-compliance-score.md
```

**Listar todos os usuários que fizeram prompts:**
```bash
grep "Responsável:" .kiro/prompt-logs/*.md | cut -d: -f3 | sort | uniq
```

**Contar prompts por usuário:**
```bash
grep "Responsável:" .kiro/prompt-logs/*.md | cut -d: -f3 | sort | uniq -c | sort -rn
```

**Ver prompts mais recentes (últimas 24 horas):**
```bash
# Assumindo que hoje é 2026-05-30
grep "2026-05-30" .kiro/prompt-logs/*.md
```

**Ver prompts de um horário específico:**
```bash
grep "14:35" .kiro/prompt-logs/*.md
```

#### Windows (PowerShell)

**Ver prompts de um usuário específico:**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "Responsável: Michele Oliveira" -Context 0,10
```

**Ver prompts de uma data específica:**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "2026-05-29"
```

**Ver prompts de um período (entre datas):**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "2026-05-2[89]|2026-05-30"
```

**Listar todos os usuários que fizeram prompts:**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "Responsável: (.+)" | 
  ForEach-Object { $_.Matches.Groups[1].Value } | 
  Sort-Object | Get-Unique
```

**Contar prompts por usuário:**
```powershell
$users = @{}
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "Responsável: (.+)" | 
  ForEach-Object { 
    $user = $_.Matches.Groups[1].Value
    if ($users.ContainsKey($user)) { $users[$user]++ } 
    else { $users[$user] = 1 }
  }
$users.GetEnumerator() | Sort-Object Value -Descending | 
  ForEach-Object { Write-Host "$($_.Key): $($_.Value)" }
```

**Ver prompts mais recentes (últimas 24 horas):**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "2026-05-30"
```

**Ver prompts de um horário específico:**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "14:35"
```

#### Windows (CMD)

**Ver prompts de um usuário específico:**
```cmd
findstr /s "Responsável: Michele Oliveira" .kiro\prompt-logs\*.md
```

**Ver prompts de uma data específica:**
```cmd
findstr /s "2026-05-29" .kiro\prompt-logs\*.md
```

---

### 4. Exportar Resultados

#### Mac/Linux

**Exportar logs de uma branch para arquivo de texto:**
```bash
cat .kiro/prompt-logs/feature-compliance-score.md > export-compliance-logs.txt
```

**Exportar prompts de um usuário para arquivo:**
```bash
grep -A 10 "Responsável: Michele Oliveira" .kiro/prompt-logs/*.md > export-user-prompts.txt
```

**Exportar prompts de uma data para arquivo:**
```bash
grep "2026-05-29" .kiro/prompt-logs/*.md > export-date-prompts.txt
```

**Exportar para CSV (formato estruturado):**
```bash
cat > export-logs.sh << 'EOF'
#!/bin/bash
echo "Branch,Usuário,Data,Hora,Título" > prompts.csv
for file in .kiro/prompt-logs/*.md; do
  branch=$(basename "$file" .md)
  grep "## Prompt:" "$file" | while read -r line; do
    title=$(echo "$line" | sed 's/## Prompt: //')
    # Extrair usuário e data do próximo prompt
    grep -A 3 "## Prompt: $title" "$file" | grep "Responsável:" | sed "s/.*: //" | tr '\n' ',' >> prompts.csv
    echo "$branch,$title" >> prompts.csv
  done
done
EOF
chmod +x export-logs.sh
./export-logs.sh
```

**Exportar para JSON (formato estruturado):**
```bash
cat > export-logs-json.py << 'EOF'
#!/usr/bin/env python3
import os
import json
import re
from pathlib import Path

logs = []
for file in Path('.kiro/prompt-logs').glob('*.md'):
    branch = file.stem
    content = file.read_text(encoding='utf-8')
    
    # Extrair prompts
    prompts = re.findall(
        r'## Prompt: (.+?)\n- Responsável: (.+?)\n- Branch: (.+?)\n- Data/hora: (.+?)\n\n### Prompt original\n```\n(.+?)\n```',
        content,
        re.DOTALL
    )
    
    for title, user, branch_name, datetime, prompt_text in prompts:
        logs.append({
            'branch': branch,
            'title': title.strip(),
            'user': user.strip(),
            'datetime': datetime.strip(),
            'prompt': prompt_text.strip()
        })

with open('prompts.json', 'w', encoding='utf-8') as f:
    json.dump(logs, f, ensure_ascii=False, indent=2)
print(f"Exportados {len(logs)} prompts para prompts.json")
EOF
python3 export-logs-json.py
```

**Exportar para HTML (relatório visual):**
```bash
cat > export-logs-html.sh << 'EOF'
#!/bin/bash
cat > prompts.html << 'HTML'
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Prompt Logs Report</title>
  <style>
    body { font-family: Arial; margin: 20px; }
    .branch { background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px; }
    .prompt { background: #fff; padding: 10px; margin: 5px 0; border-left: 4px solid #007bff; }
    .metadata { color: #666; font-size: 0.9em; }
  </style>
</head>
<body>
  <h1>Prompt Logs Report</h1>
HTML

for file in .kiro/prompt-logs/*.md; do
  branch=$(basename "$file" .md)
  echo "<div class='branch'><h2>$branch</h2>" >> prompts.html
  
  # Extrair prompts e adicionar ao HTML
  grep -A 10 "## Prompt:" "$file" | while read -r line; do
    if [[ $line == "## Prompt:"* ]]; then
      title=$(echo "$line" | sed 's/## Prompt: //')
      echo "<div class='prompt'><h3>$title</h3>" >> prompts.html
    elif [[ $line == "- Responsável:"* ]] || [[ $line == "- Branch:"* ]] || [[ $line == "- Data/hora:"* ]]; then
      echo "<div class='metadata'>$line</div>" >> prompts.html
    fi
  done
  
  echo "</div>" >> prompts.html
done

cat >> prompts.html << 'HTML'
</body>
</html>
HTML
EOF
chmod +x export-logs-html.sh
./export-logs-html.sh
```

#### Windows (PowerShell)

**Exportar logs de uma branch para arquivo de texto:**
```powershell
Get-Content ".kiro\prompt-logs\feature-compliance-score.md" | Out-File -Encoding UTF8 "export-compliance-logs.txt"
```

**Exportar prompts de um usuário para arquivo:**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "Responsável: Michele Oliveira" -Context 0,10 | 
  Out-File -Encoding UTF8 "export-user-prompts.txt"
```

**Exportar prompts de uma data para arquivo:**
```powershell
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "2026-05-29" | 
  Out-File -Encoding UTF8 "export-date-prompts.txt"
```

**Exportar para CSV (formato estruturado):**
```powershell
$csv = @()
Get-ChildItem ".kiro\prompt-logs\*.md" | ForEach-Object {
  $branch = $_.BaseName
  $content = Get-Content $_.FullName -Raw
  
  $prompts = [regex]::Matches($content, '## Prompt: (.+?)\n- Responsável: (.+?)\n- Branch: (.+?)\n- Data/hora: (.+?)\n')
  
  foreach ($match in $prompts) {
    $csv += [PSCustomObject]@{
      Branch = $branch
      Title = $match.Groups[1].Value
      User = $match.Groups[2].Value
      DateTime = $match.Groups[4].Value
    }
  }
}

$csv | Export-Csv -Path "prompts.csv" -Encoding UTF8 -NoTypeInformation
Write-Host "Exportados $($csv.Count) prompts para prompts.csv"
```

**Exportar para JSON (formato estruturado):**
```powershell
$logs = @()
Get-ChildItem ".kiro\prompt-logs\*.md" | ForEach-Object {
  $branch = $_.BaseName
  $content = Get-Content $_.FullName -Raw
  
  $prompts = [regex]::Matches($content, '## Prompt: (.+?)\n- Responsável: (.+?)\n- Branch: (.+?)\n- Data/hora: (.+?)\n\n### Prompt original\n```\n(.+?)\n```', [System.Text.RegularExpressions.RegexOptions]::Singleline)
  
  foreach ($match in $prompts) {
    $logs += @{
      branch = $branch
      title = $match.Groups[1].Value.Trim()
      user = $match.Groups[2].Value.Trim()
      datetime = $match.Groups[4].Value.Trim()
      prompt = $match.Groups[5].Value.Trim()
    }
  }
}

$logs | ConvertTo-Json | Out-File -Encoding UTF8 "prompts.json"
Write-Host "Exportados $($logs.Count) prompts para prompts.json"
```

#### Windows (CMD)

**Exportar logs de uma branch para arquivo de texto:**
```cmd
type .kiro\prompt-logs\feature-compliance-score.md > export-compliance-logs.txt
```

**Exportar prompts de um usuário para arquivo:**
```cmd
findstr /s "Responsável: Michele Oliveira" .kiro\prompt-logs\*.md > export-user-prompts.txt
```

**Exportar prompts de uma data para arquivo:**
```cmd
findstr /s "2026-05-29" .kiro\prompt-logs\*.md > export-date-prompts.txt
```

---

### 5. Casos de Uso Práticos

#### Caso 1: Preparar Code Review

Você precisa revisar uma PR e quer entender o contexto completo:

**Mac/Linux:**
```bash
# Exportar todos os prompts da feature para análise
branch="feature-compliance-score"
cat .kiro/prompt-logs/$branch.md > code-review-context.md

# Adicionar resumo
echo -e "\n\n## Resumo de Prompts\n" >> code-review-context.md
grep "## Prompt:" .kiro/prompt-logs/$branch.md >> code-review-context.md

# Abrir no editor
code code-review-context.md
```

**Windows (PowerShell):**
```powershell
$branch = "feature-compliance-score"
Get-Content ".kiro\prompt-logs\$branch.md" | Out-File -Encoding UTF8 "code-review-context.md"

# Adicionar resumo
Add-Content "code-review-context.md" "`n`n## Resumo de Prompts`n"
Select-String -Path ".kiro\prompt-logs\$branch.md" -Pattern "## Prompt:" | 
  Add-Content "code-review-context.md"

# Abrir no editor
code code-review-context.md
```

#### Caso 2: Gerar Relatório de Atividade

Você quer gerar um relatório de atividade do time:

**Mac/Linux:**
```bash
cat > activity-report.sh << 'EOF'
#!/bin/bash
echo "# Relatório de Atividade - Prompt Logging"
echo ""
echo "## Resumo Geral"
echo "- Total de prompts: $(grep -c "## Prompt:" .kiro/prompt-logs/*.md)"
echo "- Branches ativas: $(ls -1 .kiro/prompt-logs/*.md | wc -l)"
echo "- Período: $(date)"
echo ""

echo "## Prompts por Desenvolvedor"
grep "Responsável:" .kiro/prompt-logs/*.md | cut -d: -f3 | sort | uniq -c | sort -rn

echo ""
echo "## Prompts por Branch"
for file in .kiro/prompt-logs/*.md; do
  count=$(grep -c "## Prompt:" "$file" 2>/dev/null || echo 0)
  branch=$(basename "$file" .md)
  echo "- $branch: $count prompts"
done | sort -t: -k2 -rn

echo ""
echo "## Últimos 10 Prompts"
grep "## Prompt:" .kiro/prompt-logs/*.md | tail -10
EOF
chmod +x activity-report.sh
./activity-report.sh > activity-report.md
```

**Windows (PowerShell):**
```powershell
$report = @"
# Relatório de Atividade - Prompt Logging

## Resumo Geral
- Total de prompts: $((Get-ChildItem ".kiro\prompt-logs\*.md" | ForEach-Object { (Select-String -Path $_.FullName -Pattern "## Prompt:" | Measure-Object).Count } | Measure-Object -Sum).Sum)
- Branches ativas: $(Get-ChildItem ".kiro\prompt-logs\*.md" | Measure-Object).Count
- Período: $(Get-Date)

## Prompts por Desenvolvedor
"@

$users = @{}
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "Responsável: (.+)" | 
  ForEach-Object { 
    $user = $_.Matches.Groups[1].Value
    if ($users.ContainsKey($user)) { $users[$user]++ } 
    else { $users[$user] = 1 }
  }

$users.GetEnumerator() | Sort-Object Value -Descending | 
  ForEach-Object { $report += "`n- $($_.Key): $($_.Value) prompts" }

$report | Out-File -Encoding UTF8 "activity-report.md"
Write-Host "Relatório gerado: activity-report.md"
```

---

### 6. Dicas de Performance

Para logs muito grandes, use estas técnicas para melhorar performance:

#### Mac/Linux

**Buscar apenas em uma branch (mais rápido):**
```bash
grep "compliance" .kiro/prompt-logs/feature-compliance-score.md
# Em vez de:
grep -r "compliance" .kiro/prompt-logs/
```

**Usar `head` para ver apenas primeiras linhas:**
```bash
head -n 100 .kiro/prompt-logs/feature-compliance-score.md
```

**Usar `tail` para ver apenas últimas linhas:**
```bash
tail -n 50 .kiro/prompt-logs/feature-compliance-score.md
```

**Contar linhas sem ler tudo:**
```bash
wc -l .kiro/prompt-logs/feature-compliance-score.md
```

#### Windows (PowerShell)

**Buscar apenas em uma branch (mais rápido):**
```powershell
Select-String -Path ".kiro\prompt-logs\feature-compliance-score.md" -Pattern "compliance"
# Em vez de:
Select-String -Path ".kiro\prompt-logs\*.md" -Pattern "compliance"
```

**Ver apenas primeiras linhas:**
```powershell
Get-Content ".kiro\prompt-logs\feature-compliance-score.md" -Head 100
```

**Ver apenas últimas linhas:**
```powershell
Get-Content ".kiro\prompt-logs\feature-compliance-score.md" -Tail 50
```

**Contar linhas:**
```powershell
(Get-Content ".kiro\prompt-logs\feature-compliance-score.md" | Measure-Object -Line).Lines
```

---

## 🔧 Convenções de Logging

### Nomes de Arquivo

**Padrão:** `<tipo-branch>-<nome-descritivo>.md`

| Tipo de Branch | Exemplo | Arquivo |
|---|---|---|
| `feature/` | `feature/compliance-score` | `feature-compliance-score.md` |
| `bugfix/` | `bugfix/validation-error` | `bugfix-validation-error.md` |
| `hotfix/` | `hotfix/api-crash` | `hotfix-api-crash.md` |
| `release/` | `release/v1.0.0` | `release-v1.0.0.md` |
| `chore/` | `chore/update-deps` | `chore-update-deps.md` |
| `docs/` | `docs/api-guide` | `docs-api-guide.md` |
| `main` | - | `main.md` |
| `develop` | - | `develop.md` |

**Regras:**
- Converter `/` em `-` (exemplo: `feature/auth-v2` → `feature-auth-v2.md`)
- Sempre em minúsculas
- Sem espaços ou caracteres especiais
- Sem acentuação (usar equivalentes ASCII)

### Formato de Timestamp

**Padrão:** `YYYY-MM-DD HH:mm:ss` (Brasília - UTC-3)

**Exemplos válidos:**
- `2026-05-27 14:35:22` ✅
- `2026-05-27 09:15:00` ✅
- `2026-05-27 23:59:59` ✅

**Exemplos inválidos:**
- `27/05/2026 14:35:22` ❌ (formato brasileiro)
- `2026-05-27T14:35:22Z` ❌ (ISO com Z)
- `14:35:22` ❌ (sem data)

**Timezone obrigatório:** America/Sao_Paulo (UTC-3)
- Não usar UTC ou outros timezones
- Não usar horário de verão (sempre UTC-3)

### Formato de Metadados

**Estrutura obrigatória:**

```markdown
## Prompt: <título extraído do prompt>
- Responsável: <nome do usuário Git>
- Branch: <nome-da-branch>
- Data/hora: YYYY-MM-DD HH:mm:ss (Brasília - UTC-3)

### Prompt original
```
<conteúdo completo do prompt>
```
```

**Campos obrigatórios:**
- `Prompt`: Título descritivo (máx 80 caracteres)
- `Responsável`: Nome do usuário Git (usar `git config user.name`)
- `Branch`: Nome exato da branch (usar `git rev-parse --abbrev-ref HEAD`)
- `Data/hora`: Timestamp em formato padrão com timezone
- `Prompt original`: Conteúdo completo entre triple backticks

### Filtragem de Prompts

**Prompts que NÃO devem ser registrados:**

| Tipo | Exemplo | Motivo |
|---|---|---|
| Confirmações simples | "sim", "ok", "entendido" | Ruído nos logs |
| Respostas muito curtas | "próximo", "continue" | Sem valor informativo |
| Comandos de navegação | "voltar", "ir para", "sair" | Não são prompts reais |
| Respostas vazias | "" | Sem conteúdo |
| Duplicatas | Mesmo prompt repetido | Evitar redundância |

**Prompts que DEVEM ser registrados:**

| Tipo | Exemplo | Motivo |
|---|---|---|
| Instruções de implementação | "Implementar endpoint de upload" | Decisão técnica |
| Pedidos de análise | "Analisar este código" | Análise de qualidade |
| Correções de bugs | "Corrigir erro de validação" | Rastreabilidade de fixes |
| Refatorações | "Refatorar este módulo" | Melhorias de código |
| Documentação | "Documentar esta função" | Documentação viva |

**Critério de mínimo:**
- Prompts com menos de 10 caracteres são automaticamente filtrados
- Prompts sem conteúdo são automaticamente filtrados
- Confirmações simples são automaticamente filtradas

---

## 🛠️ Troubleshooting

### Logs não estão sendo criados

**Verificar:**
1. Hook existe: `.kiro/hooks/prompt-logger.json`
2. Script existe: `.kiro/scripts/log_prompt.py`
3. Permissões de execução do script
4. Logs de erro do Kiro

**Solução:**
```bash
# Testar manualmente
python .kiro/scripts/log_prompt.py --test

# Verificar se arquivo foi criado
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

### Conteúdo não é capturado

**Limitação conhecida:** O Kiro pode não expor o conteúdo do prompt via variáveis de ambiente ou stdin no contexto do hook.

**Impacto:** Logs podem conter apenas metadados (branch, usuário, timestamp) sem o conteúdo real do prompt.

**Solução:** Metadados ainda são registrados. Você pode:
1. Adicionar manualmente o conteúdo do prompt ao arquivo de log
2. Consultar o histórico do Kiro para recuperar o prompt
3. Documentar a limitação em code reviews

### Arquivo de log está vazio

**Verificar:**
1. Submeter um prompt no Kiro para criar entrada
2. Hook deve capturar automaticamente
3. Se ainda vazio, verificar instalação de dependências

**Solução:**
```bash
# Instalar pytz
pip install pytz

# Reiniciar Kiro
```

### Erro ao executar script manualmente

**Verificar:**
1. Python 3.8+ instalado: `python --version`
2. pytz instalado: `pip list | grep pytz`
3. Git configurado: `git config user.name`

**Solução:**
```bash
# Instalar dependências
pip install pytz

# Configurar Git
git config user.name "Seu Nome"
git config user.email "seu.email@example.com"
```

---

## 📝 Boas Práticas

### 1. Revisar Logs Antes de Commits

Antes de fazer commit de um arquivo de log, revise para garantir que não contém dados sensíveis:

```bash
# Ver últimas entradas
tail -n 20 .kiro/prompt-logs/feature-*.md

# Buscar por palavras-chave sensíveis
grep -i "password\|token\|secret\|key" .kiro/prompt-logs/*.md
```

### 2. Usar Logs em Code Reviews

Ao revisar uma PR, consulte os logs para entender o contexto:

```bash
# Ver prompts da feature branch
cat .kiro/prompt-logs/feature-nome-da-feature.md

# Buscar prompts relacionados ao arquivo alterado
grep -l "nome-do-arquivo" .kiro/prompt-logs/*.md
```

### 3. Documentar Decisões Importantes

Se uma decisão importante foi tomada, adicione um comentário no arquivo de log:

```markdown
## Prompt: Implementar autenticação JWT
- Responsável: Michele Oliveira
- Branch: feature-auth
- Data/hora: 2026-05-29 14:35:22 (Brasília - UTC-3)

### Prompt original
```
Implementar autenticação JWT com tokens de 24 horas de expiração.
```

### Notas
- Decisão: Usar JWT em vez de sessions para escalabilidade
- Referência: Issue #123
- Discussão: Reunião de arquitetura em 29/05/2026
```

### 4. Fazer Commits Regulares

Versione logs junto com o código:

```bash
# Adicionar logs ao commit
git add .kiro/prompt-logs/

# Commit com mensagem descritiva
git commit -m "docs: adiciona prompts de implementação da feature"
```

### 5. Referenciar Logs em PRs

Quando código é gerado por IA, referencie o log na descrição da PR:

```markdown
## Descrição

Implementa o Manufacturing Compliance Score Engine.

## Prompts Utilizados

Ver logs em `.kiro/prompt-logs/feature-compliance-score.md`

## Referências

- Design: `.kiro/specs/prompt-logging/design.md`
- Requisitos: `.kiro/specs/prompt-logging/requirements.md`
```

---

## 🔧 Troubleshooting - Guia de Resolução de Problemas

Esta seção fornece soluções para os problemas mais comuns encontrados ao usar o sistema de prompt logging.

### Problema 1: Logs não estão sendo criados

**Sintomas:**
- Arquivo `.kiro/prompt-logs/<branch>.md` não existe
- Prompts não aparecem nos logs
- Diretório `.kiro/prompt-logs/` vazio

**Causas Possíveis:**
1. Hook não está instalado ou ativado
2. Script `log_prompt.py` não existe ou não tem permissão de execução
3. Dependência `pytz` não está instalada
4. Kiro não está reconhecendo o hook

**Passos de Diagnóstico:**

```bash
# 1. Verificar se o hook existe
ls -la .kiro/hooks/prompt-logger.json

# 2. Verificar se o script existe
ls -la .kiro/scripts/log_prompt.py

# 3. Verificar se pytz está instalado
pip list | grep pytz

# 4. Verificar permissões do script
ls -la .kiro/scripts/log_prompt.py

# 5. Verificar se o diretório de logs existe
ls -la .kiro/prompt-logs/
```

**Soluções:**

**Solução 1: Instalar dependências**
```bash
# Instalar pytz
pip install pytz

# Verificar instalação
python -c "import pytz; print('pytz instalado com sucesso')"
```

**Solução 2: Dar permissão de execução ao script**
```bash
# Mac/Linux
chmod +x .kiro/scripts/log_prompt.py

# Windows (PowerShell)
# Não é necessário no Windows
```

**Solução 3: Recriar o hook no Kiro**
1. Abra o Kiro
2. Vá para Settings → Hooks
3. Remova o hook `prompt-logger`
4. Adicione novamente o hook apontando para `.kiro/hooks/prompt-logger.json`
5. Reinicie o Kiro

**Solução 4: Testar manualmente**
```bash
# Executar o script manualmente para testar
python .kiro/scripts/log_prompt.py --test

# Verificar se o arquivo foi criado
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

**Solução 5: Criar arquivo de log manualmente**
```bash
# Se nada funcionar, criar o arquivo manualmente
touch .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md

# Adicionar cabeçalho
echo "# Prompt Logs: $(git rev-parse --abbrev-ref HEAD)" > .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
echo "" >> .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
echo "Histórico de prompts executados no Kiro nesta branch." >> .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

---

### Problema 2: Conteúdo do prompt não está sendo capturado

**Sintomas:**
- Arquivo de log criado, mas sem o conteúdo do prompt
- Apenas metadados (branch, usuário, data) aparecem
- Seção "Prompt original" está vazia

**Causas Possíveis:**
1. Limitação conhecida do Kiro - não expõe conteúdo via hook
2. Variável de ambiente não configurada corretamente
3. Script não consegue acessar stdin ou variáveis de ambiente

**Passos de Diagnóstico:**

```bash
# 1. Verificar se o hook está configurado corretamente
cat .kiro/hooks/prompt-logger.json

# 2. Verificar variáveis de ambiente disponíveis
env | grep -i prompt

# 3. Verificar logs de erro do Kiro
# (Consultar logs do Kiro em Settings → Logs)

# 4. Testar com um prompt simples
# Submeter um prompt curto e verificar se é capturado
```

**Soluções:**

**Solução 1: Aceitar a limitação e adicionar manualmente**

Esta é uma limitação conhecida do Kiro. O conteúdo do prompt pode não ser exposto via hook. Neste caso:

1. Metadados (branch, usuário, timestamp) serão registrados automaticamente
2. Você pode adicionar manualmente o conteúdo do prompt ao arquivo de log:

```markdown
## Prompt: Implementar endpoint de upload
- Responsável: Michele Oliveira
- Branch: feature-upload
- Data/hora: 2026-05-29 14:35:22 (Brasília - UTC-3)

### Prompt original
```
[Adicione aqui o conteúdo do prompt manualmente]
```
```

**Solução 2: Usar alternativa - Copiar prompt para arquivo**

Se o conteúdo não for capturado automaticamente:

```bash
# 1. Copiar o prompt para um arquivo temporário
echo "Seu prompt aqui" > /tmp/prompt.txt

# 2. Executar o script com o arquivo como entrada
python .kiro/scripts/log_prompt.py < /tmp/prompt.txt

# 3. Verificar se foi capturado
tail -n 20 .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

**Solução 3: Documentar no commit**

Se o conteúdo não for capturado, documente no commit:

```bash
git commit -m "feat: implementa endpoint de upload

Prompts utilizados:
- Implementar endpoint POST /api/v1/upload
- Adicionar validação de arquivo CSV
- Criar testes unitários

Ver logs em: .kiro/prompt-logs/feature-upload.md"
```

---

### Problema 3: Arquivo de log está vazio ou corrompido

**Sintomas:**
- Arquivo `.kiro/prompt-logs/<branch>.md` existe mas está vazio
- Arquivo contém caracteres estranhos ou formatação quebrada
- Erro ao abrir o arquivo

**Causas Possíveis:**
1. Arquivo foi criado mas nenhum prompt foi registrado
2. Problema de encoding (UTF-8 vs outro)
3. Arquivo foi corrompido durante escrita
4. Permissões de arquivo incorretas

**Passos de Diagnóstico:**

```bash
# 1. Verificar tamanho do arquivo
ls -lh .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md

# 2. Verificar encoding do arquivo
file .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md

# 3. Verificar conteúdo
cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md

# 4. Verificar permissões
ls -la .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md

# 5. Contar linhas
wc -l .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

**Soluções:**

**Solução 1: Submeter um novo prompt**

Se o arquivo está vazio, simplesmente submeta um novo prompt no Kiro:

```
1. Abrir Kiro
2. Digitar um prompt simples: "Olá, teste de logging"
3. Pressionar Enter
4. Verificar se foi registrado: cat .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

**Solução 2: Recriar arquivo com cabeçalho correto**

Se o arquivo está corrompido:

```bash
# 1. Fazer backup do arquivo corrompido
cp .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md.bak

# 2. Recriar arquivo com cabeçalho correto
branch=$(git rev-parse --abbrev-ref HEAD)
cat > .kiro/prompt-logs/$branch.md << EOF
# Prompt Logs: $branch

Histórico de prompts executados no Kiro nesta branch.

---
EOF

# 3. Verificar arquivo recriado
cat .kiro/prompt-logs/$branch.md
```

**Solução 3: Verificar e corrigir encoding**

Se o arquivo tem problemas de encoding:

```bash
# Mac/Linux
# Converter para UTF-8
iconv -f ISO-8859-1 -t UTF-8 .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md > /tmp/fixed.md
mv /tmp/fixed.md .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md

# Windows (PowerShell)
# Converter para UTF-8
$file = ".kiro\prompt-logs\$(git rev-parse --abbrev-ref HEAD).md"
$content = Get-Content $file -Encoding Default
$content | Out-File -Encoding UTF8 $file
```

**Solução 4: Restaurar de backup**

Se você tem um backup anterior:

```bash
# Restaurar do backup
cp .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md.bak .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md

# Ou restaurar do Git
git checkout .kiro/prompt-logs/$(git rev-parse --abbrev-ref HEAD).md
```

---

### Problema 4: Erros ao executar o script manualmente

**Sintomas:**
- Erro ao executar `python .kiro/scripts/log_prompt.py`
- Mensagem de erro: "ModuleNotFoundError: No module named 'pytz'"
- Mensagem de erro: "Permission denied"
- Mensagem de erro: "FileNotFoundError"

**Causas Possíveis:**
1. Python não está instalado ou não está no PATH
2. Dependência `pytz` não está instalada
3. Script não tem permissão de execução
4. Caminho do arquivo está incorreto
5. Git não está configurado

**Passos de Diagnóstico:**

```bash
# 1. Verificar se Python está instalado
python --version
python3 --version

# 2. Verificar se pytz está instalado
pip list | grep pytz
pip3 list | grep pytz

# 3. Verificar permissões do script
ls -la .kiro/scripts/log_prompt.py

# 4. Verificar se Git está configurado
git config user.name
git config user.email

# 5. Verificar branch atual
git rev-parse --abbrev-ref HEAD
```

**Soluções:**

**Solução 1: Instalar Python**

Se Python não está instalado:

- **Windows**: Baixar em https://www.python.org/downloads/
- **Mac**: `brew install python3`
- **Linux**: `sudo apt-get install python3`

**Solução 2: Instalar pytz**

```bash
# Instalar via pip
pip install pytz

# Ou via pip3
pip3 install pytz

# Verificar instalação
python -c "import pytz; print('OK')"
```

**Solução 3: Dar permissão de execução**

```bash
# Mac/Linux
chmod +x .kiro/scripts/log_prompt.py

# Verificar
ls -la .kiro/scripts/log_prompt.py
```

**Solução 4: Configurar Git**

```bash
# Configurar nome
git config user.name "Seu Nome"

# Configurar email
git config user.email "seu.email@example.com"

# Verificar
git config user.name
git config user.email
```

**Solução 5: Executar com caminho absoluto**

```bash
# Usar caminho absoluto em vez de relativo
python /caminho/completo/para/.kiro/scripts/log_prompt.py

# Ou navegar até o diretório
cd /caminho/completo/para/projeto
python .kiro/scripts/log_prompt.py
```

**Solução 6: Usar Python 3 explicitamente**

```bash
# Se python não funciona, tente python3
python3 .kiro/scripts/log_prompt.py

# Ou pip3
pip3 install pytz
```

---

### Problema 5: Conflitos de merge em arquivos de log

**Sintomas:**
- Mensagem de erro ao fazer merge: "CONFLICT in .kiro/prompt-logs/feature-*.md"
- Arquivo contém marcadores de conflito (`<<<<<<<`, `=======`, `>>>>>>>`)
- Impossível fazer merge automático

**Causas Possíveis:**
1. Duas pessoas trabalharam na mesma branch simultaneamente
2. Rebase com conflitos
3. Merge de branches que modificaram o mesmo arquivo de log

**Passos de Diagnóstico:**

```bash
# 1. Ver status do merge
git status

# 2. Ver conflitos
git diff --name-only --diff-filter=U

# 3. Ver conteúdo do arquivo com conflito
cat .kiro/prompt-logs/feature-*.md | grep -A 5 -B 5 "<<<<<<<" 
```

**Soluções:**

**Solução 1: Aceitar ambas as mudanças**

Como o formato é incremental (append), você pode aceitar ambas:

```bash
# 1. Abrir o arquivo com conflito
code .kiro/prompt-logs/feature-*.md

# 2. Remover marcadores de conflito
# Remover: <<<<<<<, =======, >>>>>>>

# 3. Manter ambas as seções de prompts

# 4. Salvar e fazer commit
git add .kiro/prompt-logs/feature-*.md
git commit -m "resolve: merge de logs de prompts"
```

**Solução 2: Usar ferramenta de merge visual**

```bash
# Usar ferramenta visual (se configurada)
git mergetool .kiro/prompt-logs/feature-*.md

# Ou usar VS Code
code --merge .kiro/prompt-logs/feature-*.md
```

**Solução 3: Aceitar versão local ou remota**

```bash
# Aceitar versão local (sua branch)
git checkout --ours .kiro/prompt-logs/feature-*.md

# Ou aceitar versão remota (branch sendo mergeada)
git checkout --theirs .kiro/prompt-logs/feature-*.md

# Depois fazer commit
git add .kiro/prompt-logs/feature-*.md
git commit -m "resolve: merge de logs"
```

**Solução 4: Recriar arquivo de log**

Se o arquivo está muito corrompido:

```bash
# 1. Remover arquivo com conflito
rm .kiro/prompt-logs/feature-*.md

# 2. Recriar com cabeçalho
branch=$(git rev-parse --abbrev-ref HEAD)
cat > .kiro/prompt-logs/$branch.md << EOF
# Prompt Logs: $branch

Histórico de prompts executados no Kiro nesta branch.

---
EOF

# 3. Fazer commit
git add .kiro/prompt-logs/$branch.md
git commit -m "resolve: recria arquivo de log após conflito de merge"
```

---

### Problema 6: Arquivo de log muito grande ou lento

**Sintomas:**
- Arquivo `.kiro/prompt-logs/<branch>.md` muito grande (> 10MB)
- Demora para abrir o arquivo no editor
- Demora para fazer grep ou buscar no arquivo
- Git fica lento ao fazer operações

**Causas Possíveis:**
1. Muitos prompts acumulados (centenas ou milhares)
2. Prompts com conteúdo muito grande
3. Arquivo não foi arquivado ou rotacionado
4. Sem compressão ou limpeza periódica

**Passos de Diagnóstico:**

```bash
# 1. Verificar tamanho do arquivo
du -h .kiro/prompt-logs/feature-*.md

# 2. Contar número de prompts
grep -c "## Prompt:" .kiro/prompt-logs/feature-*.md

# 3. Ver tamanho total de logs
du -sh .kiro/prompt-logs/

# 4. Listar arquivos por tamanho
ls -lhS .kiro/prompt-logs/
```

**Soluções:**

**Solução 1: Arquivar logs antigos**

```bash
# 1. Criar diretório de arquivo
mkdir -p .kiro/prompt-logs/archive

# 2. Mover logs antigos (mais de 3 meses)
find .kiro/prompt-logs -name "*.md" -mtime +90 -exec mv {} .kiro/prompt-logs/archive/ \;

# 3. Comprimir arquivo
tar -czf .kiro/prompt-logs/archive-$(date +%Y%m).tar.gz .kiro/prompt-logs/archive/

# 4. Remover originais
rm -rf .kiro/prompt-logs/archive/*.md
```

**Solução 2: Limpar prompts duplicados**

```bash
# 1. Identificar duplicatas
sort .kiro/prompt-logs/feature-*.md | uniq -d

# 2. Remover duplicatas (cuidado!)
sort .kiro/prompt-logs/feature-*.md | uniq > /tmp/cleaned.md
mv /tmp/cleaned.md .kiro/prompt-logs/feature-*.md
```

**Solução 3: Dividir arquivo grande em múltiplos**

```bash
# 1. Contar linhas
wc -l .kiro/prompt-logs/feature-*.md

# 2. Dividir em múltiplos arquivos (ex: 1000 linhas cada)
split -l 1000 .kiro/prompt-logs/feature-*.md .kiro/prompt-logs/feature-*.md.part

# 3. Renomear partes
for file in .kiro/prompt-logs/feature-*.md.part*; do
  mv "$file" "${file%.part*}-$(date +%Y%m%d).md"
done
```

**Solução 4: Implementar rotação automática**

Criar script para rotação automática:

```bash
# Criar script de rotação
cat > .kiro/scripts/rotate_logs.py << 'EOF'
#!/usr/bin/env python3
import os
import gzip
import shutil
from datetime import datetime, timedelta

LOG_DIR = ".kiro/prompt-logs"
ARCHIVE_DIR = f"{LOG_DIR}/archive"
MAX_SIZE = 10 * 1024 * 1024  # 10MB
RETENTION_DAYS = 90

os.makedirs(ARCHIVE_DIR, exist_ok=True)

for file in os.listdir(LOG_DIR):
    if not file.endswith(".md"):
        continue
    
    filepath = os.path.join(LOG_DIR, file)
    size = os.path.getsize(filepath)
    
    if size > MAX_SIZE:
        # Comprimir e mover para arquivo
        archive_name = f"{file}.{datetime.now().strftime('%Y%m%d')}.gz"
        archive_path = os.path.join(ARCHIVE_DIR, archive_name)
        
        with open(filepath, 'rb') as f_in:
            with gzip.open(archive_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Recriar arquivo com cabeçalho
        branch = file.replace(".md", "")
        with open(filepath, 'w') as f:
            f.write(f"# Prompt Logs: {branch}\n\n")
            f.write("Histórico de prompts executados no Kiro nesta branch.\n\n")
            f.write("---\n")
        
        print(f"Arquivado: {archive_name}")

# Limpar arquivos antigos
cutoff_date = datetime.now() - timedelta(days=RETENTION_DAYS)
for file in os.listdir(ARCHIVE_DIR):
    filepath = os.path.join(ARCHIVE_DIR, file)
    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
    if mtime < cutoff_date:
        os.remove(filepath)
        print(f"Removido: {file}")
EOF

# Executar script
python .kiro/scripts/rotate_logs.py
```

---

### Checklist de Troubleshooting

Use este checklist para diagnosticar problemas:

- [ ] Hook está instalado em `.kiro/hooks/prompt-logger.json`
- [ ] Script existe em `.kiro/scripts/log_prompt.py`
- [ ] Python 3.8+ está instalado
- [ ] Dependência `pytz` está instalada
- [ ] Git está configurado (user.name e user.email)
- [ ] Diretório `.kiro/prompt-logs/` existe
- [ ] Arquivo de log tem permissão de leitura/escrita
- [ ] Arquivo de log tem encoding UTF-8
- [ ] Kiro foi reiniciado após instalar dependências
- [ ] Nenhum firewall ou antivírus está bloqueando o script

---

## ⚠️ Limitações Conhecidas

Este sistema de prompt logging possui algumas limitações técnicas que você deve estar ciente. Estas limitações são documentadas para ajudar no uso efetivo do sistema e no planejamento de melhorias futuras.

### 1. ❌ Captura de Conteúdo do Prompt (VALIDADO - 31/05/2026)

**Limitação:** O Kiro **NÃO expõe o conteúdo do prompt** via variáveis de ambiente, stdin ou argumentos de linha de comando no contexto do hook `promptSubmit`.

**Validação Técnica (Testes Realizados):**
- ❌ stdin: É um terminal interativo (TTY), sem dados disponíveis
- ❌ Variáveis de ambiente: `KIRO_PROMPT` e `USER_PROMPT` não estão disponíveis
- ❌ Argumentos CLI: Script executado sem argumentos
- ❌ Contexto do hook: Nenhuma variável Kiro específica disponível
- ✅ File descriptors: Disponíveis, mas sem dados do prompt

**Causa Técnica:** 
- O hook `promptSubmit` é acionado pelo Kiro, mas é executado em contexto isolado
- stdin é um terminal interativo, não um pipe com dados
- O Kiro não passa o conteúdo do prompt ao script do hook
- Isso é uma limitação da implementação atual do Kiro, não do script de logging

**Impacto:** 
- Logs contêm apenas metadados (branch, usuário, timestamp) sem o conteúdo real do prompt
- Arquivo de log terá a seção "Prompt original" com placeholder
- Reduz a utilidade dos logs para rastreabilidade completa

**Exemplo de Impacto:**
```markdown
## Prompt: [Conteúdo não capturado]
- Responsável: Michele Oliveira
- Branch: feature-compliance
- Data/hora: 2026-05-29 14:35:22 (Brasília - UTC-3)

### Prompt original
```
[Conteúdo do prompt não capturado automaticamente - limitação do Kiro]
```
```

**Workarounds Disponíveis:**
1. **Adicionar manualmente:** Editar o arquivo de log e adicionar o conteúdo do prompt manualmente
2. **Documentar no commit:** Incluir o conteúdo do prompt na mensagem de commit
3. **Usar comentários:** Adicionar comentários no código referenciando o prompt
4. **Consultar histórico:** Verificar o histórico do Kiro para recuperar o prompt

**Testes Realizados:**
- Script: `.kiro/scripts/test_stdin_availability.py`
- Relatório: `.kiro/reports/stdin_availability_report.md`
- Análise: `.kiro/reports/stdin_analysis_and_recommendations.md`
- Documentação: `.kiro/reports/CAPTURE_TESTS_DOCUMENTATION.md`

**Mitigação Planejada:** 
- Solicitar ao Kiro que exponha conteúdo do prompt via variável de ambiente
- Implementar captura via clipboard como alternativa
- Fase 2 pode incluir integração mais profunda com o Kiro

---

### 2. Filtragem Automática de Prompts Triviais

**Limitação:** O sistema filtra automaticamente prompts muito curtos ou triviais para evitar ruído nos logs.

**Critério de Filtragem:**
- Prompts com menos de 10 caracteres são ignorados
- Confirmações simples ("sim", "ok", "entendido") não são registradas
- Respostas vazias não são registradas
- Comandos de navegação ("próximo", "voltar", "sair") não são registradas

**Impacto:**
- Alguns prompts não aparecerão nos logs
- Histórico completo de interações pode estar incompleto
- Útil para manter logs limpos, mas pode perder contexto em alguns casos

**Exemplo de Prompts Filtrados:**
```
"sim"                    ❌ Não registrado (confirmação simples)
"ok"                     ❌ Não registrado (confirmação simples)
"próximo"                ❌ Não registrado (comando de navegação)
""                       ❌ Não registrado (vazio)
"Implementar API"        ✅ Registrado (suficientemente descritivo)
"Corrigir bug"           ✅ Registrado (suficientemente descritivo)
```

**Justificativa:** Manter logs focados em interações significativas, evitando poluição com confirmações triviais.

**Workaround:** Se você precisa registrar um prompt trivial, adicione contexto adicional para atingir o mínimo de 10 caracteres.

---

### 3. Falta de Captura de Resultados (MVP)

**Limitação:** O sistema MVP não captura o "resumo do resultado gerado pelo Kiro" ou a resposta do agente.

**Causa Técnica:** Capturar resultados requer:
- Hook `agentStop` para interceptar o fim da execução
- Acesso à resposta/output do agente
- Ambos podem não estar disponíveis na versão atual do Kiro

**Impacto:**
- Logs contêm apenas prompts (entrada), não respostas (saída)
- Não há rastreabilidade completa de prompt → resultado
- Dificulta análise de efetividade dos prompts

**Exemplo de Limitação:**
```markdown
## Prompt: Implementar endpoint de upload
- Responsável: Michele Oliveira
- Branch: feature-upload
- Data/hora: 2026-05-29 14:35:22 (Brasília - UTC-3)

### Prompt original
```
Implementar endpoint POST /api/v1/upload para receber arquivos CSV
```

### Resultado
[NÃO CAPTURADO NO MVP]
```

**Workaround:**
1. Adicionar manualmente um resumo do resultado ao arquivo de log
2. Documentar o resultado em comentários de código
3. Referenciar commits que implementaram o resultado

**Planejado:** Fase 2 com hook `agentStop` para capturar resultados automaticamente.

---

### 4. Crescimento Indefinido de Arquivos de Log

**Limitação:** Arquivos de log crescem indefinidamente com o modo append, sem rotação ou arquivamento automático.

**Causa Técnica:** O sistema MVP implementa apenas append incremental. Não há mecanismo de rotação, compressão ou arquivamento automático.

**Impacto:**
- Arquivos de log podem crescer muito (centenas de MB em branches ativas)
- Arquivos grandes são lentos para abrir/editar em editores de texto
- Operações de grep/busca podem ficar lentas
- Git pode ficar lento ao fazer operações em repositórios com logs muito grandes

**Exemplo de Crescimento:**
```
Semana 1:  50 KB  (10 prompts)
Semana 4:  200 KB (40 prompts)
Mês 1:     800 KB (160 prompts)
Mês 3:     2.4 MB (480 prompts)
Mês 6:     4.8 MB (960 prompts)
Ano 1:     9.6 MB (1920 prompts)
```

**Workarounds Disponíveis:**
1. **Arquivamento manual:** Mover logs antigos para diretório de arquivo
2. **Compressão:** Comprimir logs antigos com gzip
3. **Limpeza periódica:** Remover logs muito antigos (> 1 ano)
4. **Rotação automática:** Implementar script de rotação (ver seção Troubleshooting)

**Recomendação:** Para branches muito ativas, considere implementar rotação automática a cada 3-6 meses.

**Planejado:** Fase 4 com rotação automática e política de retenção configurável.

---

### 5. Conflitos de Merge em Arquivos de Log

**Limitação:** Se duas pessoas trabalharem na mesma branch simultaneamente, pode haver conflitos de merge no arquivo de log.

**Causa Técnica:** Ambas as pessoas adicionam entradas ao mesmo arquivo `.kiro/prompt-logs/<branch>.md`, resultando em conflitos quando fazem merge.

**Impacto:**
- Conflitos de merge ao fazer rebase ou merge
- Requer resolução manual de conflitos
- Pode ser confuso para desenvolvedores menos experientes

**Exemplo de Conflito:**
```markdown
<<<<<<< HEAD
## Prompt: Implementar validação
- Responsável: Michele Oliveira
- Branch: feature-compliance
- Data/hora: 2026-05-29 14:35:22 (Brasília - UTC-3)

### Prompt original
```
Implementar validação de ranges
```
=======
## Prompt: Criar testes
- Responsável: João Silva
- Branch: feature-compliance
- Data/hora: 2026-05-29 14:40:15 (Brasília - UTC-3)

### Prompt original
```
Criar testes unitários para compliance
```
>>>>>>> feature-compliance
```

**Impacto Prático:** Baixo - formato incremental facilita resolução manual (aceitar ambas as mudanças).

**Solução:** Aceitar ambas as mudanças ao resolver conflito, pois o formato permite múltiplas entradas.

**Recomendação:** Usar branches de curta duração para minimizar conflitos.

**Planejado:** Fase 3 com estratégia de merge automático para logs.

---

### 6. Dependência de Git Configurado

**Limitação:** O sistema depende de Git estar instalado e configurado com `user.name` e `user.email`.

**Causa Técnica:** O script de logging usa comandos Git para detectar branch e usuário.

**Impacto:**
- Se Git não estiver configurado, o sistema usa fallbacks ("unknown-branch", "Unknown User")
- Logs podem não ter informações de responsável corretas
- Fora de repositório Git, o sistema não funciona

**Workaround:**
```bash
# Configurar Git globalmente
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"

# Ou por repositório
git config user.name "Seu Nome"
git config user.email "seu.email@example.com"
```

**Impacto Prático:** Baixo - Git é obrigatório no projeto de qualquer forma.

---

### 7. Sem Suporte a Múltiplos Repositórios

**Limitação:** O sistema assume um único repositório Git. Não há suporte para monorepos ou múltiplos repositórios.

**Causa Técnica:** O script detecta apenas a branch do repositório atual via `git rev-parse`.

**Impacto:**
- Em monorepos, todos os logs vão para o mesmo arquivo de branch
- Não há isolamento por subprojeto ou workspace
- Pode ser confuso em estruturas complexas

**Workaround:** Usar branches com nomes descritivos que incluam o subprojeto:
```
feature/backend-compliance-score
feature/frontend-dashboard
feature/ml-prediction
```

**Planejado:** Fase 3 com suporte a múltiplos repositórios/workspaces.

---

### 8. Sem Criptografia de Logs

**Limitação:** Logs são armazenados em texto plano sem criptografia.

**Causa Técnica:** MVP não implementa criptografia de dados.

**Impacto:**
- Dados sensíveis em prompts podem ser expostos
- Não adequado para dados altamente confidenciais
- Requer cuidado ao compartilhar repositório

**Recomendação:**
1. **Revisar logs antes de commits** em repositórios públicos
2. **Não incluir dados sensíveis** em prompts (tokens, senhas, chaves)
3. **Usar variáveis de ambiente** para dados sensíveis
4. **Adicionar `.kiro/prompt-logs/` ao `.gitignore`** se necessário

**Planejado:** Fase 5 com criptografia opcional de logs sensíveis.

---

### Resumo de Limitações

| # | Limitação | Severidade | Impacto | Workaround | Fase |
|---|-----------|-----------|--------|-----------|------|
| 1 | Captura de conteúdo | Alta | Logs sem conteúdo | Adicionar manualmente | 2 |
| 2 | Filtragem de triviais | Baixa | Alguns prompts ignorados | Adicionar contexto | MVP |
| 3 | Sem captura de resultados | Média | Sem rastreabilidade completa | Documentar manualmente | 2 |
| 4 | Crescimento indefinido | Média | Arquivos grandes | Arquivar manualmente | 4 |
| 5 | Conflitos de merge | Baixa | Requer resolução manual | Aceitar ambas | 3 |
| 6 | Dependência de Git | Baixa | Fallback para "unknown" | Configurar Git | MVP |
| 7 | Sem múltiplos repos | Baixa | Confusão em monorepos | Usar nomes descritivos | 3 |
| 8 | Sem criptografia | Média | Dados sensíveis expostos | Revisar antes de commit | 5 |

---

### Roadmap de Melhorias

**Fase 1 (MVP - Atual):** Captura básica de prompts, organização por branch

**Fase 2:** Captura de resultados, interface de consulta

**Fase 3:** Suporte a múltiplos repositórios, merge automático de logs

**Fase 4:** Rotação automática de logs, política de retenção

**Fase 5:** Criptografia opcional, integração com ferramentas de análise

---

### Como Reportar Limitações Encontradas

Se você encontrar outras limitações não documentadas aqui, abra uma issue:

```bash
gh issue create \
  --title "Prompt Logging: Limitação encontrada - [descrição]" \
  --body "Descrição da limitação e impacto" \
  --label "prompt-logging,limitation"
```

---

## 🔐 Segurança e Privacidade

### Dados Registrados

- ✅ Branch Git (não sensível)
- ✅ Nome do usuário Git (não sensível)
- ✅ Timestamp (não sensível)
- ✅ Conteúdo do prompt (pode conter informações do projeto)

### Dados NÃO Registrados

- ❌ Tokens de API
- ❌ Senhas
- ❌ Chaves privadas
- ❌ Variáveis de ambiente sensíveis

### Recomendações

1. **Revisar logs antes de commits** em repositórios públicos
2. **Não incluir dados sensíveis** em prompts
3. **Adicionar `.kiro/prompt-logs/` ao `.gitignore`** se necessário (decisão do projeto)
4. **Usar variáveis de ambiente** para dados sensíveis

---

## 📚 Referências

- [Kiro Documentation](https://kiro.dev/docs)
- [Git Flow do Projeto](.kiro/steering/gitflow.md)
- [Estrutura do Projeto](.kiro/steering/structure.md)
- [Design Técnico](.kiro/specs/prompt-logging/design.md)
- [Requisitos](.kiro/specs/prompt-logging/requirements.md)

---

## 💡 Próximos Passos

### Fase 2: Melhorias Futuras

- [ ] Captura de resultados com hook `agentStop`
- [ ] Interface de consulta de logs (CLI)
- [ ] Filtros por data, branch, usuário
- [ ] Exportação para JSON/CSV
- [ ] Rotação automática de logs antigos
- [ ] Dashboard de análise de prompts

### Feedback

Se você tiver sugestões ou encontrar problemas, abra uma issue no repositório:

```bash
gh issue create --title "Prompt Logging: [descrição]" --body "[detalhes]"
```

---

**Versão:** 1.0.0  
**Data:** 27 de Maio de 2026  
**Status:** ✅ Documentação Completa  
**Timezone:** America/Sao_Paulo (UTC-3)  
**Idioma:** Português Brasileiro (pt-BR)
