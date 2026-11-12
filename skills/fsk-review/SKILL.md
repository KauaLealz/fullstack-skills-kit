---
name: fsk-review
description: Verifica a mudança por fidelidade, regras, segurança, impacto, escopo e simplicidade; bloqueia regra de negócio alterada sem aprovação e reverte ou ajusta ruído, overengineering e antipadrão no diff. Dispara em "revisa", "está bom?", "review". Não use para provar comportamento (fsk-prove) nem para abrir PR (fsk-ship).
user-invocable: false
effort: high
allowed-tools: Read Grep Glob
---

# fsk-review — verificação

Lê o código conectado, não só o diff, partindo do `exploracao.md` quando existir. Fixa o ponto de
comparação e confirma que o diff não está vazio. Lê `evidencias.md` em vez de reprovar.

## Eixos (sem ranking cruzado)
| Eixo | Pergunta |
|---|---|
| Fidelidade | Cada critério foi atendido? Há algo não pedido? Algo parece atendido mas está errado? |
| Regras e convenções | Segue rules, how-to e o estilo existente? A regra do repo vence a heurística genérica |
| Segurança | Borda de confiança, autorização, injeção, segredos, exposição de dados, tenant, dependência nova |
| Impacto | Chamadores (busca todos quando muda assinatura ou retorno), contratos, dados existentes, carga esperada (declara qual assumiu), corrida entre processos, compatibilidade, reversão |
| Escopo e limpeza | Cada trecho se explica por um critério, uma decisão registrada ou um pedido explícito? |
| Simplicidade | Linha inútil, abstração especulativa, duplicação, intermediário que só repassa, módulo raso (apagá-lo concentraria ou só espalharia a complexidade?), nome que não revela intenção |
| Qualidade web | Só os eixos que o projeto marcou em `rules/eixos.md` (a11y, responsivo, performance, i18n, SEO, observabilidade) — não invente eixo que o repo não adotou |

## Portão de comportamento (bloqueia)
Toda mudança em regra de negócio — condição, validação, cálculo, transição de status, permissão, valor
padrão, limite, resposta de API, mensagem que muda decisão do usuário — precisa apontar para um critério
da spec ou para um "ok" em `notas.md`. Sem isso, bloqueia e pergunta. Refactor com mudança de
comportamento bloqueia sempre.

## Toda linha do diff se justifica (corrige ou bloqueia)
Percorra o diff trecho a trecho: "que critério, decisão ou pedido explica isto?". Sem resposta, o trecho sai.
| O que | Ação |
|---|---|
| **Fora do escopo** (arquivo/função não pedido, "aproveitei e melhorei") | Sem mudar comportamento, reverte; mudando, bloqueia e pergunta |
| **Ruído** (reindentação, reformatação, reordenar imports, espaço, mover sem motivo, trocar aspas, comentário alheio) | Reverte na hora |
| **Mudança sem ganho** (rename desnecessário, reescrita equivalente, estilo por preferência, "modernização") | Reverte na hora |
| **Overengineering** (abstração, camada, opção, config, generalização para caso que não existe) | Simplifica na hora |
| **Antipadrão** (contraria o padrão/arquitetura do repo, duplica o que existe, contorna o mecanismo da casa) | Ajusta para o padrão do repo |
| **Não justificada** (dependência nova, mudança de contrato, alteração em teste existente, config sem motivo) | Bloqueia e pergunta |

Exceções, só estas: pedido explícito do usuário (em `notas.md`) ou formatação que uma ferramenta
obrigatória do repo aplica sozinha (vai em commit mecânico separado). Depois de reverter ou ajustar, rode
a prova direcionada do que foi tocado. O revertido aparece em uma linha no relatório ("removi 3 trechos
fora do escopo"), sem detalhar. Código pré-existente fora do escopo só é apontado, não consertado.

## Revisar PR de colega (sem spec/notas)
Aponta como `deveria`/`bloqueia` e pergunta — **não** reverte nem ajusta na hora. O conserto no diff
(reverter ruído, simplificar, ajustar antipadrão) só vale no **próprio** build, onde há critério e
`notas.md`. Sem spec, o eixo Fidelidade vira "o PR faz o que o título/issue diz?".

## Proporcional e saída
Padrão: uma passada inline. Só em criticidade **alta** com vários achados vale abrir eixos em subagentes
paralelos (sem misturar ranking entre eixos) — subagente custa mais, use quando o paralelismo paga.
Heurística de cheiro é sempre "possível X", nunca violação dura. Saída: achados com `arquivo:linha` e
severidade `bloqueia · deveria · sugestão`; "bloqueia" se resolve antes do ship. Erro mecânico recorrente
vira sugestão de checagem automática para o `fsk-learn`.

## Pronto quando
Num diff de teste: barra uma mudança de regra não aprovada; reverte reindentação, rename desnecessário e
trecho fora do escopo; simplifica uma abstração especulativa; ajusta um antipadrão para o padrão do repo;
preserva uma reformatação pedida explicitamente.
