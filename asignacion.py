from numpy import array, transpose, copy

def normalizar_matriz(matriz:list[list]) -> None:
    max_valor = 0
    for fila in matriz:
        max_valor = max(max_valor, max(fila))
    
    for fila in matriz:
        for k, valor in enumerate(fila):
            fila[k] = max_valor - valor


def restar_minimo_fila(matriz:array) -> None:
    # Buscamos el numero mas pequeño por fila y lo restamos al resto de valores
    for k, fila in enumerate(matriz):
        menor = min(fila)
        # Si el menor es 0 no hacemos nada, caso contrario remplazamos la fila por una nueva con la diferencia de valores
        if (menor != 0): matriz[k] = [valor - menor for valor in fila]


def eliminar_filas(matriz:array, coordenadas_eliminadas:list[list], intersecciones:list[list], invertir=False, cant_ceros=1) -> int:
    # Definimos una variable que sea la cantidad de eliminaciones
    cant_eliminaciones = 0

    for k, filas in enumerate(matriz):
        # Si la contiene mas ceros que lo pedido iniciamos a borrar filas
        cant_ceros_interes = 0

        # Buscamos si hay ceros que no han sido eliminados
        for j, valor in enumerate(filas):
            coordenadas = [k, j] if not invertir else [j, k]
            if coordenadas not in coordenadas_eliminadas and valor == 0:
                cant_ceros_interes += 1

        # Si la cantidad de ceros que no han sido eliminados es mayor que el requisito los eliminamos
        if cant_ceros_interes > cant_ceros:
            for j in range(len(filas)):
                coordenadas = [k, j] if not invertir else [j, k]
                # Si la coordenada creada en la iteracion existe en las eliminadas es una interseccion
                if coordenadas in coordenadas_eliminadas:
                    intersecciones.append(coordenadas)
                else:
                    coordenadas_eliminadas.append(coordenadas)
            # Agregamos las eliminaciones
            cant_eliminaciones += 1
    
    return cant_eliminaciones


def minimo_valor(matriz:array, coordenadas_eliminadas:list[list]) -> float:
    # Definimos el mayor valor posible
    menor = 999999999

    for k, filas in enumerate(matriz):
        for j, valor in enumerate(filas):
            coordenadas = [k, j]
            # Si la coordenada actual no fue eliminada y el menor guardado es mayor que el valor lo remplazamos
            if coordenadas not in coordenadas_eliminadas and menor > valor: menor = valor

    return menor


def actualizar_valores(valor:float, matriz:array, coordenadas_eliminadas:list[list], intersecciones=list[list]):
    for k, fila in enumerate(matriz):
        new_fila = []
        for j, valor_columna in enumerate(fila):
            coordenadas = [k, j]
            # Si las coordenadas estan en las intersecciones sumamos el valor
            if  coordenadas in intersecciones:
                new_fila.append(valor_columna + valor)
            
            # Si la coordenada no fue eliminada lo restamos
            elif coordenadas not in coordenadas_eliminadas:
                new_fila.append(valor_columna - valor)
            
            # Si la coordenada fue eliminada lo guardamos normal
            else:
                new_fila.append(valor_columna)
        
        matriz[k] = new_fila


