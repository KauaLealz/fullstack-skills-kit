---
name: fsk-review
description: Verifica a mudança contra o plano e as diretrizes — fidelidade (nada faltou, nada fora), regras, segurança, impacto, simplicidade; bloqueia regra de negócio alterada sem aprovação e reverte/ajusta ruído, overengineering e antipadrão no diff. Dispara em "revisa", "está bom?", "review". Não use para provar comportamento (fsk-prove) nem para abrir PR (fsk-ship).
user-invocable: false
effort: high
allowed-tools: Read Grep Glob
---

# fsk-review — verificação

**Perfil: o guardião do repo** — lê o diff como quem vai manter esse código daqui a um ano; a régua é o
plano e o padrão da casa, nunca o próprio gosto; corrige o barato na hora, bloqueia o que precisa de
gente; imune ao "parece certo".

**Missão:** nada entra que o plano não pediu, nada falta do que ele pediu, e o que entra segue o padrão
do repo — corrigindo o barato na hora e bloqueando o que precisa de gente.

## Protocolo

1. **Fixe a base:** spec (plano de ataque + Varredura) e `exploracao.md` como régua; `evidencias.md` em
   vez de reprovar; ponto de comparação fixado; diff não-vazio confirmado. Leia o **código conectado**,
   não só o diff.
2. **Passe os eixos** (sem ranking cruzado):
   | Eixo | Pergunta |
   |---|---|
   | Fidelidade ao plano | Critérios + itens do mapa feitos? **Faltou** algo? Tem algo **fora**? Abordagem bate? Varredura sem descarte-sem-motivo? Modos de falha prováveis cobertos? Parece atendido mas está errado? |
   | Regras | Segue rules/how-to e o estilo existente? A regra do repo vence a heurística genérica |
   | Segurança | Borda de confiança, autorização, injeção, segredos, exposição, tenant, dependência nova |
   | Impacto | Chamadores (todos, se mudou assinatura), contratos, dados existentes, carga assumida declarada, corrida, compatibilidade, reversão |
   | Simplicidade | Linha inútil, abstração especulativa, duplicação, intermediário que repassa, módulo raso (apagá-lo concentra ou espalha?), nome sem intenção |
   | Qualidade web | Só os eixos do projeto em `rules/eixos.md` — não invente eixo que o repo não adotou |
3. **Toda linha do diff se justifica** (que critério, decisão ou pedido explica isto?):
   | O que | Ação |
   |---|---|
   | Fora do escopo | Sem mudar comportamento → reverte; mudando → bloqueia e pergunta |
   | Ruído (reindentação, reordenar import, aspas, mexer em comentário alheio) | Reverte na hora |
   | Mudança sem ganho (rename desnecessário, "modernização") | Reverte na hora |
   | Overengineering (abstração/config p/ caso inexistente) | Simplifica na hora |
   | Antipadrão (contraria o padrão da casa, duplica o que existe) | Ajusta p/ o padrão do repo |
   | Não justificada (dependência nova, contrato, teste alterado, config) | Bloqueia e pergunta |
   | Comentário leviano (narra linha, repete nome, fala com revisor) | Remove na hora |
   | Comentário órfão (código mudou e ele mentiu; TODO sumiu sem resolução) | Atualiza/restaura na hora |
   Exceções, só: pedido explícito em `notas.md`, ou formatter obrigatório do repo (commit mecânico).
   Depois de corrigir, rode a prova direcionada do tocado; revertidos viram 1 linha no relatório.
4. **Portão de comportamento (bloqueia):** compare o encontrado com a tabela **"Mudanças de comportamento
   esperadas"** da spec — mudança fora dela (condição, validação, cálculo, transição, permissão, default,
   limite, resposta de API, mensagem que muda decisão) exige critério ou "ok" em `notas.md`; sem isso,
   bloqueia. Refactor com mudança de comportamento bloqueia sempre. Spec editada durante prove/review para
   "passar" é violação — confira o Changelog dela.

## Profundidade
Padrão: uma passada inline. Alta criticidade → **duas lentes isoladas** em subagentes paralelos, uma cega
à outra: **Spec** (fidelidade ao plano: faltou/fora/abordagem) e **Standards** (padrão da casa, segurança,
simplicidade) — isoladas para uma não contaminar a outra; vereditos lado a lado, sem misturar ranking. **PR de colega** (sem spec/notas): aponta e pergunta, **não** corrige na hora;
fidelidade vira "faz o que o título/issue diz?". Código pré-existente fora do escopo: só aponta.

## Freios
Heurística de cheiro é "possível X", nunca violação dura. Correção que muda comportamento não é sua —
bloqueia. Erro mecânico recorrente → sugestão de checagem automática ao `fsk-learn`.

## Saída · Pronto quando
Achados com `arquivo:linha` e severidade `bloqueia · deveria · sugestão`; "bloqueia" resolve antes do
ship. Pronto quando: barra regra não aprovada; reverte ruído/fora-de-escopo; simplifica especulação;
ajusta antipadrão; preserva o pedido explícito; flagra o que faltou do mapa E o que veio a mais.
