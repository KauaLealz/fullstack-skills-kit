# Template — dossiê de revisão (`.claude/specs/<slug>/revisao.md`)

Gerado no início do ship, a partir de spec, `notas.md`, `evidencias.md`, achados do review e diff. Nada
reconstruído de memória. Tamanho segue o rigor: S1 cabe em meia tela; S2+/alta usa todas as seções. O
corpo do PR é a versão enxuta deste dossiê (no formato de PR do repo, se houver).

```markdown
# <Título> — revisão
**Em uma frase:** <o que muda para o usuário>
**Risco:** <baixo|médio|alto> · **Porta:** <mão dupla (fácil desfazer) | mão única> · **Tempo de revisão:** <N min>

## ⚠️ Mudanças de comportamento e regra de negócio
| Antes | Depois | Por quê | Aprovado em |
|-------|--------|---------|-------------|
(vazio = "Nenhuma regra de negócio alterada")

## Onde olhar com atenção (máx. 5)
1. `caminho/arquivo.ts:42` — <por que merece olho humano: risco, baixa confiança, julgamento de produto>

## O que só você pode julgar
<decisões de produto, UX, trade-offs que a prova não responde>

## Decisões tomadas
- <decisão> — <porquê> (ref. spec/notas)

## Mapa da mudança (ordem de leitura sugerida)
| # | Intenção | Arquivos | Tipo |
|---|----------|----------|------|
| 1 | <nova regra de desconto> | `src/billing/discount.ts` | comportamento |
| 2 | <rename de campo> | 12 arquivos | mecânico — pode pular |

## Padrões seguidos
<rules e how-to do repo aplicados, com ponteiro>

## Prova
<veredito + link para evidencias.md · o que NÃO foi testado>

## Como conferir em 2 minutos
<passos manuais curtos para o revisor ver funcionando>

<details><summary>Para quem quer entender mais</summary>
<contexto do domínio, por que essa abordagem, alternativas descartadas>
</details>
```
