# main.py

import argparse
from personalizador import layout, painel, progresso, estilo

def main():
    parser = argparse.ArgumentParser(description="Ferramenta de personalização de texto com rich.")
    parser.add_argument("texto", help="Texto ou caminho para arquivo")
    parser.add_argument("-a", "--arquivo", action="store_true", help="Se o texto for de um arquivo")
    parser.add_argument("-m", "--modulo", choices=["layout", "painel", "progresso", "estilo"], required=True, help="Escolha o módulo")
    parser.add_argument("-f", "--funcao", choices=["exibir_layout", "exibir_layout_simples", "exibir_painel", "exibir_painel_com_estilo", "mostrar_progresso", "mostrar_progresso_detalhado", "exibir_com_estilo", "exibir_com_estilo_advanced"], required=True, help="Escolha a função do módulo")
    
    args = parser.parse_args()

    if args.modulo == "layout":
        if args.funcao == "exibir_layout":
            layout.exibir_layout(args.texto, args.arquivo)
        elif args.funcao == "exibir_layout_simples":
            layout.exibir_layout_simples(args.texto, args.arquivo)
    elif args.modulo == "painel":
        if args.funcao == "exibir_painel":
            painel.exibir_painel(args.texto, args.arquivo)
        elif args.funcao == "exibir_painel_com_estilo":
            painel.exibir_painel_com_estilo(args.texto, args.arquivo)
    elif args.modulo == "progresso":
        if args.funcao == "mostrar_progresso":
            progresso.mostrar_progresso(args.texto, args.arquivo)
        elif args.funcao == "mostrar_progresso_detalhado":
            progresso.mostrar_progresso_detalhado(args.texto, args.arquivo)
    elif args.modulo == "estilo":
        if args.funcao == "exibir_com_estilo":
            estilo.exibir_com_estilo(args.texto, args.arquivo)
        elif args.funcao == "exibir_com_estilo_advanced":
            estilo.exibir_com_estilo_advanced(args.texto, args.arquivo)

if __name__ == "__main__":
    main()
