# Design system, BiotecPredict (frontend)

Este documento descreve a linguagem visual usada em `src/`. É a mesma
linguagem do produto irmão **Root-Spector** (mesma paleta, tipografia e
escala de controles), padronizada entre os dois produtos de propósito
industrial/biotecnologia — a única diferença deliberada é a arte de
marca (logo), que é própria de cada produto.

Superfície do produto clara e neutra, roxo cheio reservado ao botão de
ação (nunca como preenchimento de área grande), e o semáforo dos
indicadores de compliance/risco como o único elemento colorido de peso.
Alvos grandes (48 pixels de altura mínima) e nenhuma informação depende
só da cor, porque quem usa o sistema está no piso de produção.

## Onde vive

- `src/styles/tokens.css`: todas as CSS custom properties (cores,
  tipografia, altura de controle, raio de borda, sombra). Único lugar
  com valores de cor hardcoded; todo o resto do CSS consome
  `var(--token)`.
- `src/index.css`: reset global, tipografia base (`h1`–`h3`, `p`, `a`),
  controles (`button`, `input`, `select`, `textarea`) e a classe de
  badge genérica (`.badge`, `.badge--ok/warn/critical/neutral`).
  Importa `tokens.css`.
- CSS por componente (`Dashboard.css`, `UploadCard.css`,
  `*.module.css` de `Layout`/`Navigation`/páginas): layout específico de
  cada tela, sempre consumindo os tokens — nenhuma cor hardcoded fora de
  `tokens.css`.

## Paleta e tema

Superfície única, clara e neutra (`color-scheme: light` em
`tokens.css`), não segue o tema do sistema operacional. Nenhum
componente decide cor por conta própria, todos leem os tokens
(`--paper`, `--ink`, `--accent`, etc.), então a paleta muda sem tocar em
`index.css` ou nos componentes.

| Token | Uso |
|---|---|
| `--paper` / `--paper-raised` / `--paper-sunken` | fundo da página / fundo dos cards / campos e cabeçalho de tabela |
| `--ink` / `--ink-soft` | texto principal / texto secundário |
| `--line` / `--line-soft` | bordas e divisores |
| `--accent` / `--accent-ink` / `--accent-soft` | cor de marca (botão primário, links, nav ativa) |
| `--accent-deep` / `--accent-border` | texto sobre `--accent-soft` / borda discreta em acento |
| `--accent-art` | reservado à arte da logo própria do BiotecPredict, sem contraste suficiente sobre branco pra uso em texto/borda |
| `--accent-hover` / `--accent-active` | estado de hover / clique do botão primário |
| `--control-height` / `--field-height` | altura mínima de botão (48px) / campo de resposta (52px) |
| `--control-border` / `--control-border-strong` | borda padrão / borda em hover de campos e botão secundário |
| `--disabled-bg` / `--disabled-fg` | fundo e texto de controle desabilitado |
| `--shadow` / `--shadow-lg` | sombra sutil dos cards |

### Cores "semáforo"

Nunca vermelho/amarelo/verde saturados, sempre fundo pastel, borda na
mesma família de cor e texto legível. No dashboard, o compliance score
e a predição de risco usam essas cores via `getStatusTone()` /
`getRiskTone()` em `Dashboard.tsx`, que mapeiam o valor da API
(`ACCEPTABLE`/`WARNING`/`CRITICAL`, `LOW_RISK`/`MEDIUM_RISK`/`HIGH_RISK`)
para um tom (`ok`/`warn`/`critical`/`neutral`) e o aplicam via variáveis
CSS locais (`--badge-bg`/`--badge-border`/`--badge-fg`), nunca com cor
hardcoded no componente:

| Token (bg/border/fg) | Significado | Usado em |
|---|---|---|
| `--ok-bg` / `--ok-border` / `--ok-fg` | aceitável / baixo risco | badges de compliance/risco, `.badge--ok`, `.feedback-success` |
| `--warn-bg` / `--warn-border` / `--warn-fg` | atenção / risco médio | badges, `.disclaimer` |
| `--critical-bg` / `--critical-border` / `--critical-fg` | crítico / alto risco | badges, `.error-banner`, `.feedback-error` |
| `--neutral-bg` / `--neutral-border` / `--neutral-fg` | classificação não mapeada / sem dado | `.status-badge`, badge de score ausente |

## Tipografia

Duas famílias, carregadas via Google Fonts em `index.html`, cada uma
com um papel fixo (mesmo carregamento do Root-Spector):

- **Sans** (`--font-sans`, Inter): corpo do texto e títulos (`h1`, `h2`,
  peso 500, `card-title`, `sensor-name`).
- **Mono** (`--font-mono`, JetBrains Mono): rótulos curtos em caixa alta
  com letter-spacing — `h3`, `.section-title`, cabeçalho de tabela,
  badges, `batch-id`, unidades de sensor. Sinaliza "metadado", não texto
  de leitura corrida.

## Padrões de layout e componentes

- Todo bloco de conteúdo (KPI card, sensor card, seção de histórico de
  batches, área de upload) segue o mesmo desenho: `--paper-raised`,
  borda `--line`, `border-radius: var(--radius)`, `box-shadow:
  var(--shadow)`.
- Badges (`.badge`, `.card-badge`, `.score-badge`, `.risk-badge`,
  `.status-badge`): pílula (`border-radius: 100px`), fundo pastel, borda
  na mesma família, texto em mono, com um ponto sólido (`::before`)
  reforçando o estado pra quem não distingue bem as cores.
- Alertas (`.error-banner`, `.disclaimer`, `.feedback-success`/`.feedback-error`):
  mesmo padrão de fundo pastel + borda + texto da cor do estado.
- Botões: retângulo cheio de `--accent` com texto branco é a única ação
  primária por tela; `.retry-button`/`.pagination-button` seguem a
  mesma altura mínima (`--control-height`) e raio (`--radius-sm`).
- Navegação (`Navigation.module.css`): barra clara (`--paper-raised`)
  com borda inferior sutil, sem faixa escura — item ativo/hover em
  `--accent-soft` + `--accent-ink`.

## Adicionando um novo componente

1. Todo bloco de conteúdo deve ter `background: var(--paper-raised)`,
   `border: 1px solid var(--line)`, `border-radius: var(--radius)` e
   `box-shadow: var(--shadow)` — não redefina esses valores.
2. Use `h1`/`h2`/`h3` para títulos: nunca defina `font-family` inline,
   os estilos já vêm de `index.css`.
3. Se o componente exibir uma classificação/risco vindo da API, mapeie
   para um tom (`ok`/`warn`/`critical`/`neutral`) como em
   `getStatusTone()`/`getRiskTone()` em `Dashboard.tsx`: não crie uma
   nova cor.
4. Qualquer cor nova (fundo, texto, borda) deve ser adicionada como
   token em `tokens.css`, nunca como valor hardcoded no componente.
5. Nenhum controle interativo (botão, campo, link de ação) deve ter
   menos de 48 pixels de altura, ver `--control-height` / `--field-height`.
