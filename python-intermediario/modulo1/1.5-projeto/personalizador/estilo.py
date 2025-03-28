# personalizador/estilo.py

from rich.console import Console
from rich.style import Style

def exibir_com_estilo(texto: str, isArquivo: bool):
    """
    Exibe o texto com um estilo simples.

    :param texto: Texto a ser exibido.
    :param isArquivo: Se for True, o texto será lido de um arquivo.
    """
    if isArquivo:
        with open(texto, 'r') as file:
            texto = file.read()

    console = Console()
    estilo = Style(color="red", bold=True)
    console.print(texto, style=estilo)

def exibir_com_estilo_advanced(texto: str, isArquivo: bool):
    """
    Exibe o texto com estilo avançado.

    :param texto: Texto a ser exibido.
    :param isArquivo: Se for True, o texto será lido de um arquivo.
    """
    if isArquivo:
        with open(texto, 'r') as file:
            texto = file.read()

    console = Console()
    estilo = Style(color="yellow", underline=True, blink=True)
    console.print(texto, style=estilo)
