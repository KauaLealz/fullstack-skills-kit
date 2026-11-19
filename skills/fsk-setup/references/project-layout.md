# Estrutura padrão que o setup cria no projeto

Proponha isto e grave só com "ok". O do time sempre vence; aqui é o default quando não há nada.

## As três camadas (precedência: projeto → usuário → kit)

| Camada | Onde vive | O que carrega | Versionado? |
|---|---|---|---|
| **Projeto (time)** | `AGENTS.md` + `.claude/rules` + `how-to` + `specs` | convenção, fluxo de entrega, mapa | ✅ git do time |
| **Usuário (pessoal)** | `~/.claude/` (CLAUDE.md, memória) + `.claude/fsk.local.json` | preferências (worktree, explicação, estilo de entrega) | ❌ nunca |
| **Kit (default)** | `~/.claude/skills/fsk-*` + núcleo | comportamento base, sobrescrevível pelas camadas acima | — |

## Bloco fsk no `.gitignore` (o setup sempre oferece)
```gitignore
# fsk:gitignore:start
.claude/fsk.local.json
.worktrees/
# modo local (dev solo) acrescenta: AGENTS.md, CLAUDE.md, .claude/, .cursor/, .agents/ …
# fsk:gitignore:end
```

```
AGENTS.md                         # roteador < 150 linhas
CLAUDE.md                         # @AGENTS.md
.claude/
  fsk.json                        # versão do kit, commit de origem, tracker, data
  fsk.local.json                  # preferências pessoais (política de worktree) — fora do git
  rules/
    <tema>.md                     # api, data, ui, security, testing, pr, commits, docs… só o que existe
  skills/
    how-to-<tarefa>/SKILL.md      # técnico DO PROJETO, derivado de exemplos reais
  specs/
    <slug>/
      spec.md                     # critérios, impacto, decisões, fatias
      exploracao.md               # ponteiros de contexto (fsk-explore)
      notas.md                    # registro corrido do build: decisões, aprovações, baixa confiança
      evidencias.md               # relatório de prova (fsk-docs)
      revisao.md                  # dossiê para o revisor humano (fsk-docs, no ship)
  docs-templates/                 # opcional: templates da empresa (.docx com {{campos}}, CSS de PDF)
docs/                             # documentação para humanos, se o projeto já tem ou se você pedir
```

## AGENTS.md — seções (roteador, não enciclopédia)

O `AGENTS.md` **abre com o bloco do núcleo** (`<!-- fsk:start -->…<!-- fsk:end -->`): como subagentes
herdam o AGENTS.md, isso leva o comportamento-base a eles também (os nativos Explore/Plan são a exceção —
pulam a memória; o setup os desliga em favor das `fsk-*`). Depois vêm as seções:

Stack · Comandos (só os não óbvios, validados) · **Mapa** (por domínio: ponto de entrada, arquivos
centrais, feature de referência) · **Não ler** · Crítico · **Vocabulário** (termos do domínio e o que
cada um significa, sem implementação) · Ferramentas de navegação · Worktree (receita, se validada) ·
Onde está cada regra.

Se o Vocabulário crescer, vira `rules/dominio.md`.

## rules/ — convenção por caminho

Cada `rules/<tema>.md` tem frontmatter com `paths` (globs); o Claude Code carrega a regra só quando o
agente toca um arquivo que casa. Nasce de 2+ exemplos no código ou de declaração/correção do usuário.
Regra de implementação é mínima e por caminho; padrão completo fica para o `fsk-review`.

```markdown
---
paths:
  - "src/api/**/*.ts"
---
# API — convenções
- Todo endpoint valida a entrada. (evidência: `src/api/users.ts:12-30`, PR #84)
- Erro no formato padrão do projeto (ver feature de referência no Mapa).

origem: a1b2c3d
```
Toda rule cita a evidência de onde nasceu e leva o commit de origem — sem evidência, não grava; código
citado mudou, revalida ou remove (drift detectável).

## fsk.json (versionado) e fsk.local.json (fora do git)

```json
// .claude/fsk.json
{ "kit_version": "2.0", "origin_commit": "<sha>", "tracker": "github|jira|linear|none", "setup_date": "<data>" }
```
```json
// .claude/fsk.local.json  (preferência pessoal; entra no .gitignore)
{ "worktree_policy": "ask|never|always_s2", "explain_level": "curto|explicado" }
```

## Não duplicar

Não copie para a rule o que um comando já responde (scripts do `package.json`, configs). Registre o que
não se descobre olhando: convenção não escrita, o porquê, a pegadinha. Guardrail mecânico (lint, hook,
CI) é preferível a qualquer texto de regra.
