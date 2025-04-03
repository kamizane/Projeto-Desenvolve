import random
def criar_labirinto(seed, linhas=11, colunas=11):  # Aumentado para garantir (10,10)
    labirinto = [['#' for _ in range(colunas)] for _ in range(linhas)]
    
    inicio = (1, 1)
    fim = (10, 10)  # Agora o 'S' será colocado na posição correta
    
    def esculpir_caminho(x, y):
        direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(direcoes)
        
        for dx, dy in direcoes:
            nx, ny = x + dx * 2, y + dy * 2
            if 1 <= nx < linhas - 1 and 1 <= ny < colunas - 1 and labirinto[nx][ny] == '#':
                labirinto[x + dx][y + dy] = ' '
                labirinto[nx][ny] = ' '
                esculpir_caminho(nx, ny)
    
    labirinto[inicio[0]][inicio[1]] = ' '
    esculpir_caminho(inicio[0], inicio[1])
    
    # Garante que a saída seja acessível
    x, y = fim
    if labirinto[x-1][y] == '#' and labirinto[x][y-1] == '#':
        labirinto[x-1][y] = ' '
    
    labirinto[fim[0]][fim[1]] = 'S'

    if (seed == 1):
        labirinto[1][9] = '*'
    elif (seed == 2):
        labirinto[3][3] = '*'
    elif (seed == 3):
        labirinto[7][9] = '*'
    elif (seed == 4):
        labirinto[9][1] = '*'
    elif (seed == 5):
        labirinto[1][9] = '*'
        labirinto[9][1] = '*'
    
    return labirinto


def imprimir_labirinto(labirinto, controle):
    for i, linha in enumerate(labirinto):
        for j, celula in enumerate(linha):
            if (i, j) == (1,1) and (controle == 0):
                print('P', end=' ')
            else:
                print(celula, end=' ')
        print()
