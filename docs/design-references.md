# Referências de design e arquitetura (consulta)

Material para **consultar** quando a decisão aparece — não é skill e não compete por gatilho. Os
princípios gerais (menor mudança, cirúrgico, organização por fronteira) já vivem no núcleo; o técnico de
cada stack vira rule do projeto (via `fsk-setup`/`fsk-learn`). Aqui ficam as fontes para aprofundar.

## Quando consultar
Decisão de arquitetura, escolha de padrão, trade-off de escalabilidade/resiliência, organização de
módulos, refactor estrutural.

## Princípios (ordem de prioridade)
1. A melhor mudança é a menor que resolve. YAGNI/KISS antes de qualquer abstração.
2. Resiliência ("degrade, don't die"): timeouts, retry com backoff, circuit breaker, bulkhead,
   load-shedding, graceful degradation.
3. Observabilidade como código: logging estruturado com correlation IDs, métricas RED/USE, tracing,
   SLOs — instrumentar ao escrever, não depois.
4. Organização por fronteira, não por tipo: agrupe por domínio/feature; camadas (Clean/Hexagonal/DDD) só
   quando o tamanho justifica.
5. Decisão registrada vai para a seção "Decisões" da spec e, se vale para o projeto, para a rule afetada
   (o kit não usa ADR numerado).

## Fontes curadas (consulte o original quando precisar de profundidade)
- Arquitetura: https://github.com/keez97/claude-architecture-skills
- Anti-overengineering: https://github.com/alvindemesadev/boring-engineering ·
  https://github.com/kayaman/skills/blob/main/yagni-principle/SKILL.md
- Clean-code multi-linguagem: https://github.com/unrealandychan/clean-code-skill ·
  https://github.com/JordanCoin/codingskills
- Resiliência/observabilidade: https://github.com/bjgreenberg/senior-engineering-partner
- Refactoring/debug: https://github.com/cskwork/improve-code-skill

## Boas práticas por stack
Quando o projeto é de uma linguagem/framework específico, o `/fsk-setup` sugere a referência de boas
práticas correspondente do `manifest.yaml` (ex.: React/Next → vercel-react-best-practices; Vue →
vue-best-practices). Novas referências por stack são adicionadas ao manifest conforme surgem.
