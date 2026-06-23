TAMANHO = 10
NAVIOS = [3, 2, 1]

def cor_jogador(jogador):
    if jogador == 1:
        return "\033[91m"
    else:
        return "\033[94m"

def reset_cor():
    return "\033[0m"

def criar_tabuleiro():
    return [["~"] * TAMANHO for _ in range(TAMANHO)]

def limpar_tela():
    print("\n" * 50)

def celula_visivel(celula, esconder_navios=False):
    if esconder_navios and celula == "N":
        return "~"
    return celula


def formatar_celula(celula, jogador):
    if celula == "~":
        return celula
    if jogador is not None:
        return f"{cor_jogador(jogador)}{celula}{reset_cor()}"
    return celula


def formatar_texto(texto, jogador):
    if jogador is not None:
        return f"{cor_jogador(jogador)}{texto}{reset_cor()}"
    return texto


def mostrar_tabuleiro(tabuleiro, esconder_navios=False, jogador=None):
    colunas = " ".join(formatar_texto(str(col), jogador) for col in range(TAMANHO))
    print("    " + colunas)
    for linha in range(TAMANHO):
        celulas = []
        for coluna in range(TAMANHO):
            celula = tabuleiro[linha][coluna]
            celulas.append(formatar_celula(celula_visivel(celula, esconder_navios), jogador))
        print(formatar_texto(f"{linha:2}", jogador) + "  " + " ".join(celulas))


def ler_inteiro(mensagem, minimo, maximo):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
        except ValueError:
            pass
        print(f"Digite um número entre {minimo} e {maximo}.")


def ler_coordenada():
    linha = ler_inteiro("Linha: ", 0, TAMANHO - 1)
    coluna = ler_inteiro("Coluna: ", 0, TAMANHO - 1)
    return linha, coluna


def posicao_valida(tabuleiro, linha, coluna, tamanho, horizontal):
    if horizontal:
        if coluna + tamanho > TAMANHO:
            return False
        for offset in range(tamanho):
            if tabuleiro[linha][coluna + offset] != "~":
                return False
    else:
        if linha + tamanho > TAMANHO:
            return False
        for offset in range(tamanho):
            if tabuleiro[linha + offset][coluna] != "~":
                return False
    return True


def colocar_navio(tabuleiro, linha, coluna, tamanho, horizontal):
    if horizontal:
        for offset in range(tamanho):
            tabuleiro[linha][coluna + offset] = "N"
    else:
        for offset in range(tamanho):
            tabuleiro[linha + offset][coluna] = "N"


def ler_orientacao():
    while True:
        orientacao = input("Orientação (H=horizontal, V=vertical): ").strip().upper()
        if orientacao in ("H", "V"):
            return orientacao == "H"
        print("Digite H ou V.")


def posicionar_navios(jogador, tabuleiro):
    limpar_tela()
    cor = cor_jogador(jogador)
    reset = reset_cor()
    print(f"=== {cor}Jogador {jogador}{reset}: posicione seus navios ===")
    print("Navios: tamanhos 3, 2 e 1")
    print(f"Legenda: ~=água  {cor}N{reset}=navio\n")

    for tamanho in NAVIOS:
        while True:
            mostrar_tabuleiro(tabuleiro, jogador=jogador)
            print(f"\nNavio de tamanho {tamanho}")
            linha, coluna = ler_coordenada()
            horizontal = ler_orientacao()

            if posicao_valida(tabuleiro, linha, coluna, tamanho, horizontal):
                colocar_navio(tabuleiro, linha, coluna, tamanho, horizontal)
                break

            print("Posição inválida. Tente novamente.\n")

    limpar_tela()
    print(f"{cor}Jogador {jogador}{reset}, seus navios estão prontos!")
    mostrar_tabuleiro(tabuleiro, jogador=jogador)
    input("\nPressione Enter para continuar...")


def atirar(tabuleiro, linha, coluna):
    celula = tabuleiro[linha][coluna]
    if celula in ("X", "O"):
        return "ja_atirou"
    if celula == "N":
        tabuleiro[linha][coluna] = "X"
        return "acertou"
    tabuleiro[linha][coluna] = "O"
    return "errou"


def todos_navios_afundados(tabuleiro):
    for linha in tabuleiro:
        for celula in linha:
            if celula == "N":
                return False
    return True


def turno_ataque(atacante, defensor, tabuleiro_alvo):
    limpar_tela()
    cor_atacante = cor_jogador(atacante)
    cor_defensor = cor_jogador(defensor)
    reset = reset_cor()
    print(f"=== Turno do {cor_atacante}Jogador {atacante}{reset} ===")
    print(f"Tabuleiro do {cor_defensor}Jogador {defensor}{reset} (navios ocultos):")
    print(f"Legenda: ~=não atirou  {cor_defensor}X{reset}=acertou  O=errou\n")
    mostrar_tabuleiro(tabuleiro_alvo, esconder_navios=True, jogador=defensor)

    while True:
        print("\nEscolha onde atirar:")
        linha, coluna = ler_coordenada()
        resultado = atirar(tabuleiro_alvo, linha, coluna)

        if resultado == "ja_atirou":
            print("Você já atirou nessa posição. Tente outra.")
            continue

        if resultado == "acertou":
            print(f"{cor_defensor}Acertou!{reset}")
        else:
            print("Errou!")

        input("\nPressione Enter para passar a vez...")
        return resultado


def jogar():
    print("=== BATALHA NAVAL ===")
    print("Dois jogadores, mesmo computador.")
    print("Coordenadas de 0 a 9.\n")
    input("Pressione Enter para começar...")

    tabuleiro_j1 = criar_tabuleiro()
    tabuleiro_j2 = criar_tabuleiro()

    posicionar_navios(1, tabuleiro_j1)
    posicionar_navios(2, tabuleiro_j2)

    jogador_atual = 1

    while True:
        if jogador_atual == 1:
            turno_ataque(1, 2, tabuleiro_j2)
            if todos_navios_afundados(tabuleiro_j2):
                limpar_tela()
                cor = cor_jogador(1)
                reset = reset_cor()
                print(f"{cor}Jogador 1{reset} venceu! Todos os navios do Jogador 2 foram afundados.")
                break
            jogador_atual = 2
        else:
            turno_ataque(2, 1, tabuleiro_j1)
            if todos_navios_afundados(tabuleiro_j1):
                limpar_tela()
                cor = cor_jogador(2)
                reset = reset_cor()
                print(f"{cor}Jogador 2{reset} venceu! Todos os navios do Jogador 1 foram afundados.")
                break
            jogador_atual = 1


def main():
    jogar()


if __name__ == "__main__":
    main()
