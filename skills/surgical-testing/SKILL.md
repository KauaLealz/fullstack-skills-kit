---
name: surgical-testing
description: Decide em que nível testar, o que não testar e quando rodar o quê. e2e é o padrão; integração quando o e2e não isola; unitário só quando nenhum dos dois consegue observar o que precisa ser provado — e com o motivo escrito no arquivo. No frontend, só e2e. Durante o trabalho roda-se apenas o escopo tocado; a suíte completa roda uma vez, no fechamento. Dispara ao escrever, revisar, planejar ou RODAR teste, ao fechar uma mudança, ao orquestrar fases e subagentes, ao herdar suíte frágil e sempre que alguém propuser "cobertura".
---

# Surgical Testing

Teste existe para pegar a quebra que **você não veria**. Não para provar o que você acabou de
escrever, nem para encher relatório de cobertura.

A pergunta não é "quantos testes?", é **"que mudança futura isso pega?"**. Sem resposta concreta,
o teste é custo: tokens para escrever, tempo para rodar, atrito para refatorar.

## Regra de ouro

> Prove pelo fluxo real. Só desça de nível quando o nível de cima **não conseguir observar** o
> que precisa ser provado.

## A ordem

1. **E2E — o padrão.** Jornada como o usuário faz: requisição real, banco real, fila real. Um e2e
   de "criar pedido → cobrar → emitir nota" protege dezenas de unidades **e a integração entre
   elas**, que é onde a quebra mora.
2. **Integração.** Quando o e2e não isola o ponto: contrato de API, borda do módulo com o banco,
   serialização de evento, migration aplicada de verdade.
3. **Unitário — último recurso.** Só quando os dois acima não alcançam.

### Não existe categoria pré-aprovada

Não há lista de casos que "podem" ser unitários. Nem cálculo, nem parser, nem máquina de estado,
nem tabela de decisão — porque qualquer regra de negócio pode ser descrita assim, e a lista vira
a porta dos fundos por onde o viés volta.

Para descer, o agente **nomeia o que o nível acima não consegue observar naquele caso concreto**:

> ✅ "O valor intermediário do rateio só existe em memória; nenhuma resposta da API nem registro
> no banco o expõe, então o e2e não consegue afirmar que ele está certo."
>
> ❌ "A lógica é complexa e tem muitos casos." — alegação genérica não serve.

Se o agente não consegue escrever essa frase, o teste é e2e ou integração.

## Frontend é só e2e

No frontend **não se escreve unitário nem teste de componente**. Nada de jsdom, nada de montar
componente isolado. Ou o comportamento é provado no navegador, ou não é provado.

Isso vale inclusive para função pura — formatador, validador, reducer. É uma escolha deliberada:
teste de componente no front tende a verificar a própria marcação em vez do que o usuário obtém,
e envelhece a cada refatoração de UI.

## Repositório sem infra de teste

Na **primeira mudança não-trivial** de um repositório sem suíte, a infra é parte do trabalho:

- runner configurado, rodando por um comando único;
- **smoke do caminho crítico do produto** — não só o fluxo que a mudança toca. Autenticação mais
  as jornadas que sustentam o sistema.

**O agente decide quais são os fluxos críticos** lendo o código, e **grava a lista no `AGENTS.md`**
do repositório, em seção própria. Se não houver `AGENTS.md`, cria um enxuto só com essa seção —
é o começo natural da base de conhecimento do repo. O próximo agente lê em vez de reinventar, e o
dono corrige a lista quando discordar.

### As duas exceções

Entregam com **evidência manual registrada** (comando e saída, requisição, tela) e **card aberto
para a infra**, no mesmo movimento:

1. **Hotfix urgente.** Produção quebrada não espera o Playwright subir.
2. **Mudança trivial** — lista fechada, sem julgamento de tamanho: texto, label, tradução, cor,
   espaçamento, comentário, log, rename interno sem mudança de contrato.

Qualquer coisa que altere **o que o sistema faz** está fora da lista, por menor que seja o diff.
Uma linha derruba produção.

## Teste o que o próximo agente quebra

Quem vem depois — humano ou agente — não conhece as decisões tomadas. Teste **o que não está
óbvio no código**:

- **Invariante de arquitetura.** Camada que não pode importar outra, domínio sem framework, use
  case que não fala com repositório direto. Um agente refatorando "melhora" isso sem perceber.
  ArchUnit (Java/Kotlin), dependency-cruiser ou eslint-plugin-boundaries (TS/JS), import-linter
  (Python). **Um arquivo desses vale mais que cem unitários.**
- **Contrato publicado.** Resposta de API, DTO, evento, schema — quebra silenciosa que só aparece
  no cliente.
- **Isolamento de tenant, permissão e dinheiro.** O teste que impede vazamento entre organizações
  é o mais barato que existe perto do estrago que evita.
- **Bug que já aconteceu.** Todo defeito corrigido deixa teste no nível em que apareceu.
- **Comportamento sob falha.** Timeout, retry, idempotência, rollback.

## Não teste

