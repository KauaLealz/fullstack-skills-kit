# Template — runbook

Para operar e responder a incidente. Público: plantão, SRE, dev de sobreaviso. Passos executáveis.

```markdown
# Runbook — <serviço / fluxo>

## Sinais de que algo está errado
- <sintoma> — <onde ver: dashboard, log, alerta>

## Diagnóstico rápido
1. <comando / consulta> → <o que indica>

## Mitigação (antes de entender a causa)
- <rollback / flag / escala> — reversível? <sim|não> · precisa de "ok"? <sim>

## Causa raiz e correção
<para o fsk-debug; registre a hipótese confirmada>

## Contatos e dependências
- <serviço externo, dono, vendor>
```
