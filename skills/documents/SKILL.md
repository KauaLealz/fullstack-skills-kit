---
name: documents
description: Criar, editar ou ler arquivos de documento — planilhas (.xlsx .xlsm .csv), apresentações (.pptx .potx), PDFs (.pdf) e documentos Word (.docx .dotx). Roteia para o playbook do tipo pedido e instala a skill oficial correspondente sob demanda.
---

# Documents (router)

Porta de entrada única para documentos, **sem carregar os 4 playbooks de uma vez**. Detecta o tipo e
lê **só** o playbook daquele tipo (progressive disclosure).

## Como rotear
1. Identifique a extensão / o tipo pedido.
2. Leia **apenas** o arquivo de referência correspondente — **nunca** os outros:

| Tipo | Extensões | Leia |
|---|---|---|
| Planilha | .xlsx .xlsm .csv .tsv | `references/xlsx.md` |
| Apresentação | .pptx .potx | `references/pptx.md` |
| PDF | .pdf | `references/pdf.md` |
| Word | .docx .dotx | `references/docx.md` |

3. Siga o playbook: ele instala a **skill oficial** daquele tipo (Anthropic) e delega a ela.

## Importante (licença)
As skills de documento da Anthropic são **Proprietary**. Esta skill **instala/aponta** para a oficial do
tipo — não reimplementa nem copia o conteúdo delas. O papel aqui é só **rotear** e preservar o lazy-load.
