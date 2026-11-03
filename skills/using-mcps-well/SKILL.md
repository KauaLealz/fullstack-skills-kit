---
name: using-mcps-well
description: Use antes de ligar ou chamar qualquer servidor MCP. Decide quando um MCP vale o custo de contexto e quando uma CLI, read ou grep resolve mais barato. Dispara ao considerar banco, filas, infra, browser, observabilidade, cloud ou qualquer tool de MCP.
---

# Using MCPs Well

MCP é **caro**: registra tools a cada turno e custa **4–32x mais tokens** que a CLI equivalente para a
mesma operação. Esta skill é o guarda-portão de eficiência.

## Regra de ouro
> Antes de chamar um MCP, pergunte: **um `read`, `grep` ou CLI resolve?** Se sim, não use o MCP.

## Checklist (aplique sempre)
1. **CLI primeiro.** Commit/PR → `gh`. Rodar teste → o runner do projeto. Ler arquivo → `read`. Só vá
   ao MCP quando a operação precisa de estado externo vivo (banco, fila, cluster, dashboard, API remota).
2. **Read-only primeiro.** Comece pela tool de leitura; escrita só com necessidade e, em dados/infra,
   com aprovação explícita.
3. **Ligue só o necessário.** Num projeto, mantenha ativos só os MCPs que a stack usa. Desligue o resto
   — cada MCP ligado é imposto de contexto em todo turno.
4. **Batch e filtre.** Prefira uma chamada com filtro/em lote a muitas chamadas pequenas (ex: busca de
   ícones em lote, não uma por ícone).
5. **Consulte o `usage` do item.** Cada MCP no `install/manifest.yaml` tem `usage.when`, `usage.avoid`
   e `usage.pattern`. Siga-os.

## Quando o MCP REALMENTE vale
- Estado externo que não está no código: linhas de um banco, mensagens de uma fila, pods de um cluster,
  issues de observabilidade, componentes de um registry remoto, docs versionadas de lib.
- Operação que o shell não expressa bem ou exige auth/estrutura (OAuth, tool tipada auditável).

## Quando NÃO vale
- Qualquer coisa que o repositório já contém (use CodeGraph/read/grep).
- Operações de git do dia-a-dia (use `gh`/git CLI).
- Instalar componente quando a **skill** correspondente já faz via CLI (ex: shadcn skill > shadcn MCP).

## Sinal de desperdício (pare e reavalie)
Vários MCPs ligados sem uso no projeto · chamada de MCP para ler algo que está no código · loop de
chamadas pequenas onde cabia uma em lote · MCP de um vendor que o time nem usa.
