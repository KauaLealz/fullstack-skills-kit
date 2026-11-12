# Template — `.claude/specs/<slug>/spec.md`

Preencha só o que a rota pede. S1 cabe em meia tela; S2+/alta usa todas as seções. Se o time tem pasta
de specs/RFC própria, use o formato dele e acrescente só os critérios de aceite que faltarem.

```markdown
# <Título da demanda>
**Classificação:** <tipo> · <tamanho> · criticidade <alta|média|baixa>
**Worktree:** <sim: caminho | não>

## Objetivo
<o que muda para o usuário, em 1–3 linhas>

## Critérios de aceite
- [ ] <observável de fora> — esperado: <vindo do negócio> · canal: <navegador|API|estado|log> · durável: <sim|não>
- [ ] <caminho infeliz, se criticidade média/alta>

## Impacto (fsk-explore, em S2+/alta)
- Chamadores: `arquivo:linhas`
- Contratos afetados: <API, evento, schema>
- Dados existentes: <tabela/coleção> · reversão: <como desfazer>

## Decisões
- <decisão> — <porquê> · <vira rule? qual>

## Fatias (S3: verticais, com dependências)
1. <fatia> — depende de: <—> · critério: <…>
2. <fatia> — depende de: 1
```

## Regras de preenchimento
- **Critério observável de fora**, nunca "a função X retorna Y". O esperado vem do negócio, não é
  recalculado pela implementação.
- **Decisão com porquê.** Sem o porquê, não é decisão, é preferência — e preferência não entra na spec.
- **Fatia é vertical:** atravessa as camadas e entrega algo provável sozinho. Fatia horizontal (só
  banco, só UI) não é fatia.
- A spec é a fonte da verdade entre fases. O build lê daqui; a prova lê os critérios daqui **antes** de
  ver o diff; o ship monta o dossiê daqui.
