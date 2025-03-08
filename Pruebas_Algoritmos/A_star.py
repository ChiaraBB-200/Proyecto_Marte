import numpy as np
import heapq

mars_map = np.load('data/mars_map.npy')
nr, nc = mars_map.shape
print(f"Dimensiones del mapa: {nr} filas x {nc} columnas")
# Coordenadas en metros (Dadas en la actividad)
start_x, start_y = 2850, 6400 
goal_x, goal_y = 3150, 6800

# Coordenadas a índices
def coordenadas_a_indices(x, y, nr, escala):
    r = nr - round(y / escala)
    c = round(x / escala)
    return int(r), int(c)

escala = 10.0174  # Escala en metros por píxel
start = coordenadas_a_indices(start_x, start_y, nr, escala)
goal = coordenadas_a_indices(goal_x, goal_y, nr, escala)

print(f"Punto de inicio: {start}, Punto de fin: {goal}")

def a_star(mars_map, start, goal, max_height_diff):
    def heuristic(a, b):
        return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < nr and 0 <= neighbor[1] < nc:
                height_diff = abs(mars_map[neighbor] - mars_map[current])
                if mars_map[neighbor] == -1 or height_diff > max_height_diff:
                    continue

                tentative_g_score = g_score[current] + np.sqrt(dx**2 + dy**2)

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))

    return None

max_height_diff = 0.25  # Diferencia máxima de altura permitida
path_a_star = a_star(mars_map, start, goal, max_height_diff)
if path_a_star:
    print(f"Ruta encontrada por A*: {path_a_star}")
else:
    print("No se encontró una ruta válida con A*.")

def calcular_distancia_recorrida(path, escala):
    distancia = 0
    for i in range(1, len(path)):
        dx = (path[i][1] - path[i-1][1]) * escala
        dy = (path[i][0] - path[i-1][0]) * escala
        distancia += np.sqrt(dx**2 + dy**2)
    return distancia

if path_a_star:
    distancia = calcular_distancia_recorrida(path_a_star, escala)
    print(f"Distancia recorrida por A*: {distancia:.2f} metros")
    