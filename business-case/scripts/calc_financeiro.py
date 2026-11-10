#!/usr/bin/env python3
"""Indicadores financeiros de um business case.

Uso:
    python3 calc_financeiro.py entrada.json              saída em JSON
    python3 calc_financeiro.py entrada.json --markdown   tabelas prontas para colar no documento

Entrada (JSON):
    {
      "moeda": "R$",
      "taxa_desconto_anual": 0.12,
      "cenarios": {
        "base": {
          "investimento_inicial": 100000,
          "anos": [
            {"beneficios_caixa": 40000, "beneficios_capacidade": 10000, "custos": 0}
          ]
        }
      }
    }

    beneficios_caixa       receita nova ou gasto que de fato deixa de existir
    beneficios_capacidade  horas liberadas sem corte de gasto (informadas à parte)
    custos                 custos fixos recorrentes do ano
    custo_variavel_pct     opcional: custo que acompanha o benefício de caixa, em % dele
                           (ex.: custo do produto vendido). Padrão: 0
    "beneficios" (sem sufixo) é aceito e conta como caixa.

    Opcional, na raiz: "sensibilidade": {"variacao_beneficios_pct": [-20, -10, 0, 10, 20],
                                         "variacao_taxa_pontos": [-2, -1, 0, 1, 2]}
    Esses são os valores padrão da grade de sensibilidade.

Convenção: investimento no ano 0; benefícios e custos de cada ano no fim do ano.

Saída (JSON), por cenário: ROI, payback simples e descontado (em anos), VPL, TIR,
ponto de equilíbrio, grade de sensibilidade (VPL para cada combinação de variação
dos benefícios de caixa e da taxa de desconto) e capacidade liberada. ROI, payback,
VPL e TIR usam só os benefícios de caixa.

Só usa a biblioteca padrão do Python 3.8 ou mais novo.
"""
import json
import sys

NOTA = ("ROI, payback, VPL e TIR usam só benefícios de caixa. "
        "A capacidade liberada é informada à parte e não entra nessas contas.")


def vpl(taxa, investimento, liquidos):
    """Valor presente líquido dos fluxos anuais, descontado o investimento do ano 0."""
    return -investimento + sum(f / (1 + taxa) ** t for t, f in enumerate(liquidos, 1))


def payback(investimento, liquidos, taxa=0.0):
    """Anos até o acumulado zerar, com interpolação dentro do ano. None se não zera."""
    acumulado = -investimento
    for t, fluxo in enumerate(liquidos, 1):
        valor = fluxo / (1 + taxa) ** t
        if acumulado + valor >= 0:
            return round(t - 1 + (-acumulado / valor if valor else 0), 2)
        acumulado += valor
    return None


def tir(investimento, liquidos):
    """Taxa interna de retorno por bisseção entre -99% e 1000%. None se não houver raiz."""
    def f(taxa):
        return vpl(taxa, investimento, liquidos)

    baixo, alto = -0.99, 10.0
    if f(baixo) * f(alto) > 0:
        return None
    for _ in range(200):
        meio = (baixo + alto) / 2
        if f(baixo) * f(meio) <= 0:
            alto = meio
        else:
            baixo = meio
    return round((baixo + alto) / 2, 4) + 0.0  # evita "-0.0"


GRADE_PADRAO = {"variacao_beneficios_pct": [-20, -10, 0, 10, 20], "variacao_taxa_pontos": [-2, -1, 0, 1, 2]}


def fluxos_liquidos(caixa, fixos, variavel_pct, fator=1.0):
    """Fluxo de cada ano: benefício de caixa (vezes o fator) menos o custo variável e o fixo."""
    return [b * fator * (1 - v / 100) - f for b, f, v in zip(caixa, fixos, variavel_pct)]


def grade_sensibilidade(investimento, caixa, fixos, variavel_pct, taxa, config):
    """VPL para cada variação dos benefícios de caixa (linhas) e da taxa de desconto (colunas)."""
    variacoes = [float(x) for x in config.get("variacao_beneficios_pct", GRADE_PADRAO["variacao_beneficios_pct"])]
    pontos = [float(x) for x in config.get("variacao_taxa_pontos", GRADE_PADRAO["variacao_taxa_pontos"])]
    linhas = []
    for variacao in variacoes:
        liquidos = fluxos_liquidos(caixa, fixos, variavel_pct, 1 + variacao / 100)
        linhas.append([round(vpl(taxa + p / 100, investimento, liquidos), 2) if taxa + p / 100 > -1 else None
                       for p in pontos])
    return {"variacao_beneficios_pct": variacoes, "variacao_taxa_pontos": pontos,
            "taxas": [round(taxa + p / 100, 4) for p in pontos], "vpl": linhas}


