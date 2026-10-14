METODOS = ("manual", "mecanica")

LIMITES_PADRAO = {"manual": 5.0, "mecanica": 15.0}


def calcular_perda(estimada, colhida):
    return (estimada - colhida) / estimada * 100


def calcular_prejuizo(estimada, colhida, preco):
    return (estimada - colhida) * preco


def calcular_produtividade(colhida, area):
    return colhida / area


def classificar(perda, limite):
    if perda <= limite:
        return "OK"
    if perda <= limite * 1.5:
        return "ATENCAO"
    return "CRITICO"


def prejuizo_evitavel(lote, limites):
    perda = calcular_perda(lote["estimada"], lote["colhida"])
    excesso = max(0.0, perda - limites[lote["metodo"]])
    return excesso / 100 * lote["estimada"] * lote["preco"]


def analisar_lote(lote, limites):
    perda = calcular_perda(lote["estimada"], lote["colhida"])
    limite = limites[lote["metodo"]]
    return {
        "perda": perda,
        "limite": limite,
        "status": classificar(perda, limite),
        "prejuizo": calcular_prejuizo(lote["estimada"], lote["colhida"], lote["preco"]),
        "evitavel": prejuizo_evitavel(lote, limites),
        "produtividade": calcular_produtividade(lote["colhida"], lote["area"]),
    }


def resumir(lotes, limites):
    resumo = {"prejuizo": 0.0, "evitavel": 0.0, "por_metodo": {}, "pior": None}
    maior_perda = -1.0
    for lote in lotes:
        analise = analisar_lote(lote, limites)
        resumo["prejuizo"] += analise["prejuizo"]
        resumo["evitavel"] += analise["evitavel"]
        grupo = resumo["por_metodo"].setdefault(lote["metodo"], [])
        grupo.append(analise["perda"])
        if analise["perda"] > maior_perda:
            maior_perda = analise["perda"]
            resumo["pior"] = lote
    resumo["media_metodo"] = {m: sum(p) / len(p) for m, p in resumo["por_metodo"].items()}
    return resumo


def recomendar(lote, analise):
    if analise["status"] == "OK":
        return "Perda dentro do limite. Manter o manejo atual."
    if lote["metodo"] == "mecanica":
        return "Regular a colhedora (velocidade e altura) e revisar o momento da colheita."
    return "Revisar o ponto de maturacao e o treinamento da equipe de colheita."
