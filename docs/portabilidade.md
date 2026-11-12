# Portabilidade — o kit em 7 provedores

O comportamento do kit roda além do Claude Code. A base é **AGENTS.md** (todos leem) e **`SKILL.md`**
(mesmo formato em 5 de 7). O resto é adaptado por alvo pelo instalador e pelo `/fsk-setup`.

## Instalar por alvo

```bash
python install/fsk.py core --target claude        # ~/.claude + @import no CLAUDE.md
python install/fsk.py core --target codex         # ~/.codex/skills + bloco em ~/.codex/AGENTS.md
python install/fsk.py core --target opencode      # ~/.config/opencode/skills + AGENTS.md
python install/fsk.py core --target cursor        # ~/.cursor/skills (núcleo vai no AGENTS.md do projeto)
python install/fsk.py core --target gemini        # ~/.gemini/skills + bloco em GEMINI.md
python install/fsk.py core --target antigravity   # ~/.gemini/config/skills + AGENTS.md
python install/fsk.py core --target copilot --project .   # .github/prompts/*.prompt.md + copilot-instructions.md
```

Claude Code também tem o plugin (`/plugin marketplace add …`), que empacota skills + o hook de núcleo.

## O que cada provedor usa

| Provedor | Memória lida | AGENTS.md | Skills | Rules por glob | Hooks (bloqueia) |
|---|---|---|---|---|---|
| **Claude Code** | `~/.claude/CLAUDE.md` | sim (import) | `SKILL.md` | `.claude/rules` `paths` | sim |
| **Codex CLI** | `~/.codex/AGENTS.md` | sim (hierárquico) | `SKILL.md` | — (AGENTS aninhado) | sim |
| **OpenCode** | `AGENTS.md` (+CLAUDE.md) | sim (sem merge) | `SKILL.md` (lê `.claude/skills`) | — | sim |
| **Cursor** | `.cursor/rules` + AGENTS.md | sim | `SKILL.md` | `.mdc` `globs:` | sim |
| **Gemini CLI** | `GEMINI.md` | via `context.fileName` | `SKILL.md` | — | sim |
| **Antigravity** | `.agents/` + `~/.gemini/` | sim | `SKILL.md` | `.agents/rules` `trigger: glob` | sim |
| **GitHub Copilot** | `.github/copilot-instructions.md` | sim | `*.prompt.md` (gerado) | `.instructions.md` `applyTo:` | sim (preview) |

## Camadas e portabilidade

- **Núcleo** → bloco `<!-- fsk:start -->…<!-- fsk:end -->` no arquivo de memória do alvo (import no
  Claude). Também entra no `AGENTS.md` do projeto, que os 7 leem — é a garantia universal.
- **Skills `fsk-*`** → `SKILL.md` reusado em Claude/Codex/OpenCode/Cursor/Gemini/Antigravity; no Copilot,
  o instalador gera `*.prompt.md` equivalente (sem as `references/`, que ficam como limite conhecido).
- **Rules** → fonte única; o `/fsk-setup` grava no formato do alvo (glob nativo nos 3 que têm; AGENTS.md
  aninhado nos que não têm).
- **Hooks (guardrails)** → opt-in; o formato muda por alvo (cada um tem `PreToolUse`/`beforeShell…` com
  bloqueio). O `guard.py` é portável; só o arquivo de registro muda.
- **MCP** → universal nos 7 (config difere, as tools não).

## Limites conhecidos
- OpenCode não mescla AGENTS.md hierárquico (first-match); em monorepo, use
  `"instructions": ["packages/*/AGENTS.md"]` no `opencode.json`.
- Codex/OpenCode/Gemini não têm rule por glob — a convenção por caminho vira AGENTS.md na subpasta.
- Copilot não usa `SKILL.md`; os prompt files cobrem o disparo por `/nome`, mas não o auto-disparo por
  `description` nem as `references/`.
