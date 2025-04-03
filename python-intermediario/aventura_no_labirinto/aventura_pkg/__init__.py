"""
Pacote principal do jogo Aventura no Labirinto.
"""
from .labirinto import criar_labirinto, imprimir_labirinto
from .jogador import iniciar_jogador, mover, pontuar, mostrar_pontuacao
from .utils import imprime_instrucoes, exibir_menu, existe_caminho
import random
import time

__all__ = [
    "criar_labirinto", "imprimir_labirinto",
    "iniciar_jogador", "mover", "pontuar",
    "imprime_instrucoes", "exibir_menu", "mostrar_pontuacao", "existe_caminho"
]
