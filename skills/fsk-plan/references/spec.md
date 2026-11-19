# Template — `.claude/specs/<slug>/spec.md`

**A spec é o maior investimento de tokens do fluxo.** O plan pensa; os demais executam. Ela é organizada
**por consumidor**: cada agente abre a sua seção e encontra TUDO que precisa — builder não redescobre, QA
não deduz, revisor não adivinha, ship não pergunta. S1 usa só Essência+Builder+QA em meia tela; S2+/alta
usa tudo. Pasta da demanda: `spec.md` · `exploracao.md` · `notas.md` · `evidencias.md` · `revisao.md`.
Time com pasta própria de specs/RFC: use o formato dele e acrescente o que faltar.

```markdown
# <Título>
**Classificação:** <tipo> · <tamanho> · criticidade <alta|média|baixa> · **Worktree:** <sim: caminho | não>

## Essência
**Combinado (confirmado em <data>):** <o entendimento ecoado e aprovado, em linguagem simples>
**Critérios de aceite** (observáveis de fora; infeliz incluído em média/alta):
- [ ] C1 <comportamento> — esperado: <do negócio> · canal: <navegador|API|estado> · durável: <sim|não>

## Para o builder (fsk-build executa, não pensa)
| Fatia | Arquivo(s) : onde | Abordagem (como) | Porquê | Referência a copiar | Estado |
|---|---|---|---|---|---|
| 1 | `src/…:linhas` | <como> | <porquê> | `exemplo:linhas` | pendente |
- **Ordem/dependências:** <1→2; 3 paralela> · **Interfaces** (quando definidas): <assinaturas>
- **Não tocar:** <o que parece relacionado mas está fora> · **Como subir/rodar:** <ponteiro AGENTS.md §Comandos>
- **Inventário do codemod** (só tipo massa): alvo, `grep` → N arquivos/M ocorrências, exclusões, risco AST×regex, amostra

## Para o QA (fsk-prove segue o roteiro)
- **Setup da prova:** <seed, usuário de teste, dados, como chegar na tela/endpoint>
- **Roteiro por critério:** C1 → <passos exatos> → <o que observar: tela, rede, estado persistido>
- **Negativos obrigatórios** (auth/permissão/tenant/entrada): <quais>
- **Modos de falha prováveis:** <os 2–3 jeitos mais prováveis DESTA mudança quebrar — prove e review concentram aqui>

## Para o revisor (fsk-review compara declarado × encontrado)
- **Mudanças de comportamento esperadas:** | Antes | Depois | Critério que autoriza | — tudo fora desta tabela é não-autorizado
- **Onde olhar:** <pontos de risco/julgamento> · **Quem chama / o que quebra:** `arquivo:linhas`
- **Contratos:** <API/evento/schema — e se é aditivo ou quebra>

## Para a entrega (fsk-ship executa o rito)
- **Dados:** <migration? ordem de deploy? reversão?> · **Flag/rollout:** <se houver>
- **Pronto quando:** <a definição de pronto DESTA demanda> · **Card:** <link do tracker>

## Decisões
- <decisão> — <porquê> · <vira rule? qual>

## Varredura (dimensões descartadas, com motivo)
- <dimensão> — sem impacto porque <motivo>   ← o que não está aqui nem em Decisões não foi pensado

## Changelog (toda mudança pós-"ok")
- <data> <o que mudou> — <motivo> · aprovado: <"ok" do usuário | ajuste sem impacto, registrado>
```

## Política de mudança (por fase)
| Fase | Pode mudar a spec? |
|---|---|
| **Plan (antes do "ok")** | Livre — é o trabalho |
| **Build** | Esclarecimento/detalhe aditivo: edita + linha no Changelog. Abordagem diferente com o mesmo comportamento: `notas.md`, spec intacta. **Critério/escopo/comportamento: PARA → re-plan da parte afetada → Changelog + novo "ok"** |
| **Prove/Review** | **Nunca edite a spec para o código passar** — divergência se resolve mudando o código, ou voltando ao plan com "ok". Spec que se dobra ao código não prova nada |
| **Ship** | Congelada. Mudança aqui é demanda nova |

**Nova spec em vez de editar** quando: a demanda muda de identidade ("aproveita e faz X" = outra demanda,
outra pasta); a spec já foi entregue (mudança pós-merge é sempre demanda nova); ou o Combinado inteiro
caducou (re-plan do zero custa menos que remendar).

## Regras de preenchimento
Critério observável de fora, esperado do negócio (nunca recalculado da implementação). Decisão sem porquê
não é decisão. Fatia é vertical (atravessa camadas, prova sozinha). Preencha as seções com conteúdo, não
com "ver acima" — cada consumidor lê a SUA seção sem caçar nas outras (repetir ali é investimento, não
redundância). Exemplo completo de qualidade: `exemplo-spec.md`.