- Getter, setter, mapper trivial, DTO burro, wiring de framework.
- Mock que valida o mock: montar o dublê, chamar, conferir que o dublê foi chamado.
- **Um teste por método.** Suíte que espelha implementação trava refatoração — muda o desenho sem
  mudar comportamento e 30 testes ficam vermelhos, então ninguém refatora.
- O mesmo caminho em três níveis.
- Cobertura como meta. Cobertura alta com asserção fraca dá confiança sem dar proteção.

## Antes de escrever, três perguntas

1. **Que mudança futura isso pega?** Sem resposta concreta, não escreva.
2. **Já está coberto por um nível acima?** Se sim, pare.
3. **Se eu refatorar sem mudar comportamento, isso quebra?** Se quebra, está acoplado à
   implementação — suba de nível ou teste pelo efeito observável.

## Como fica o teste cirúrgico

- **Uma falha possível por teste.** O nome diz o que quebrou: `rejeita_cobranca_duplicada`, não
  `testaServicoDeCobranca`.
- **Dado real, não fantasia.** Fixture inventada esconde o caso que acontece em produção.
- **Sem dublê do que dá para rodar.** Banco em container é mais fiel e quase sempre mais simples
  que um mock de repositório com oito expectativas.
- **Falha que explica.** A mensagem diz o esperado e o obtido — quem lê às 2h da manhã não deve
  precisar abrir o código.
- Desceu para unitário? **Comentário no topo do arquivo com o motivo**, na forma da regra acima.

## Suíte herdada

**Não abra frente de migração.** A regra vale para teste novo.

Quando for mexer num teste existente — porque quebrou ou porque a área mudou — aí sim: se ele
espelha implementação, sobe de nível e **apaga o antigo no mesmo commit**, para a cobertura real
não cair sem ninguém ver.

Encontrou suíte frágil que não vai tocar agora? **Reporte ao usuário no fim do trabalho** e
pergunte o que fazer: ajustar na hora, abrir card ou descartar. Não desvie o trabalho atual por
conta própria, e não deixe o achado morrer no chat.

## Como rodar: direcionado agora, completo uma vez

Rodar a suíte inteira a cada passo é o maior desperdício de tempo do ciclo. Dez minutos de
espera repetidos seis vezes numa tarefa são uma hora parada para pegar, quase sempre, nada.

**Durante o trabalho: rode só o que você tocou.** O teste do arquivo, da classe, do fluxo. Nunca
a suíte global entre um passo e outro.

| Stack | Direcionado |
|---|---|
| Maven | `mvn test -Dtest=NomeDaClasse` · `-Dtest=Classe#metodo` |
| Gradle | `gradle test --tests "*NomeDaClasse*"` |
| Jest | `jest --findRelatedTests <arquivos>` · `--onlyChanged` |
| Vitest | `vitest related <arquivos>` · `vitest run <caminho>` |
| Playwright | `npx playwright test e2e/fluxo.spec.ts` · `--grep "@tag"` |
| pytest | `pytest caminho/test_x.py::test_y` · `-k "expressao"` |
| Go | `go test ./pacote/... -run TestNome` |

**Suíte completa: uma vez, no fechamento.** Antes de declarar pronto, não antes de cada commit
intermediário. Se o repositório tem CI que roda tudo a cada push, a execução completa pode ficar
com o CI — diga isso no relatório em vez de repetir localmente o que a esteira já faz.

**O trade-off é consciente**: erro em área não tocada aparece mais tarde — no fechamento ou no
CI, não a cada passo. Essa demora é preferível a parar o trabalho seis vezes para revalidar o
que ninguém mexeu.

### Trabalho em fases e com subagentes

É onde o desperdício explode: cinco subagentes rodando a suíte global dão cinco execuções
completas para validar cinco pedaços pequenos.

- **Cada fase roda só o escopo dela.** Quem implementa a fase 2 roda os testes da fase 2.
- **Subagente nunca roda a suíte global.** Ele valida o próprio pedaço e reporta o comando e a
  saída de volta.
- **A execução completa acontece uma vez**, por quem fecha a última fase ou integra o trabalho.
- Se duas fases tocam a mesma área, quem fecha roda aquela área **uma vez**, não uma por fase.

Ao orquestrar, diga isso ao subagente explicitamente — por padrão ele roda o que achar que deve,
e o que ele acha costuma ser `npm test`.

## Fechamento

Escrever o teste não é o fim. **Rode os testes afetados e cole a saída real no relatório** —
comando executado e resultado. Teste que ninguém viu passar não prova nada, e entregar suíte que
nem compila é pior que não ter entregado.

Se a execução completa do fechamento quebrar em área que você não tocou, isso é informação, não
desculpa: investigue antes de entregar ou registre explicitamente o que ficou quebrado e por quê.

## Sinais de que a estratégia azedou

- A suíte demora tanto que as pessoas pulam.
- Falha vermelha vira ruído: "ah, esse sempre quebra".
- Mudar uma assinatura quebra dezenas de arquivos de teste.
- Ninguém sabe dizer qual bug real a suíte já pegou.
