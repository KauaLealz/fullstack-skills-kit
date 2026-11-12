---
name: fsk-debug
description: Diagnostica e corrige bug pela causa raiz — loop vermelho primeiro, hipóteses falsificáveis, correção mínima no ponto compartilhado. Dispara em "quebrou", "erro", "não funciona", stack trace, ou algo lento/falhando. Não use para feature nova (fsk-plan/fsk-build) nem para só validar o que já funciona (fsk-prove).
user-invocable: false
effort: high
---

# fsk-debug — bug pela causa raiz

0. **Sem ponto de partida no código** → `fsk-explore` com a pergunta "que caminho o sintoma percorre?".
1. **Loop vermelho primeiro.** Um comando que já roda e falha neste bug, no canal mais perto do usuário
   possível: rápido, determinístico, rodável sem humano. Sem loop, não há hipótese. Bug intermitente:
   suba a taxa de reprodução até ficar depurável. Não conseguiu: diga o que tentou e peça acesso,
   artefato capturado ou permissão para instrumentar.
2. **Reproduza e minimize.** Confirme que é o sintoma do usuário; corte até sobrar só o essencial.
3. **3–5 hipóteses falsificáveis** ("se X é a causa, mudar Y faz sumir"), ranqueadas e mostradas ao
   usuário sem bloquear.
4. **Instrumente uma variável por vez.** Logs temporários com prefixo único para limpar depois com um
   grep. Performance: meça primeiro, corrija depois.
5. **Causa raiz.** Busque todos os chamadores e corrija no ponto compartilhado, uma vez.
6. **Regressão** no nível em que o bug apareceu (`fsk-prove`). Se não existe um ponto bom para travar o
   bug, isso é achado para o `fsk-learn`.
7. **Limpeza.** Loop original verde, logs temporários removidos, hipótese correta registrada no commit.
8. **Produção quebrada:** mitigue primeiro (rollback, flag) com "ok"; entenda depois.

## Pronto quando
Um bug real resolvido a partir de um loop vermelho, com a causa raiz corrigida no ponto compartilhado e a
regressão travando o retorno.
