# Exemplo resolvido (dados fictícios)

Caso: trocar o sistema de atendimento. Serve para mostrar o raciocínio; os números são inventados.

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

## O que vira o resultado
A redução do terceirizado. No cenário base, os benefícios de caixa precisam chegar a 82% do estimado, ou seja, R$ 122.940 por ano. Como R$ 60.000 são certos, o terceirizado precisa cair pelo menos R$ 62.940 por ano. No conservador (queda de R$ 45 mil), o caso não se paga.

## Objeção da banca que ficou em aberto
Finanças: "o contrato do terceirizado tem volume mínimo; a redução pode não virar caixa no primeiro ano." Evidência que resolve: a cláusula de volume mínimo do contrato.

## Recomendação
**Seguir com condições:** aprovar um piloto de 60 dias em uma fila e renegociar o volume mínimo do terceirizado antes de assinar a implantação completa. Sem a renegociação, adiar.

Repare no que o exemplo faz: abre pelo custo de não fazer nada, separa caixa de capacidade, admite que o cenário conservador não fecha e nomeia a premissa que decide o caso.
