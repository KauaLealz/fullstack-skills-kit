---
name: fullstack-setup
description: Configura o kit curado num projeto. Detecta a stack, faz um grill curto sobre os vendors que o time usa, e instala só o que faz sentido — o núcleo global (uma vez) mais os opcionais por-projeto que casam com a stack. Dispara ao entrar num projeto novo ou existente, ou quando o usuário pede para configurar/instalar as ferramentas.
---

# Fullstack Setup

O instalador inteligente. Em vez de empurrar tudo, **detecta** e **pergunta** antes de ligar qualquer
coisa cara. Lê o `install/manifest.yaml` como fonte da verdade.

## Fluxo

### 1. Núcleo global (só uma vez por máquina)
Se ainda não instalado em `~/.claude`, instale os itens `scope: global` do manifest: disciplina
(Karpathy+Ponytail), `using-mcps-well`, skills de fluxo, conventional-commit, as skills originais do kit,
e os **2 MCPs genéricos** (CodeGraph, Context7). Nada mais vai para o global.

### 2. Detecte a stack (sinais no repositório)
**Motor:** rode `python install/fsk.py plan --path .` — ele já detecta a stack, casa com o manifest e
imprime o plano (núcleo global + opcionais que casam) com **custo, confiança e telemetria** por item.
Use a saída como base; confirme/complemente lendo manifests e arquivos-sinal para inferir `stack_match`:
- `package.json` (e deps: react/next/vue/svelte/angular, tailwind, playwright...)
- `pyproject.toml`/`requirements.txt`, `go.mod`, `pom.xml`/`build.gradle`, `Cargo.toml`
- `Dockerfile`/`compose`, `*.tf`, `*.yaml` (k8s/helm), `.gitlab-ci.yml`/`.circleci`
- `*.sql`, drivers de banco, `*.openapi.yaml`/`swagger`
- `.figma`, config de observabilidade, etc.

### 3. Grill curto (só o que a detecção não resolve)
Pergunte **apenas** o que muda a seleção e não dá para inferir — uma pergunta por vez, recomendação
primeiro. Tipicamente **vendors**:
- "Qual observabilidade o time usa?" (Grafana / Sentry / Datadog / CloudWatch / nenhuma)
- "Qual cloud?" (AWS / Azure / nenhuma)
- "Task manager?" (Linear / Jira / nenhum)
- "Secrets?" (Infisical / Vault / nenhum)
- "Banco com escrita/migrations?" (Neon / Supabase / PlanetScale / CLI própria)

### 4. Selecione e proponha
Monte a lista: itens cujo `stack_match` casa com a stack detectada **+** os vendors confirmados no grill.
**Apresente a lista** (o que vai ligar e por quê, com o custo 🟢/🔴) e **espere o "ok"**. Não instale MCP
sem confirmação.

### 5. Instale e configure o `usage`
Para cada item aprovado, rode o `install` do manifest e registre o bloco `usage` (when/avoid/pattern)
onde o agente consiga consultar (a `using-mcps-well` depende disso). Fixe no `AGENTS.md` o que for
decisão de projeto (ex: 1 biblioteca de ícones).

### 6. Sugira skills por-stack
Com base na linguagem/framework, sugira as referências/boas-práticas correspondentes
(ex: React/Next → vercel-react-best-practices; Vue → vue-best-practices; Java → boas práticas Java;
banco X → boas práticas do banco X). Confirme antes de adicionar.

### 7. Bootstrap da Base de Conhecimento (PKB) — o passo que mais gera valor
Não deixe o agente redescobrir o padrão (e gastar tokens) a cada sessão. Já no setup, crie a base:
- **Projeto brownfield (tem código/histórico):** rode a `project-onboarding` — ela minera código + git +
  PRs e **propõe** `AGENTS.md`, `rules/` de convenção (ex: `pr.md`, `commits.md`, `testing.md`,
  `error-handling.md`) e **pattern skills** ("how-to-create-dto", "how-to-add-endpoint"...). Grave com "ok".
- **Projeto greenfield (novo):** semeie a base mínima — `AGENTS.md` esqueleto (stack escolhida, comandos),
  `rules/_candidates.md` vazio, e defina a **cadeia de orquestração de desenvolvimento novo** do Matt Pocock
  (`to-spec → implement → tdd → code-review → pr`). As rules/pattern skills nascem conforme o código surge,
  via `project-learning`.

### 8. Ligue o aprendizado contínuo
Garanta `project-learning` ativa: a partir daqui, toda convenção/decisão/padrão repetido vira proposta de
enriquecimento da PKB (com "ok"). A base fica mais afiada a cada sessão.

## Princípios
- **Nada caro no global** além dos 2 MCPs genéricos.
- **Nunca ligar um MCP de vendor que o time não usa.**
- **Propor-e-confirmar** antes de instalar MCP e antes de gravar qualquer artefato da PKB.
- **A PKB é o maior multiplicador**: destila uma vez, lê barato para sempre. Priorize criá-la no setup.
- Escopo: aplicações web (ver `scope_focus` no manifest).
