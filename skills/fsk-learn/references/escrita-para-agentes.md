# Escrever para agente (como gravar AGENTS.md, rules e how-to)

O leitor é um agente com contexto limitado. Cada linha gravada é imposto de contexto em sessões futuras —
só fica o que muda o comportamento padrão do modelo.

## Princípios
- **Curto, imperativo, dizendo o que fazer** (não o que evitar). Proibição só como trava dura, junto do
  alvo positivo.
- **Uma regra, um lugar.** Nada repetido entre `AGENTS.md` e rules; skill aponta para skill, não copia.
- **Não copie o que o ambiente já responde** num comando (scripts do `package.json`, configs). Registre o
  que não se descobre olhando: convenção não escrita, o porquê, a pegadinha.
- **Regra de implementação mínima e por caminho** (`paths`); padrão completo fica para o `fsk-review`, que
  tem menos pressão de contexto.
- **Remova o que não muda o comportamento.** Pode o que envelheceu. Instrução que o modelo já seguiria
  sozinho é ruído.

## AGENTS.md é roteador, não enciclopédia
Mantenha < 150 linhas. Ele diz **onde** está cada coisa (Mapa, comandos, crítico, vocabulário,
ponteiros); o **como** mora nas rules e how-to, alcançados pelos ponteiros.

## Forma da rule e do how-to
Rule: a regra em 1–3 linhas + **evidência citada** (`arquivo:linha` ou link do PR de onde veio) + rodapé
`origem: <commit-sha>`. How-to: o **template concreto** — o trecho de código-modelo real do repo, onde o
arquivo novo vive, e 2–3 do/don'ts — nunca prosa abstrata ("siga o padrão do projeto" não ensina nada).

## Teste antes de gravar
- Isso muda o que o agente faria por padrão? Se não, não grave.
- Uma ferramenta consegue checar? Então vira checagem (lint/hook/CI), não texto.
- Vale para o projeto todo ou só para um caminho? Caminho → rule com `paths`.
- Apareceu 2+ vezes ou foi declarado/corrigido pelo usuário? Senão, espere — uma ocorrência não vira regra.
