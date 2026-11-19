# Situações de execução — como agir, com exemplo

## 1. Caminho direto (site institucional: "muda o botão do hero pra verde #2E7D32")
Gate do núcleo: pedido extremamente claro e específico ✓ · sem impacto (visual, reversível) ✓ → direto.
```
1. Mapa aponta frontend → grep "hero" → components/Hero.tsx:28
2. Edit: 1 linha (classe/token da cor)
3. Prova no canal real: abre no navegador, confere o verde (light e dark se o site tem tema)
4. Relatório: "✅ Botão do hero verde #2E7D32 — Provei: visto no navegador em / (desktop)."
```
Sem spec, sem notas, sem review formal — e **com** prova. Se no meio aparecer decisão ("o hover escurece
quanto?"), o gate quebrou: pergunta ou vira plan.

## 2. Mudança em massa (fintech: "troque as strings de status de transação por enum" — 83 arquivos)
É tipo **massa** — a spec trouxe o inventário; o build roda o protocolo:
```
1. Inventário da spec: grep -rn "'(pending|settled|refused)'" src/ → 83 arquivos, 214 ocorrências
   exclusões: src/legacy/ (Não ler), fixtures de teste entram SIM (contagem separada: 31)
2. Script: ast-grep (estrutura importa: só literais em posição de status, não logs) →
   .claude/specs/status-enum/codemod.yml — idempotente
3. Amostra: aplica em payments.service.ts, refund.worker.ts, status.spec.ts → diff revisado ✓
4. Aplica no todo → validação: 214 substituições ✓ · grep residual = 0 ✓ · tsc ✓ · vitest related ✓
5. Commit mecânico: "refactor(mecânico): status de transação string→TransactionStatus enum"
```
A mão nunca tocou os 83 arquivos; a contagem fecha a prova de completude.

## 3. Desvio do mapa (a abordagem planejada não serve)
O plano dizia "filtrar no service"; na prática o filtro precisa ir pra query (N+1 com 10k linhas).
```
notas.md ← "Fatia 2: filtro movido do service p/ query (N+1 com volume real; medido 4.2s→80ms).
            Comportamento idêntico, abordagem diferente da planejada."
```
Comportamento não mudou → segue com o desvio **registrado**. Se mudasse (ex.: paginação vira obrigatória),
para e pergunta. O que nunca se faz: trocar a abordagem em silêncio.

## 4. evidencias.md preenchido (o fecho da prova do caso 2)
```markdown
# Status enum — evidências
**Veredito:** passou · **Ambiente:** local (docker) · **SHA:** 7c21e09 · **Data:** 15/11

| ID | Resultado | Canal | Evidência |
|----|-----------|-------|-----------|
| C1 transação nova grava enum | ✅ | API | POST /payments → row status='PENDING' (psql \x) |
| C2 telas exibem status certo | ✅ | navegador | /transactions: badge "Liquidada" p/ settled (print) |
| C3 dado legado continua lendo | ✅ | API | GET /payments/1823 (row antiga) → 200, status mapeado |
| C4 contagem do codemod | ✅ | mecânico | 214/214 · grep residual 0 · tsc limpo |

## Cobertura explícita
- Não testei: export contábil (fora do inventário — não usa os literais; confirmado por grep)
## Achados
- [suspeita] webhook externo manda "SETTLED" maiúsculo — mapper aceita, mas vale card (anotado)
```
O SHA amarra a prova ao commit; o ship confere. A linha "não testei" vale tanto quanto as verdes.
