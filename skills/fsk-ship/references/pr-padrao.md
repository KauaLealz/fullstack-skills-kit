# PR padrão do kit (quando o repo não tem formato próprio)

O corpo do PR é a versão enxuta do `revisao.md`. Se o repo tem template (`.github/pull_request_template.md`),
ele vence e o dossiê preenche as seções dele.

```markdown
## <Título> — <o que muda para o usuário, em uma frase>

### Resumo
<a menor visualização que deixa claro: pseudocódigo, árvore de chamadas, árvore de componentes, árvore de
arquivos, Mermaid ou diff-esboço> + o texto curto que ela sustenta.

### Evidência
<antes/depois · captura de tela quando a mudança é visual, saída de execução quando não é (do evidencias.md)>

### Risco de merge
- **Porta:** <mão única | mão dupla (dá para desfazer?)>
- **Raio de impacto:** <chamadores, dados, contratos>
- **Reversão / ordem de deploy:** <passos, migration>

### Mudanças de comportamento
<tabela do dossiê, ou "Nenhuma regra de negócio alterada">
```

## Commits por intenção
`mecânico` (rename, mover, formatação) · `refactor` (comportamento idêntico) · `comportamento` (muda o
que o produto faz) — em commits separados, no formato do repo (conventional commit se o histórico usa). O
revisor pula o mecânico com segurança.

## Comentários do agente no PR
Máx. 5, um por "Onde olhar com atenção", ancorado na linha, prefixo `🤖 fsk:`, três linhas no máximo,
nunca em linha mecânica. Some quando o time não usa bot.
