# Skill de business case

Uma skill para agentes de IA que monta um **business case** e o põe à prova antes de você levar a quem decide.

Business case é o documento que justifica um projeto, investimento ou iniciativa dentro de uma empresa: comprar um sistema, abrir uma filial, contratar uma equipe, mudar um processo. A skill conduz o agente por um roteiro, faz as contas com um script e simula uma banca de críticos para achar os pontos fracos antes da reunião.

> **Estado: versão 0.2.0.** As contas do script têm testes automáticos. O roteiro foi testado só com dados de exemplo e ainda não foi validado em business cases reais. Relatos de uso são muito bem-vindos.

## Para quem é
Para quem precisa defender um investimento e não é especialista em finanças: gestores, analistas, empreendedores, consultores.

**Não é para:** plano de negócios da empresa inteira, proposta comercial para cliente, "caso de uso" de sistema nem "estudo de caso". A skill confere isso logo no começo.

## Como funciona
| Passo | O que acontece |
|---|---|
| 0. Conferir o pedido | Confirma que é um business case, volta ao problema se o pedido chegar pela solução e escolhe o modo: uma página (padrão), completo ou revisão |
| 1. Entradas | Pergunta, de uma vez, quanto custa não fazer nada, quem decide, quem patrocina, o escopo, o que a empresa já tem e quem precisa estar de acordo. Identifica o nicho |
| 2. Cadeia de drivers | Monta a conta à vista: investimento → entrega → benefício → caixa. Cada número é marcado como fato, estimativa, premissa ou desconhecido, e as fontes são numeradas |
| 3. Documento | Escreve as sete seções: problema, alternativas, benefícios, custos, análise financeira, riscos, plano e KPIs |
| 4. Contas | Roda o script em três cenários (conservador, base e otimista) e gera a grade de sensibilidade |
| 5. Banca de críticos | De três a cinco papéis atacam o caso em uma rodada. As objeções entram no documento |
| 6. Simulação de reação | Opcional e rara: só quando a decisão depende da reação de muita gente |
| 7. Conferência | Checklist, nota de prontidão em quatro dimensões e recomendação: seguir, seguir com condições ou adiar |
| 8. Depois da decisão | Registra a resposta e, na data de cada KPI, compara o medido com o prometido |

## As regras que ela impõe ao agente
- **Conclusão primeiro.** O resumo abre pela recomendação e pela decisão pedida.
- **O corpo abre pelo custo de não fazer nada**, não pelo que será construído.
- **Todo número tem fonte ou vem marcado como premissa.** O agente não inventa número, fonte nem cotação.
- **Contas só pelo script.** Nada de ROI calculado "de cabeça" pelo modelo.
- **Caixa separado de hora liberada.** Hora economizada só vira dinheiro se um gasto de fato cair.
- **Recomendação pelo cenário conservador.** Se o caso só se paga no otimista, o documento diz isso.
- **As premissas que viram o resultado ficam nomeadas**, com o limite de cada uma.
- **O que foi procurado e não encontrado fica à vista**, em vez de escondido.
- **Taxa de desconto da empresa**, não a que favorece o caso.
- **Se a conta não fecha, o caso diz que não vale a pena.** Não se ajusta premissa para chegar ao "sim".

## Instalação
A skill segue o formato de pasta com `SKILL.md`. Você precisa de Python 3.8 ou mais novo para as contas; não há dependências.

**Claude Code, para todos os seus projetos:**
```bash
git clone https://github.com/alm36918/skill-business-case.git
mkdir -p ~/.claude/skills
cp -R skill-business-case/business-case ~/.claude/skills/
```

**Claude Code, só em um projeto:** copie a pasta `business-case` para `.claude/skills/` dentro do projeto.

**Outros agentes:** copie a pasta `business-case` para o diretório de skills do seu agente. Consulte a documentação dele para saber qual é.

## Como usar
Peça em linguagem normal. Exemplos:

