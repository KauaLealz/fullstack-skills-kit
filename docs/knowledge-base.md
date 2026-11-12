# Conhecimento do projeto — o que o setup cria e o aprendizado mantém

O kit não guarda o técnico de cada projeto; o projeto guarda. Esta é a estrutura que o `/fsk-setup`
propõe e o `fsk-learn` mantém verdadeira.

```
AGENTS.md                         # roteador < 150 linhas
CLAUDE.md                         # @AGENTS.md
.claude/
  fsk.json                        # versão do kit, commit de origem, tracker, data
  fsk.local.json                  # preferências pessoais (worktree, nível de explicação) — fora do git
  rules/<tema>.md                 # convenção por caminho (frontmatter `paths`), em 2+ exemplos ou declarada
  skills/how-to-<tarefa>/         # procedimento do projeto, repetido 2+ vezes
  specs/<slug>/                   # spec.md · exploracao.md · notas.md · evidencias.md · revisao.md
  docs-templates/                 # opcional: templates da empresa (.docx com {{campos}})
docs/                             # documentação para humanos
```

## AGENTS.md — seções
Stack · Comandos (só os não óbvios, validados) · **Mapa** (por domínio: ponto de entrada, arquivos
centrais, feature de referência) · **Não ler** · Crítico · **Vocabulário** · Ferramentas de navegação ·
Worktree (receita, se validada) · Onde está cada regra.

## Quem escreve o quê

| Artefato | Dono | Quando |
|---|---|---|
| AGENTS.md (roteamento, Mapa) | `fsk-setup`, `fsk-learn` | setup; e no mesmo PR que o torna falso |
| `rules/<tema>.md` | `fsk-learn` | convenção em 2+ exemplos ou correção do usuário |
| `how-to-<tarefa>` | `fsk-learn` | procedimento repetido 2+ vezes |
| `specs/<slug>/*` | plan, explore, build, prove, docs | durante a demanda |
| Checagem (lint/hook/CI) | `fsk-learn` | erro mecânico que uma ferramenta pega |

## Portabilidade
Só o `AGENTS.md` é portável para outros agentes; rules, how-to e specs ficam no formato do Claude Code,
alcançáveis pelos ponteiros do AGENTS.md. Tudo é Markdown legível por humano e por qualquer agente,
mesmo sem o kit instalado.

## Mapa sempre verdadeiro
`fsk.py check-map` confere que todo caminho citado no AGENTS.md, nos `paths` das rules e nos how-to
existe — rodável em hook ou CI. O PR não abre com o Mapa desatualizado.
