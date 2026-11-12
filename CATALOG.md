# CATALOG — o que o kit traz

Duas camadas: **comportamento** (as skills `fsk-*`, sempre do kit) e **ferramentas** (MCPs e skills
técnicas por stack, propostas pelo `/fsk-setup` conforme a stack). Fonte da verdade das ferramentas:
[install/manifest.yaml](./install/manifest.yaml). Créditos: [NOTICE.md](./NOTICE.md).

## 🧠 Comportamento — núcleo + 10 skills `fsk-*` (global, do kit)

| Item | Invocação | Papel |
|---|---|---|
| **núcleo** (`global/fsk-workflow.md`) | sempre | Pensar/mudar, navegação barata, travas, comunicação |
| **/fsk-setup** | slash (sugerida) | Prepara o repo no padrão, idempotente |
| **/fsk-plan** | slash + automática | Classifica e entrega o menor plano que fecha decisões |
| **/fsk-build** | slash + automática | Constrói em fatias verticais, provando cada uma |
| **/fsk-ship** | slash (sugerida) | Commit e PR no formato do repo, com evidência |
| **fsk-prove** | agente | Prova sem viés (navegador > API > integração > unitário) |
| **fsk-review** | agente | Fidelidade, regras, segurança, impacto, simplicidade; limpa o diff |
| **fsk-explore** | agente | Contexto de uma área → ponteiros, não conteúdo |
| **fsk-debug** | agente | Loop vermelho, causa raiz, correção mínima |
| **fsk-docs** | agente | Documentação, apresentações, tour guiado |
| **fsk-learn** | agente | Aprendizado → AGENTS.md, rules, how-to |

## 🧰 Ferramentas por stack (do `manifest.yaml`, instaladas com "ok")

Legenda: 🟢 barato (skill) · 🔴 caro (MCP) · 🌐 global · 📦 projeto


### 🔎 Code Intelligence
| Item | tipo | onde | fase | Papel |
|---|---|---|---|---|
| **CodeGraph (MCP)** | 🔴 | 🌐 | explore, build, review | entender fluxo/impacto/blast-radius que grep não segue (dispatch dinâmico) |
| **Context7 (MCP)** | 🔴 | 🌐 | explore, build, review | usar lib/framework cuja API pode ter mudado de versão |

### 🎨 Frontend / UI / UX
| Item | tipo | onde | fase | Papel |
|---|---|---|---|---|
| **Axe / Accessibility (MCP)** | 🔴 | 📦 | build, prove | checar conformidade WCAG com relatório |
| **Better Design (31 design systems)** | 🔴 | 📦 | build, prove | 'construa no estilo da Stripe/Linear/Apple' — tokens+componentes de marca |
| **Better Icons (ícones)** | 🟢 | 📦 | build, prove | buscar ícones existentes (200k, 150+ coleções) |
| **Figma (MCP)** | 🔴 | 📦 | build, prove | o time tem designs prontos no Figma |
| **frontend-design (Anthropic)** | 🟢 | 📦 | build, prove | direção estética — fugir da 'cara de IA' |
| **Material 3 (MCP)** | 🔴 | 📦 | build, prove | projeto Material 3 (componentes/tokens/a11y) |
| **shadcn MCP (opcional, sem-Bash)** | 🔴 | 📦 | build, prove | ambiente sem shell (chat puro) |
| **shadcn (skill oficial)** | 🟢 | 📦 | build, prove | usar/instalar componentes shadcn (evita reinventar) |
| **ui-ux-pro-max (criar)** | 🟢 | 📦 | build, prove | criar UI com estilo/paleta/tipografia/UX consistentes |
| **Vercel React/Next Best Practices** | 🟢 | 📦 | build, prove | otimizar perf React/Next (waterfalls, bundle, render) |
| **Vue Best Practices** | 🟢 | 📦 | build, prove | boas práticas/perf Vue |
| **web-design-guidelines (Vercel, revisar)** | 🟢 | 📦 | build, prove | auditar UI contra Web Interface Guidelines |

