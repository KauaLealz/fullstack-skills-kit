---
name: fsk-ship
description: Entrega a mudança seguindo o fluxo de git do time à risca — dossiê de revisão, rodada final "está 100%?", push/PR no formato do repo com evidência e Mapa atualizado no mesmo PR. Dispara por "abre PR", "entrega", "manda pro main", "push" (o agente sugere, nunca aciona sozinho; o commit local é do /fsk-build). Não use para planejar/implementar (fsk-plan/fsk-build) nem só para revisar (fsk-review).
disable-model-invocation: true
effort: medium
---

# fsk-ship — entrega

**Missão:** levar o trabalho para fora da máquina do jeito que o **time** entrega, com o revisor humano
recebendo tudo pré-organizado. Nada sai sem "ok". PR padrão (só sem formato do time):
`references/pr-padrao.md`.

## Protocolo

1. **O fluxo do time primeiro.** Leia a seção **Fluxo de entrega** do AGENTS.md (gitflow, trunk-based,
   develop→main, naming, squash×merge, quem mergeia) e `rules/pr.md`/`commits.md` — **siga à risca**.
   Sem seção: infira do histórico real (log + PRs mesclados), **confirme com o usuário** e proponha ao
   `fsk-learn` gravar. O que a dúvida revelar (formato de PR, estratégia de merge) **nunca se adivinha** —
   pergunta, e a resposta vira convenção gravada (projeto) ou preferência pessoal (global do usuário).
2. **Dossiê de revisão** (`revisao.md` via `fsk-docs`, de spec+notas+evidencias+review+diff — nada de
   memória). Confira o **SHA** do `evidencias.md` contra o diff; review mexeu depois → re-prova. Prova só
   com canal de checagem e sem justificativa → **bloqueia** e manda provar no canal real.
3. **Rodada final "está 100%?"** — pergunte; houve ajuste → corrige, re-prova e pergunta de novo.
4. **Mapa em dia (obrigatório):** `fsk.py check-map` + diff×AGENTS.md; mudança estrutural → `fsk-learn`
   atualiza o AGENTS.md **no mesmo PR**, commit próprio. PR não abre com mapa falso.
5. **Base atualizada:** traga a base do fluxo (`git merge <base>`) se avançou e rode a prova direcionada.
6. **Saída pelo fluxo do time** (branch na convenção, commits no formato, ordem de deploy com migration,
   CLI do host — `gh`/`glab`/Bitbucket/Azure). **Push, PR e merge só com "ok".** Feche o card no tracker.
   Liste os `shortcut:` novos.
7. **Comentários no PR** (com "ok"): máx. 5, um por "Onde olhar", ancorado na linha, 3 linhas, prefixo
   `🤖 fsk:`; nunca em linha mecânica. Time sem bot → não posta e avisa uma vez.
8. **Pós-PR:** CI vermelho → `fsk-debug`; conflito → resolve com "ok"; comentário do revisor → responde e
   ajusta no mesmo PR; conferência pós-merge se o fluxo pede.
9. **Limpeza e retro:** worktree/branch local removidos após o merge com "ok"; `fsk-learn` para a
   retrospectiva curta.

## Profundidade
| Dimensão | Regra |
|---|---|
| Tamanho | >~400 linhas de comportamento → propõe PRs empilhados (alerta, não bloqueio) |
| Evidência | antes/depois no corpo; captura se visual, saída real se não |
| Risco de merge | porta de mão única×dupla + raio de impacto declarados no PR |
| Preferência | precedência: convenção do projeto → preferência do usuário (global) → default do kit |

## Freios
Nunca contorne hook. Nunca adivinhe convenção de entrega. Commits locais são do build; aqui é publicação.
Headless/CI: nada destrutivo — para e reporta.

## Saída · Pronto quando
Reporta o que saiu da máquina (branch/PR com link/merge), estado do worktree e do card. Pronto quando: PR
no fluxo e formato do time com comentários ancorados; mapa atualizado no mesmo PR; worktree limpo após o
merge com "ok".
