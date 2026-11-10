"""Testes do script de contas. Rode na raiz do repositório:
    python3 -m unittest discover -s tests -v
"""
import importlib.util
import json
import pathlib
import subprocess
import sys
import unittest

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = RAIZ / "business-case" / "scripts" / "calc_financeiro.py"
EXEMPLOS = RAIZ / "business-case" / "exemplos"

spec = importlib.util.spec_from_file_location("calc_financeiro", SCRIPT)
calc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc)


def anos(n, **campos):
    return [dict(campos) for _ in range(n)]


class Indicadores(unittest.TestCase):
    def setUp(self):
        # 100 mil de investimento e 40 mil de caixa por ano, por 4 anos, a 10% ao ano
        self.base = calc.calcular({
            "taxa_desconto_anual": 0.10,
            "cenarios": {"base": {"investimento_inicial": 100000, "anos": anos(4, beneficios_caixa=40000, custos=0)}},
        })["cenarios"]["base"]

    def test_vpl_bate_com_a_formula_da_anuidade(self):
        esperado = -100000 + 40000 * (1 - 1.1 ** -4) / 0.1
        self.assertAlmostEqual(self.base["vpl"], esperado, places=2)

    def test_payback_simples(self):
        self.assertEqual(self.base["payback_simples_anos"], 2.5)

    def test_payback_descontado_e_maior_que_o_simples(self):
        self.assertGreater(self.base["payback_descontado_anos"], self.base["payback_simples_anos"])

    def test_roi(self):
        self.assertAlmostEqual(self.base["roi"], 0.6)

    def test_tir_zera_o_vpl(self):
        taxa = self.base["tir"]
        self.assertAlmostEqual(calc.vpl(taxa, 100000, [40000] * 4), 0, delta=50)

    def test_ponto_de_equilibrio_zera_o_vpl(self):
        fracao = self.base["ponto_de_equilibrio"]["beneficios_minimos_pct"]
        self.assertAlmostEqual(calc.vpl(0.10, 100000, [40000 * fracao] * 4), 0, delta=20)
        teto = self.base["ponto_de_equilibrio"]["investimento_maximo_pct"]
        self.assertAlmostEqual(calc.vpl(0.10, 100000 * teto, [40000] * 4), 0, delta=20)


class CaixaECapacidade(unittest.TestCase):
    def test_capacidade_nao_entra_nas_contas(self):
        com = calc.calcular({"taxa_desconto_anual": 0.1, "cenarios": {"c": {"investimento_inicial": 100000,
              "anos": anos(4, beneficios_caixa=40000, beneficios_capacidade=99999, custos=0)}}})["cenarios"]["c"]
        sem = calc.calcular({"taxa_desconto_anual": 0.1, "cenarios": {"c": {"investimento_inicial": 100000,
              "anos": anos(4, beneficios_caixa=40000, custos=0)}}})["cenarios"]["c"]
        for campo in ("vpl", "roi", "tir", "payback_simples_anos"):
            self.assertEqual(com[campo], sem[campo])
        self.assertEqual(com["capacidade_liberada_total"], 4 * 99999)

    def test_so_capacidade_da_payback_nao_estabelecido(self):
        r = calc.calcular({"taxa_desconto_anual": 0.1, "cenarios": {"c": {"investimento_inicial": 50000,
            "anos": anos(2, beneficios_capacidade=30000, custos=0)}}})["cenarios"]["c"]
        self.assertTrue(r["payback_simples_anos"].startswith("não estabelecido"))
        self.assertEqual(r["vpl"], -50000.0)

    def test_campo_beneficios_sem_sufixo_conta_como_caixa(self):
        r = calc.calcular({"taxa_desconto_anual": 0.1, "cenarios": {"c": {"investimento_inicial": 100000,
            "anos": anos(4, beneficios=40000, custos=0)}}})["cenarios"]["c"]
        self.assertEqual(r["payback_simples_anos"], 2.5)


