# Arquitetura & boas práticas (referência)

Conteúdo curado para o agente **arquitetar, resiliência, escalabilidade e observabilidade** — lido como
referência pela disciplina (Karpathy+Ponytail) e pelo review. **Não é uma skill** que compete pelo
gatilho "architecture/bug/refactor" — é material que sharpeniza a decisão quando ela aparece.

## Quando consultar
Decisão de arquitetura, escolha de padrão, trade-off de escalabilidade/resiliência, ADR, organização
de arquivos/módulos, refactor estrutural.

## Princípios (ordem de prioridade)
1. **A melhor mudança é a menor que resolve.** YAGNI/KISS antes de qualquer abstração (dono: Karpathy+Ponytail).
2. **Decisão registrada = ADR.** Contexto → alternativas consideradas → consequência. Numerado em `docs/adr/`.
3. **Resiliência ("degrade, don't die").** Timeouts, retry com backoff, circuit breaker, bulkhead,
   load-shedding, graceful degradation.
4. **Observabilidade como código.** Structured logging com correlation IDs, métricas RED/USE, tracing
   distribuído, SLOs — instrumentar ao escrever, não depois.
5. **Organização por fronteira, não por tipo.** Agrupe por domínio/feature; camadas (Clean/Hexagonal/DDD)
   só quando o tamanho justifica — não por reflexo.

## Fontes curadas (consultar o original quando precisar de profundidade)
- Arquitetura/ADR: https://github.com/keez97/claude-architecture-skills
- Anti-overengineering (decisão): https://github.com/alvindemesadev/boring-engineering ·
  https://github.com/kayaman/skills/blob/main/yagni-principle/SKILL.md
- Clean-code multi-linguagem (TS/Py/Go/Java): https://github.com/unrealandychan/clean-code-skill ·
  https://github.com/JordanCoin/codingskills
- Resiliência/observabilidade: https://github.com/bjgreenberg/senior-engineering-partner
- Refactoring/debug: https://github.com/cskwork/improve-code-skill

## Stack-specific (a `fullstack-setup` detecta e sugere)
Quando o projeto é de uma linguagem/framework específico, a setup sugere a referência de boas práticas
correspondente (ex: React/Next → vercel-react-best-practices; Vue → vue-best-practices; e assim por
diante por linguagem e por banco). Novas referências por stack são adicionadas aqui pela
`project-learning` conforme surgem.
