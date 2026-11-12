---
name: fsk-explore
description: Levanta contexto de uma área e devolve ponteiros (arquivo:linha), nunca conteúdo bruto. Dispara quando o usuário pergunta "onde fica X", "como funciona Y", "o que isso afeta", ou numa área desconhecida ou de impacto amplo antes de planejar/implementar. Não use para planejar, implementar, revisar ou provar — só para descobrir e apontar.
user-invocable: false
context: fork
background: false
effort: medium
allowed-tools: Read Grep Glob
---

# fsk-explore — contexto sem desperdício

Dona única de "como levantar contexto". Plan, build, debug, review e docs pedem a ela em vez de cada um
ter o seu "leia o terreno". Roda em subagente com contexto limpo: a leitura bruta nunca volta para a
janela principal, só os ponteiros.

**Quando entra:** área desconhecida para a sessão, demanda S2+, análise de impacto, bug sem ponto de
partida, ou pergunta direta do usuário. Para o resto, a escada de custo do núcleo resolve sem skill.

## Comportamento

1. **Receba perguntas, não um tema.** Quem chama diz o que precisa saber (3–5 perguntas). Sem perguntas
   claras, formule e confirme em uma linha.
2. **Siga a escada de custo do núcleo** e as ferramentas registradas no `AGENTS.md`: CLI primeiro;
   navegação por símbolos se houver; CodeGraph só para fluxo que a busca por nome não segue ou para raio
   de impacto.
3. **Git como contexto barato:** histórico do arquivo para o porquê; arquivos que mudam juntos para
   dependência escondida; PRs recentes da área para o padrão vigente.
4. **Pare quando as perguntas estiverem respondidas.** Não "termine de entender o módulo".
5. **Devolva ponteiros, não conteúdo**, no formato fixo abaixo.

```markdown
# Exploração — <slug ou pergunta>
## Respostas
1. <pergunta> → <resposta em 1–2 linhas> (`arquivo:linhas`)
## Onde mexer
- `arquivo:linhas` — <papel> · padrão a seguir: `arquivo-exemplo:linhas`
## Quem chama / o que pode quebrar
- `arquivo:linhas` — <relação>
## Regras e how-to que se aplicam
- `.claude/rules/<tema>.md` · `how-to-<tarefa>`
## Não olhei
- <o que ficou de fora e por quê>
```

6. **Salve em `.claude/specs/<slug>/exploracao.md`** quando houver spec; sem spec, devolva só no chat.
7. **Alimente e corrija o Mapa:** resposta que demorou e vale para o futuro → proponha ao `fsk-learn` um
   ponteiro novo no Mapa do `AGENTS.md`. Ponteiro do Mapa que aponta para algo inexistente ou movido é
   reportado na hora para correção.

## Freios
Não leia arquivo inteiro sem necessidade; não liste diretórios recursivamente; não abra o que está em
"Não ler"; não opine sobre a solução — isso é do `fsk-plan` e do `fsk-build`.

## Pronto quando
Responde as 3–5 perguntas num repo real devolvendo só ponteiros, e a janela principal não recebe
nenhum conteúdo bruto.
