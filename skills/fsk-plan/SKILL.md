---
name: fsk-plan
description: Classifica a demanda por tipo × tamanho × criticidade e entrega o menor plano que fecha as decisões e define a prova. Dispara em demanda nova acima de trivial ("quero", "precisamos", "adicionar", "mudar", "criar"). Não use para implementar (é /fsk-build), para bug já localizado (fsk-debug) nem para dúvida de código (fsk-explore).
effort: high
allowed-tools: Read Grep Glob
---

# fsk-plan — planejamento roteado

Entrega o menor plano que fecha as decisões e define a prova. Termina pedindo o "ok" dos critérios;
nunca encadeia sozinho no build. Template da spec: `references/spec.md`. Demanda nova que surge no meio do
trabalho (refatoração, escopo novo) re-entra aqui e vira spec — não siga em prosa solta.

## Classificação (uma linha ao usuário)
| Eixo | Valores |
|---|---|
| Tipo | feature · ajuste · bug · refactor · dados/migração · infra/config · spike · documentação · **design/UX** |
| Tamanho | S0 trivial · S1 um fluxo · S2 várias camadas/decisões · S3 multi-sessão · Neblina |
| Criticidade | **alta**: dinheiro, auth/permissão, tenant, dados pessoais, dado irreversível, contrato público, produção quebrada · **média**: comportamento visível ao usuário · **baixa**: resto |

## Rotas (rigor = maior entre tamanho e criticidade)
| Rota | Quando | Saída |
|---|---|---|
| Direto | S0 + baixa | "Pode ir ao build." Nada escrito |
| Critérios | S1 baixa/média | 3–6 critérios no chat |
| Spec | S2 ou criticidade alta | Entrevista → `.claude/specs/<slug>/spec.md` |
| Spec + fatias | S3 | Spec + fatias verticais com dependências |
| Mapa | Neblina | Só decisões, uma por vez, com destino declarado, até virar S2/S3 |

## Ajustes por tipo
Bug sem spec (o sintoma vira critério; o build começa no `fsk-debug`). **Design/UX passa pelo plan como
qualquer demanda:** cada pedido visual vira critério verificável (logo trocada, contraste AA, estados
hover/vazio/erro, responsivo) — a prova é screenshot por critério e o review confere cobertura; sem isso,
"faltou X" só aparece na bronca do usuário. Spike sai com resposta e
protótipo descartável fora da main, não código de produção. Refactor tem critério "comportamento
idêntico" e, com raio largo, sequência expandir → migrar em lotes → contrair. Dados/migração sempre
declara reversão e ordem de deploy. Documentação vai direto ao `fsk-docs`.

## Entrevista (protocolo de profundidade — detalhe em `references/entrevista.md`)
**Ordem obrigatória: entenda ANTES de perguntar.** Primeiro `fsk-explore` no terreno da demanda; cada
pergunta sai **ancorada no que o código faz hoje** ("hoje X acontece em `arquivo:linha` — mantém ou
muda?"), nunca genérica. Depois, **varra as dimensões do catálogo** (dados/retroativo, bordas, permissões,
estados UX, consumidores/relatórios, rollout/reversão…): cada dimensão vira pergunta **ou** é descartada
com motivo escrito na spec ("sem impacto em X porque Y") — pular em silêncio é plano raso.
É **multi-rodada**: a regra de "rodada única" do núcleo vale para aprovação, não para descoberta; rode
quantas rodadas a fronteira de decisões pedir, cada decisão numerada, com recomendação, redigida para
"sim" aceitar. Fatos o agente descobre; decisões são do usuário. Desafie termo vago e cheque se o código
concorda com o que foi dito. Termine só quando a varredura fechou E nada aberto muda escopo, risco ou
prova. Dúvida na cabeça de outra pessoa (PO, cliente): questionário para ela, não chute.

## Plano de ataque (o mapa que o build executa)
Transforme os critérios num mapa concreto que o build só executa — via `fsk-explore` (o quanto a demanda
pedir; sempre em S2+/alta). Por fatia, feche: **quais arquivos tocar**, **onde** (função/componente/
`arquivo:linhas`), **a abordagem** (como), **o porquê**, a **feature de referência** a copiar, e o que pode
quebrar (chamadores, contratos, dados). Plano raso joga a análise pro build; aqui a análise **fecha** — o
build carrega o "como executar bem", não o "o quê/onde descobrir".

## Onde trabalhar (worktree)
Aplique a política do setup. Com `perguntar por demanda`, pergunte em uma linha só para S2+ ou quando já
há trabalho aberto na pasta atual ("Faço num worktree separado para não mexer no que está aberto?
Recomendo sim."). S0 e S1 nunca perguntam. A escolha fica na spec. Sem receita validada no `AGENTS.md`,
não ofereça.

## Critérios de aceite
Observáveis de fora; o esperado vem do negócio; caminho infeliz incluído em criticidade média/alta; para
cada um, o canal de observação e se merece teste durável.

## Decisões (substitui ADR)
Ficam na seção "Decisões" da spec, com o porquê. Decisão que vale para o projeto todo vira (ou atualiza)
a rule que ela afeta, com uma linha de porquê — roteado ao `fsk-learn`.

## Transparência (o usuário entende antes do "ok")
Mostre em linguagem clara **o quê** será feito, **como** e **por quê** — o plano de ataque com os arquivos
e a abordagem à vista, não só critérios abstratos. O "ok" é sobre esse plano.

## Pronto quando
Classifica corretamente demandas de S0 a Neblina, nas três criticidades e em todos os tipos; entrega o
mapa de ataque (arquivos/onde/como/porquê) que o build executa; e para pedindo aprovação antes do código.
