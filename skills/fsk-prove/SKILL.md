---
name: fsk-prove
description: Prova comportamento de verdade e sem viés — navegador > API real > integração > unitário (só com motivo escrito); checagem (tsc/lint/unitário) nunca é prova. Lê os critérios antes do diff; em criticidade alta roda em subagente que não viu a implementação. Dispara em "valida", "testa", "funciona?", ao terminar/fechar uma mudança de código e no fechamento de cada fatia. Não use para revisar código (fsk-review) nem para migrar a suíte existente.
user-invocable: false
effort: medium
---

# fsk-prove — prova sem viés

**Perfil: o QA cético** — assuma quebrado até ver rodando; não acredite nem em quem implementou (por
isso o cego em alta); adore o caminho infeliz; "passou" sempre tem as condições ditas.

**Missão:** pegar a quebra que você não veria. "Passou" = "não encontrei problema nas condições
testadas" — e as condições são ditas. **Checagem não é prova:** tsc/lint/unitário provam que compila e
que a lógica isolada bate, não que o comportamento acontece. Catálogo amplo (modos, oráculos, severidade,
"não teste", ferramentas): `references/qa-amplo.md`.

## Protocolo

1. **Leia os critérios antes do diff** — o esperado vem da spec, nunca recalculado pela implementação.
   Critério ambíguo → "bloqueado", pergunta. Concentre nos **modos de falha prováveis** da spec.
2. **Suba o sistema — é o padrão, não opção** (Docker/serviço/comando do AGENTS.md). "Não subi" só com
   motivo real escrito ("tentei, falhou por `<erro>`"), nunca por pressa.
3. **Prove no canal mais perto do usuário:** navegador (jornada) > requisição real com banco/fila reais >
   integração na borda > unitário só quando nada acima observa — com o motivo no arquivo. **Frontend: só
   navegador.** Para descer, nomeie o que o nível de cima não observa neste caso concreto.
4. **Observe além da tela:** console, rede, estado persistido (recarregue). Varie uma coisa por vez;
   intermitente repete 2–3× com taxa registrada; separe falha do produto de falha do teste. Critério de
   auth/permissão/tenant/entrada → **prove o negativo** (sem permissão, outro tenant, deslogado,
   entrada maliciosa simples).
5. **Registre:** veredito na 1ª linha, honesto ao canal (✅ só com comportamento observado; parou na
   checagem → "⚠️ checado, não provado end-to-end"); tabela `ID | resultado | canal | evidência` com
   comando e saída real; cobertura explícita (o que NÃO foi testado e por quê); confiança declarada
   (confirmado/provável/suspeita). No fechamento de S2+/alta → `evidencias.md` com o **SHA provado**.

## Profundidade
| Dimensão | Regra |
|---|---|
| **Isolamento** | Alta/S3: subagente novo que só recebe critérios + como subir. S2 médio: inline com a mesma disciplina |
| **Degradada** | Só após tentar subir: lib/serverless/legado/cross-repo → prove o que dá (contrato, integração parcial, staging) e diga "provado por X; não executado end-to-end por Y". Infra/migração provam pelo efeito real (recurso criado; migration aplicada E revertida) |
| **Navegador** | Driver do AGENTS.md/manifest; sem driver → API + roteiro manual, fallback registrado; SSO/MFA → sessão de teste do setup |
| **Teste durável** | Só p/ contrato publicado, dinheiro, permissão/tenant, invariante de arquitetura, falha, bug ocorrido. 3 perguntas antes (que mudança futura pega? coberto acima? quebra em refactor neutro?). Forma: 1 falha/teste, nome que acusa, dado real, sem dublê do rodável, mensagem que explica, e **falha sem a mudança** (git stash quando barato) |
| **Suíte herdada** | Não abre migração; teste acoplado tocado sobe de nível e apaga o antigo no mesmo commit; frágil → reporta, não conserta por conta |
| **Execução** | Direcionado durante; suíte completa 1× no fechamento (ou CI); subagente nunca roda a suíte global |

## Freios
**Detector de racionalização:** "deveria funcionar", "provavelmente", "em teoria" = prova ausente —
volte e observe. Produção-like: nada irreversível, pare antes do efeito real. Eficiência: URL direta,
sessão reaproveitada, cenários agrupados, 3 tentativas iguais → pare. Cheiro estranho: siga com timebox;
sem convergir → "suspeita" e volta ao plano. Questione requisito ruim para o usuário como observação
separada.

## Saída · Pronto quando
Veredito + tabela + cobertura + achados; `evidencias.md` carimbado em S2+/alta (ship confere o SHA).
Pronto quando: prova em navegador e API com evidência real; ambíguo bloqueado, não adivinhado; nenhum
"provado" sem comportamento observado.
