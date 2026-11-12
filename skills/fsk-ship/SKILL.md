---
name: fsk-ship
description: Entrega a mudança — dossiê de revisão, push e PR no formato do repo, com evidência e Mapa atualizado no mesmo PR. Dispara por "abre PR", "entrega", "manda pro main", "push" (o agente sugere, nunca aciona sozinho; o commit local é do /fsk-build). Não use para planejar/implementar (fsk-plan/fsk-build) nem só para revisar (fsk-review).
disable-model-invocation: true
effort: medium
---

# fsk-ship — entrega

1. **Dossiê de revisão primeiro.** O `fsk-docs` gera o `revisao.md` a partir de spec, `notas.md`,
   `evidencias.md`, achados do review e diff — nada de memória. Confira que o **SHA** do `evidencias.md`
   bate com o diff; se o review mexeu no código depois da prova, re-prove antes de abrir. Mostre o dossiê
   e só siga com "ok".
2. **Formato do repo vence.** Siga `rules/pr.md` e `rules/commits.md`; sem elas, infira do histórico real
   (log e PRs mesclados) e proponha gravar a rule. Sem padrão nenhum, use `references/pr-padrao.md`.
3. **Diff limpo** (sem log temporário), commits por intenção no formato do repo, branch na convenção,
   ordem de deploy com migration, via CLI do repo (`gh`/`glab`, ou Bitbucket/Azure DevOps conforme o
   host). **Push, PR e merge só com "ok".** Feche as tarefas no tracker. Liste os `shortcut:` novos.
4. **Mapa em dia (obrigatório antes do PR).** Rode `fsk.py check-map` e compare o diff com o `AGENTS.md`.
   Se a mudança criou, moveu, renomeou ou apagou algo que o Mapa cita (ponto de entrada, arquivo central,
   feature de referência, domínio novo), mudou um comando listado ou tornou falso um item de "Não ler",
   "Crítico" ou "Vocabulário", o `fsk-learn` atualiza o `AGENTS.md` **no mesmo PR**, em commit próprio. O
   PR não abre com mapa desatualizado.
5. **Alerta de tamanho:** mudança de comportamento acima de ~400 linhas → proponha dividir em PRs
   empilhados. É alerta, não bloqueio.
6. **Comentários no PR** (depois do PR criado, com "ok"): um por item de "Onde olhar com atenção" (máx.
   5), ancorado na linha, via `gh`/`glab`. Cada um em até 3 linhas: por que o ponto merece atenção, o que
   foi decidido, o que conferir. Nunca em linha mecânica, nunca repetindo o corpo do PR. Prefixo
   `🤖 fsk:`. Se o time não usa comentário de bot, não poste e avise uma vez.
7. **Worktree:** depois do merge (ou quando o usuário disser que terminou), proponha remover o worktree e
   a branch local; liste worktrees antigos esquecidos. Remoção só com "ok".
8. **Depois do PR:** CI vermelho → `fsk-debug`; conflito de merge → resolve com "ok"; comentário do
   revisor → responde e ajusta no mesmo PR; conferência pós-merge quando o fluxo do time pede.
9. **Fecho:** acione o `fsk-learn` para a retrospectiva curta.

## Pronto quando
PR no formato do repo com comentários nos pontos de atenção; mudança que move um arquivo citado no Mapa
sai com o `AGENTS.md` atualizado no mesmo PR; worktree removido após o merge.
