# Instalação

O kit tem um CLI executável — **`fsk.py`** — que valida a curadoria, detecta a stack do projeto e monta o
**plano de instalação** (com custo, confiança e telemetria). Ele **não instala nada sozinho**: gera o plano
para você aprovar (propor-e-confirmar). Cross-platform (Windows/macOS/Linux).

## Pré-requisito
- Python 3.8+ e PyYAML:
  ```
  pip install pyyaml
  ```

## O CLI `fsk`

| Comando | O que faz |
|---|---|
| `python install/fsk.py validate` | Valida o schema do `manifest.yaml` (campos, ids, áreas, custo). |
| `python install/fsk.py doctor --links` | Lista `#VERIFY`, confiança `unverified`, telemetria; `--links` checa os sources por HTTP. |
| `python install/fsk.py detect --path .` | Detecta a stack (tokens) a partir dos arquivos-sinal do projeto. |
| `python install/fsk.py plan --path .` | Monta o plano: núcleo global + opcionais que casam com a stack. |

O fluxo-alvo é a skill `/fullstack-setup`, que roda o `plan`, faz o grill de vendors e instala com a sua
confirmação. Até lá, rode o `plan` e instale manualmente os itens aprovados.

## Instalação do núcleo global (uma vez)

Barato, serve qualquer projeto web. **Escolha a aba do seu shell.**

### Linux / macOS (bash/zsh)
```bash
# Disciplina (always-on) — Karpathy + Ponytail: importe no seu ~/.claude/CLAUDE.md
#   fonte: https://github.com/AbdullahHameedKhan/karpathy-ponytail-skills

npx skills add mattpocock/skills        # cadeia greenfield: to-spec, implement, tdd, code-review, pr, diagnosing-bugs
npx skills add github/awesome-copilot    # commits: git-commit, conventional-commit
claude mcp add context7 -- npx -y @upstash/context7-mcp
#   CodeGraph: rode `codegraph init` dentro de cada repo que quiser indexar

cp -r skills/using-mcps-well skills/documents skills/fullstack-setup \
      skills/project-learning skills/project-onboarding  ~/.claude/skills/
```

### Windows (PowerShell)
```powershell
# Disciplina — Karpathy + Ponytail: importe no seu $HOME\.claude\CLAUDE.md
#   fonte: https://github.com/AbdullahHameedKhan/karpathy-ponytail-skills

npx skills add mattpocock/skills
npx skills add github/awesome-copilot
claude mcp add context7 -- npx -y "@upstash/context7-mcp"
#   CodeGraph: rode `codegraph init` dentro de cada repo

$dst = "$HOME\.claude\skills"
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item -Recurse -Force skills\using-mcps-well, skills\documents, skills\fullstack-setup, `
  skills\project-learning, skills\project-onboarding $dst
```

## Por projeto

```
python install/fsk.py plan --path .
```
Revise o plano, confirme, e instale os itens aprovados (cada entrada do [manifest](./manifest.yaml) tem o
`install` e um bloco `usage`). Projeto brownfield → rode antes a `project-onboarding` para gerar a PKB.

## Gate de confiança (regra #4)

O `plan` marca cada item com a confiança:
- **oficial** (Anthropic/vendor) · **proprio** (deste kit) · **comunidade** (revisar) ·
  **NAO-VERIFICADO ⟵ AUDITAR ANTES** (link `#VERIFY` pendente ou baixa adoção).

Instalar skill/MCP = executar código de terceiros. **Nunca** instale um item `NAO-VERIFICADO` sem auditar a
fonte, e avalie itens com **telemetria** antes de ligar em contexto corporativo sensível.

## Notas de licença

- As 4 skills de documento da Anthropic (xlsx/pptx/pdf/docx) são **Proprietary** — a skill `documents`
  **instala/aponta** para as oficiais, não redistribui conteúdo.
- `nautilus` e `argonaut` são mantidos pelo autor do kit; licença pública a declarar.
