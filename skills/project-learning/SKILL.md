---
name: project-learning
description: Mantém e enriquece continuamente a Base de Conhecimento Pré-Destilada (PKB) do projeto. Dispara ao detectar uma convenção, decisão, padrão repetido ou correção que vale durar — ou quando uma rule/pattern skill existente ficou desatualizada. PROPÕE (nunca grava sozinha) entrada no AGENTS.md, rule, ou pattern skill local, e só persiste com o "ok".
---

# Project Learning → enriquece a PKB (contínuo)

A `project-onboarding` cria a PKB de uma vez; esta skill a mantém **viva**. Cada sessão que passa deixa o
agente mais contextualizado e mais barato — é o efeito "anabolizante" composto. **Propor-e-confirmar:
nunca grava sem o "ok".**

## O que observar (gatilhos)
- **Convenção** revelada pelo código ou pelo usuário (naming, estrutura, lib preferida, padrão de teste/erro).
- **Decisão** com justificativa (por que X e não Y) → candidata a ADR.
- **Padrão repetido** de tarefa (pediu a mesma coisa 2+ vezes) → candidato a **pattern skill** ("how to X").
- **Correção**: o usuário corrigiu o agente → aprendizado imediato.
- **Drift**: uma rule/pattern skill não bate mais com o código atual → propor atualização.

## Onde cada aprendizado vai
| Artefato | Quando | Freio |
|---|---|---|
| **AGENTS.md** (roteador < 150 linhas) | fato de contexto que orienta sempre | manter enxuto; propor prune a cada ~10 entradas |
| **rules/** (convenção/decisão/ADR) | regra que vale repetidamente | **1ª ocorrência → `rules/_candidates.md`; 2ª → vira rule** |
| **pattern skill** (`.claude/skills/<projeto>/`) | tarefa repetida com passos estáveis (≥2) | usar skill-creator como motor; só na 2ª+ repetição |

## Fluxo (sempre)
1. Detectou algo durável → **formule a proposta** (qual artefato, texto exato, onde, evidência file:line/PR).
2. **Apresente o diff** e espere o "ok". Sem "ok", não grava.
3. Com "ok" → grave; registre a ocorrência (para a regra da 2ª) e o commit de origem (para revalidar no drift).
4. Item errado/velho → **corrija ou remova** (é git, dá para voltar).

## Exemplos do valor (destravam token e evitam redescoberta)
- Rule `pr.md`: *"nunca abra PR sem descrição no formato X"* (derivado dos PRs existentes).
- Pattern skill `how-to-create-dto`: o template exato do projeto + onde fica + validações — o agente para
  de inferir do zero toda vez.
- Rule `error-handling.md`: como o projeto trata erro/log/validação, com exemplo real.

## Base técnica
Para criar/otimizar pattern skills, use **skill-creator** (Anthropic) — já formaliza rascunho → casos de
teste → benchmark com/sem skill → grading → refino, e resolve a otimização da `description` (gatilho).

## Freios anti-inchaço
- AGENTS.md é roteador curto; propor prune quando crescer.
- Nada de rule na 1ª ocorrência (vai para `_candidates.md`).
- Nada de pattern skill para algo que aconteceu uma vez.
- Nunca duplicar no AGENTS.md o que já é regra em `rules/`.
- Toda rule nasce de evidência real (cite file:line / PR) — nunca convenção inventada.
