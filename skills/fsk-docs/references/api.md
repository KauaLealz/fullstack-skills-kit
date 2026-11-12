# Template — API

Contrato de um endpoint ou serviço. Público: quem integra. Monte da spec e do código, não de memória.

```markdown
# <Método> <rota>
<o que faz, em uma linha>

## Requisição
- Auth: <esquema / escopo>
- Parâmetros / corpo: `<campo>` <tipo> — <regra>

## Resposta
- `200` <forma> · `4xx/5xx` <quando> → <corpo de erro no formato padrão do projeto>

## Regras e limites
- <idempotência, paginação, rate limit, versionamento>

## Exemplo
<request real → resposta real>
```
