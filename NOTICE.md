# NOTICE — créditos

As skills `fsk-*` foram **escritas do zero** para este fluxo. Ideias aproveitadas de terceiros recebem
crédito aqui. Nenhuma skill de processo de terceiros é instalada ou redistribuída.

| Fonte | Licença | Ideias aproveitadas | Onde |
|---|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | MIT | grilling (entrevista por decisões), domain-modeling (vocabulário), wayfinder, to-tickets (fatias verticais), implement/implement-spec (grafo de tarefas, branch de integração), tdd (teste por comportamento público), diagnosing-bugs (loop vermelho, hipóteses falsificáveis), code-review (eixos sem ranking cruzado), pr (menor visualização, porta de mão única/dupla), retro, writing-for-agents, handoff, wizard, ask-matt (fronteiras de fase) | fsk-plan, fsk-build, fsk-prove, fsk-debug, fsk-review, fsk-ship, fsk-learn, núcleo |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | MIT | escada da menor mudança, completo no alcance, nunca cortar segurança, `shortcut:`, ordem de revisão, declarar carga assumida, ledger de atalhos | núcleo, fsk-build, fsk-review, fsk-learn |
| [AbdullahHameedKhan/karpathy-ponytail-skills](https://github.com/AbdullahHameedKhan/karpathy-ponytail-skills) | — | suposições ditas, mudança cirúrgica, objetivo verificável antes de agir | núcleo, fsk-build |
| [KauaLealz/docgen-mcp-server](https://github.com/KauaLealz/docgen-mcp-server) | — | tools de leitura/escrita de docx/pdf/pptx/xlsx, HTML→PDF/slides/imagem, templates com campos | fsk-docs |
| e2e-browser-qa (autor) | — | risco = impacto × probabilidade, observar console/rede/estado, separar falha do produto da falha do teste, confiança declarada, veredito primeiro, cobertura explícita, segurança em produção | fsk-prove |

Ferramentas de terceiros listadas no `install/manifest.yaml` (MCPs, skills técnicas) mantêm suas próprias
licenças e são instaladas a partir das fontes originais, nunca copiadas para este repositório.
