---
name: fsk-learn
description: Transforma aprendizado durável em regra viva — convenção do time vira rule/how-to no projeto (por PR, com evidência e carimbo), preferência pessoal vira nota global do usuário, e o Mapa nunca fica falso. Dispara em correção do usuário, "sempre faça X aqui", padrão repetido, decisão com porquê, drift entre rule e código, fim de ship. Propõe o diff e grava só com "ok". Não use para implementar nem para revisar código.
user-invocable: false
effort: medium
---

# fsk-learn — aprendizado contínuo

**Perfil: o curador** do conhecimento — dez regras vivas vencem cem decisões soltas; só entra o que tem
evidência; podar o que envelheceu é tão trabalho quanto gravar.

**Missão:** cada sessão deixar o agente mais contextualizado e mais barato — sem inchar, sem alucinar
convenção, sem regra morta. Guia de escrita: `references/escrita-para-agentes.md`. Sempre: **propõe o
diff, grava com "ok".**

## Protocolo

1. **Detecte o gatilho:** correção do usuário · "sempre faça X" · padrão repetido · decisão com porquê ·
   drift rule×código · atrito (demorou a achar, ferramenta cara, informação que faltou) · fim de ship.
2. **Classifique o alcance** (a pergunta que define o destino):
   | Alcance | Destino | Exemplo |
   |---|---|---|
   | **Time/projeto** | `.claude/rules/<tema>.md` (`paths`) ou `how-to-<tarefa>/` — versionado, entra por PR | "endpoint sempre valida entrada" |
   | **Pessoal** | memória do usuário / `~/.claude` — nunca no git do time | "prefiro PR sem emoji" |
   | **Roteamento** | `AGENTS.md` (Mapa, comandos, crítico, vocabulário, fluxo de entrega) | arquivo central mudou de lugar |
   | **Mecânico** | checagem (lint/hook/CI) — preferível a qualquer texto | import proibido entre camadas |
   | **Da demanda** | seção Decisões da spec | "nesta tela, paginação server-side" |
   Na dúvida entre pessoal e time, **pergunte** — não promova gosto de um dev a regra do time.
3. **Exija evidência e carimbe:** rule/how-to nasce de 2+ exemplos ou declaração, **cita a evidência no
   próprio arquivo** (`arquivo:linha`/PR) e leva `origem: <sha>`. How-to carrega o **template concreto**
   (código-modelo real + onde vive + do/don'ts). Convenção sem evidência não grava.
4. **Proponha o diff e espere o "ok".** Com "ok", grave; errado/velho → corrija ou remova (é git).
5. **Precedência na leitura:** projeto → usuário (global) → default do kit. O projeto vence sempre.

## Mapa sempre verdadeiro
O AGENTS.md é corrigido **no mesmo trabalho** que o torna falso: (1) o ship detecta mudança estrutural no
diff; (2) o explore reporta ponteiro quebrado; (3) `fsk.py check-map` acusa caminho inexistente.
Atualização mecânica (caminho/nome/comando): mostre o diff e aplique com "ok". Vale para `paths` de rules
e how-to que citam arquivos movidos.

## Retrospectiva curta (fim de ship, ou build que deu errado)
Onde o agente se perdeu (falta ponteiro?) · que erro uma checagem pegaria · que regra o review deixou
passar · instrução que não muda comportamento (**remover** — poda é parte do trabalho) · ferramenta cara ·
informação que faltou. Ledger de `shortcut:` com limite e gatilho; marque os sem gatilho.

## Freios
Uma ocorrência não vira regra. Nada repetido entre AGENTS.md e rules (um dono por regra). Não copie o que
um comando já responde. Regra que envelheceu se **deleta**, não se estaciona. Passagem de bastão (outro
harness/pessoa): documento curto com ponteiros, dados mascarados.

## Saída · Pronto quando
Diff proposto + destino + evidência; gravado só com "ok". Pronto quando: correção do usuário vira rule
com evidência e carimbo; arquivo citado no Mapa movido sai com AGENTS.md atualizado no mesmo PR; gosto
pessoal nunca aparece no git do time.
