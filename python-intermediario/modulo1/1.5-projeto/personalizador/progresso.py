# personalizador/progresso.py

from rich.progress import Progress
from rich.console import Console

def mostrar_progresso(texto: str, isArquivo: bool):
    """
    Exibe uma barra de progresso com base no texto fornecido.

    :param texto: Texto a ser exibido.
    :param isArquivo: Se for True, o texto será lido de um arquivo.
    """
    if isArquivo:
        with open(texto, 'r') as file:
            texto = file.read()

    console = Console()
    with Progress() as progress:
        task = progress.add_task("[cyan]Processando...", total=100)
        while not progress.finished:
            progress.update(task, advance=1)
            console.print(texto)

def mostrar_progresso_detalhado(texto: str, isArquivo: bool):
    """
    Exibe uma barra de progresso com detalhes sobre o progresso.

    :param texto: Texto a ser exibido.
    :param isArquivo: Se for True, o texto será lido de um arquivo.
    """
    if isArquivo:
        with open(texto, 'r') as file:
            texto = file.read()

    console = Console()
    with Progress() as progress:
        task = progress.add_task("[green]Carregando...", total=200)
        while not progress.finished:
            progress.update(task, advance=2)
            console.print(texto)