- "Revise este business case que recebi e me diga se ele se sustenta." (modo revisão)
- "Monte um business case para trocarmos o sistema de atendimento. Custa R$ 180 mil para implantar e R$ 4 mil por mês."
- "Vale a pena contratar duas pessoas para o suporte em vez de terceirizar?"
- "Preciso justificar para a diretoria a compra de uma ferramenta de IA para o time comercial."

O agente vai fazer algumas perguntas antes de escrever. Quanto mais dados reais você der (contratos, notas, horas medidas), melhor o resultado. O que você não souber, ele marca como premissa.

## O script de contas
Funciona sozinho, sem agente:

```bash
python3 business-case/scripts/calc_financeiro.py business-case/exemplos/entrada.json
```

Com `--markdown`, ele devolve as tabelas prontas para colar no documento.

Ele recebe investimento, benefícios de caixa, capacidade liberada, custos fixos e custo variável por ano, em um ou mais cenários, e devolve:
- ROI, payback simples e descontado, VPL e TIR;
- o **ponto de equilíbrio**: quanto dos benefícios precisa se realizar, e quanto o investimento pode estourar, antes de o caso deixar de se pagar;
- a **grade de sensibilidade**: o VPL para cada combinação de variação dos benefícios e da taxa de desconto.

Resultado do exemplo incluído (dados fictícios, 3 anos, taxa de 12% ao ano):

| Indicador | Conservador | Base | Otimista |
|---|---|---|---|
| ROI | −3% | 39% | 67% |
| Payback simples | não atinge | 1,76 ano | 1,36 ano |
| VPL | R$ −43.096 | R$ 64.987 | R$ 137.042 |
| TIR | −3% | 32% | 53% |

Grade de sensibilidade do cenário base (VPL):

| Benefícios | 10% | 11% | 12% | 13% | 14% |
|---|---|---|---|---|---|
| −20% | R$ −947 | R$ −4.053 | R$ −7.068 | R$ −9.997 | R$ −12.842 |
| −10% | R$ 36.356 | R$ 32.603 | R$ 28.959 | R$ 25.420 | R$ 21.982 |
| plano | R$ 73.659 | R$ 69.259 | R$ 64.987 | R$ 60.838 | R$ 56.806 |
| +10% | R$ 110.962 | R$ 105.915 | R$ 101.014 | R$ 96.255 | R$ 91.631 |
| +20% | R$ 148.264 | R$ 142.570 | R$ 137.042 | R$ 131.672 | R$ 126.455 |

Leitura: com 10% a menos de benefícios o caso ainda se paga; com 20% a menos, não.

O caso completo, com a recomendação, está em [`business-case/references/exemplo.md`](business-case/references/exemplo.md).

## Nichos
O roteiro e as contas não mudam com o nicho. Mudam os drivers de benefício, os custos que costumam ser esquecidos, os riscos, os KPIs e quem critica. Por isso a skill usa **perfis de nicho**: arquivos em `business-case/references/perfis/` que o agente só lê quando o caso pede.

- Perfil pronto: [automação e IA](business-case/references/perfis/automacao-e-ia.md).
- Sem perfil para o seu caso, o agente faz as perguntas do [modelo de perfil](business-case/references/perfis/_modelo.md) e segue com um perfil provisório.
- Perfil não traz número pronto: referência de mercado só entra com fonte e data.

Quer acrescentar um nicho? Veja [CONTRIBUTING.md](CONTRIBUTING.md).

## Banca de críticos
Antes de entregar, o agente simula de três a cinco papéis (finanças, operação, tecnologia, cliente e um diretor cético). Cada um analisa o caso sozinho, aponta objeções e diz que evidência o faria mudar de ideia. O autor responde, e o documento sai com as objeções respondidas e as que ficaram em aberto.

Os críticos são simulados por IA. São hipóteses de objeção, não a opinião das pessoas reais, e o documento diz isso. O protocolo está em [`banca-de-criticos.md`](business-case/references/banca-de-criticos.md).

