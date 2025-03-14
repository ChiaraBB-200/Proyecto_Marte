import numpy as np
import time
import sys

sys.setrecursionlimit(1000000)

# Cargar el mapa de alturas
mars_map = np.load('/Users/danteespinosa/PycharmProjects/Proyecto_Marte/Data/mars_map.npy')
nr, nc = mars_map.shape
print(f"Dimensiones del mapa: {nr} filas x {nc} columnas")

# Coordenadas en metros (Dadas en la actividad)
start_x, start_y = 2850, 6400
goal_x, goal_y = 3150, 6800
max_height_diff = 0.25  # Diferencia máxima de altura permitida


# Función para convertir coordenadas a índices
def coordenadas_a_indices(x, y, nr, escala):
    r = nr - round(y / escala)
    c = round(x / escala)
    return int(r), int(c)


escala = 10.0174  # Escala en metros por píxel
start = coordenadas_a_indices(start_x, start_y, nr, escala)
goal = coordenadas_a_indices(goal_x, goal_y, nr, escala)


# Función para calcular la distancia recorrida
def calcular_distancia_recorrida(path, escala):
    distancia = 0
    for i in range(1, len(path)):
        dx = (path[i][1] - path[i - 1][1]) * escala
        dy = (path[i][0] - path[i - 1][0]) * escala
        distancia += np.sqrt(dx ** 2 + dy ** 2)
    return distancia


# Algoritmo DFS recursivo
def dfs(mars_map, current, goal, max_height_diff, visited, came_from):
    if current == goal:
        return True
    visited.add(current)

    # Movimientos posibles (8 direcciones)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1),
                   (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dx, dy in movimientos:
        neighbor = (current[0] + dx, current[1] + dy)

        if 0 <= neighbor[0] < mars_map.shape[0] and 0 <= neighbor[1] < mars_map.shape[1]:
            if mars_map[neighbor] != -1 and abs(mars_map[neighbor] - mars_map[current]) <= max_height_diff:
                if neighbor not in visited:
                    came_from[neighbor] = current
                    if dfs(mars_map, neighbor, goal, max_height_diff, visited, came_from):
                        return True
    return False


visited = set()
came_from = {start: None}

# Ejecutar DFS
start_time = time.time()
encontrado = dfs(mars_map, start, goal, max_height_diff, visited, came_from)
end_time = time.time()
total_time = end_time - start_time

# Reconstruir y mostrar el camino si se encontró una ruta
if encontrado:
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path = path[::-1]

    print(f"Ruta encontrada por DFS: {path}")
    distancia = calcular_distancia_recorrida(path, escala)
    print(f"Distancia recorrida por DFS: {distancia:.2f} metros")
    print(f"Tiempo de ejecución del algoritmo DFS: {total_time:.2f} segundos")
else:
    print("No se encontró una ruta válida con DFS.")
