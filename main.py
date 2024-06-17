from asignacion import metodo_hungaro, normalizar_matriz, asignacion

if __name__ == '__main__':
    with open('data.csv', 'r') as file:
        matriz = []
        for line in file.readlines():
            matriz.append(list(int(number) for number in line.strip('\n').split(';')))
    
    matriz_copy = [list(row) for row in matriz]
    normalizar_matriz(matriz)
    matriz = metodo_hungaro(matriz)
    asignacion(matriz, matriz_copy)