---
name: fsk-build
description: Constrói a demanda em fatias verticais, cirúrgico, provando cada fatia, com commits por intenção e registro para a revisão. Dispara com critérios confirmados (do plan ou do chat) ou quando o usuário diz "implementa", "faz", "corrige", "commita" (o build faz os commits locais por intenção). Não use para planejar (é /fsk-plan) nem para push/PR (é /fsk-ship).
effort: high
---

# fsk-build — execução cirúrgica

1. **Entrada.** Sem critérios e acima de S0, escreva 3–6 e confirme. Criticidade alta sem spec, volte ao
   `fsk-plan`. Bug: `fsk-debug` primeiro.
2. **Leia o terreno** pela escada do núcleo: código tocado, chamadores, rules que carregam para esses
   caminhos, how-to da tarefa. Se existe `exploracao.md`, parta dele; área desconhecida sem exploração →
   `fsk-explore`.
3. **Liste o alcance** (chamadores, contratos, migrations, fixtures, telas). Isso é o escopo; o resto não.
4. **Por fatia vertical:** menor mudança completa → checagem direcionada (só o que tocou) → `fsk-prove`
   da fatia. Decisão não prevista: pare e pergunte.
5. **Fechamento:** prova de todos os critérios (subagente independente só em criticidade alta; S2 médio
   prova inline), suíte completa uma vez ou CI, `fsk-review`, relatório no formato do núcleo.

## Disciplina do diff
- **Diff mínimo desde o início:** não reformate, não reindente, não reordene, não renomeie e não
  "aproveite para melhorar" nada que a demanda não exige. Pedido explícito disso é anotado em `notas.md`
  e vai em commit mecânico separado.
- **Commits por intenção:** mudança mecânica (rename, mover, formatação), refactor e mudança de
  comportamento em commits separados, para o revisor pular o mecânico com segurança.
- **Registro corrido para a revisão:** cada decisão tomada, cada mudança de comportamento aprovada e cada
  lugar de menor confiança vão para `.claude/specs/<slug>/notas.md` no momento em que acontecem (uma
  linha cada). É a matéria-prima do dossiê; nada é reconstruído de memória no fim.

## Worktree
Se o plan decidiu por worktree, crie pela receita do `AGENTS.md` (branch na convenção do repo), prepare
o ambiente e trabalhe lá; a pasta principal fica intocada. Diga o caminho em uma linha.

## S3 — fatias em paralelo
Fatias de fato independentes e grandes rodam em paralelo, um subagente por fatia em worktree a partir de
uma branch de integração (poucas ou acopladas → sequência; política de worktree `nunca` → sequência na
pasta atual). Notas de
exploração salvas fora do repo e passadas por ponteiro. Merge da ponta da integração antes de reportar;
fechamento único no fim. Estado por fatia na spec (feita · em andamento · bloqueada) para retomar de onde
parou; demanda abandonada é marcada, não apagada.

## Freios
Fora do escopo se anota, não se conserta. Demanda cresceu, reclassifique na fronteira. Commits locais
ok; push, PR e merge são do `fsk-ship`.

## Pronto quando
Uma demanda S1 e uma S2 de ponta a ponta, com `notas.md` e commits por intenção; a S2 feita em worktree
com a pasta principal intocada.
