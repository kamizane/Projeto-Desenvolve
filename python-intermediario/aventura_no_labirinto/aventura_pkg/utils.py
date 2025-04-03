from rich.console import Console
import random

def gerar_numero(seed):
    random.seed(seed)
    return random.randint(1, 4)

def imprime_instrucoes():
    """Imprime as instruções do jogo formatadas."""
    console = Console()
    console.print("\n[bold green]Bem-vindo à Aventura no Labirinto![/]")
    console.print("Use W A S D para se mover e encontre a saída!")
    console.print("Encontrar a fruta rara (*) garante pontos extras\n")

def exibir_menu():
    """Exibe o menu principal formatado."""
    console = Console()
    console.print("[bold cyan]1.[/] Jogar")
    console.print("[bold cyan]2.[/] Instruções")
    console.print("[bold cyan]3.[/] Pontuação")
    console.print("[bold cyan]4.[/] Sair")

def existe_caminho(labirinto, inicio, objetivo):
    """Verifica se existe um caminho entre o jogador e a saída usando BFS."""
    from collections import deque

    filas = deque([inicio])
    visitados = set()

    while filas:
        x, y = filas.popleft()
        if (x, y) == objetivo:
            return True  # Existe um caminho!

        if (x, y) in visitados:
            continue
        visitados.add((x, y))

        # Movimentos possíveis (cima, baixo, esquerda, direita)
        movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in movimentos:
            novo_x, novo_y = x + dx, y + dy
            if 0 <= novo_x < len(labirinto) and 0 <= novo_y < len(labirinto[0]) and labirinto[novo_x][novo_y] != "#":
                filas.append((novo_x, novo_y))

    return False  # Se esgotou as opções e não encontrou o objetivo
