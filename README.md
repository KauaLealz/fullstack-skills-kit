# fullstack-skills-kit

Um núcleo de comportamento + **10 skills `fsk-*`** que levam uma demanda do pedido ao PR, no padrão de
cada repo. A skill define **como pensar, quando parar, o que provar**; a técnica (como se cria endpoint,
formato de PR, padrão de doc) vive **no projeto**, criada pelo `/fsk-setup` e alimentada pelo `fsk-learn`.

## Instalar

```bash
python install/fsk.py core                 # núcleo + 10 skills em ~/.claude (idempotente)
python install/fsk.py core --target codex  # ou: opencode, cursor, gemini, antigravity, copilot
```

Funciona em **7 provedores** (Claude Code, Codex, OpenCode, Cursor, Gemini CLI, Antigravity, Copilot) —
`SKILL.md` é o mesmo formato em 5 deles; o Copilot recebe prompt files. Detalhes e o que cada um lê:
`docs/portabilidade.md`. No Claude Code também há o plugin: `/plugin marketplace add <este repo>`.

Depois, uma vez por repositório:

```
/fsk-setup                         # detecta a stack, minera convenções, gera AGENTS.md + rules
```

O `fsk.py` também faz: `validate` (schema do manifest), `detect`/`plan` (ferramentas da stack),
`check-map` (confere que todo caminho citado no `AGENTS.md` existe — rodável em hook/CI).

**Guardrails** (bloquear git destrutivo e leitura de `.env`, pre-commit `check-map`) são **opt-in**: o
`/fsk-setup` pergunta e instala só com "ok" — nada vem travando por padrão.

## As 10 skills

| Skill | Papel |
|---|---|
| `/fsk-setup` | Deixa o repo no padrão do workflow, idempotente (slash; o agente sugere) |
| `/fsk-plan` | Classifica tipo × tamanho × criticidade e entrega o menor plano que fecha decisões e define a prova |
| `/fsk-build` | Constrói em fatias verticais, cirúrgico, provando cada fatia |
| `/fsk-ship` | Commit e PR no formato do repo, com evidência (slash; o agente sugere) |
| `fsk-prove` | Evidência real de comportamento, sem viés (navegador > API > integração > unitário) |
| `fsk-review` | Fidelidade, regras, segurança, impacto, simplicidade; limpa o diff |
| `fsk-explore` | Levanta contexto de uma área e devolve ponteiros, não conteúdo |
| `fsk-debug` | Loop vermelho, causa raiz, correção mínima |
| `fsk-docs` | Documentação, apresentações e tour guiado, no padrão do projeto |
| `fsk-learn` | Transforma aprendizado em AGENTS.md, rules e how-to |

`/fsk-plan` e `/fsk-build` também disparam sozinhas quando a demanda pede; as 6 de agente respondem a
pedido em linguagem natural ("revisa isso", "por que quebrou?", "me guia pela mudança").

## Roteiro ponta a ponta

```
/fsk-setup  (1x)
      │
/fsk-plan ── classifica · Direto · Critérios · Spec · Spec+fatias · Mapa
      │        S2+/alta: fsk-explore (impacto) antes de fechar a spec
      ▼
/fsk-build ── por fatia: muda ─► checa direcionado ─► fsk-prove
      │        bug? fsk-debug antes · fechamento: fsk-prove ─► fsk-docs ─► fsk-review
      ▼
/fsk-ship ── commits + PR no padrão do repo ─► fsk-learn (retro curta)

fsk-explore sempre que faltar contexto.  fsk-docs também a pedido.  fsk-learn quando surgir algo durável.
```

## Ferramentas por stack

O núcleo é barato e sempre ativo. Ferramentas caras (MCPs) e skills técnicas por stack ficam no
`install/manifest.yaml` e são propostas pelo `/fsk-setup` só quando a stack casa, instaladas com "ok".
Os créditos às fontes de inspiração estão em `NOTICE.md`.
