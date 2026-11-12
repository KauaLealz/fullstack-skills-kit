---
name: fsk-docs
description: Gera documentação, apresentações e o tour guiado da mudança no padrão do projeto — relatório de evidências, dossiê de revisão, feature, API, runbook, notas de release, apresentação, relatório executivo. Markdown é escrito direto; formatos binários via docgen MCP quando o projeto o tem, senão pelas skills oficiais de documento (docgen é opcional). Dispara em "documenta", "gera doc/apresentação/relatório", "me guia pela mudança", "tour". Não use para provar (fsk-prove) nem para abrir PR (fsk-ship). Idioma dos artefatos segue o do repo.
user-invocable: false
effort: medium
---

# fsk-docs — documentação, apresentações e tour

Templates de formato (não técnica) em `references/`: `evidencias`, `revisao`, `feature`, `api`,
`runbook`, `release`, `apresentacao`, `executivo`. Como gerar cada formato (com ou sem docgen):
`references/formatos.md`.

## Gatilhos
1. **Automático no fechamento da prova** (S2+/alta, ou se a rule do projeto mandar): relatório de
   evidências → `.claude/specs/<slug>/evidencias.md`, usado pelo ship no PR.
2. **No início do ship:** o dossiê de revisão → `.claude/specs/<slug>/revisao.md` (template `revisao`).
3. **Tour guiado** ("me guia pela mudança", "tour", "explica o que mudou"): percorre a mudança na ordem
   do dossiê, uma intenção por vez, com pausa para perguntas.
4. **A pedido:** comportamento, feature, fluxo, API, arquitetura, onboarding, runbook, notas de release,
   guia de uso, relatório executivo, apresentação.

## Comportamento
- **Padrão do projeto primeiro.** Procure `rules/docs.md`, templates em `.claude/docs-templates/` e docs
  existentes (leia `.docx`/`.pdf`/`.pptx` com `read_doc` do docgen para copiar estrutura e tom). Sem
  padrão, use o template do kit e, ao final, proponha ao `fsk-learn` gravar o escolhido.
- **Público antes de forma.** Quem lê (dev, QA, PO, cliente, diretoria) decide profundidade, vocabulário
  e formato. Pergunte só se não der para inferir.
- **Fontes primárias, não redescoberta.** Monte a partir da spec, da tabela de prova, do diff, do
  `git log` e do código já lido na sessão. Explore só o que falta.
- **Formato pelo destino:** Markdown no repo por padrão (sempre direto, sem MCP). Binário só quando o
  destino pede — `.docx`/`.pdf`/`.pptx`/`.xlsx`/imagem — pelo caminho de `references/formatos.md`: docgen
  quando o projeto o tem (um passo, templates com `mergeFields`), senão as skills oficiais de documento.
  O conteúdo é o mesmo nos dois caminhos; a escolha é só de ferramenta.
- **Conciso e verificável:** conclusão primeiro, cada afirmação ligada a uma evidência ou trecho de
  código, diagrama só se reduz texto (Mermaid no Markdown).
- **Atualize em vez de duplicar:** doc do assunto já existe, edite; código mudou e o doc envelheceu,
  aponte o drift. Linguagem do núcleo (simples e direta) em toda saída.

## Tour guiado
Funciona para quem fez e para quem revisa em outra máquina (basta a branch e o `revisao.md`). Segue a
ordem de leitura do dossiê, uma intenção por vez: o que mudou, por quê, trecho curto do diff e o que
conferir. Pausa ao fim de cada parada para perguntas. Mecânico vira uma linha ("12 arquivos de rename,
pode pular") e só abre se pedirem. Pergunta que revela lacuna no dossiê vira sugestão para o `fsk-learn`.

## Pronto quando
Gera `evidencias.md` e `revisao.md`, um `.docx` e um `.pptx` via docgen, e o tour percorre uma mudança
real respeitando o nível de explicação da pessoa.
