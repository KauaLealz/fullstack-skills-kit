# Playbook — PDF (.pdf)

Delega à skill oficial **pdf** da Anthropic (Proprietary).

1. Garanta a skill instalada:
   `npx skills add https://github.com/anthropics/skills --skill pdf`
2. Siga o SKILL.md oficial. Libs: `pypdf`, `pdfplumber`, `reportlab`.
3. O oficial usa progressive disclosure: carrega `reference.md` / `forms.md` só quando o caso exige
   (extração de tabelas, preenchimento de formulário, OCR). Deixe a skill oficial puxar esses arquivos.

Fonte: https://github.com/anthropics/skills/tree/main/skills/pdf
