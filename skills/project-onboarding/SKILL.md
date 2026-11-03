---
name: project-onboarding
description: Estrutura a Base de Conhecimento Pré-Destilada (PKB) de um projeto web já existente. Dispara quando o repositório não tem AGENTS.md nem base de conhecimento. Minera código, git e histórico de PRs e gera AGENTS.md, rules de convenção e pattern skills ("how to X do nosso jeito") — para o agente parar de redescobrir o padrão (e gastar tokens) a cada sessão.
---

# Project Onboarding → gera a PKB

Destila UMA vez (caro) o que o agente leria MUITAS vezes (redescoberta cara). Aponta para um projeto web
em andamento e escreve uma base concisa que torna o agente contextualizado e barato.

> Por que mais eficiente que CodeGraph sozinho: CodeGraph responde "onde/o quê" **a cada query** (custa
> tokens toda vez). A PKB responde "**como fazemos X aqui**" já escrito, e captura o **tácito** que o
> CodeGraph não vê (formato de PR, "nunca fazemos Y", estilo de teste). CodeGraph **alimenta** a PKB.

## Quando rodar
Projeto sem `AGENTS.md`/PKB, ou PKB desatualizada (o `index.json` guarda o commit de origem; se bate com
o HEAD, **não refaça** — pare).

## Fluxo de geração (minere → destile → proponha → grave com "ok")

### 1. Passada estrutural
- `/init` nativo → `CLAUDE.md` inicial (comandos build/test, estrutura).
- **CodeGraph** (`codegraph init` se preciso) → símbolos, chamadas, blast-radius, entry-points, dead code.

### 2. Minere as fontes (cada uma vira conhecimento destilado)
| Fonte | Comando/meio | Vira |
|---|---|---|
| Histórico de PRs | `gh pr list --state merged --limit 30` + corpo | `rules/pr.md` (formato de descrição de PR real do time) |
| Git log | `git log --oneline -n 100` | `rules/commits.md` (convenção), `rules/branching.md` |
| Configs | lint/prettier/tsconfig/editorconfig/CI | `rules/style.md`, `rules/ci.md` |
| Amostragem por camada | ler 2–3 exemplos reais de DTO/endpoint/service/teste/componente | **pattern skills** (abaixo) |
| README/docs | ler | `AGENTS.md` (arquitetura, pontos de integração) |

### 3. Destile os 3 artefatos da PKB
- **AGENTS.md** (roteador < 150 linhas): stack, comandos, onde cada coisa vive, ponteiros p/ rules e skills.
- **rules/** (convenções observadas): `pr.md`, `commits.md`, `naming.md`, `structure.md`, `testing.md`,
  `error-handling.md`, `api-shape.md`, `_candidates.md`. Cada regra cita o padrão + 1 exemplo real (file:line).
  Ex: *"Nunca abra PR sem descrição no formato de `rules/pr.md`"* — derivado dos PRs existentes.
- **Pattern skills** (`.claude/skills/<projeto>/`) — só para padrões que **recorrem (≥2–3 exemplos)**:
  `how-to-create-dto`, `how-to-add-endpoint`, `how-to-write-service`, `how-to-write-test`,
  `how-to-add-migration`, `how-to-create-component`. Cada uma: o template concreto + onde fica + o do/don't.
  Use **skill-creator** (Anthropic) como motor:
  `npx skills add https://github.com/anthropics/skills --skill skill-creator`.

### 4. Confirme antes de gravar
Apresente a PKB proposta (lista de rules + pattern skills + AGENTS.md) e **espere o "ok"** — mesma
disciplina propor-e-confirmar da `project-learning`. Sem "ok", não grava.

### 5. Carimbe a origem
`.claude/repo-map/index.json` com `last_built_commit` e, por artefato, o commit de onde foi derivado —
para a `project-learning` revalidar no drift.

## Freios
- Só pattern skill para padrão que **recorre** — não gerar skill de algo que aparece uma vez.
- AGENTS.md é roteador curto, não despejo.
- Nada de inventar convenção: toda rule nasce de evidência real no repo (cite file:line / PR).
- Escopo web (ver manifest `scope_focus`).
