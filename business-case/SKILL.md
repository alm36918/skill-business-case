---
name: business-case
description: Monta e põe à prova um business case que justifica um projeto, investimento ou iniciativa interna perante quem decide. Parte do custo de não fazer nada, calcula ROI, payback, VPL e TIR por script, aponta as premissas que viram o resultado e passa o caso por uma banca de críticos antes da entrega. Use quando pedirem um business case, a justificativa de um investimento ou "vale a pena fazer isso?". Não use para plano de negócios, proposta comercial, caso de uso de sistema nem estudo de caso.
---

# Business case

Resultado esperado: um documento que quem decide lê em 10 minutos e consegue aprovar, aprovar com condições ou adiar. Quem assina precisa conseguir explicar o caso em 60 segundos e defender cada número.

Confirme antes que o pedido é mesmo um business case: a justificativa de um investimento ainda não decidido. "Caso de uso" (o que um sistema faz) e "estudo de caso" (análise de algo que já aconteceu) são outros documentos; se for um deles, diga isso e não force este roteiro.

Se o pedido chegar pela solução ("precisamos comprar a ferramenta X"), volte ao problema antes de seguir: que dor ela resolve e quanto essa dor custa. Caso que começa pela ferramenta é o primeiro a ser recusado.

Os caminhos citados aqui são relativos à pasta desta skill. Escreva o documento no idioma de quem pediu.

Escolha o modo pelo pedido:
- **Uma página** (padrão): resumo de `references/modelo.md`, para decisões pequenas ou primeira conversa.
- **Completo**: as sete seções, para valores altos ou comitê formal.
- **Revisão**: quando o pedido for avaliar um business case já pronto, seu ou de outra pessoa. Siga `references/revisao.md` em vez dos passos 1 a 3.

## 1. Levante as entradas (pergunte só o que faltar, de uma vez)
- O problema ou a oportunidade e **quanto custa não fazer nada**: gasto direto, capacidade perdida, oportunidade travada, risco exposto. As perguntas que revelam cada tipo estão em `references/guia.md`.
- Quem decide e o que essa pessoa exige (teto de valor, prazo de retorno, modelo de documento da empresa).
- O pedido: valor, pessoas e prazo. E o **escopo**: o que entra, o que fica de fora e o que ainda está em aberto.
- **Patrocinador e alinhamento**: quem apoia o caso, se essa pessoa tem autoridade sobre o orçamento e a qual objetivo da empresa a iniciativa serve. Sem patrocinador, registre isso como risco.
- **O que já existe**: a empresa já tem ferramenta, licença, equipe ou projeto que resolve isso, mesmo em parte? Registre com quem isso foi conferido.
- **Quem precisa estar de acordo**: finanças, tecnologia, operação e a área que vai usar. Se der, recomende ouvir essas pessoas antes de fechar o caso; a banca simulada do passo 5 não substitui a conversa real.
- Horizonte da análise (padrão: 3 anos) e taxa de desconto da empresa. Sem taxa informada, use 12% ao ano e marque como premissa.

Se a empresa tem modelo próprio, siga o dela e use esta skill para conferir o que falta.

**Nicho.** Identifique o tipo de iniciativa (software ou automação, contratação, expansão, equipamento, mudança de processo, campanha) e o setor. Se existir um perfil em `references/perfis/`, leia só esse arquivo e use os drivers, custos esquecidos, riscos, KPIs e papéis da banca que ele traz. Se não existir, faça as perguntas de `references/perfis/_modelo.md` a quem pediu e siga com esse perfil provisório. O roteiro e as contas não mudam com o nicho; mudam os drivers, os riscos, os KPIs e quem critica. Nunca use referência de mercado sem fonte e data.

## 2. Monte a cadeia de drivers antes do texto
Uma conta que quem decide consegue refazer:
`investimento → o que entrega → benefício (com unidade e fonte) → caixa líquido no horizonte`
- Escreva a aritmética à vista: 3 pessoas × 8 h/semana × R$ 75/h × 52 semanas.
- Separe **capacidade liberada** de **economia de caixa**. Horas só viram dinheiro se o gasto de fato cair (hora extra, terceiro, contratação evitada). Diga quem realiza o benefício e como.
- Classifique cada número: **fato** (com fonte), **estimativa** (com faixa), **premissa** ou **desconhecido**. Nunca invente número, fonte ou cotação.
- Não some o número pequeno e certo com o risco grande e incerto, nem conte o mesmo benefício duas vezes.
- Numere as fontes (F1, F2…) numa tabela, com o dado que cada uma sustenta, e liste o que foi procurado e não encontrado. O modelo está em `references/modelo.md`.

Um caso resolvido, do começo ao fim, está em `references/exemplo.md`. Leia-o na primeira vez.

