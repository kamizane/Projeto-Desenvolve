import argparse
from aventura_pkg.labirinto import criar_labirinto, imprimir_labirinto
from aventura_pkg.jogador import iniciar_jogador, mover, pontuar, mostrar_pontuacao
from aventura_pkg.utils import imprime_instrucoes, exibir_menu
import random

def main():
    parser = argparse.ArgumentParser(description="Aventura no Labirinto")
    parser.add_argument("--name", type=str, required=True, help="Nome do jogador")
    parser.add_argument("--color", type=str, help="Cor do texto no terminal")
    args = parser.parse_args()

    print(f"Bem-vindo, {args.name}!")
    jogador = iniciar_jogador()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")
        match opcao:
            case "1":
                seed = random.randint(0,5)
                labirinto = criar_labirinto(seed)
                

                imprimir_labirinto(labirinto, jogador["andou"])

                # 🔄 LOOP DO JOGO: Aguarda comandos de movimento até o jogador vencer/sair
                while True:
                    direcao = input("Digite W/A/S/D para mover ou Q para sair: ").lower()

                    if direcao == "q":
                        print("Você saiu do jogo.")
                        break

                    mover(jogador, labirinto, direcao)  # Movimenta o jogador
                    imprimir_labirinto(labirinto, jogador["andou"])  # Atualiza o labirinto
                    if (jogador["posicao"] == (1,9) and (seed == 1 or seed == 5)):  # Verifica se coletou a fruta
                        pontuar(jogador, 1)
                    if (jogador["posicao"] == (3,3) and seed == 2):   # Verifica se coletou a fruta
                        pontuar(jogador, 1)
                    if (jogador["posicao"] == (7,9) and seed == 3):  # Verifica se coletou a fruta
                        pontuar(jogador, 1)
                    if (jogador["posicao"] == (9,1) and (seed == 4 or seed == 5)):  # Verifica se coletou a fruta
                        pontuar(jogador, 1) # Verifica vitória
                    if jogador["posicao"] == jogador["objetivo"]:  # Verifica vitória
                        pontuar(jogador, 0)
                        print("🎉 Parabéns! Você saiu do labirinto! 🎉")
                        break

            case "2":
                imprime_instrucoes()
            case "3":
                mostrar_pontuacao(jogador)
            case "4":
                print("Saindo do jogo...")
                break
            case _:
                print("Opção inválida!")

if __name__ == "__main__":
    main()
