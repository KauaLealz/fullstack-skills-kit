# Como gerar cada formato (docgen opcional, fallback consistente)

**Markdown** é sempre escrito direto, sem ferramenta. Para formato **binário**, há dois caminhos — o
conteúdo e a estrutura (vindos do template do tipo) são os mesmos; muda só a ferramenta.

## 1. Com docgen MCP (atalho, quando o projeto o tem)
O `/fsk-setup` propõe o docgen quando há trabalho de documento. Presente, use-o — resolve em um passo e
suporta papel timbrado:
- `.docx`/`.pdf`: `write_doc` (com `templatePath` + `mergeFields` quando a empresa tem modelo)
- `.pptx`: `render_slide` · `.xlsx`: `write_sheet` · imagem/PDF de HTML: `render_image`
- ler modelo existente para copiar tom/estrutura: `read_doc`

## 2. Sem docgen (fallback padrão, sempre disponível)
Use as **skills oficiais de documento** (docx, pptx, xlsx, pdf). Não reimplemente nem copie o conteúdo
delas — instale a do tipo e siga o SKILL.md oficial. Caminho por tipo:

| Tipo | Skill oficial | Libs que ela usa |
|---|---|---|
| Planilha `.xlsx/.csv` | `xlsx` | `openpyxl`, `pandas` (valor calculado: recalc via LibreOffice) |
| Word `.docx` | `docx` | `docx-js` (criar), `pandoc` (ler); tracked changes e comments |
| Apresentação `.pptx` | `pptx` | template + `python-pptx` |
| PDF | `pdf` | geração/leitura conforme o SKILL oficial |

Instalar sob demanda: `npx skills add https://github.com/anthropics/skills --skill <tipo>`.

## Regra de consistência
Monte primeiro o conteúdo em Markdown a partir das fontes primárias (spec, tabela de prova, diff,
`git log`) usando o template do tipo em `references/`. Só então renderize para o binário pelo caminho
disponível. Assim o mesmo documento sai idêntico com docgen ou sem — o docgen só economiza passos.
