# COMPOSITION — como o kit é composto

## Princípios
1. **Skill define comportamento, nunca técnica.** O técnico de cada projeto vive no projeto (AGENTS.md,
   rules, how-to), criado pelo setup e alimentado pelo aprendizado.
2. **Poucas portas de entrada.** 4 skills via slash; o resto o agente aciona quando a situação pede.
3. **Skills próprias.** Inspiradas em Matt Pocock, Ponytail, Karpathy e no e2e-browser-qa, com crédito
   (`NOTICE.md`), mas escritas para o nosso fluxo. Nenhuma skill de processo de terceiros instalada.
4. **Processo proporcional ao risco.** Rigor = maior entre tamanho e criticidade.
5. **Prova o mais perto do usuário possível.** Navegador > integração real > unitário (só com motivo
   escrito). Quem prova não é quem implementou.
6. **Comunicação simples por padrão**, sem o usuário pedir.
7. **Um dono por comportamento.** Nenhuma regra repetida em dois lugares.
8. **O kit se adapta ao repo, não o contrário.** Fluxo e convenções já estabelecidos vencem.
9. **Código simples e legível vence código esperto.**
10. **Revisão humana é parte do produto.** A entrega vem pré-organizada para revisar rápido.
11. **Comportamento de negócio só muda com pedido ou "ok".**

## Arquitetura em 4 camadas

| Camada | O que é | Quando carrega |
|---|---|---|
| **Núcleo** | `global/fsk-workflow.md` importado no `~/.claude/CLAUDE.md` (≤ 55 linhas) | Sempre |
| **Skills de comportamento** | 10 skills `fsk-*` globais | Sob demanda (slash ou agente) |
| **Conhecimento do projeto** | `AGENTS.md` + `.claude/rules/` (com `paths`) + `how-to-*` + `.claude/specs/` | AGENTS.md sempre; rules pelo caminho do arquivo; o resto sob demanda |
| **Ferramentas** | MCPs (incluindo docgen) e skills técnicas opcionais por stack (`manifest.yaml`) | Só onde o setup propôs e você aprovou |

O núcleo existe porque comportamento "sempre ativo" não funciona como skill — skill só carrega quando
dispara.

**Guardrails (opt-in):** hooks mecânicos que bloqueiam o irreversível (git `--force`/`--no-verify`/
`reset --hard`, leitura de `.env`) e um pre-commit `check-map`. Não vêm ligados — o `/fsk-setup`
pergunta. O plugin do Claude Code só injeta o núcleo; o bloqueio é escolha do time.

## Portabilidade (7 provedores)
Base portável: **AGENTS.md** (todos leem) + **`SKILL.md`** (mesmo formato em Claude, Codex, OpenCode,
Cursor, Gemini, Antigravity; Copilot usa prompt files gerados). `fsk.py core --target <provider>` instala
em cada um. Rules de fonte única viram o formato do alvo (glob nativo onde há; AGENTS.md aninhado onde
não). Ver `docs/portabilidade.md`.

## Mudanças conscientes sobre o plano v2
- **Decisão 15 (plugin) revertida:** o kit agora empacota como plugin do Claude Code (update/uninstall,
  nuvem, CI, hooks) além do `fsk.py core`. Resolve as travas mecânicas e a distribuição.
- **Decisão 3 (portabilidade) ampliada:** não é só o AGENTS.md — as skills (`SKILL.md`) são portáveis a 5
  provedores e o instalador cobre os 7, com adaptadores por alvo para rules e hooks.
- **docgen opcional:** `fsk-docs` gera binários via docgen quando existe, senão pelas skills oficiais de
  documento — o conteúdo sai idêntico.

## Acionamento (frontmatter do Claude Code)

| Skill | Frontmatter | Efeito |
|---|---|---|
| `/fsk-plan`, `/fsk-build` | `description` com gatilhos | Slash **e** o agente aciona sozinho quando a demanda pede |
| `/fsk-setup`, `/fsk-ship` | `disable-model-invocation: true` | Só por slash; o agente **sugere** em uma linha |
| explore, prove, review, debug, docs, learn | `user-invocable: false` | Fora do menu de slash; agente e pedido natural acionam |

## De 44 para 10

As skills de processo antigas (karpathy-ponytail, using-mcps-well, fullstack-setup, project-onboarding,
project-learning, documents, surgical-testing e a cadeia Matt Pocock) foram **absorvidas** pelo núcleo e
pelas 10 `fsk-*`. O que cada fonte deixou está em `NOTICE.md`. O manifest ficou só com ferramentas.
```
discipline+flow+documents+qa de processo  →  núcleo + fsk-*
manifest                                   →  só MCPs e skills técnicas por stack (+ docgen)
```
