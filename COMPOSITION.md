# COMPOSITION — como as peças trabalham juntas (sem conflito, sem desperdício)

Este é o diferencial do kit. Curar não é só escolher boas ferramentas — é garantir que elas
**convivam**: sem redundância, sem brigar pelo mesmo gatilho, sem estourar o contexto.

## As 10 regras

1. **CLI > MCP quando equivalem.** MCP custa 4–32x mais tokens que a CLI. Ex: `gh` para commit/PR,
   não o GitHub MCP. Só use MCP quando read/grep/CLI **não** resolvem.
2. **Nenhum orquestrador pesado.** `superpowers` e `gsd-core` ficam fora. A disciplina de trabalho
   vem de Karpathy+Ponytail (always-on, leve) + skills de fluxo opt-in (mattpocock). Nada auto-injeta
   processo a cada turno.
3. **Um dono por princípio.** Karpathy+Ponytail é a **única** fonte do princípio de enxugamento
   (YAGNI/KISS). Nenhuma outra skill repete essa regra no mesmo prompt — senão geram instruções
   contraditórias.
4. **Um MCP por motor de banco por conexão.** Não ligar dois MCPs que cobrem o mesmo Postgres — é
   contexto dobrado para a mesma coisa. `nautilus` cobre leitura multi-DB; escrita só na área de migrations.
5. **Segredo nunca vai bruto ao agente.** Secrets por MCP read-only / injeção via env (Infisical),
   nunca `read_secret` jogando credencial no contexto.
6. **Migration nunca aplica sem aprovação.** Preferir branching (Neon) ou preview antes de `apply`.
   O agente propõe o diff da migration; quem aplica é você.
7. **Observabilidade e cloud = categoria multi-vendor.** Ligar só o do time (Grafana hub, ou
   Sentry/Datadog/CloudWatch conforme o caso). Nunca travar num fornecedor fixo.
8. **Um só gate de design por tela.** `ui-ux-pro-max` **cria**, `web-design-guidelines` **revisa**.
   `frontend-design` entra como camada anti-"cara de IA" — **não** como segundo gate estético
   disparando junto com o ui-ux-pro-max.
9. **Uma biblioteca de ícones fixa.** Escolha uma (ex: Lucide) e fixe no AGENTS.md para o agente não
   misturar estilos. `better-icons` busca; o AGENTS.md manda no estilo.
10. **Não duplicar memória.** AGENTS.md + rules/ são a memória **local** do projeto (fonte da verdade).
    MCP de memória externo, se usado, é só para o que **atravessa** projetos — nunca repetir o que já
    está no AGENTS.md.

## Pares que se complementam (não são redundância)

| Par | Papel de cada um |
|---|---|
| `ui-ux-pro-max` + `web-design-guidelines` | criar · revisar |
| `shadcn` (skill) + `frontend-design` | quais componentes/código · decisões estéticas |
| `e2e-browser-qa` + `Playwright MCP`/`Chrome DevTools MCP` | orquestra o QA · driver de browser/evidência |
| `webapp-testing` + `Playwright MCP` | suíte reproduzível p/ CI · exploração ad-hoc |
| `nautilus` (read) + área de migrations (write) | ler dados/esquema · aplicar mudança com aprovação |
| `/security-review` + `cloudflare-audit` + `Semgrep` | rápido no diff · auditoria profunda · SAST contínuo |
| `CodeGraph` + `Context7` | mapa do SEU código · docs das libs de terceiros |

## Redundâncias resolvidas (o que ficou de fora e por quê)

- **shadcn MCP** → fora no Claude Code (a **skill** já busca+instala via CLI). Só vale sem Bash.
- **GitHub MCP** → não para commit/PR diário (use `gh` + conventional-commit). Fica só para
  Actions/code-scanning/Projects.
- **superpowers / gsd-core** → orquestradores pesados, contra a filosofia. Fora.
- **frontend-design vs ui-ux-pro-max** → não rodam como dois gates; ui-ux-pro-max lidera o "criar",
  frontend-design é camada de taste opcional.

## Global × Projeto

| Fica GLOBAL (`~/.claude`) | Fica no PROJETO (`.claude/`) |
|---|---|
| Disciplina (Karpathy+Ponytail), using-mcps-well | AGENTS.md, rules/ do projeto |
| Skills de fluxo (to-spec, diagnosing-bugs, code-review) | Config dos MCPs da stack |
| `fullstack-setup`, `project-learning`, `project-onboarding`, `documents` | Saída do onboarding, skills locais |
| conventional-commit, /security-review | — |
| **2 MCPs genéricos**: CodeGraph, Context7 | **Todos os outros MCPs** (ligados por stack) |

## Telemetria (sinalizada, mesmo sem perfil empresa ainda)

Itens marcados no manifest com `telemetry: operational|anonymous` mandam algum dado para fora:
Atlas (anônima — desligar com `ATLAS_NO_ANON_TELEMETRY=true`), Sentry/Datadog/Linear/Atlassian/Figma
(operacional). Num contexto corporativo sensível, avalie antes de ligar.
