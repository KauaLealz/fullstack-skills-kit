# Entrevista — árvore de decisões + catálogo de varredura

A entrevista rasa faz 2 perguntas óbvias e fecha. A profunda trabalha em **árvore por tema**:

1. **Monte a árvore de decisões** da demanda e **pode** os ramos que a exploração já fechou (o que o
   código/tracker/conversa respondem não vira pergunta; **contradição entre fontes é a pergunta**).
2. **Agrupe o que sobrou por tema** — cada tema é uma rodada. O critério de entrar na árvore: ambíguo,
   **perigoso inferir**, ou muda escopo/risco/prova. Respostas podem abrir ramos novos → rodada nova.
3. **Forma da pergunta:** 2–4 opções, a recomendada primeiro, cada opção com a **consequência em uma
   frase** ("per capita conta zero → famílias sem renda entram na faixa mínima").
4. **Encerramento:** pare quando só restarem decisões que não mudam o resultado ou cujo erro não custa
   refazer — não entreviste por entrevistar.
5. **Eco do Combinado:** feche devolvendo o entendimento em linguagem simples e confirme antes da spec.

Para garantir amplitude, **varra este catálogo**: cada dimensão que toca a demanda ou vira pergunta, ou
entra na spec como descarte com motivo ("sem impacto em X porque Y"). O que não aparece nem como pergunta
nem como descarte **não foi pensado**.

## Antes de qualquer pergunta
1. **Consulte o que já foi respondido:** rules, preferências, decisões de specs anteriores, Vocabulário.
   **A mesma pergunta nunca se faz duas vezes** — se já foi respondida, a resposta está gravada; se não
   está gravada, o `fsk-learn` falhou (grave agora). Perguntar é sempre bem-vindo; repetir é que cansa.
2. `fsk-explore` no terreno: o que o código faz hoje no caminho da demanda, quem chama, que dados toca.
Pergunta boa cita o estado atual: "hoje o RG é string livre sem validação (`dto.ts:42`) — a marcação CIN
valida o formato ou aceita qualquer coisa?". Pergunta sem âncora no código é chute vestido de pergunta.

## As dimensões

| Dimensão | O que perguntar (exemplos) |
|---|---|
| **Dados & retroativo** | Grava onde? Deriva ou clona? E os registros JÁ existentes — migra, ignora, oferece correção? (ex.: "aplicar nos 16 RGs que já são iguais ao CPF?") |
| **Desfazer & reversão** | O que acontece ao desmarcar/excluir/cancelar depois de salvo? O valor derivado some, fica, vira histórico? |
| **Bordas & caminho infeliz** | Entrada vazia/inválida/duplicada; concorrência (dois salvando); limite (0, 1, muitos); o que o usuário vê no erro? |
| **Permissões & tenant** | Quem pode fazer/ver? Muda por perfil? Vaza entre organizações? Precisa de aprovação de alguém? |
| **Estados & UX** | Por entidade ou por contexto (ex.: por pessoa ou por entrevista)? Estados vazio/carregando/erro; o que acontece ao navegar no meio? |
| **Consumidores & relatórios** | Quem LÊ esse dado depois? Relatórios, exportações, integrações, dashboards (ex.: "o CEBAS imprime RG — trata o documento novo?") |
| **Escala & performance** | Volume esperado? Roda em lote? Trava tela? Declare a carga assumida. |
| **Rollout & compatibilidade** | Vai por flag? Ordem de deploy (migration antes/depois)? Quebra API/contrato publicado? Convive com o fluxo antigo? |
| **Prova** | Como VOU provar cada critério — canal, dado de teste, usuário de teste? Se não sei provar, o critério está mal escrito. |

**Por tipo**, some: design/UX → estados visuais, responsivo, contraste, conteúdo real vs placeholder ·
dados/migração → janela, lock, rollback testado · refactor → inventário de chamadores e "comportamento
idêntico" medível · infra/config → ambiente por ambiente, segredo, custo.

## Forma das rodadas
0. **Cap por rodada: máx. 5 perguntas**, priorizadas escopo > segurança/dados > UX. A varredura pode
   gerar mais — o excedente vira descarte fundamentado ou espera a rodada seguinte; 12 perguntas de uma
   vez é despejo, não entrevista.
1. Rodada 1: tudo que a exploração destravou — decisões numeradas, recomendação em cada, "sim" aceita.
2. Respostas abrem fronteira nova? Rodada 2 com o que destravou. Repita até fechar.
3. Fecho da entrevista na spec: a lista de descartes com motivo + as decisões tomadas. Esse registro é o
   que o `fsk-review` usa para cobrar cobertura depois.

## Cheiro de entrevista rasa (pare e refaça)
Só 1 rodada num trabalho de médio pra cima; nenhuma pergunta cita `arquivo:linha`; nenhuma dimensão descartada por
escrito; o usuário respondeu e nada mudou no plano; critérios idênticos ao pedido original (entrevista
que não descobriu nada).
