# Base de Conhecimento Pré-Destilada (PKB) — o maior multiplicador do kit

A diferença entre um agente que tateia e um agente afiado não são mais ferramentas — é **conhecimento do
projeto escrito de forma concisa e barata de ler**. A PKB é esse pilar.

## O problema que resolve
Sem PKB, o agente **redescobre** o padrão do projeto a cada sessão — lê arquivos, infere convenção,
tenta adivinhar o formato de PR, o jeito de criar um DTO, como se testa aqui. Isso queima **tokens de
input** e ainda sai inconsistente.

## O princípio
> **Destila uma vez (caro), lê para sempre (barato).**

A redescoberta é um custo recorrente. A PKB paga esse custo **uma vez** (no setup/onboarding) e escreve o
resultado de forma concisa, lazy-load. Depois, o agente **já sabe** — custo de leitura perto de zero.

## PKB × CodeGraph (complementares, não concorrentes)
| | CodeGraph | PKB |
|---|---|---|
| Responde | "onde / o quê" (estrutura) | "**como fazemos X aqui**" (padrão + tácito) |
| Custo | tokens **a cada** query | escrito uma vez, leitura barata |
| Enxerga o tácito? | não (formato de PR, "nunca fazemos Y") | **sim** |
| Papel | **alimenta** a geração da PKB | cache destilado do conhecimento |

## Os 3 artefatos
1. **AGENTS.md** — roteador < 150 linhas: stack, comandos, onde cada coisa vive, ponteiros.
2. **rules/** — convenções mineradas, cada uma com evidência real (file:line / PR):
   `pr.md` (formato de descrição de PR), `commits.md`, `branching.md`, `naming.md`, `structure.md`,
   `testing.md`, `error-handling.md`, `api-shape.md`, `style.md`, `_candidates.md` (1ª ocorrência), ADRs.
3. **Pattern skills** (`.claude/skills/<projeto>/`) — "**how to X do nosso jeito**", derivadas de ≥2–3
   exemplos reais: `how-to-create-dto`, `how-to-add-endpoint`, `how-to-write-service`, `how-to-write-test`,
   `how-to-add-migration`, `how-to-create-component`, ... Cada uma: template concreto + onde fica + do/don't.

## De onde vem (mineração)
- **Histórico de PRs** (`gh pr list --state merged`) → formato de PR, checklist, tamanho típico.
- **Git log** → convenção de commit e de branch.
- **Amostragem por camada** (ler 2–3 exemplos) → pattern skills.
- **Configs** (lint/prettier/tsconfig/CI) → rules de estilo/qualidade.
- **README/docs + CodeGraph** → arquitetura, módulos, pontos de integração.

## Ciclo de vida
- **Setup/onboarding** (`project-onboarding`): gera a PKB inicial (propor-e-confirmar).
- **Uso diário** (`project-learning`): enriquece continuamente — convenção nova, decisão, padrão repetido.
- **Drift**: cada artefato guarda o commit de origem; quando o código diverge, `project-learning` **propõe**
  atualizar.

## Freios (para não virar ruído)
- **Propor-e-confirmar** sempre: nada entra na PKB sem o "ok".
- **Recorrência**: pattern skill só para padrão que aparece ≥2–3 vezes.
- **Evidência**: toda rule nasce de algo real no repo (cite file:line / PR) — nunca convenção inventada.
- **Enxuto**: AGENTS.md é roteador, não despejo; prune proposto quando crescer.
- **1ª→candidato, 2ª→rule**: a primeira ocorrência fica em `_candidates.md`.

## Exemplos de valor imediato
- *Rule* `pr.md`: "nunca abra PR sem descrição no formato X" → PRs consistentes, zero redescoberta.
- *Pattern skill* `how-to-create-dto`: o agente cria no padrão do projeto na primeira tentativa.
- *Rule* `error-handling.md`: tratamento de erro/log/validação padronizado, com exemplo real.