### 🔧 Backend / API
| Item | tipo | onde | fase | Papel |
|---|---|---|---|---|
| **MCP Builder (Anthropic)** | 🟢 | 📦 | build | construir um servidor MCP próprio |
| **OpenAPI Bridge (MCP)** | 🔴 | 📦 | build | interagir com API descrita por OpenAPI (1 tool/endpoint) |

### 🗄️ Dados (leitura)
| Item | tipo | onde | fase | Papel |
|---|---|---|---|---|
| **Nautilus (multi-DB read-only) [próprio]** | 🔴 | 📦 | explore, prove | inspecionar dados/esquema em LEITURA |

### 🗄️ Dados (migrations)
| Item | tipo | onde | fase | Papel |
|---|---|---|---|---|
| **Migrations (provider MCP ou skill-CLI)** | 🔴 | 📦 | build, ship | criar/aplicar migration/schema |

### 📨 Filas
| Item | tipo | onde | fase | Papel |
|---|---|---|---|---|
| **Argonaut (filas unificado) [próprio]** | 🔴 | 📦 | build, prove | inspecionar/diagnosticar filas e tópicos |

### ☁️ Infra / DevOps
| Item | tipo | onde | fase | Papel |
|---|---|---|---|---|
| **AWS (awslabs/mcp)** | 🔴 | 📦 | ship, setup | projeto em AWS |
| **Azure (microsoft/mcp)** | 🔴 | 📦 | ship, setup | projeto em Azure |
| **CI/CD (GitLab oficial / CircleCI)** | 🔴 | 📦 | ship, setup | ler logs de pipeline/rodar pipeline |
| **Docker MCP Gateway** | 🔴 | 📦 | ship, setup | orquestrar MCPs containerizados com isolamento + segredos via Docker Desktop |
| **Kubernetes (MCP)** | 🔴 | 📦 | ship, setup | inspecionar cluster (pods/logs) |
| **Terraform (HashiCorp)** | 🔴 | 📦 | ship, setup | navegar módulos/providers/docs do Registry; validar IaC |

### 🔐 Secrets
| Item | tipo | onde | fase | Papel |
|---|---|---|---|---|
| **Infisical (secrets)** | 🔴 | 📦 | setup, build | gerenciar segredos com telemetria zero |

### 📋 Tasks / Tickets
| Item | tipo | onde | fase | Papel |
|---|---|---|---|---|
| **Atlassian (Jira/Confluence)** | 🔴 | 📦 | plan, ship | enterprise com Jira; auditoria por tool-call |
| **Linear (task manager)** | 🔴 | 📦 | plan, ship | amarrar código a ticket Linear |

### 📈 Observabilidade
| Item | tipo | onde | fase | Papel |
|---|---|---|---|---|
| **AWS CloudWatch (logs/métricas)** | 🔴 | 📦 | prove, debug | logs/alarmes/root-cause em AWS |
| **Datadog (métricas/APM/logs)** | 🔴 | 📦 | prove, debug | time usa Datadog |
| **Grafana (observabilidade hub)** | 🔴 | 📦 | prove, debug | consultar dashboards/datasources (Prometheus+Loki+Tempo)/alertas |
| **Sentry (erros/APM)** | 🔴 | 📦 | prove, debug | time usa Sentry p/ erros/traces |

### ✅ QA / Testes
| Item | tipo | onde | fase | Papel |
|---|---|---|---|---|
| **Chrome DevTools (MCP)** | 🔴 | 📦 | prove | evidenciar bug de rede/performance/console detalhado |
| **Playwright (MCP)** | 🔴 | 📦 | prove | exploração interativa de app + evidências (screenshot/trace) |

### 🛡️ Segurança
| Item | tipo | onde | fase | Papel |
|---|---|---|---|---|
| **Semgrep (SAST)** | 🔴 | 📦 | review | SAST/SCA/secrets contínuo em tempo de edição |

### 📄 Documentos
| Item | tipo | onde | fase | Papel |
|---|---|---|---|---|
| **docgen (MCP)** | 🔴 | 📦 | docs, prove, plan | gerar/ler docx/pdf/pptx/xlsx, HTML->PDF/slides/imagem, templates com campos |