## 3. Escreva as seções
Modelo em `references/modelo.md`. O resumo abre pela conclusão: a recomendação e a decisão pedida vêm na primeira linha, e os dados depois.
1. **Problema ou oportunidade**, abrindo pelo custo de não fazer nada, seguido do escopo (dentro, fora e a definir).
2. **Alternativas consideradas**: "não fazer nada", "usar ou ampliar o que a empresa já tem" (quando existir) e pelo menos uma alternativa real além da recomendada. Se "fazer em casa" for alternativa, conte manutenção, segurança e o tempo de quem faz.
3. **Benefícios esperados**: financeiros separados dos estratégicos. Percorra quatro frentes para não esquecer nenhuma: eficiência, receita, redução de risco e agilidade. Benefício estratégico não recebe valor em dinheiro sem base; meça-o por um indicador substituto (por exemplo, rotatividade no lugar de "satisfação da equipe").
4. **Custos estimados**: implantação, operação, horas internas, treinamento, adoção e migração. No investimento inicial entram também capital de giro e custos de lançamento. Inclua uma reserva de contingência e diga o percentual e o motivo.
5. **Análise financeira**: veja o passo 4.
6. **Riscos e mitigações**: 3 a 6 riscos, com probabilidade, impacto, mitigação e dono. Mitigação que custa dinheiro entra na seção de custos e nas contas.
7. **Plano de implementação e KPIs**: marcos com responsável e, para cada benefício, o KPI com valor de hoje (medido antes de começar), meta e data de medição. Quando a incerteza for decisiva, o plano começa por um piloto com critério de sucesso e data para decidir entre seguir e parar, e diz o que muda do piloto para a escala.

Ajuste a ênfase a quem decide (tabela em `references/guia.md`). O detalhe vai para anexo.

## 4. Análise financeira e sensibilidade (sempre pelo script)
Monte um JSON como `exemplos/entrada.json` e rode `python3 scripts/calc_financeiro.py entrada.json`. Os períodos são anos. Se não for possível rodar o script, diga isso e entregue a entrada pronta com as fórmulas; não apresente indicador que não foi calculado.
- Informe `beneficios_caixa` (receita nova ou gasto que deixa de existir) separado de `beneficios_capacidade` (horas liberadas). ROI, payback, VPL e TIR usam só o caixa; sem benefício de caixa, o payback sai como "não estabelecido" e é assim que vai para o documento.
- Em iniciativa que gera receita, informe `custo_variavel_pct`: o custo que cresce junto com a venda.
- Use a taxa de desconto da empresa. Não escolha a taxa que favorece o caso.
- Três cenários: conservador, base e otimista. Copie os valores como saíram; com `--markdown` o script entrega as tabelas prontas.
- O script devolve, por cenário, o **ponto de equilíbrio**: quanto dos benefícios precisa se realizar e quanto o investimento pode estourar antes de o VPL zerar. Use isso para nomear **as uma ou duas premissas que viram o resultado**, com o limite de cada uma.
- O script devolve também a **grade de sensibilidade**: o VPL para cada combinação de variação dos benefícios e da taxa de desconto. Mostre a grade do cenário base e diga a partir de que ponto o VPL fica negativo.
- Recomende com base no cenário conservador. Se o caso só se paga no otimista, escreva isso.
- Se a conta não fecha, o business case diz que não vale a pena. Nunca ajuste premissas para chegar ao "sim". Se contestarem um número, abra as entradas e diga qual medição resolve a dúvida.

## 5. Banca de críticos (obrigatória no modo completo)
Antes de entregar, ponha o caso à prova. Protocolo em `references/banca-de-criticos.md`:
rodada independente de 3 a 5 papéis → checagem → confronto de até duas afirmações por papel → revisão registrada em tabela. Uma rodada só.
O que sobreviver entra no documento como **objeções respondidas**; o que não tiver resposta entra como **objeções em aberto**, com a evidência ou o piloto que resolveria. Objeção não é voto: uma objeção com evidência vale mais que quatro opiniões.

## 6. Simulação de reação (opcional, raramente)
Só quando a decisão depende de como muita gente vai reagir (clientes, público, grande número de funcionários). Veja `references/simulacao-de-reacao.md`. O resultado de uma simulação é hipótese: alimenta riscos e desenho de piloto, nunca vira número do caso.

## 7. Confira antes de entregar
Lista em `references/checklist.md`. O mínimo: o pedido cabe em uma frase; "não fazer nada" está nas alternativas; os totais do texto batem com a entrada do script; as premissas que viram o resultado estão nomeadas; cada benefício tem KPI; as objeções em aberto aparecem.

Dê a **nota de prontidão** em quatro dimensões (clareza do problema, viabilidade, apoio e alinhamento estratégico), cada uma como forte, média ou fraca, com o motivo. Os critérios estão em `references/checklist.md`. Dimensão fraca aparece no documento; não a esconda.

Feche com a recomendação em uma de três formas: **seguir**, **seguir com condições** (diga quais) ou **adiar** (diga o que falta saber).

Teste final: quem assina consegue explicar o caso em 60 segundos? Se não, corte até conseguir. Se a pessoa for apresentar o caso a um comitê, ofereça o ensaio de `references/ensaio-do-pitch.md`.

## 8. Depois da decisão
Registre a resposta de quem decidiu (aprovado, aprovado com mudanças, adiado), com data e condições. Na data de cada KPI, compare o medido com o prometido.

Criar o documento não autoriza enviá-lo a ninguém: entregue a quem pediu.