class Sensibilidade(unittest.TestCase):
    def setUp(self):
        self.dados = {"taxa_desconto_anual": 0.10, "cenarios": {"base": {"investimento_inicial": 100000,
                      "anos": anos(4, beneficios_caixa=40000, custos=0)}}}
        self.base = calc.calcular(self.dados)["cenarios"]["base"]
        self.grade = self.base["sensibilidade"]

    def test_centro_da_grade_e_o_vpl_do_cenario(self):
        i = self.grade["variacao_beneficios_pct"].index(0)
        j = self.grade["variacao_taxa_pontos"].index(0)
        self.assertEqual(self.grade["vpl"][i][j], self.base["vpl"])

    def test_celula_bate_com_calculo_direto(self):
        # benefícios -20% e taxa +2 pontos: 32 mil por ano a 12%
        i = self.grade["variacao_beneficios_pct"].index(-20)
        j = self.grade["variacao_taxa_pontos"].index(2)
        self.assertAlmostEqual(self.grade["vpl"][i][j], calc.vpl(0.12, 100000, [32000] * 4), places=2)

    def test_vpl_cresce_com_beneficio_e_cai_com_taxa(self):
        vpl = self.grade["vpl"]
        for linha in vpl:
            self.assertEqual(linha, sorted(linha, reverse=True))
        for coluna in zip(*vpl):
            self.assertEqual(list(coluna), sorted(coluna))

    def test_grade_personalizada(self):
        dados = dict(self.dados, sensibilidade={"variacao_beneficios_pct": [-50, 0], "variacao_taxa_pontos": [0]})
        grade = calc.calcular(dados)["cenarios"]["base"]["sensibilidade"]
        self.assertEqual(len(grade["vpl"]), 2)
        self.assertEqual(len(grade["vpl"][0]), 1)

    def test_saida_em_markdown(self):
        texto = calc.em_markdown(calc.calcular(self.dados))
        self.assertIn("| VPL |", texto)
        self.assertIn("Grade de sensibilidade", texto)
        self.assertIn("| plano |", texto)


class CustoVariavel(unittest.TestCase):
    def caso(self, pct):
        return calc.calcular({"taxa_desconto_anual": 0.10, "cenarios": {"c": {"investimento_inicial": 100000,
               "anos": anos(4, beneficios_caixa=100000, custo_variavel_pct=pct, custos=20000)}}})["cenarios"]["c"]

    def test_custo_variavel_reduz_o_fluxo(self):
        # 100 mil de receita, 40% de custo variável e 20 mil fixos = 40 mil líquidos por ano
        r = self.caso(40)
        self.assertAlmostEqual(r["vpl"], calc.vpl(0.10, 100000, [40000] * 4), places=2)
        self.assertEqual(r["custos_variaveis_totais"], 160000)
        self.assertEqual(r["payback_simples_anos"], 2.5)

    def test_grade_move_o_custo_variavel_junto(self):
        r = self.caso(40)
        g = r["sensibilidade"]
        i, j = g["variacao_beneficios_pct"].index(-10), g["variacao_taxa_pontos"].index(0)
        # receita de 90 mil: margem de 54 mil menos 20 mil fixos = 34 mil
        self.assertAlmostEqual(g["vpl"][i][j], calc.vpl(0.10, 100000, [34000] * 4), places=2)

    def test_ponto_de_equilibrio_considera_o_custo_variavel(self):
        r = self.caso(40)
        fracao = r["ponto_de_equilibrio"]["beneficios_minimos_pct"]
        fluxo = 100000 * fracao * 0.6 - 20000
        self.assertAlmostEqual(calc.vpl(0.10, 100000, [fluxo] * 4), 0, delta=30)

    def test_percentual_fora_da_faixa(self):
        with self.assertRaises(ValueError):
            self.caso(120)


class CasosLimite(unittest.TestCase):
    def test_caso_que_nao_se_paga(self):
        r = calc.calcular({"taxa_desconto_anual": 0.1, "cenarios": {"c": {"investimento_inicial": 100000,
            "anos": anos(3, beneficios_caixa=10000, custos=0)}}})["cenarios"]["c"]
        self.assertEqual(r["payback_simples_anos"], "não atinge no horizonte")
        self.assertLess(r["vpl"], 0)

    def test_entrada_invalida(self):
        with self.assertRaises(KeyError):
            calc.calcular({"taxa_desconto_anual": 0.1})
        with self.assertRaises(ValueError):
            calc.calcular({"taxa_desconto_anual": 0.1, "cenarios": {}})
        with self.assertRaises(ValueError):
            calc.calcular({"taxa_desconto_anual": -1, "cenarios": {"c": {"investimento_inicial": 1, "anos": anos(1, beneficios_caixa=1)}}})


class Exemplo(unittest.TestCase):
    def test_saida_do_exemplo_esta_atualizada(self):
        entrada = json.loads((EXEMPLOS / "entrada.json").read_text(encoding="utf-8"))
        esperado = json.loads((EXEMPLOS / "saida.json").read_text(encoding="utf-8"))
        self.assertEqual(calc.calcular(entrada), esperado)

    def test_linha_de_comando_markdown(self):
        r = subprocess.run([sys.executable, str(SCRIPT), str(EXEMPLOS / "entrada.json"), "--markdown"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("| Indicador |", r.stdout)

    def test_linha_de_comando(self):
        r = subprocess.run([sys.executable, str(SCRIPT), str(EXEMPLOS / "entrada.json")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("cenarios", json.loads(r.stdout))


if __name__ == "__main__":
    unittest.main()
