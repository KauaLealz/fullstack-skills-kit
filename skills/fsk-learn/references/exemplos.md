# Exemplos — quando e como o aprendizado vira artefato

Caso-base: SaaS B2B de gestão de contratos (multi-tenant). Cinco cenários reais + contra-exemplos.

## 1. Correção do usuário → rule (na hora, com "ok")
Durante um build, o usuário corrige: *"nunca retorne entidade do TypeORM direto no controller, sempre DTO"*.
É convenção do time (vale além da demanda) → proposta no mesmo turno:

```markdown
---
paths:
  - "src/**/*.controller.ts"
---
# API — resposta sempre por DTO
- Controller nunca retorna entidade do ORM; mapeia para o DTO de resposta.
  (evidência: correção do usuário em 14/11 + padrão em `contracts.controller.ts:45`, `users.controller.ts:30`)

origem: e4f2a91
```
→ `.claude/rules/api.md`, gravada após o "ok". Repare: `paths` restringe a carga, evidência citada,
carimbo de origem.

## 2. Resposta de grill → preferência pessoal (global, nunca no git)
No ship, perguntado sobre formato de PR, o usuário responde "sem emoji no título, sempre".
Não é convenção do repo (o time usa emoji) — é gosto **dele** → memória global do usuário:
`PRs que eu abro: título sem emoji (preferência pessoal, 14/11)`. **Não** vira rule no repo.

## 3. Procedimento repetido 2× → how-to com template concreto
Segunda vez que se cria um relatório exportável no projeto. Vira skill de projeto:

```markdown
---
name: how-to-relatorio-exportavel
description: Criar um relatório exportável (CSV/PDF) do jeito deste projeto — query paginada + formatter + endpoint de export. Use ao criar qualquer tela/endpoint de relatório novo.
---
# Como criar relatório exportável (nosso jeito)
1. Query em `src/reports/queries/<nome>.query.ts` — copie `expiring-contracts.query.ts` (paginação keyset).
2. Formatter em `src/reports/formatters/` implementando `ReportFormatter` — copie `csv-contracts.formatter.ts`.
3. Endpoint: adicione o case em `reports.controller.ts:28` (switch de tipos) — NÃO crie controller novo.
Do/don't: ✅ keyset pagination (relatórios grandes) · ❌ offset (estoura memória — incidente #231) ·
❌ gerar arquivo em memória: use o stream helper `report-stream.ts`.

origem: b7d3c02 · evidência: PR #88, PR #102
```
O valor está no **template concreto** (arquivos reais a copiar + pegadinha com porquê) — prosa abstrata
("siga o padrão de relatórios") não ensina nada.

## 4. Drift detectado → atualizar ou remover
O explore reporta: `rules/api.md` cita `contracts.controller.ts:45`, mas o arquivo virou
`contracts/http/controller.ts`. → Proposta mecânica: atualizar a citação e o `origem:`; se a convenção
em si morreu (ex.: migraram para GraphQL), propor **remover** a rule — regra morta engana.

## 5. Fim de ship → retrospectiva que vira melhoria concreta
Retro detecta: o agente demorou 15 min para achar onde nasce o PDF. → Proposta: 1 linha no Mapa do
AGENTS.md (`Relatórios/PDF → src/reports/, entrada reports.controller.ts`). Não vira rule (não é
convenção) — é **roteamento**, vai pro Mapa.

## Contra-exemplos (o que NÃO grava)
- **1ª ocorrência:** "usamos Luxon aqui" visto uma vez → ainda não é convenção; espere a 2ª ou a
  declaração do usuário.
- **Gosto pessoal no repo:** "prefiro aspas simples" de UM dev ≠ rule do time (se o lint já decide, nem
  é assunto — guardrail mecânico vence texto).
- **O que um comando responde:** "o teste roda com `pnpm test`" está no package.json — não gaste rule.
- **Regra inventada:** "APIs REST devem..." sem evidência no repo → não grava. Toda rule nasce de
  evidência citada.
