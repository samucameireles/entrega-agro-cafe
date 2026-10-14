import arquivos
import banco
from calculos import METODOS, analisar_lote, recomendar, resumir
from validacao import ler_decimal, ler_opcao, ler_texto

MENU = """
==== CONTROLE DE PERDAS NA COLHEITA DE CAFE ====
1 - Registrar colheita
2 - Listar colheitas
3 - Analisar perdas
4 - Gerar relatorio (TXT)
5 - Enviar dados para o Oracle
6 - Carregar dados do Oracle
0 - Sair
"""


def proximo_id(lotes):
    return max((lote["id"] for lote in lotes), default=0) + 1


def registrar(lotes):
    print("\n-- Nova colheita --")
    talhao = ler_texto("Talhao (nome ou codigo): ")
    metodo = ler_opcao(f"Metodo de colheita ({'/'.join(METODOS)}): ", METODOS)
    area = ler_decimal("Area colhida em hectares: ")
    estimada = ler_decimal("Producao estimada em sacas de 60 kg: ")
    colhida = ler_decimal("Producao efetivamente colhida em sacas: ", maximo=estimada, permite_minimo=True)
    preco = ler_decimal("Preco da saca em R$: ")
    lote = {
        "id": proximo_id(lotes), "talhao": talhao, "metodo": metodo,
        "area": area, "estimada": estimada, "colhida": colhida, "preco": preco,
    }
    lotes.append(lote)
    arquivos.salvar_lotes(lotes)
    print(f"Colheita {lote['id']} registrada.")


def listar(lotes, limites):
    if not lotes:
        print("\nNenhuma colheita registrada.")
        return
    print(f"\n{'ID':<4}{'Talhao':<14}{'Metodo':<10}{'Estimada':>10}{'Colhida':>10}{'Perda':>9}  Status")
    print("-" * 66)
    for lote in lotes:
        a = analisar_lote(lote, limites)
        print(
            f"{lote['id']:<4}{lote['talhao']:<14}{lote['metodo']:<10}"
            f"{lote['estimada']:>10.1f}{lote['colhida']:>10.1f}{a['perda']:>8.1f}%  {a['status']}"
        )


def analisar(lotes, limites):
    if not lotes:
        print("\nNenhuma colheita registrada.")
        return
    print()
    for lote in lotes:
        a = analisar_lote(lote, limites)
        print(f"Talhao {lote['talhao']} ({lote['metodo']})")
        print(f"  Perda: {a['perda']:.1f}% (limite {a['limite']:.0f}%) - {a['status']}")
        print(f"  Produtividade: {a['produtividade']:.1f} sacas/ha")
        print(f"  Prejuizo: {arquivos.moeda(a['prejuizo'])}  |  Evitavel: {arquivos.moeda(a['evitavel'])}")
        print(f"  Recomendacao: {recomendar(lote, a)}")
    r = resumir(lotes, limites)
    print("\n-- Resumo --")
    print(f"Prejuizo total: {arquivos.moeda(r['prejuizo'])}")
    print(f"Prejuizo evitavel: {arquivos.moeda(r['evitavel'])}")
    for metodo, media in r["media_metodo"].items():
        print(f"Perda media ({metodo}): {media:.1f}%")
    pior = r["pior"]
    print(f"Maior perda: talhao {pior['talhao']}")


def sincronizar_envio(lotes):
    if not lotes:
        print("\nNada para enviar.")
        return
    try:
        total = banco.enviar_lotes(lotes)
        print(f"{total} registro(s) enviado(s) ao Oracle.")
    except Exception as erro:
        print(f"Nao foi possivel usar o Oracle: {erro}")


def sincronizar_carga(lotes):
    try:
        recebidos = banco.buscar_lotes()
    except Exception as erro:
        print(f"Nao foi possivel usar o Oracle: {erro}")
        return lotes
    arquivos.salvar_lotes(recebidos)
    print(f"{len(recebidos)} registro(s) carregado(s) do Oracle.")
    return recebidos


def main():
    lotes = arquivos.carregar_lotes()
    limites = arquivos.carregar_limites()
    while True:
        print(MENU)
        opcao = ler_opcao("Escolha: ", ("0", "1", "2", "3", "4", "5", "6"))
        if opcao == "1":
            registrar(lotes)
        elif opcao == "2":
            listar(lotes, limites)
        elif opcao == "3":
            analisar(lotes, limites)
        elif opcao == "4":
            if lotes:
                print("Relatorio salvo em", arquivos.gerar_relatorio(lotes, limites))
            else:
                print("\nNenhuma colheita registrada.")
        elif opcao == "5":
            sincronizar_envio(lotes)
        elif opcao == "6":
            lotes = sincronizar_carga(lotes)
        else:
            print("Ate logo.")
            break


if __name__ == "__main__":
    main()
