# Compliance e Governança de Dados - BiotecPredict

Diretrizes de conformidade, rastreabilidade e qualidade de dados do BiotecPredict.
Este arquivo fornece contexto permanente ao agente Kiro sobre as regras de compliance do projeto.

---

## Disclaimer Obrigatório

**Todo output do sistema deve incluir o disclaimer:**

> "Esta análise é baseada em dados históricos de manufatura. Não constitui recomendação de ação. A decisão final sobre ações corretivas é sempre do operador."

- O disclaimer deve aparecer em **toda predição gerada pelo modelo ML**
- Deve estar visível no dashboard em todas as páginas de análise
- Nunca omitir ou encurtar o disclaimer em respostas da API

---

## Fontes de Dados — Conformidade de Uso

| Fonte | Tipo de uso permitido | Restrições |
|---|---|---|
| **Kaggle Dataset** | Dados públicos para uso educativo e pesquisa | Respeitar licença do dataset; não redistribuir dados brutos |
| **Sensores Industriais** | Dados de processo para análise | Dados anonimizados; sem informações de identificação pessoal |

**Regras de coleta:**
- Dados são coletados apenas para processamento interno
- Não redistribuir dados brutos de fontes externas
- Manter rastreabilidade de origem dos dados

---

## Rastreabilidade das Fontes

Cada dado persistido no banco deve ter rastreabilidade de origem:

| Campo | Tabela | Fonte |
|---|---|---|
| `temperature`, `ph`, `dissolved_oxygen`, `pressure`, `agitator_speed` | `sensor_reading` | CSV Upload |
| `compliance_score` | `batch` | Cálculo determinístico (ComplianceService) |
| `risk_prediction` | `batch` | RandomForestClassifier (MLService) |
| `upload_date`, `status` | `batch` | Sistema (timestamp automático) |

> Não existe tabela `prediction` separada. O resultado do ML é persistido diretamente no campo `risk_prediction` da tabela `batch`, calculado durante o processamento do upload.

---

## Política de Retenção de Dados

| Tabela | Retenção | Justificativa |
|---|---|---|
| `batch` | 2 anos | Histórico de manufatura + compliance + risco |
| `sensor_reading` | 2 anos | Análise de tendências e auditoria |

**Limpeza periódica:** executar trimestralmente via script de manutenção.

---

## Qualidade dos Dados — Regras de Validação

### Indicadores de Sensores (ranges esperados)

| Indicador | Range válido | Ação se fora do range |
|---|---|---|
| Temperature | 20 a 45 °C | Log de anomalia; não persistir |
| pH | 4.0 a 9.0 | Log de anomalia; não persistir |
| Dissolved Oxygen | 0 a 100 % | Log de anomalia; não persistir |
| Pressure | 0 a 10 bar | Log de anomalia; não persistir |
| Agitator Speed | 0 a 500 RPM | Log de anomalia; não persistir |

### Regra de mínimo de dados
- Todo batch deve ter **≥ 5 leituras de sensores** válidas
- Verificação automática ao processar CSV
- Batches que não atingirem o mínimo são rejeitados com mensagem clara

---

## Auditoria e Monitoramento

### Logs obrigatórios
- Toda coleta de dados (fonte, timestamp, usuário)
- Erros de validação com código e mensagem
- Batches rejeitados (motivo e data)
- Scores calculados com valores de entrada
- Predições geradas (modelo, confiança, latência)

### Relatórios automáticos

Avisos e resultados de processamento são retornados diretamente na resposta da API (campo `warnings` interno ao `BatchService`). Não há geração de arquivos de relatório em disco — a pasta `backend/reports/` foi removida do projeto.

---

## Segurança

- `DATABASE_URL` nunca no código — sempre via variável de ambiente
- Arquivo `.env` no `.gitignore` — nunca versionado
- Banco SQLite local não versionado (arquivo .db no .gitignore)
- Logs não devem conter dados sensíveis

---

## Contexto para o Agente Kiro

Ao trabalhar neste projeto:

1. **Sempre incluir o disclaimer** em predições geradas pelo modelo ML
2. **Validar ranges** antes de persistir dados de sensores no banco
3. **Registrar a fonte** de cada dado coletado nos logs
4. **Nunca expor** chaves de API, senhas ou tokens em código ou logs
5. **Transparência obrigatória** — o campo `confidence_score` deve sempre refletir a confiança da predição; o frontend deve exibir essa informação ao usuário
6. **Rastreabilidade completa** — manter histórico de todas as operações para auditoria

---

**Versão**: 0.1.0  
**Data**: 24 de Maio de 2026  
**Status**: ✅ Compliance Definido