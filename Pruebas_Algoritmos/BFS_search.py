import numpy as np
from collections import deque

# Cargar el mapa de alturas
mars_map = np.load('data/mars_map.npy')
nr, nc = mars_map.shape
print(f"Dimensiones del mapa: {nr} filas x {nc} columnas")

# Coordenadas en metros (Dadas en la actividad)
start_x, start_y = 2850, 6400
goal_x, goal_y = 3150, 6800

max_height_diff = 0.25  # Diferencia máxima de altura permitida

# Coordenadas a índices
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
        dx = (path[i][1] - path[i-1][1]) * escala
        dy = (path[i][0] - path[i-1][0]) * escala
        distancia += np.sqrt(dx**2 + dy**2)
    return distancia

# Algoritmo BFS
def bfs(mars_map, start, goal, max_height_diff):
    # Definir movimientos posibles (8 direcciones)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    # Inicializar cola para BFS
    cola = deque()
    cola.append(start)

    # Diccionario para registrar el camino
    came_from = {start: None}

    # Bucle principal de BFS
    while cola:
        current = cola.popleft()

        # Si llegamos al objetivo, reconstruir el camino
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Invertir el camino para que vaya de inicio a fin

        # Explorar vecinos
        for dx, dy in movimientos:
            neighbor = (current[0] + dx, current[1] + dy)

            # Verificar si el vecino está dentro de los límites del mapa
            if 0 <= neighbor[0] < mars_map.shape[0] and 0 <= neighbor[1] < mars_map.shape[1]:
                # Verificar si el vecino es válido (altura != -1) y cumple con la diferencia de altura
                if mars_map[neighbor] != -1 and abs(mars_map[neighbor] - mars_map[current]) <= max_height_diff:
                    # Si el vecino no ha sido visitado, agregarlo a la cola
                    if neighbor not in came_from:
                        cola.append(neighbor)
                        came_from[neighbor] = current

    # Si no se encuentra una ruta, retornar None
    return None

# Ejecutar BFS
path_bfs = bfs(mars_map, start, goal, max_height_diff)

# Mostrar resultados
if path_bfs:
    print(f"Ruta encontrada por BFS: {path_bfs}")
    distancia = calcular_distancia_recorrida(path_bfs, escala)
    print(f"Distancia recorrida por BFS: {distancia:.2f} metros")
else:
    print("No se encontró una ruta válida con BFS.")