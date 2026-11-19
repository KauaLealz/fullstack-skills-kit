# Exemplo — um repo antes e depois do setup

Caso: helpdesk interno (Next.js + NestJS + Postgres), brownfield, time de 4 devs com develop→main.

## Antes
```
helpdesk/
  frontend/ · backend/ · docker-compose.yml · README.md (desatualizado)
```
Sem AGENTS.md. Cada sessão de agente redescobria como subir o app e qual era o padrão de módulo.

## Depois
```
helpdesk/
  AGENTS.md                      ← roteador (abre com o bloco do núcleo)
  CLAUDE.md                      ← @AGENTS.md
  .claude/
    fsk.json                     ← {kit 2.0, origem a1b2c3d, tracker github, 15/11}
    fsk.local.json               ← worktree_policy: ask (NO GITIGNORE)
    rules/
      api.md                     ← paths src/**/*.controller.ts · evidência+origem
      testing.md                 ← paths **/*.spec.ts
    skills/how-to-criar-modulo/  ← template concreto do módulo Nest do projeto
    specs/                       ← uma pasta por demanda
  .gitignore                     ← + bloco fsk (fsk.local.json, .worktrees/)
  frontend/ · backend/ · ...
```

## O AGENTS.md gerado (resumido — repare no que ele responde sem ninguém perguntar)
```markdown
<!-- fsk:start -->  (núcleo do workflow)  <!-- fsk:end -->

# Helpdesk — AGENTS
**Stack:** Next 14 (frontend/) · NestJS 10 (backend/) · Postgres 16 · pnpm

## Comandos (validados em 15/11)
subir tudo: `docker compose up -d && pnpm dev` · seed+login de teste: `pnpm seed` (admin@local/test123)
teste direcionado: `pnpm vitest related <arquivo>` · suíte: `pnpm test` · logs: `docker compose logs -f api`

## Fluxo de entrega
branch `feat|fix/<slug>` a partir de `develop` · PR p/ develop (template .github/) · squash · quem
mergeia: autor após 1 aprovação · release: develop→main sexta

## Mapa
| Domínio | Entrada | Centrais | Referência p/ copiar |
|---|---|---|---|
| Tickets | `backend/src/tickets/tickets.controller.ts` | `tickets.service.ts`, `ticket.entity.ts` | feature "comments" (PR #42) |
| Auth/SSO | `backend/src/auth/azure.strategy.ts` | `auth.guard.ts` | — (não mexer sem o Pedro) |

## Não ler
`**/dist`, `**/.next`, `pnpm-lock.yaml`, `backend/src/migrations/2023*`

## Crítico
SLA de resposta (tickets.service `calculateSla`) — mexeu, prova com os 3 cenários do seed.

## Vocabulário
**Ticket** = chamado do funcionário · **Fila** = equipe que atende (não é fila de mensageria) ·
**SLA estourado** = 1º status visível pro gestor

## Worktree (receita validada 15/11)
`python install/fsk.py worktree <slug>` → copia .env, `pnpm i`, portas 3100/3101 (compose override)
```

## Por que isso é um bom resultado de setup
Os comandos foram **rodados**, não copiados do README (que estava errado — o seed novo é `pnpm seed`).
O Fluxo de entrega veio da entrevista (develop→main não estava escrito em lugar nenhum). O Vocabulário
desarma a armadilha real do domínio ("fila" ≠ mensageria). Cada rule nasceu com 2+ evidências e carimbo.
E `fsk.local.json` ficou fora do git — preferência do dev não virou regra do time.
