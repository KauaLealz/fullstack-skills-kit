# Template — relatório de evidências (`.claude/specs/<slug>/evidencias.md`)

Gerado no fechamento da prova (S2+/alta). Fonte: tabela do `fsk-prove`, não memória.

```markdown
# <Título> — evidências
**Veredito:** <passou com ressalvas | passou | reprovado> · **Ambiente:** <local|staging> · **Data:** <data>

## Critérios provados
| ID | Resultado | Canal | Evidência (comando + saída truncada) |
|----|-----------|-------|--------------------------------------|
| C1 | ✅ | navegador | <passo/print> |
| C2 | ❌ | API | <request → resposta> |
| C3 | ⚠️ | estado | <observação> |
| C4 | ⏸ | — | bloqueado: <critério ambíguo> |

## Prova de segurança (se tocou auth/permissão/tenant/entrada)
- <negativo testado> → <resultado>

## Cobertura explícita
- **Não testei:** <o quê> — <por quê>
- **Intermitências:** <cenário> — taxa <n/N>

## Achados (confiança declarada)
- [confirmado|provável|suspeita] <achado> · severidade <bloqueia|grave|menor>

## Observação de produto (se houver)
<comportamento "correto" que é ruim para o usuário>
```