def metodo_hungaro(matriz:list[list]) -> array:
    # Restamos los valores minimos a cada fila
    matriz = array(matriz)
    print(matriz)
    restar_minimo_fila(matriz=matriz)
    
    # Trasponemos la matriz y aplicamos el mismo algoritmo
    matriz = transpose(matriz)
    restar_minimo_fila(matriz=matriz)

    # Trasponemos la matriz para volver a la original
    matriz = transpose(matriz)

    # Definimos esta variable de control de ciclo
    cant_eliminaciones = 0

    while cant_eliminaciones < len(matriz[0]):
        coordenadas_eliminadas = []
        coordenadas_intersecciones = []

        # Vamos eliminando las filas por iteraciones
        cant_eliminaciones = eliminar_filas(
            matriz=matriz,
            coordenadas_eliminadas=coordenadas_eliminadas,
            intersecciones=coordenadas_intersecciones,
            invertir=False,
            cant_ceros=1
        )
        
        # Trasponemos la matriz y aplicamos lo mismo solo que cambiando el orden
        matriz = transpose(matriz)
        cant_eliminaciones += eliminar_filas(
            matriz=matriz,
            coordenadas_eliminadas=coordenadas_eliminadas,
            intersecciones=coordenadas_intersecciones,
            invertir=True,
            cant_ceros=0
        )

        # Si la cantidad de eliminaciones es mayor la longitud de la matriz paramos
        if cant_eliminaciones >= len(matriz[0]):
            matriz = transpose(matriz)
            break
        
        # Devolvemos la matriz a su estado original
        matriz = transpose(matriz)

        menor_valor = minimo_valor(matriz=matriz, coordenadas_eliminadas=coordenadas_eliminadas)

        actualizar_valores(
            valor=menor_valor,
            matriz=matriz,
            coordenadas_eliminadas=coordenadas_eliminadas,
            intersecciones=coordenadas_intersecciones
        )

    # Retornamos la matriz resultante
    return matriz


def asignacion(matriz_resultado:array, matriz_puntuaciones):
    # Creamos los indices de los trabajadores
    materias = []
    for k in range(len(matriz_resultado)):
        materias.append(f"Materia {k+1}")
    
    coordenadas_esperadas = [[k, k] for k in range(len(matriz_resultado))]

    while True:
        for k, fila in enumerate(matriz_resultado):
            cambiado = False
            for j, valor in enumerate(fila):
                if valor == 0 and  not cambiado:
                    # Intercambiamos las filas de la matriz
                    fila_aux = copy(matriz_resultado[k])
                    matriz_resultado[k] = matriz_resultado[j]
                    matriz_resultado[j] = fila_aux

                    # Intercambiamos los indices de los trabajadores
                    trabajador_aux = materias[k]
                    materias[k] = materias[j]
                    materias[j] = trabajador_aux

                    # Intercambiamos la matriz costo
                    fila_aux = matriz_puntuaciones[k]
                    matriz_puntuaciones[k] = matriz_puntuaciones[j]
                    matriz_puntuaciones[j] = fila_aux

                    # Marcamos que ya cambiamos las filas
                    cambiado = True
        
        encontradas = 0

        for coordenada in coordenadas_esperadas:
            if matriz_resultado[coordenada[0]][coordenada[1]] == 0:
                encontradas += 1
        
        if encontradas == len(matriz_resultado):
            break

        if encontradas == len(matriz_resultado) - 2:
            filas_not_zero_diagonal = []
            for k in range(matriz_resultado.shape[0]):
                if matriz_resultado[k, k] != 0:
                    filas_not_zero_diagonal.append(k)
            
            fila_aux = copy(matriz_resultado[filas_not_zero_diagonal[0]])
            fila_aux_2 = copy(matriz_resultado[filas_not_zero_diagonal[1]])

            matriz_resultado[filas_not_zero_diagonal[0]] = fila_aux_2
            matriz_resultado[filas_not_zero_diagonal[1]] = fila_aux

            trabajador_aux = materias[filas_not_zero_diagonal[0]]
            trabajador_aux_2 = materias[filas_not_zero_diagonal[1]]
            materias[filas_not_zero_diagonal[0]] = trabajador_aux_2
            materias[filas_not_zero_diagonal[1]] = trabajador_aux

            fila_aux = matriz_puntuaciones[filas_not_zero_diagonal[0]]
            fila_aux_2 = matriz_puntuaciones[filas_not_zero_diagonal[1]]
            matriz_puntuaciones[filas_not_zero_diagonal[0]] = fila_aux_2
            matriz_puntuaciones[filas_not_zero_diagonal[1]] = fila_aux
            

            break
    
    print('')
    for k, materia in enumerate(materias):
        print(f'{materia}: Profesor {k+1} - {matriz_puntuaciones[k][k]} puntos.')
