# Playbook — Planilhas (.xlsx .xlsm .csv .tsv)

Delega à skill oficial **xlsx** da Anthropic (Proprietary).

1. Garanta a skill instalada:
   `npx skills add https://github.com/anthropics/skills --skill xlsx`
2. Siga o SKILL.md oficial. Libs: `openpyxl`, `pandas`, `markitdown`.
3. Lembrete do oficial: ao gravar valores calculados, use `scripts/recalc.py` (LibreOffice) — `openpyxl`
   não grava valores em cache de fórmula.

Fonte: https://github.com/anthropics/skills/tree/main/skills/xlsx