def calcular_cenario(cenario, taxa, config_grade=None):
    investimento = float(cenario["investimento_inicial"])
    anos = cenario["anos"]
    if not anos:
        raise ValueError("o cenário precisa de pelo menos um ano")
    caixa = [float(a.get("beneficios_caixa", a.get("beneficios", 0))) for a in anos]
    capacidade = [float(a.get("beneficios_capacidade", 0)) for a in anos]
    fixos = [float(a.get("custos", 0)) for a in anos]
    variavel_pct = [float(a.get("custo_variavel_pct", 0)) for a in anos]
    if any(v < 0 or v > 100 for v in variavel_pct):
        raise ValueError("custo_variavel_pct precisa estar entre 0 e 100")
    variaveis = [b * v / 100 for b, v in zip(caixa, variavel_pct)]
    custos = [f + v for f, v in zip(fixos, variaveis)]
    liquidos = fluxos_liquidos(caixa, fixos, variavel_pct)
    custo_total = investimento + sum(custos)

    # margem = benefício de caixa já descontado o custo variável
    vp_caixa = sum(b * (1 - v / 100) / (1 + taxa) ** t for t, (b, v) in enumerate(zip(caixa, variavel_pct), 1))
    vp_custos = sum(f / (1 + taxa) ** t for t, f in enumerate(fixos, 1))
    sem_caixa = not any(caixa)

    def texto_payback(valor):
        if valor is not None:
            return valor
        return "não estabelecido: sem benefício de caixa" if sem_caixa else "não atinge no horizonte"

    taxa_interna = tir(investimento, liquidos)
    return {
        "horizonte_anos": len(anos),
        "beneficios_totais": round(sum(caixa), 2),
        "custos_totais": round(custo_total, 2),
        "roi": round((sum(caixa) - custo_total) / custo_total, 4) if custo_total else None,
        "payback_simples_anos": texto_payback(payback(investimento, liquidos)),
        "payback_descontado_anos": texto_payback(payback(investimento, liquidos, taxa)),
        "vpl": round(vpl(taxa, investimento, liquidos), 2),
        "tir": taxa_interna if taxa_interna is not None else "indefinida",
        "ponto_de_equilibrio": {
            # fração dos benefícios de caixa estimados que precisa se realizar para o VPL zerar
            "beneficios_minimos_pct": round((investimento + vp_custos) / vp_caixa, 4) if vp_caixa else None,
            # quanto o investimento inicial pode custar, em relação ao estimado, antes de o VPL zerar
            "investimento_maximo_pct": round((vp_caixa - vp_custos) / investimento, 4) if investimento else None,
        },
        "sensibilidade": grade_sensibilidade(investimento, caixa, fixos, variavel_pct, taxa, config_grade or {}),
        "custos_variaveis_totais": round(sum(variaveis), 2),
        "capacidade_liberada_total": round(sum(capacidade), 2),
        "nota": NOTA,
    }


def calcular(dados):
    taxa = float(dados["taxa_desconto_anual"])
    if taxa <= -1:
        raise ValueError("taxa_desconto_anual precisa ser maior que -1")
    cenarios = dados["cenarios"]
    if not cenarios:
        raise ValueError("informe pelo menos um cenário")
    return {
        "moeda": dados.get("moeda", "R$"),
        "taxa_desconto_anual": taxa,
        "cenarios": {nome: calcular_cenario(c, taxa, dados.get("sensibilidade")) for nome, c in cenarios.items()},
    }


def _dinheiro(valor, moeda):
    if valor is None:
        return "-"
    texto = f"{abs(valor):,.0f}".replace(",", ".")
    return f"{moeda} {'-' if valor < 0 else ''}{texto}"


def _pct(valor):
    return "-" if valor is None or isinstance(valor, str) else f"{valor * 100:.0f}%".replace(".", ",")


def _anos(valor):
    return valor if isinstance(valor, str) else f"{valor:.2f}".replace(".", ",") + " ano(s)"


def em_markdown(resultado):
    """Tabelas prontas para colar no documento: indicadores por cenário e grade de cada cenário."""
    moeda, cenarios = resultado["moeda"], resultado["cenarios"]
    nomes = list(cenarios)
    linhas = ["| Indicador | " + " | ".join(nomes) + " |", "|---|" + "---|" * len(nomes)]

    def linha(rotulo, funcao):
        linhas.append(f"| {rotulo} | " + " | ".join(funcao(cenarios[n]) for n in nomes) + " |")

    linha("ROI", lambda c: _pct(c["roi"]))
    linha("Payback simples", lambda c: _anos(c["payback_simples_anos"]))
    linha("Payback descontado", lambda c: _anos(c["payback_descontado_anos"]))
    linha("VPL", lambda c: _dinheiro(c["vpl"], moeda))
    linha("TIR", lambda c: _pct(c["tir"]) if not isinstance(c["tir"], str) else c["tir"])
    linha("Benefícios mínimos para empatar", lambda c: _pct(c["ponto_de_equilibrio"]["beneficios_minimos_pct"]))
    linha("Investimento máximo para empatar", lambda c: _pct(c["ponto_de_equilibrio"]["investimento_maximo_pct"]))
    linha("Capacidade liberada (à parte)", lambda c: _dinheiro(c["capacidade_liberada_total"], moeda))
    for nome in nomes:
        grade = cenarios[nome]["sensibilidade"]
        linhas += ["", f"Grade de sensibilidade do VPL, cenário {nome} (linhas: benefícios de caixa; colunas: taxa de desconto):", "",
                   "| Benefícios | " + " | ".join(_pct(t) for t in grade["taxas"]) + " |",
                   "|---|" + "---|" * len(grade["taxas"])]
        for variacao, valores in zip(grade["variacao_beneficios_pct"], grade["vpl"]):
            rotulo = "plano" if variacao == 0 else f"{variacao:+.0f}%"
            linhas.append(f"| {rotulo} | " + " | ".join(_dinheiro(v, moeda) for v in valores) + " |")
    return "\n".join(linhas)


def main(argv):
    args = [a for a in argv[1:] if a != "--markdown"]
    markdown = "--markdown" in argv[1:]
    if len(args) != 1 or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if args and args[0] in ("-h", "--help") else 2
    try:
        with open(args[0], encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        resultado = calcular(dados)
    except (OSError, ValueError, KeyError, TypeError) as erro:
        campo = f"campo ausente: {erro}" if isinstance(erro, KeyError) else str(erro)
        print(f"Erro na entrada: {campo}", file=sys.stderr)
        return 1
    print(em_markdown(resultado) if markdown else json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
