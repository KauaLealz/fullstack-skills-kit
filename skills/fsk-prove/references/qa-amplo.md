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
