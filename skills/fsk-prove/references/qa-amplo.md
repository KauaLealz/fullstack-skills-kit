# QA amplo — modos de prova, oráculos e severidade

Carregue quando a prova passa de "confere o critério" para cobrir risco de verdade (S2+/alta, release,
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

## Não teste (a lista negativa)
- Getter, setter, mapper trivial, DTO burro, wiring de framework.
- Mock que valida o mock: montar o dublê, chamar, conferir que o dublê foi chamado.
- **Um teste por método** — suíte que espelha implementação trava refatoração.
- O mesmo caminho em três níveis. Cobertura como meta (cobertura alta com asserção fraca dá confiança
  sem dar proteção).

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
