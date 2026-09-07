# Changelog

Todas as mudanças notáveis deste projeto são documentadas neste arquivo.

## [v1.0.0] - 2026-09-07

Primeira release estável do BiotecPredict, consolidando o MVP entregue
como módulo avaliativo (upload de CSV, compliance score, predição de
risco, dashboard analítico) com identidade visual e licenciamento
próprios.

### feat

- Padroniza o design system do frontend com a mesma linguagem visual
  do Root-Spector: paleta, tipografia (Inter + JetBrains Mono) e escala
  de controles/raio/sombra, com semáforo de compliance/risco em tons
  tradicionais de verde/amarelo/vermelho.
- Adiciona a identidade visual própria do BiotecPredict: mark +
  wordmark no header, favicons, faixa de marca no topo do Dashboard e
  da tela de Upload, banner no README.

### fix

- Corrige o título do UploadCard, que herdava o estilo mono/uppercase
  global de `h3`.
- Corrige o círculo do Compliance Score, que cortava o valor para
  scores de 5 caracteres (ex. `92.39`).
- Separa os tokens de cor de texto (`--*-fg`) dos tokens de
  preenchimento sólido grande (`--*-strong`), evitando que o amarelo
  do semáforo aparecesse como mostarda/oliva no círculo e no ponto de
  confiança.

### chore

- Remove `App.module.css`, `Dashboard.module.css` (componente) e
  `UploadCard.module.css`: duplicatas mortas, nunca importadas.
- Muda a licença de Apache License 2.0 para Copyright / Todos os
  Direitos Reservados, mantendo a propriedade da ideia e do código.

### docs

- Atualiza os prints do README para refletir a identidade visual nova.
- Reorganiza o cabeçalho do README com o banner de marca.
