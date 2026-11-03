# fullstack-engineer-curated-skills

Kit curado de **skills, MCPs e ferramentas** para um engenheiro de software fullstack trabalhar com
agentes de IA de forma **mais eficiente, contextualizada, rápida e assertiva** — em projeto pessoal,
na empresa, ou em qualquer stack.

Não é uma lista. É uma **curadoria com critério**: o que entra, por que entra, o que fica de fora,
e **como as peças trabalham juntas sem conflito** nem desperdício de contexto.

## Escopo

Foco **explícito** em **aplicações web** — frontend web, backend/API, dados, filas, infra, observabilidade,
segurança e QA de web, ponta a ponta. **Fora de escopo por ora** (declarado, não esquecido): mobile/native
(React Native, Flutter, iOS/Android), desktop nativo e ML/data-engineering. Isso mantém a curadoria densa e
sem prometer o que não entrega.

## Princípio-mestre

> **Skill é barato. MCP é caro.**
> Uma *skill* só entra no contexto quando dispara (lazy-load). Um *MCP* registra tools a cada turno
> e custa **4–32x mais tokens** que a CLI equivalente para a mesma operação.

Disso decorre tudo:

- A **plataforma global** (`~/.claude`) carrega só o **barato** (skills de disciplina/fluxo) + **2 MCPs
  genéricos** que servem qualquer projeto (CodeGraph, Context7).
- **Todo o resto é por-projeto**, ligado pela skill `fullstack-setup` **só quando a stack pede** —
  nada de MCP de Kafka num projeto sem fila.
- Quando uma **CLI resolve** (ex: `gh` para commit), **não se usa MCP**.

## Como funciona

```
1. Instala o núcleo global (uma vez)      → skills de disciplina + CodeGraph + Context7
2. Em cada projeto: roda  /fullstack-setup → detecta a stack, faz um grill curto (vendors),
                                              e liga só os opcionais que fazem sentido
3. Usando o projeto: /project-learning     → aprende suas convenções e PROPÕE (com seu "ok")
                                              AGENTS.md, rules e skills locais — fica mais rápido
                                              conforme você usa
```

## O que tem dentro

| | |
|---|---|
| **Disciplina (sempre-on, barato)** | Karpathy+Ponytail (pensar antes, mudança cirúrgica, anti-overengineering) · using-mcps-well |
| **Fluxo (on-demand)** | to-spec · diagnosing-bugs · code-review · security-audit · spec-kit (tarefa grande) |
| **Code intelligence (2 MCPs globais)** | CodeGraph · Context7 |
| **Por-projeto, por stack** | Frontend/UI · Backend/API · Banco · Filas · Infra · Secrets · Tasks · Observabilidade · QA · Segurança |
| **Skills originais** | `fullstack-setup` · `project-learning` · `project-onboarding` · `using-mcps-well` · `documents` |

Catálogo completo em **[CATALOG.md](./CATALOG.md)**. Regras de convivência em **[COMPOSITION.md](./COMPOSITION.md)**.
Fonte da verdade (machine-readable) em **[install/manifest.yaml](./install/manifest.yaml)**.

## Instalação

Enquanto a `fullstack-setup` não está publicada, veja **[install/README.md](./install/README.md)** para
instalação manual do núcleo. O objetivo final é: `/fullstack-setup` e pronto.

## Filosofia de curadoria

- **Sem redundância.** Duas ferramentas que fazem a mesma coisa → fica a melhor (ex: shadcn **skill**
  no lugar do shadcn MCP no Claude Code; `gh` CLI no lugar do GitHub MCP para commits).
- **Sem orquestrador pesado.** `superpowers` e `gsd-core` ficaram **de fora** — contrariam a filosofia
  de mudança mínima. A disciplina vem de Karpathy+Ponytail, leve.
- **Observabilidade e cloud são categorias multi-vendor**, não um fornecedor fixo. A setup liga o que
  o seu time usa (Grafana/Sentry/Datadog/CloudWatch...).
- **Evolui com você.** `project-learning` transforma o kit num sistema que fica mais afiado por projeto.
