from pynput import keyboard
from rich.console import Console

def iniciar_jogador():
    return {
        "posicao": (1, 1),  # Posição inicial do jogador
        "objetivo": (10, 10),  # Defina a posição de saída do labirinto
        "pontos" : 0,
        "andou" : 0

    }
def mover(jogador, labirinto, direcao):
    x, y = jogador["posicao"]

    if direcao == "w":
        novo_x, novo_y = x - 1, y
    elif direcao == "s":
        novo_x, novo_y = x + 1, y
    elif direcao == "a":
        novo_x, novo_y = x, y - 1
    elif direcao == "d":
        novo_x, novo_y = x, y + 1
    else:
        print("Comando inválido!")
        return
    

    # Verifica se a nova posição está dentro dos limites do labirinto
    if 0 <= novo_x < len(labirinto) and 0 <= novo_y < len(labirinto[0]):
        if labirinto[novo_x][novo_y] != "#":  # Se não for parede, move o jogador
            jogador["posicao"] = (novo_x, novo_y)
            labirinto[x][y] = " "  # Limpa a posição antiga
            jogador["andou"] = 1
            labirinto[novo_x][novo_y] = "P"  # Atualiza a nova posição do jogador

        else:
            print("Movimento inválido! Há uma parede.")
    else:
        print("Movimento inválido! Fora dos limites do labirinto.")


def pontuar(jogador, flag):
    #Atualiza a pontuação do jogador.
    if (flag == 1):
        jogador['pontos'] += 25 # Ganha pontos ao coletar a fruta(*)
    else:
        jogador['pontos'] += 100  # Ganha pontos ao chegar na saída

def mostrar_pontuacao(jogador):
    console = Console()
    console.print(f"Pontuação total: {jogador['pontos']}")
