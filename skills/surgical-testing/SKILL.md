---
name: surgical-testing
description: Decide em que nível testar e o que não testar. Prioriza e2e e integração; teste unitário é último recurso, só quando os níveis acima não alcançam o fluxo. Dispara ao escrever, revisar ou planejar testes, ao fechar uma mudança ("rode os testes"), ao herdar suíte lenta ou frágil, e sempre que alguém propuser "cobertura".
---

# Surgical Testing

Teste existe para pegar a quebra que **você não veria**. Não para provar o que você acabou de
escrever, nem para encher relatório de cobertura.

A pergunta não é "quantos testes?", é **"que mudança futura isso pega?"**. Se a resposta for
"nenhuma", o teste é custo: tokens para escrever, tempo para rodar, atrito para refatorar.

## Regra de ouro

> Prove pelo fluxo real. Só desça de nível quando o nível de cima **não alcançar** o que precisa
> ser provado.

## A ordem (de cima para baixo)

1. **E2E — o padrão.** Exercita a jornada como o usuário faz: requisição real, banco real,
   fila real. Um e2e que cobre "criar pedido → cobrar → emitir nota" protege dezenas de unidades
   de uma vez, e protege a **integração entre elas** — que é onde a quebra mora.
2. **Integração.** Quando o e2e não isola o que você quer provar: contrato de API, borda do
   módulo com o banco, serialização de evento, migration aplicada de verdade.
3. **Unitário — último recurso.** Só quando os dois acima **não conseguem** validar o que
   importa. São os casos honestos: cálculo com muitas combinações, parser, máquina de estado,
   regra com tabela de decisão grande. Aí o unitário é a ferramenta certa — rodar 40 combinações
   por e2e seria absurdo.

Escolheu unitário? Diga no código **por que** o nível de cima não servia. Uma linha de comentário
evita que o próximo agente ache que é só preguiça.

## Teste o que o próximo agente quebra

Quem vem depois — humano ou agente — não conhece as decisões que você tomou. Teste **as regras
que não estão óbvias no código**:

- **Invariante de arquitetura.** Camada que não pode importar outra, domínio sem dependência de
  framework, use case que não fala com repositório direto. Um agente refatorando "melhora" isso
  sem perceber. Ferramentas: ArchUnit (Java/Kotlin), dependency-cruiser ou eslint-plugin-boundaries
  (TS/JS), import-linter (Python). **Um arquivo desses vale mais que cem unitários.**
- **Contrato publicado.** Resposta de API, DTO, evento, schema. Quebra silenciosa que só aparece
  no cliente.
- **Isolamento de tenant, permissão e dinheiro.** O teste que impede o vazamento entre
  organizações é o mais barato que existe perto do estrago que evita.
- **Bug que já aconteceu.** Todo defeito corrigido deixa um teste no nível em que ele apareceu.
- **Comportamento sob falha.** Timeout, retry, idempotência, rollback — o caminho triste é o que
  ninguém testa à mão.

## Não teste

- Getter, setter, mapper trivial, DTO burro, wiring de framework.
- Mock que valida o mock: montar o dublê, chamar, conferir que o dublê foi chamado. Isso testa
  que você sabe configurar mock.
- **Um teste por método.** Suíte que espelha a implementação trava refatoração: muda o desenho
  sem mudar comportamento e 30 testes ficam vermelhos — então ninguém refatora.
- O mesmo caminho em três níveis. Se o e2e cobre, o unitário igual é redundância que você vai
  manter para sempre.
- Cobertura como meta. Cobertura alta com asserção fraca é pior que cobertura baixa: dá confiança
  sem dar proteção.

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
- **Falha que explica.** A mensagem diz o que era esperado e o que veio — quem lê às 2h da manhã
  não deve precisar abrir o código.
- **Teste é código.** Mesma régua de clareza; teste ilegível não é protegido por ninguém.

## Ao herdar suíte existente

Não saia apagando. Rode, veja o que falha por motivo real e o que falha por forma. Os que quebram
a cada refatoração sem apontar defeito são candidatos a subir de nível — substitua um punhado de
unitários frágeis por um e2e do mesmo fluxo e apague os antigos **no mesmo commit**, para a
cobertura real não cair sem ninguém ver.

## Sinais de que a estratégia azedou

- A suíte demora tanto que as pessoas pulam.
- Falha vermelha vira ruído: "ah, esse sempre quebra".
- Mudar uma assinatura de método quebra dezenas de arquivos de teste.
- Ninguém sabe dizer qual bug real a suíte já pegou.
