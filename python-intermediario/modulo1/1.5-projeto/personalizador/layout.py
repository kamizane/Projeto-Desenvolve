# personalizador/layout.py

from rich.layout import Layout
from rich.console import Console

def exibir_layout(texto: str, isArquivo: bool):
    """
    Exibe o texto com formatação de layout.

    :param texto: Texto a ser exibido.
    :param isArquivo: Se for True, o texto será lido de um arquivo.
    """
    console = Console()
    layout = Layout()
    layout.split_row(Layout(name="top"), Layout(name="bottom"))
    layout["top"].update(texto)
    
    if isArquivo:
        with open(texto, 'r') as file:
            texto = file.read()
    
    layout["bottom"].update(texto)
    console.print(layout)

def exibir_layout_simples(texto: str, isArquivo: bool):
    """
    Exibe o texto de forma simples no layout.

    :param texto: Texto a ser exibido.
    :param isArquivo: Se for True, o texto será lido de um arquivo.
    """
    if isArquivo:
        with open(texto, 'r') as file:
            texto = file.read()

    console = Console()
    layout = Layout()
    layout.split_column(Layout(name="main"))
    layout["main"].update(texto)
    
    console.print(layout)
