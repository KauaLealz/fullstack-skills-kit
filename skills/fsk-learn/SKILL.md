---
name: fsk-learn
description: Transforma aprendizado durável em AGENTS.md, rule ou how-to e mantém o Mapa sempre verdadeiro. Dispara em correção do usuário, "sempre faça X aqui", padrão repetido, decisão com porquê, drift entre rule e código, fim de ship. Propõe o diff e grava só com "ok". Não use para implementar nem para revisar código.
user-invocable: false
effort: medium
---

# fsk-learn — aprendizado contínuo

Guia de escrita para agente em `references/escrita-para-agentes.md`. Sempre: **proponha o diff, grave com
"ok".**

## Gatilhos
Correção do usuário, padrão repetido, decisão com porquê, drift entre rule e código, atrito (demorou para
achar algo, chamada de ferramenta cara, informação que faltou), fim de ship.

**Pessoal × time (divisão com a memória nativa).** A memória automática do Claude Code já guarda
preferência individual, local e sem "ok" — deixe com ela. O `fsk-learn` cuida só da **convenção do
time**: vira rule ou how-to e entra por PR, com "ok". Não promova gosto de um dev a regra do time sem
confirmação; na dúvida entre pessoal e time, pergunte.

## Destino
| Destino | Quando |
|---|---|
| `AGENTS.md` | Só roteamento: comandos não óbvios, Mapa, o que é crítico, ponteiros |
| `.claude/rules/<tema>.md` (com `paths`) | Convenção do time em 2+ exemplos ou declarada; correção do usuário vira rule com "ok" (gosto pessoal fica na memória local) |
| `.claude/skills/how-to-<tarefa>/` | Procedimento do projeto repetido 2+ vezes |
| Checagem automática (lint, hook, CI) | Erro mecânico que uma ferramenta pega — preferível a qualquer texto |
| Seção "Decisões" da spec ou a rule afetada | Decisão com porquê |

## Retrospectiva curta (fim de ship, ou build que deu errado)
Onde o agente se perdeu (falta ponteiro no Mapa?), que erro uma checagem pegaria, que regra o review
deixou passar, que instrução do `AGENTS.md` não muda comportamento (remover), que ferramenta saiu cara,
que informação faltou (ex: logs do servidor acessíveis).

## Mapa sempre verdadeiro
O `AGENTS.md` é atualizado no mesmo trabalho que o torna falso, nunca depois. Três gatilhos: (1) o ship
detecta mudança estrutural no diff; (2) o `fsk-explore` acha um ponteiro quebrado e reporta; (3) o
`fsk.py check-map` acusa caminho inexistente. Atualização de mapa é mecânica (caminho, nome, comando):
mostre o diff e aplique com "ok" junto do resto. Vale o mesmo para `paths` de rules e how-to que citam
arquivos movidos.

## Ledger de atalhos
Liste os `shortcut:` com limite e gatilho de evolução; marque os sem gatilho.

## Passar o trabalho adiante (outro harness, outra pessoa)
Documento curto em pasta temporária, apontando para spec, commits e evidências em vez de copiar, com
dados sensíveis mascarados.

## Pronto quando
Uma correção do usuário vira rule; uma mudança que move um arquivo citado no Mapa sai com o `AGENTS.md`
atualizado no mesmo PR.
