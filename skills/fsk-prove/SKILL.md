---
name: fsk-prove
description: Prova comportamento de verdade e sem viés — navegador > API real > integração > unitário (só com motivo escrito). Lê os critérios antes do diff; em S2+/alta roda em subagente que não viu a implementação. Dispara em "valida", "testa", "funciona?", ao terminar/fechar uma mudança de código, e no fechamento de cada fatia. Não use para revisar código (fsk-review) nem para migrar a suíte existente.
user-invocable: false
effort: medium
---

# fsk-prove — prova sem viés

Prova existe para pegar a quebra que você não veria. "Passou" significa "não encontrei problema nas
condições testadas" — e as condições são ditas. Catálogo de smoke/regressão/exploratório, oráculos e
severidade: `references/qa-amplo.md`.

**Checagem não é prova.** `tsc`, lint, typecheck e teste unitário rodam sem subir o sistema — provam que
compila e que a lógica isolada bate, **não** que o comportamento acontece. Verde neles nunca é
"provado"/"funciona": é o degrau de checagem (o **último** da escada), não a prova.

## Canal (o mais perto do usuário primeiro)
Navegador (jornada do usuário) > requisição real com banco e fila reais > integração na borda do módulo
> unitário só quando nada acima observa o efeito, com a frase do motivo escrita no arquivo. **Frontend:
só navegador.** Para descer de nível, nomeie o que o nível de cima não consegue observar naquele caso
concreto — alegação genérica ("é complexo") não serve. **Subir o sistema é o padrão, não opção:** antes
de descer de canal ou degradar, suba de verdade (inicie o Docker/serviço, rode o comando de subir do
`AGENTS.md`). "Não subi" só vale com o motivo real escrito — "tentei subir, falhou por `<erro>`" — nunca
como atalho por pressa.

## Quando o ambiente não sobe (prova degradada)
Só **depois de tentar subir de verdade** e o ambiente genuinamente não subir: lib, design system,
serverless, legado que não roda, mudança que atravessa repositórios. Não é atalho para quando subir dá
trabalho — é para quando subir é impossível. Prove o que dá — contrato e tipo, integração no pedaço que roda, consumidor real
em staging quando existir — e **diga no relatório**: "provado por X; não executado end-to-end por falta
de Y". Nunca chame de provado o que não foi observado. Infra/config e dados/migração provam pelo efeito
real (recurso criado; migration aplicada e revertida), não pela tela.

## Ferramenta de navegador
Quem dirige o navegador vem do `AGENTS.md`/manifest (ex.: Playwright, Chrome DevTools MCP). Sem driver
(WSL, container, máquina travada), caia para prova por API + verificação manual roteirizada e registre o
fallback. Login SSO/MFA/captcha: use a sessão de teste semeada no setup ou peça acesso.

## Anti-viés
- Leia os critérios **antes** do diff; o esperado vem da spec, nunca recalculado pela implementação.
- Criticidade **alta** (ou S3): rode em subagente novo que só recebe os critérios + como subir o app. Em
  S2 médio, prove inline com a mesma disciplina (ler os critérios antes do diff) — subagente só se pagar.
- Critério ambíguo vira "bloqueado" e você pergunta.

## Como observar
Além da tela: console, rede e estado persistido (recarregue a página). Varie uma coisa por vez. Repita
2–3 vezes o que parecer intermitente e registre a taxa. Separe falha do produto de falha do teste
(seletor, timing, dado ruim, ambiente). Siga um cheiro estranho com limite de tempo; sem convergir,
marque "suspeita" e volte ao plano. Eficiência: URL direta depois do primeiro caminho, sessão logada
reaproveitada, cenários com o mesmo setup agrupados, pare depois de 3 tentativas iguais.

## Segurança na prova
Quando o critério toca auth, permissão, tenant ou entrada de usuário, prove o negativo: sem permissão,
outro tenant, entrada maliciosa simples, rota protegida deslogado. Em ambiente que parece produção, nada
irreversível — pare antes do efeito real.

## Teste durável (só quando vale)
Só para contrato publicado, dinheiro, permissão/tenant, invariante que o próximo agente quebraria sem
perceber (inclusive de arquitetura, como camada que não pode importar outra), comportamento sob falha,
bug que já aconteceu. No nível mais alto que observa. Antes de escrever, três perguntas: que mudança
futura isso pega? já está coberto acima? quebra se eu refatorar sem mudar comportamento? Forma: uma
falha possível por teste, nome que diz o que quebrou, dado real, sem dublê do que dá para rodar, mensagem
de falha que explica. Suíte herdada: não abra frente de migração; ao tocar um teste acoplado, suba de
nível e apague o antigo no mesmo commit; suíte frágil encontrada é reportada, não consertada por conta.

## Execução
A suíte (tsc, lint, unitário, integração) é **checagem**: roda direcionada durante o trabalho e uma vez
no fechamento (ou CI). A **prova** dos critérios é separada — comportamento no canal real. Suíte verde não
fecha a prova. Subagente nunca roda a suíte completa.

## Saída
Veredito na primeira linha, **honesto ao canal**: ✅ só com o comportamento observado no canal real.
Parou em checagem/unitário sem subir o sistema? O veredito é "⚠️ checado, não provado end-to-end" e a
cobertura explícita nomeia o que falta subir — nunca "✅ provado". Depois a tabela `ID | resultado
(✅ ❌ ⚠️ ⏸) | canal | evidência`, com comando e saída real truncada. Cobertura explícita: o que **não** foi testado e por quê. Achados com
confiança declarada (confirmado, provável, suspeita). Questione o requisito quando o comportamento
"correto" é ruim para o usuário, como observação separada. No fechamento de S2+/alta, grave o
`evidencias.md` carimbando o **SHA do commit provado** (o `fsk-docs` só o formata para PR/binário quando
pedido; o `fsk-ship` confere que o SHA ainda bate com o diff, e re-prova se o review mexeu depois).

## Pronto quando
Prova em navegador e por API com evidência real; critério ambíguo é bloqueado, não adivinhado.
