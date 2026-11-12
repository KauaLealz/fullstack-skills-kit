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
| Tipo | feature · ajuste · bug · refactor · dados/migração · infra/config · spike · documentação |
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
Bug sem spec (o sintoma vira critério; o build começa no `fsk-debug`). Spike sai com resposta e
protótipo descartável fora da main, não código de produção. Refactor tem critério "comportamento
idêntico" e, com raio largo, sequência expandir → migrar em lotes → contrair. Dados/migração sempre
declara reversão e ordem de deploy. Documentação vai direto ao `fsk-docs`.

## Entrevista
Rodadas pela fronteira de decisões: todas as decisões desbloqueadas, numeradas, cada uma com
recomendação e redigida para "sim" aceitar a recomendação. Fatos o agente descobre (em `fsk-explore`,
sem bloquear o resto); decisões são do usuário. Desafie termo vago ou ambíguo do domínio e cheque se o
código concorda com o que foi dito. Termine quando nada aberto muda escopo, risco ou prova. Dúvida que
está na cabeça de outra pessoa (PO, cliente): gere um questionário para ela, não chute.

## Impacto
Em S2+ ou criticidade alta, acione `fsk-explore` para levantar chamadores, contratos e dados afetados
antes de fechar a spec. Em S1, a escada do núcleo basta.

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

## Pronto quando
Classifica corretamente demandas de S0 a Neblina, nas três criticidades e em todos os tipos, e para
pedindo aprovação dos critérios antes de qualquer código.
