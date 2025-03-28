# personalizador/painel.py

from rich.panel import Panel
from rich.console import Console

def exibir_painel(texto: str, isArquivo: bool):
    """
    Exibe o texto em um painel.

    :param texto: Texto a ser exibido.
    :param isArquivo: Se for True, o texto será lido de um arquivo.
    """
    if isArquivo:
        with open(texto, 'r') as file:
            texto = file.read()

    console = Console()
    painel = Panel(texto, title="Painel de Texto", width=40)
    console.print(painel)

def exibir_painel_com_estilo(texto: str, isArquivo: bool):
    """
    Exibe o texto em um painel com um estilo específico.

    :param texto: Texto a ser exibido.
    :param isArquivo: Se for True, o texto será lido de um arquivo.
    """
    if isArquivo:
        with open(texto, 'r') as file:
            texto = file.read()

    console = Console()
    painel = Panel(texto, title="Painel Estilizado", style="bold blue", width=50)
    console.print(painel)
