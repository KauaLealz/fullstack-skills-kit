# Exemplo de spec preenchida (referência de qualidade)

Caso: e-commerce. Pedido original do usuário: *"quero cupom de desconto que só vale para uma categoria"*.
Repare: a entrevista descobriu 3 decisões que o pedido não dizia; o plano dá arquivo e abordagem por
fatia; a Varredura registra o que foi descartado e por quê.

```markdown
# Cupom por categoria
**Classificação:** feature · médio · risco **alto** (mexe em dinheiro/total do pedido)
**Worktree:** sim: .worktrees/cupom-categoria

## Combinado (ecoado e confirmado em 14/11)
Cupom ganha um campo opcional "categoria"; com categoria, o desconto aplica só sobre a soma dos itens
daquela categoria (não sobre o frete, não sobre o total). Cupom sem categoria segue como hoje. Carrinho
misto mostra no resumo "desconto aplicado a N itens". Admin escolhe a categoria num select no form de
cupom existente.

## Critérios de aceite
- [ ] C1 Cupom com categoria desconta só os itens dela — esperado: subtotal da categoria × % · canal:
      navegador (checkout) · durável: sim (dinheiro)
- [ ] C2 Cupom sem categoria mantém o comportamento atual — canal: navegador · durável: sim (regressão)
- [ ] C3 Carrinho sem item da categoria: cupom aceito porém desconto R$0 + aviso "nenhum item elegível"
      — canal: navegador (caminho infeliz) · durável: sim
- [ ] C4 Frete nunca entra na base do desconto — canal: API (total detalhado) · durável: sim (dinheiro)
- [ ] C5 Admin cria/edita cupom com categoria — canal: navegador (admin) · durável: não (CRUD simples)

## Plano de ataque
| Fatia | Arquivo(s) : onde | Abordagem (como) | Porquê | Referência a copiar |
|---|---|---|---|---|
| 1 Campo+migração | `db/migrations/`, `models/coupon.ts:12` | coluna nullable `category_id` FK | opcional = sem quebrar cupom existente | migração `20xx_add_free_shipping.ts` |
| 2 Cálculo | `services/discount.ts:40-88` (`applyCoupon`) | filtrar itens pela categoria antes da base | o cálculo mora num ponto só | função `applyFreeShipping` no mesmo arquivo |
| 3 Resumo no front | `components/CartSummary.tsx:55` | linha "desconto (N itens)" | transparência pro cliente | linha de frete grátis existente |
| 4 Admin | `admin/CouponForm.tsx:30` | select de categoria (fonte: `useCategories`) | reuso do hook existente | campo "validade" do mesmo form |

- **Quem chama / o que quebra:** `applyCoupon` ← `checkout.service.ts:102` e `order-preview.ts:33`
  (os DOIS recalculam total — mudar a assinatura quebra o preview)
- **Contratos:** resposta de `POST /checkout/preview` ganha `discount_items_count` (aditivo, não quebra)
- **Dados:** cupons existentes ficam `category_id = null` · reversão: dropar a coluna
- **Modos de falha prováveis (Review Focus):** (1) desconto aplicado sobre o total em vez do subtotal da
  categoria; (2) cupom antigo (null) cair no caminho novo; (3) arredondamento por item × por subtotal

## Decisões
- Desconto sobre subtotal da categoria, nunca sobre frete — porquê: política comercial dita pelo usuário
- Carrinho sem item elegível ACEITA o cupom com R$0 + aviso — porquê: UX de recusar confunde mais
  (decisão do usuário na rodada 2) · vira rule? não (específica desta feature)
- 1 categoria por cupom (não lista) — porquê: YAGNI; o uso real pedido é 1; evoluir se pedirem

## Varredura (dimensões descartadas, com motivo)
- Permissões — sem impacto: só admin já acessa o form de cupom (guard existente `admin.guard.ts`)
- Escala — sem impacto: cálculo é por carrinho (≤ dezenas de itens), nada em lote
- Rollout — sem flag: comportamento novo só ativa quando um cupom novo tem categoria
- i18n — descartado com ressalva: aviso "nenhum item elegível" entra no arquivo de mensagens existente
```

## O que faz esta spec ser boa
Pedido de 1 linha virou 3 decisões reveladas (frete, carrinho vazio, 1×N categorias) — nenhuma inventada,
todas perguntadas com recomendação. Cada critério tem canal e veredito de durabilidade. Cada fatia tem
arquivo:linha e referência a copiar — o build não redescobre nada. Os modos de falha dizem ao review e ao
prove onde concentrar. A Varredura prova que as dimensões foram pensadas, não esquecidas.
