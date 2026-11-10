# Exemplo resolvido (dados fictícios)

Caso: trocar o sistema de atendimento. Serve para mostrar o raciocínio; os números são inventados.

## Resumo
**Recomendação:** seguir com condições. **Decisão solicitada:** aprovar um piloto de 60 dias e a renegociação do contrato do terceirizado.
O caso se paga no cenário base, mas não no conservador. Tudo depende de a redução do terceirizado virar economia de caixa.

## Pedido, patrocinador e o que já existe
- Pedido: R$ 180 mil para implantar e R$ 48 mil por ano de operação.
- Patrocinador: a diretora de operações, que responde pelo orçamento da área.
- Objetivo da empresa: reduzir o custo de atendimento por chamado.
- Escopo: entram a fila única e as respostas prontas; ficam de fora o atendimento por telefone e a troca do cadastro de clientes; a definir, a integração com o sistema de cobrança.
- O que já existe: conferido com a área de tecnologia. O sistema atual não tem fila única e não há outra ferramenta contratada que faça isso.

## Custo de não fazer nada
- Gasto direto: o contrato do sistema atual custa R$ 60 mil por ano (fonte: contrato).
- Gasto direto: R$ 180 mil por ano com atendimento terceirizado para dar conta da fila (fonte: notas fiscais dos últimos 12 meses).
- Capacidade: 4 atendentes × 6 h/semana × R$ 40/h × 48 semanas = R$ 46.080 por ano em retrabalho (estimativa do coordenador; faixa de 3 a 6 h).

## Cadeia de drivers
Investimento de R$ 180 mil + R$ 48 mil por ano de operação
→ entrega: fila única e respostas prontas
→ benefício de **caixa**: fim do contrato antigo (R$ 60 mil/ano, fato) + redução do terceirizado (R$ 90 mil/ano no cenário base, **premissa**)
→ benefício de **capacidade**: R$ 46.080/ano em horas liberadas. Não entra no payback, porque ninguém será desligado.

## Análise financeira (saída do script, 3 anos, 12% ao ano)
| Indicador | Conservador | Base | Otimista |
|---|---|---|---|
| ROI | -3% | 39% | 67% |
| Payback simples | não atinge no horizonte | 1,76 anos | 1,36 anos |
| VPL | R$ -43.096 | R$ 64.987 | R$ 137.042 |
| TIR | -3% | 32% | 53% |
| Benefícios mínimos para empatar | 117% | 82% | 68% |
| Capacidade liberada (à parte) | R$ 69.120 | R$ 138.240 | R$ 138.240 |

### Grade de sensibilidade do VPL, cenário base
Linhas: variação dos benefícios de caixa. Colunas: taxa de desconto.

| Benefícios | 10% | 11% | 12% | 13% | 14% |
|---|---|---|---|---|---|
| -20% | R$ -947 | R$ -4.053 | R$ -7.068 | R$ -9.997 | R$ -12.842 |
| -10% | R$ 36.356 | R$ 32.603 | R$ 28.959 | R$ 25.420 | R$ 21.982 |
| plano | R$ 73.659 | R$ 69.259 | R$ 64.987 | R$ 60.838 | R$ 56.806 |
| +10% | R$ 110.962 | R$ 105.915 | R$ 101.014 | R$ 96.255 | R$ 91.631 |
| +20% | R$ 148.264 | R$ 142.570 | R$ 137.042 | R$ 131.672 | R$ 126.455 |

Com 10% a menos de benefícios, o caso ainda se paga em qualquer taxa da grade. Com 20% a menos, o VPL fica negativo em todas.

## O que vira o resultado
A redução do terceirizado. No cenário base, os benefícios de caixa precisam chegar a 82% do estimado, ou seja, R$ 122.940 por ano. Como R$ 60.000 são certos, o terceirizado precisa cair pelo menos R$ 62.940 por ano. No conservador (queda de R$ 45 mil), o caso não se paga.

## Objeção da banca que ficou em aberto
Finanças: "o contrato do terceirizado tem volume mínimo; a redução pode não virar caixa no primeiro ano." Evidência que resolve: a cláusula de volume mínimo do contrato.

## Recomendação
**Seguir com condições:** aprovar um piloto de 60 dias em uma fila e renegociar o volume mínimo do terceirizado antes de assinar a implantação completa. Sem a renegociação, adiar.

## Nota de prontidão
| Dimensão | Nível | Motivo |
|---|---|---|
| Clareza do problema | Forte | O custo de não fazer nada tem número e fonte |
| Viabilidade | Média | O cenário conservador não se paga; depende da renegociação do terceirizado |
| Apoio | Forte | Há patrocinadora com autoridade sobre o orçamento |
| Alinhamento estratégico | Forte | Serve a um objetivo declarado e não duplica ferramenta existente |

Repare no que o exemplo faz: abre pelo custo de não fazer nada, separa caixa de capacidade, admite que o cenário conservador não fecha e nomeia a premissa que decide o caso.
