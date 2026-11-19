# QA amplo — pirâmide, modos de prova, oráculos e severidade

## A pirâmide (velocidade embaixo, custo em cima — e a validação mora em cima)
| Camada | Papel | Quando roda |
|---|---|---|
| **Exploratório** | Cheiro fora do roteiro, com timebox | Área nova/suspeita, release |
| **E2E** | Validar a jornada como o usuário vive (navegador) | Prova de critério — o canal padrão |
| **Aceitação** | Validar o critério pela borda real (API + banco/fila reais) | Quando o E2E não isola o ponto |
| **Integração** | Borda do módulo: contrato, serialização, migration real | Quando a camada acima não observa |
| **Unitário** | **Sustentação, não validação**: lógica que nada acima observa, com motivo escrito | Direcionado no trabalho; suíte 1× no fechamento — **requisito de entrega** |

Regra de ouro: **valide na camada mais alta viável; desça só nomeando o que a de cima não observa.**
Validar comportamento "só no unitário" é o anti-padrão que esta pirâmide existe para impedir.

Carregue quando a prova passa de "confere o critério" para cobrir risco de verdade (trabalho maior ou arriscado, release,
caminho crítico).

## Risco = impacto × probabilidade
Priorize cenário por risco, não por facilidade de testar. Alto impacto + alta chance primeiro: dinheiro,
auth, perda de dado, jornada que sustenta o produto.

## Modos de prova
| Modo | Para quê | Quando |
|---|---|---|
| **Smoke** | O caminho crítico sobe e responde | Toda mudança não trivial; após deploy |
| **Critério** | Cada item de aceite observável de fora | Sempre |
| **Regressão** | O que já funcionava continua | Mudança em área com histórico de quebra |
| **Negativo** | Sem permissão, outro tenant, entrada inválida/maliciosa | Critério toca auth/permissão/tenant/entrada |
| **Exploratório** | Cheiro fora do roteiro, com limite de tempo | Área nova ou suspeita; registra o que achar |
| **Carga leve** | Comportamento sob a carga esperada (declare qual) | Só quando o critério fala de volume |

## Oráculos (como saber que está certo)
- **Esperado da spec** — a fonte primária; nunca recalcule pela implementação.
- **Estado persistido** — recarregue e confira o que ficou no banco/armazenamento, não só a tela.
- **Antes/depois** — compare o comportamento com o estado anterior à mudança.
- **Consistência** — o mesmo dado bate entre tela, API e banco.
- **Invariante** — o que nunca pode ser verdade (saldo negativo, pedido sem dono).

## Severidade do achado
| Nível | Critério | Efeito |
|---|---|---|
| **Bloqueia** | Caminho crítico quebrado, perda de dado, falha de permissão | Não entrega |
| **Grave** | Jornada secundária quebrada, erro visível sem perda | Corrige antes do ship ou registra com "ok" |
| **Menor** | Cosmético, borda rara, mensagem imprecisa | Anota; corrige se barato |
| **Suspeita** | Cheiro sem reprodução estável | Marca e devolve ao plano, não bloqueia sozinho |

## Separar falha do produto de falha do teste
Antes de reportar bug, descarte: seletor frágil, timing/espera, dado de setup ruim, ambiente. Falha de
teste vira conserto do teste (ou report da suíte frágil), não bug do produto.

## O teste nasce da spec
O critério de aceite define o ponto observável; o teste deriva dele. Confirmar que o teste falha sem a
mudança serve para validar que ele testa algo real. Critério sem canal de prova definido é critério mal
escrito — volta ao plan.

## Não teste — anti-padrões com o "tell" que os delata
- **Acoplado à implementação** · tell: quebra num refactor que não muda comportamento.
- **Tautológico** · tell: a asserção confirma o que o próprio teste montou (mock valida o mock).
- **Fatia horizontal** · tell: testa uma camada isolada, não um comportamento que alguém pediu.
- **Espelho de método** (um teste por método) · tell: mudar uma assinatura quebra dezenas de testes.
- **Cobertura como meta** · tell: cobertura alta com asserção fraca — confiança sem proteção.
- Getter, setter, mapper trivial, DTO burro, wiring de framework: não teste. O mesmo caminho em três
  níveis: não repita.

## Invariante de arquitetura (um arquivo vale cem unitários)
Camada que não importa outra, domínio sem framework, use case que não fala com repositório direto — o
próximo agente "melhora" isso sem perceber. Ferramentas: **ArchUnit** (Java/Kotlin),
**dependency-cruiser** / **eslint-plugin-boundaries** (TS/JS), **import-linter** (Python).

## Teste direcionado por stack (anti-voltas; o do repo vai no AGENTS.md)
| Stack | Direcionado |
|---|---|
| Jest | `jest --findRelatedTests <arquivos>` · `--onlyChanged` |
| Vitest | `vitest related <arquivos>` · `vitest run <caminho>` |
| Playwright | `npx playwright test e2e/fluxo.spec.ts` · `--grep "@tag"` |
| pytest | `pytest caminho/test_x.py::test_y` · `-k "expressão"` |
| Maven/Gradle | `mvn test -Dtest=Classe#metodo` · `gradle test --tests "*Classe*"` |
| Go | `go test ./pacote/... -run TestNome` |

## As duas únicas exceções de prova (com evidência manual + card da infra)
1. **Hotfix urgente** — produção quebrada não espera o runner subir.
2. **Mudança trivial, lista fechada:** texto, label, tradução, cor, espaçamento, comentário, log, rename
   interno sem mudança de contrato. Qualquer coisa que altere **o que o sistema faz** está fora da lista,
   por menor que seja o diff.

## Sinais de que a suíte azedou (reporte)
Demora tanto que pulam · falha vermelha virou ruído ("esse sempre quebra") · mudar uma assinatura quebra
dezenas de testes · ninguém sabe qual bug real a suíte já pegou.
