import json
import os

from calculos import LIMITES_PADRAO, analisar_lote, resumir

PASTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
ARQ_LOTES = os.path.join(PASTA, "colheitas.json")
ARQ_PARAMETROS = os.path.join(PASTA, "parametros.json")
ARQ_RELATORIO = os.path.join(PASTA, "relatorio.txt")


def carregar_json(caminho, padrao):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return padrao
    except json.JSONDecodeError:
        print(f"  Arquivo {os.path.basename(caminho)} esta corrompido. Usando dados vazios.")
        return padrao


def salvar_json(caminho, dados):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)


def carregar_lotes():
    return carregar_json(ARQ_LOTES, [])


def salvar_lotes(lotes):
    salvar_json(ARQ_LOTES, lotes)


def carregar_limites():
    limites = carregar_json(ARQ_PARAMETROS, None)
    if limites is None:
        salvar_json(ARQ_PARAMETROS, LIMITES_PADRAO)
        return dict(LIMITES_PADRAO)
    return limites


def moeda(valor):
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_relatorio(lotes, limites):
    linhas = ["RELATORIO DE PERDAS NA COLHEITA DE CAFE", "=" * 60]
    for lote in lotes:
        a = analisar_lote(lote, limites)
        linhas.append(
            f"Lote {lote['id']} | Talhao {lote['talhao']} | {lote['metodo']} | "
            f"perda {a['perda']:.1f}% (limite {a['limite']:.0f}%) | {a['status']} | "
            f"prejuizo {moeda(a['prejuizo'])}"
        )
    r = resumir(lotes, limites)
    linhas.append("=" * 60)
    linhas.append(f"Prejuizo total: {moeda(r['prejuizo'])}")
    linhas.append(f"Prejuizo evitavel (acima do limite): {moeda(r['evitavel'])}")
    for metodo, media in r["media_metodo"].items():
        linhas.append(f"Perda media {metodo}: {media:.1f}%")
    with open(ARQ_RELATORIO, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(linhas) + "\n")
    return ARQ_RELATORIO