## Modo revisão e ensaio do pitch
- **Revisão:** recebeu um business case pronto? A skill refaz as contas, lê a grade de sensibilidade, aponta o que falta e entrega um parecer: sustenta-se, sustenta-se com condições ou não se sustenta. Roteiro em [`revisao.md`](business-case/references/revisao.md).
- **Ensaio do pitch:** vai apresentar a um comitê? O agente faz as seis perguntas que um comitê costuma fazer, uma por vez, e avalia cada resposta como forte, média ou fraca. Roteiro em [`ensaio-do-pitch.md`](business-case/references/ensaio-do-pitch.md).

## Simulação de reação
Para decisões que dependem de como muita gente vai reagir, existem simuladores com muitos agentes de IA, como o [MiroFish](https://github.com/666ghj/MiroFish). A skill orienta quando isso faz sentido e como usar o resultado (como hipótese, nunca como número), mas **não instala nem aciona** nenhuma ferramenta. Detalhes em [`simulacao-de-reacao.md`](business-case/references/simulacao-de-reacao.md).

## O que tem no repositório
| Caminho | Para que serve |
|---|---|
| `business-case/SKILL.md` | O roteiro que o agente segue |
| `business-case/references/modelo.md` | Modelo do documento |
| `business-case/references/guia.md` | Perguntas para achar o custo de não fazer nada, ênfase por público, como apresentar, o que fazer quando contestam um número |
| `business-case/references/exemplo.md` | Um caso resolvido do começo ao fim |
| `business-case/references/banca-de-criticos.md` | Protocolo da banca |
| `business-case/references/simulacao-de-reacao.md` | Quando e como usar simulação |
| `business-case/references/checklist.md` | Conferência antes de entregar e critérios da nota de prontidão |
| `business-case/references/revisao.md` | Como avaliar um business case já pronto |
| `business-case/references/ensaio-do-pitch.md` | Treino de perguntas e respostas |
| `business-case/references/perfis/` | Perfis de nicho |
| `business-case/scripts/calc_financeiro.py` | As contas |
| `business-case/exemplos/` | Entrada e saída de exemplo |
| `tests/` | Testes do script |

## Limites
- **Não é aconselhamento financeiro, contábil nem jurídico.** A decisão e a responsabilidade pelos números são de quem assina o business case.
- A qualidade do resultado depende dos dados que você fornece. Com premissas fracas, o caso sai fraco, e a skill foi desenhada para deixar isso visível.
- O script trabalha com períodos anuais, sem impostos nem inflação. Para análises mais finas, use a planilha da sua empresa.
- O roteiro ainda não foi validado em business cases reais.

## Próximos passos
- Validar em casos reais e enxugar o que o agente já faz sozinho.
- Aceitar períodos mensais no script.
- Mais perfis de nicho: dados e marketing, contratação, expansão.
- Trabalhar com faixas de valores e simular a incerteza.
- Lista de categorias de valor, indicadores antecedentes e modo sem perguntas.

## Testes
```bash
python3 -m unittest discover -s tests -v
```

## Contribuir
Veja [CONTRIBUTING.md](CONTRIBUTING.md). O que mais ajuda é o relato de quem usou num caso real.

## Licença e créditos
Licença [MIT](LICENSE). Parte do método foi adaptada dos projetos [FDEOps](https://github.com/suboss87/FDEOps) e [24-strategy-skills-for-claude](https://github.com/Natan-Mohart/24-strategy-skills-for-claude), ambos sob licença MIT. As demais referências e os detalhes estão em [CREDITOS.md](CREDITOS.md).

## In English
An agent skill (the `SKILL.md` folder format) that builds an internal investment business case in Brazilian Portuguese: cost of doing nothing, visible driver model, ROI/payback/NPV/IRR and a sensitivity grid computed by a dependency-free Python script, a simulated panel of critics, a review mode for existing cases, a pitch rehearsal and niche profiles. Version 0.2.0; not yet validated on real cases.
