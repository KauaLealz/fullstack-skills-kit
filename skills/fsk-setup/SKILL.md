---
name: fsk-setup
description: Deixa o repo no padrão do workflow fsk de uma vez, idempotente — diagnostica stack e artefatos, roda os comandos reais, minera convenções com evidência e gera AGENTS.md (Mapa + Não ler), rules e how-to. Dispara quando o repo não tem AGENTS.md ou o usuário pede para configurar/preparar o projeto. Não use para planejar nem implementar demanda — isso é /fsk-plan e /fsk-build.
disable-model-invocation: true
effort: high
---

# fsk-setup — preparar o repo

Deixa o repositório no padrão do workflow numa passada, sem quebrar o que o time já usa (modo adoção).
Rerodar trabalha só no drift. Detalhe da estrutura gerada: `references/project-layout.md`.

As skills de comportamento (`fsk-*`) já vêm pelo `fsk.py core` e valem para todo projeto — o setup **não**
mexe nelas. Aqui se decide só as **ferramentas por stack** (do manifest), que são opcionais e instaladas
com "ok".

## Passos

1. **Diagnóstico sem perguntar.** Greenfield ou brownfield; artefatos existentes (`AGENTS.md`,
   `CLAUDE.md`, `.cursor`, `CONTRIBUTING`, `docs`, templates de PR/empresa); stack. Reuse tudo que achar.
2. **Comandos do workflow, rodados de verdade.** Instalar, subir tudo, seed + usuário de teste,
   typecheck/lint, teste de um arquivo, suíte completa, e onde ler os logs do servidor. Cada comando é
   validado rodando; o que falta é o primeiro achado (a prova depende disso). Grave só os não óbvios.
3. **Repo sem infraestrutura de prova.** Proponha o mínimo para provar o caminho crítico: runner e2e que
   roda por um comando, smoke da autenticação e das jornadas que sustentam o produto. Grave as jornadas
   críticas no `AGENTS.md`.
4. **Uma rodada de perguntas**, só sobre o que não dá para inferir: tracker, o que é crítico no produto,
   deploy, vendors, padrão de documentação, e **quais eixos de qualidade valem** (a11y, responsivo,
   performance, i18n, SEO, observabilidade) → grava `rules/eixos.md` que o review e o prove leem. Rodada
   única, cada pergunta com recomendação. Pergunta também o **modo**: compartilhado (artefatos no git do
   time) ou **local** (dev sozinho num time que ainda não adotou — AGENTS.md/rules/specs fora do git, via
   `.gitignore` ou dir pessoal, sem poluir o PR do time).
5. **Minere convenções com evidência:** PRs e commits mesclados, configs, 2–3 exemplos por camada, docs
   existentes. Padrão confirmado em 2+ exemplos ou declarado por você vira rule ou how-to; o que aparece
   uma vez não vira nada. A rule é gravada **no formato do provedor atual** (fonte única, adapta por
   alvo): Claude `.claude/rules/*.md` (`paths`) · Cursor `.cursor/rules/*.mdc` (`globs`) · Copilot
   `.github/instructions/*.instructions.md` (`applyTo`) · Antigravity `.agents/rules/*.md` (`trigger:
   glob`) · Codex/OpenCode/Gemini (sem glob) → AGENTS.md aninhado na subpasta.
6. **Gere o Mapa de navegação** no `AGENTS.md`: por domínio, o ponto de entrada (rota, tela, handler), os
   2–3 arquivos centrais e uma feature de referência para copiar o padrão. Gere a lista **Não ler**
   (build, gerado, lockfile, vendor, migration antiga). Detecte as ferramentas de navegação disponíveis
   (busca por CLI, navegação por símbolos, CodeGraph) e registre qual usar. O `AGENTS.md` **abre com o
   bloco do núcleo** (`fsk:start/end`), para que subagentes que o herdam tenham o comportamento-base — os
   nativos Explore/Plan pulam a memória, por isso o setup os desliga em favor das `fsk-*`.
7. **Guardrails mecânicos antes de regra escrita.** Sem lint/typecheck em hook ou CI, isso é achado.
   Regra que uma ferramenta consegue checar vira checagem, não texto. **Oferece (opt-in)** os guardrails
   do kit — bloquear git destrutivo e leitura de `.env` (`hooks/guardrails.settings.json`) e um pre-commit
   que roda `fsk.py check-map`; mescla no `.claude/settings.json` só com "ok". Nada disso vem ligado sozinho.
8. **Etapas que só um humano faz** (secrets, painel de cloud, CI): gere um roteiro guiado, em vez de
   explicar a cada sessão.
9. **Proponha a estrutura completa** (`references/project-layout.md`) e espere o "ok" antes de gravar.
10. **Ferramentas da stack** pelo manifest, com custo e telemetria (inclui o docgen). Instala só com "ok".
11. **Worktrees (opcional, perguntado aqui uma vez):** política `nunca` · `perguntar por demanda`
    (recomendado) · `sempre em S2+`. Se não for `nunca`, monte e **valide de verdade** a receita do repo:
    crie um worktree de teste, prepare o ambiente (dependências, copiar `.env` e não versionados, portas
    que não colidem, banco compartilhado ou isolado), suba o app e remova. A receita validada vai para a
    seção "Worktree" do `AGENTS.md`; a política, que é preferência de cada pessoa, vai para
    `.claude/fsk.local.json` (fora do git).
12. **Carimbe** `.claude/fsk.json` (versão do kit, commit de origem, tracker, data).

## Compatibilidade (o do time vence)
Mantenha `CLAUDE.md`/`AGENTS.md` próprios e some só um bloco `<!-- fsk:start -->…<!-- fsk:end -->` que
você mesmo atualiza. Leia `.cursor/rules`, `copilot-instructions`, `.windsurf` como fonte de convenção,
sem duplicar. Template de PR e CODEOWNERS do time vencem. commitlint/husky/lefthook/CI são gates a
seguir, nunca contornar. Pasta de specs/RFC do time substitui `.claude/specs`. Skills **nativas** com gatilho parecido
(`/verify`, `/code-review`, `/debug`, `/simplify`, `/run`, auto-memory): por padrão a `fsk-*` assume e a
concorrente nativa é desligada no projeto; registra a escolha. Divide o gatilho só quando o time preferir
manter as duas. Skills de terceiros com gatilho parecido: mesma decisão. Quando os fluxos
discordam, o do time vence e a diferença é dita uma vez.

## Pronto quando
Roda num brownfield real e num vazio; a segunda execução não altera nada; gera Mapa e "Não ler"; com
política de worktree diferente de `nunca`, cria, sobe e remove um worktree de teste. Ao final, roteia o
que endura para o `fsk-learn` gravar.
