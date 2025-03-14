import numpy as np
import time

mars_map = np.load('/Users/danteespinosa/PycharmProjects/Proyecto_Marte/Data/crater_map.IMG.npy')
nr, nc = mars_map.shape
print(f"Dimensiones del mapa: {nr} filas x {nc} columnas")

max_height_diff = 2  # Diferencia máxima de altura permitida en metros
escala = 10.045  # Escala en metros por píxel


def coordenadas_a_indices(x, y, nr, escala):
    r = nr - round(y / escala)
    c = round(x / escala)
    return int(r), int(c)


def indices_a_coordenadas(r, c, nr, escala):
    x = c * escala
    y = (nr - r) * escala
    return x, y


def descenso_explorador(mars_map, start, max_height_diff):
    # Movimientos posibles en 8 direcciones
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1),
                   (-1, -1), (-1, 1), (1, -1), (1, 1)]

    actual = start
    camino = [actual]

    while True:
        altura_actual = mars_map[actual]
        vecinos_validos = []

        for dx, dy in movimientos:
            vecino = (actual[0] + dx, actual[1] + dy)
            if 0 <= vecino[0] < mars_map.shape[0] and 0 <= vecino[1] < mars_map.shape[1]:
                altura_vecino = mars_map[vecino]
                if (altura_vecino < altura_actual) and ((altura_actual - altura_vecino) <= max_height_diff):
                    vecinos_validos.append((altura_vecino, vecino))

        if not vecinos_validos:
            break

        vecino_elegido = min(vecinos_validos, key=lambda x: x[0])[1]

        camino.append(vecino_elegido)
        actual = vecino_elegido

    return camino


# Prueba del algoritmo en la posición dada en la tarea
start_x, start_y = 3350, 5800
start = coordenadas_a_indices(start_x, start_y, nr, escala)

start_time = time.time()
camino_descenso = descenso_explorador(mars_map, start, max_height_diff)
end_time = time.time()

camino_coordenadas = [indices_a_coordenadas(r, c, nr, escala) for (r, c) in camino_descenso]

altura_final = mars_map[camino_descenso[-1]]

print(
    f"El explorador llegó a la posición con coordenadas: {camino_coordenadas[-1]} después de {len(camino_coordenadas)} movimientos.")
print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
print(f"Altura final: {altura_final:.2f} metros")


