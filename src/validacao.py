def ler_texto(mensagem, maximo=30):
    while True:
        valor = input(mensagem).strip()
        if not valor:
            print("  Campo obrigatorio.")
        elif len(valor) > maximo:
            print(f"  Use no maximo {maximo} caracteres.")
        else:
            return valor


def ler_decimal(mensagem, minimo=0.0, maximo=None, permite_minimo=False):
    while True:
        bruto = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(bruto)
        except ValueError:
            print("  Digite um numero valido (ex: 12.5).")
            continue
        if valor < minimo or (valor == minimo and not permite_minimo):
            print(f"  O valor deve ser maior que {minimo:g}.")
        elif maximo is not None and valor > maximo:
            print(f"  O valor nao pode passar de {maximo:g}.")
        else:
            return valor


def ler_opcao(mensagem, opcoes):
    while True:
        valor = input(mensagem).strip().lower()
        if valor in opcoes:
            return valor
        print("  Opcao invalida. Escolha entre: " + ", ".join(opcoes))
