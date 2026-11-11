# CATALOG — tudo que o kit curou, por área

Legenda: **tipo** skill·mcp·cli·ref · **custo** 🟢baixo(lazy) 🔴alto(MCP) · **onde** 🌐global ·📦projeto ·
**carga** sempre·on-demand. Fonte da verdade: [install/manifest.yaml](./install/manifest.yaml).

> A plataforma global instala só o 🌐. Os 📦 são ligados pela `fullstack-setup` conforme a stack.

## 🧠 Disciplina & Fluxo (barato, a base)
| Item | tipo | onde | Papel |
|---|---|---|---|
| **Karpathy+Ponytail** | skill 🟢 | 🌐 sempre | Pensar antes de codar, mudança cirúrgica, anti-overengineering. Dono do YAGNI/KISS. |
| **using-mcps-well** (nossa) | skill 🟢 | 🌐 sempre | Quando/como usar MCP sem desperdiçar contexto. |
| **Matt Pocock — cadeia greenfield** | skill 🟢 | 🌐 on-demand | **Orquestra desenvolvimento novo**: `to-spec → implement → tdd → code-review → pr`. |
| **diagnosing-bugs** (mattpocock) | skill 🟢 | 🌐 on-demand | Hipótese → reprodução → causa raiz. |

> `spec-kit` e `gsd-core` **descartados** (pesados/redundantes) — a cadeia do Matt Pocock cobre a orquestração de forma leve.

## 🔎 Code Intelligence (os 2 MCPs genéricos globais)
| Item | tipo | onde | Papel |
|---|---|---|---|
| **CodeGraph** | mcp 🔴 | 🌐 | Mapa do seu código (fluxo/impacto/blast-radius). |
| **Context7** | mcp 🔴 | 🌐 | Docs das libs ao vivo (anti-alucinação de API). |

## 🔀 Version Control
| Item | tipo | onde | Papel |
|---|---|---|---|
| **conventional-commit + git-commit** | cli 🟢 | 🌐 on-demand | Commit/PR via `gh` (sem MCP). |
| **GitHub MCP** | mcp 🔴 | 📦 on-demand | **Só** Actions/code-scanning/Projects. |

## 🎨 Frontend / UI / UX
| Item | tipo | onde | Papel |
|---|---|---|---|
| **ui-ux-pro-max** | skill 🟢 | 📦 | **Criar** UI (estilos, paletas, fontes, UX). |
| **web-design-guidelines** (Vercel) | skill 🟢 | 📦 | **Revisar** UI → achados arquivo:linha. |
| **frontend-design** (Anthropic) | skill 🟢 | 📦 | Camada anti-"cara de IA" (opcional). |
| **shadcn** (skill oficial) | skill 🟢 | 📦 | Componentes shadcn sem reinventar. |
| **better-design** | mcp 🔴 | 📦 | "No estilo da Stripe/Linear/Apple" — 31 design systems. |
| **Material 3** | mcp 🔴 | 📦 | Projetos Material (componentes/tokens/a11y). |
| **better-icons** | skill 🟢 | 📦 | 200k ícones, busca em lote (fixar 1 lib no AGENTS.md). |
| **Figma MCP** | mcp 🔴 | 📦 | Quando há designs prontos no Figma. |
| **Axe (a11y)** | mcp 🔴 | 📦 | Conformidade WCAG. |
| **vercel-react** / **vue-best-practices** | skill 🟢 | 📦 | Boas práticas por framework (stack-specific). |

## 🔧 Backend / API
| Item | tipo | onde | Papel |
|---|---|---|---|
| **OpenAPI Bridge** | mcp 🔴 | 📦 | 1 tool por endpoint da spec. |
| **mcp-builder** (Anthropic) | skill 🟢 | 📦 | Construir MCP próprio. |

## 🗄️ Dados & Filas
| Item | tipo | onde | Papel |
|---|---|---|---|
| **Nautilus** (próprio) | mcp 🔴 | 📦 | Leitura multi-DB (8 bancos), read-only. |
| **Migrations** (Neon/Supabase/CLI) | mcp 🔴 | 📦 | Escrita/schema — nunca aplica sem "ok". |
| **Argonaut** (próprio) | mcp 🔴 | 📦 | Filas unificadas (Kafka/RabbitMQ/SQS/SNS/Redis). |

