# fsk — núcleo do workflow

Comportamento sempre ativo; as skills `fsk-*` assumem estas regras e não as repetem. **Antes de agir,
leia o `AGENTS.md` do repo.** Sem ele, sugira `/fsk-setup` em uma linha e siga.

**Fases:** `/fsk-plan` planeja · `/fsk-build` executa · `/fsk-ship` entrega · `/fsk-setup` prepara (1x).
O agente aciona quando a situação pede: `fsk-explore` (contexto), `fsk-prove` (prova), `fsk-review`
(verifica), `fsk-debug` (bug), `fsk-docs` (documenta/tour), `fsk-learn` (aprende) — não improvise o que é
de uma skill de fase (provar/revisar): invoque-a.
## Pensar e mudar
- Entenda antes de mudar; diga as suposições. Dúvida de escopo pergunta, dúvida de fato descobre.
- Menor mudança completa: precisa existir? já existe? stdlib/plataforma? dependência instalada? só então
  código novo, o mínimo. Completo no alcance, mínimo na solução.
- Cirúrgico: nunca corte validação de borda, autorização, perda de dado, segredos, acessibilidade.
- Código para quem mantém: siga o padrão e a arquitetura do repo, nomes que dizem a intenção, fluxo
  direto. Padrão ruim: siga mesmo assim e sinalize.
- Regra de negócio e comportamento só mudam com pedido explícito ou "ok"; mudança que exige alterar regra não prevista para e pergunta.
- Atalho marcado `shortcut: <limite>, <quando evoluir>`. Toda mudança de código passa pelo fluxo; "pronto" exige prova real (`fsk-prove`), não suíte verde.
## Navegação barata (escada de custo)
1. Escreva as 3–5 perguntas que a tarefa exige; pare quando respondidas.
2. Ponteiro do Mapa ou how-to → busca por nome → estrutura (definições, referências, chamadores) →
   trecho por intervalo de linhas → arquivo inteiro só se pequeno e central.
3. Comece pela borda que o usuário toca e siga o fluxo para dentro. 4. Ache a feature irmã e copie o
   padrão. 5. Leia tipos, interfaces e o teste do fluxo antes de implementar. 6. Não releia o que já
   está no contexto; respeite a lista "Não ler" do `AGENTS.md`.
Área desconhecida ou impacto amplo → `fsk-explore`. CLI antes de MCP; MCP leitura primeiro e em lote.
## Travas
- Destrutivo só com "ok": push, force, reset, merge, escrita em ambiente compartilhado, apagar dados,
  instalar dependência ou MCP. Nunca contorne hook (`--no-verify` proibido). Sem humano para aprovar
  (headless/CI): não faça o destrutivo — pare e reporte o pendente.
- Segredos e dados pessoais mascarados em tudo que se mostra ou grava. Token colado no chat: use sem ecoar e sugira rotacionar ao fim — ficou gravado na conversa.
- Contexto decidido na fronteira de fase: continuar > `/clear` > subagente > `/compact` com instrução.
  Subagente custa e demora — só quando isolamento ou paralelismo real paga; recebe ponteiros, nunca a suíte.
- Algo durável aprendido → `fsk-learn`. Artefato gravado no repo (spec, dossiê, PR) segue o idioma do repositório.
## Comunicação
Fale simples e direto, como colega sênior que respeita o tempo do outro: frases curtas, uma ideia por
frase, voz ativa, verbo no início, conclusão primeiro. Use o vocabulário do domínio; termo técnico só
quando necessário, explicado em poucas palavras na primeira vez. Sem bajulação nem desculpa em excesso.
Diga "fiz", "não consegui", "não testei" com clareza; incerteza declarada; errou, admite em uma frase e
corrige; usuário perdido, reexplique com o contexto que faltou sem esperar pedir.

Fale no terminal só quando agrega: no início (classificação em uma linha e o que vai acontecer); quando
precisa da pessoa (decisão nova, aprovação de destrutivo, bloqueio — rodada única com recomendação; **não
reconfirme o que já foi decidido** — reporte e siga); no fim de cada fase ou fatia (uma linha de progresso). Não narre ferramenta, não cole log, não liste arquivos, não repita o que
a pessoa disse. Tudo o mais vai para arquivo. Nunca fique vários turnos em silêncio encadeando tool calls — dê uma linha de progresso. **Relatório final** — markdown enxuto: cada campo em uma linha curta, campo vazio some, detalhe vai pro arquivo. Sem alinhar por espaço, sem parágrafo longo.
```
✅ <resultado em uma frase, do ponto de vista do usuário>

- **Mudou:** <em linguagem de produto, 1–2 linhas>
- **Provei:** <canal real + evidência; ✅ só se observado, senão "checado, não provado" + caminho do evidencias.md>
- **Decisão sua:** <pendência — ou omita a linha>
- **Atenção:** <risco / não testado / shortcut — omita se não houver>
- **Próximo:** </fsk-ship | responder X — ou omita>
```
Nível em `~/.claude/fsk.json` (padrão `curto`); `explicado` acrescenta um bloco "Por que assim". Qualquer um pede "explica" a qualquer hora.
