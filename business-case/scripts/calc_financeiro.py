#!/usr/bin/env python3
"""Indicadores financeiros de um business case.

Uso:
    python3 calc_financeiro.py entrada.json

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
    custos                 custos recorrentes do ano
    "beneficios" (sem sufixo) é aceito e conta como caixa.

Convenção: investimento no ano 0; benefícios e custos de cada ano no fim do ano.

Saída (JSON), por cenário: ROI, payback simples e descontado (em anos), VPL, TIR,
ponto de equilíbrio e capacidade liberada. ROI, payback, VPL e TIR usam só os
benefícios de caixa.

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


def calcular_cenario(cenario, taxa):
    investimento = float(cenario["investimento_inicial"])
    anos = cenario["anos"]
    if not anos:
        raise ValueError("o cenário precisa de pelo menos um ano")
    caixa = [float(a.get("beneficios_caixa", a.get("beneficios", 0))) for a in anos]
    capacidade = [float(a.get("beneficios_capacidade", 0)) for a in anos]
    custos = [float(a.get("custos", 0)) for a in anos]
    liquidos = [b - c for b, c in zip(caixa, custos)]
    custo_total = investimento + sum(custos)

    vp_caixa = sum(b / (1 + taxa) ** t for t, b in enumerate(caixa, 1))
    vp_custos = sum(c / (1 + taxa) ** t for t, c in enumerate(custos, 1))
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
        "cenarios": {nome: calcular_cenario(c, taxa) for nome, c in cenarios.items()},
    }


def main(argv):
    if len(argv) != 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0 if len(argv) == 2 else 2
    try:
        with open(argv[1], encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        resultado = calcular(dados)
    except (OSError, ValueError, KeyError, TypeError) as erro:
        campo = f"campo ausente: {erro}" if isinstance(erro, KeyError) else str(erro)
        print(f"Erro na entrada: {campo}", file=sys.stderr)
        return 1
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
