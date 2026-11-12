# Instalação

O kit tem um CLI — **`fsk.py`** — que instala o comportamento (núcleo + skills `fsk-*`) e cuida das
ferramentas por stack. Cross-platform (Windows/macOS/Linux). Pré-requisito: Python 3.8+ e PyYAML
(`pip install pyyaml`).

## 1. Comportamento (uma vez, global)

```bash
python install/fsk.py core
```

Isso copia `global/fsk-workflow.md` e as 10 skills `fsk-*` para `~/.claude/` e adiciona
`@fsk-workflow.md` ao seu `~/.claude/CLAUDE.md`. É idempotente — rodar de novo sincroniza. Use
`--dry-run` para ver o que faria sem escrever, ou `--home <dir>` para um alvo de teste.

## 2. Por projeto

```
/fsk-setup
```

Detecta a stack, minera convenções, gera o `AGENTS.md` (Mapa + Não ler), as rules e o `.claude/fsk.json`.
Propõe as ferramentas da stack e instala só com o seu "ok".

## O CLI `fsk`

| Comando | O que faz |
|---|---|
| `python install/fsk.py core [--home ~] [--dry-run]` | Instala núcleo + skills `fsk-*` em `~/.claude`. |
| `python install/fsk.py validate` | Valida o schema do `manifest.yaml` (campos, ids, áreas, custo). |
| `python install/fsk.py detect --path .` | Detecta a stack (tokens) a partir dos arquivos-sinal. |
| `python install/fsk.py plan --path .` | Monta o plano de ferramentas que casam com a stack. Não instala. |
| `python install/fsk.py doctor [--links]` | `#VERIFY`, confiança `unverified`, telemetria; `--links` checa sources. |
| `python install/fsk.py check-map --path .` | Confere que todo caminho citado no `AGENTS.md`/rules/how-to existe. |
| `python install/fsk.py worktree <nome>` | Cria worktree em `.worktrees/<nome>` e copia os não-versionados (artefatos de agente, `.env`). |
| `python install/fsk.py git-hooks [--local-mode]` | Instala hooks git (opt-in): post-checkout propaga p/ worktree nova; pre-commit barra segredo + `check-map`. `--local-mode` ignora os artefatos de agente no git. |

## Ferramentas por stack

O `plan` e o `/fsk-setup` leem o `manifest.yaml` (só ferramentas: MCPs e skills técnicas por stack, com
custo, confiança e telemetria). Nada é instalado sem a sua confirmação; itens `unverified` pedem auditoria
antes. O `check-map` serve para hook ou CI — sai com erro se o Mapa do `AGENTS.md` aponta para um caminho
que não existe mais.
