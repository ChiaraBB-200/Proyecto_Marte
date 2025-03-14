import numpy as np
import time
import math
import random

mars_map = np.load('/Users/danteespinosa/PycharmProjects/Proyecto_Marte/Data/crater_map.IMG.npy')
nr, nc = mars_map.shape
print(f"Dimensiones del mapa: {nr} filas x {nc} columnas")

max_height_diff = 2.0
escala = 10.0174

T0 = 10.0
alpha = 0.99
max_iter = 1000


def coordenadas_a_indices(x, y, nr, escala):
    r = nr - round(y / escala)
    c = round(x / escala)
    return int(r), int(c)


def indices_a_coordenadas(r, c, nr, escala):
    x = c * escala
    y = (nr - r) * escala
    return x, y


def simulated_annealing(mars_map, start, max_height_diff, T0, alpha, max_iter):
    # Movimientos posibles en 8 direcciones
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1),
                   (-1, -1), (-1, 1), (1, -1), (1, 1)]

    current = start
    path = [current]
    T = T0

    for i in range(max_iter):
        vecinos = []
        for dx, dy in movimientos:
            vecino = (current[0] + dx, current[1] + dy)
            if 0 <= vecino[0] < mars_map.shape[0] and 0 <= vecino[1] < mars_map.shape[1]:
                if abs(mars_map[vecino] - mars_map[current]) <= max_height_diff:
                    vecinos.append(vecino)
        if not vecinos:
            break

        nuevo = random.choice(vecinos)
        current_height = mars_map[current]
        nuevo_height = mars_map[nuevo]

        if nuevo_height < current_height:
            current = nuevo
            path.append(current)
        else:
            delta = nuevo_height - current_height  # delta > 0
            prob = math.exp(-delta / T) if T > 0 else 0
            if random.random() < prob:
                current = nuevo
                path.append(current)
        # Enfriar la temperatura
        T *= alpha

    return path


start_x, start_y = 3350, 5800
start = coordenadas_a_indices(start_x, start_y, nr, escala)

start_time = time.time()
camino_sa = simulated_annealing(mars_map, start, max_height_diff, T0, alpha, max_iter)
end_time = time.time()

camino_coordenadas = [indices_a_coordenadas(r, c, nr, escala) for (r, c) in camino_sa]

altura_final = mars_map[camino_sa[-1]]

print(f"El explorador llegó a la posición (en coordenadas): {camino_coordenadas[-1]} después de {len(camino_coordenadas)} movimientos.")
print(f"Altura final: {altura_final:.2f} metros")
print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