## ☁️ Infra / DevOps / Secrets
| Item | tipo | onde | Papel |
|---|---|---|---|
| **AWS** (awslabs/mcp) | mcp 🔴 | 📦 | Projetos AWS. |
| **Azure** (microsoft/mcp) | mcp 🔴 | 📦 | Projetos Azure. |
| **Docker MCP Gateway** | mcp 🔴 | 📦 | Orquestrar MCPs com isolamento. |
| **Terraform** (HashiCorp) | mcp 🔴 | 📦 | IaC: módulos/providers/validação. |
| **Kubernetes** | mcp 🔴 | 📦 | Inspeção de cluster. |
| **CI** (GitLab/CircleCI) | mcp 🔴 | 📦 | Logs/execução de pipeline. |
| **Infisical** (secrets) | mcp 🔴 | 📦 | Secrets com telemetria zero. |

## 📋 Tasks & Observabilidade
| Item | tipo | onde | Papel |
|---|---|---|---|
| **Linear** | mcp 🔴 | 📦 | Tickets (endpoint read-only). |
| **Atlassian** (Jira) | mcp 🔴 | 📦 | Enterprise + auditoria. |
| **Grafana** | mcp 🔴 | 📦 | Hub observabilidade (Prometheus+Loki+Tempo). |
| **Sentry / Datadog / CloudWatch** | mcp 🔴 | 📦 | Por vendor do time. |

## ✅ QA / Testes
| Item | tipo | onde | Papel |
|---|---|---|---|
| **surgical-testing** (nossa) | skill 🟢 | 🌐 on-demand | **Decide o nível do teste**: e2e > integração > unitário (último recurso). Testa invariante de arquitetura, contrato e caminho de dinheiro/permissão. |
| **e2e-browser-qa** | skill 🟢 | 📦 | Orquestra QA: plano por risco, evidências, relatório, converte p/ Playwright/Cypress. |
| **Playwright MCP** | mcp 🔴 | 📦 | Driver de browser + evidência (ad-hoc). |
| **Chrome DevTools MCP** | mcp 🔴 | 📦 | Performance/rede/console detalhado. |
| **webapp-testing** (Anthropic) | skill 🟢 | 📦 | Scripts Playwright reproduzíveis p/ CI. |

## 🔐 Segurança
| Item | tipo | onde | Papel |
|---|---|---|---|
| **/security-review** (nativo) | skill 🟢 | 🌐 on-demand | Revisão rápida do diff. |
| **cloudflare-security-audit** | skill 🟢 | 🌐 on-demand | Auditoria adversarial profunda. |
| **Semgrep** | mcp 🔴 | 📦 | SAST/SCA/secrets contínuo. |

## 📄 Documentos & Produtividade
| Item | tipo | onde | Papel |
|---|---|---|---|
| **documents** (nossa, router) | skill 🟢 | 🌐 on-demand | Roteia p/ xlsx/pptx/pdf/docx (progressive disclosure). |
| **i-have-adhd** | output-style 🟢 | 🌐 on-demand | Respostas action-first, sem preâmbulo. |

## 🏛️ Referência (rules/ — conteúdo, não skill)
| Item | Papel |
|---|---|
| **Arquitetura & ADR** | Resiliência, escalabilidade, ADR, clean-code multi-linguagem, resiliência/observabilidade, refactoring. Lido pela disciplina e pelo review. |

## 🛠️ Skills originais do kit (o motor "anabolizante")
| Item | Papel |
|---|---|
| **fullstack-setup** | Detecta stack + grill → instala núcleo + opcionais que casam + **bootstrap da PKB**. |
| **project-onboarding** | Brownfield → minera código+git+PRs → gera a **PKB** (AGENTS.md + rules + pattern skills). |
| **project-learning** | Enriquece a **PKB** continuamente; PROPÕE (com "ok") rule / pattern skill / AGENTS.md. |
| **using-mcps-well** | Governa o uso eficiente dos MCPs. |
| **surgical-testing** | Governa **onde** testar: e2e/integração primeiro, unitário só em último caso. |
| **documents** | Router de documentos (xlsx/pptx/pdf/docx). |

> **PKB — Base de Conhecimento Pré-Destilada** ([docs/knowledge-base.md](./docs/knowledge-base.md)): o maior
> multiplicador. Destila o padrão do projeto **uma vez** (formato de PR, "how to create DTO", convenções)
> para o agente parar de redescobrir e gastar tokens a cada sessão. Complementa o CodeGraph.
