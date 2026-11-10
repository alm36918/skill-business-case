# Modo revisão: avaliar um business case já pronto

Use quando receber um business case escrito, seu ou de outra pessoa, e o pedido for conferir, criticar ou decidir se aprova. Não reescreva o documento: entregue um parecer.

## Passos
1. **Extraia a conta.** Identifique investimento, benefícios, custos, horizonte e taxa de desconto. Se o documento traz só um número final, peça as entradas; sem elas, diga que o caso não pode ser conferido.
2. **Refaça as contas** com `scripts/calc_financeiro.py`, em pelo menos dois cenários: o do documento e um conservador (benefícios menores ou mais lentos). Compare com os números apresentados e aponte diferenças.
3. **Leia a grade de sensibilidade.** A partir de que queda nos benefícios, ou de que taxa, o VPL fica negativo? Caso que só se sustenta com o plano cumprido quase à risca é frágil, mesmo com VPL alto.
4. **Confira o que falta**, pela ordem de `references/checklist.md`. Os buracos mais comuns:
   - só um cenário, sem sensibilidade;
   - receita ou benefício em uma linha só, sem os drivers;
   - hora liberada contada como economia de caixa;
   - investimento sem capital de giro, treinamento ou migração;
   - "não fazer nada" ausente das alternativas;
   - número sem fonte;
   - taxa de desconto que não é a da empresa;
   - risco listado sem mitigação nem dono.
5. **Rode a banca de críticos** (`references/banca-de-criticos.md`) sobre o documento.

## O parecer
- **Veredito:** sustenta-se, sustenta-se com condições ou não se sustenta.
- **Contas refeitas**, lado a lado com as do documento.
- **Condições para o caso valer**, em linguagem direta: "exige que os benefícios cheguem a pelo menos X% do previsto e vale até uma taxa de Y%".
- **Até cinco pontos fracos**, do mais grave ao menos grave, cada um com o que resolveria.
- **Perguntas para o autor.**

Critique o caso, não o autor. Se faltar dado para concluir, diga qual dado e não complete com suposição.
