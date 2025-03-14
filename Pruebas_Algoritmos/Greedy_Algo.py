import numpy as np
import heapq
import time

# Cargar el mapa de alturas
mars_map = np.load('/Users/danteespinosa/PycharmProjects/Proyecto_Marte/Data/mars_map.npy')
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
        dx = (path[i][1] - path[i - 1][1]) * escala
        dy = (path[i][0] - path[i - 1][0]) * escala
        distancia += np.sqrt(dx ** 2 + dy ** 2)
    return distancia


# Algoritmo de búsqueda Greedy (mejor primero)
def greedy_search(mars_map, start, goal, max_height_diff):
    # Definir movimientos posibles (8 direcciones)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    # Función heurística: distancia Euclidiana desde el nodo actual al objetivo
    def heuristic(node):
        dx = node[0] - goal[0]
        dy = node[1] - goal[1]
        return np.sqrt(dx ** 2 + dy ** 2)

    # Inicializar la cola de prioridad con el nodo inicial
    open_set = []
    heapq.heappush(open_set, (heuristic(start), start))

    # Diccionario para reconstruir el camino
    came_from = {start: None}

    while open_set:
        current_priority, current = heapq.heappop(open_set)

        # Verificar si hemos alcanzado el objetivo
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Invertir el camino para obtenerlo de inicio a fin

        # Explorar los vecinos
        for dx, dy in movimientos:
            neighbor = (current[0] + dx, current[1] + dy)

            # Verificar que el vecino esté dentro de los límites del mapa
            if 0 <= neighbor[0] < mars_map.shape[0] and 0 <= neighbor[1] < mars_map.shape[1]:
                # Verificar que el vecino sea válido y cumpla con la diferencia de altura
                if mars_map[neighbor] != -1 and abs(mars_map[neighbor] - mars_map[current]) <= max_height_diff:
                    if neighbor not in came_from:
                        came_from[neighbor] = current
                        priority = heuristic(neighbor)
                        heapq.heappush(open_set, (priority, neighbor))

    # Si no se encuentra una ruta, retornar None
    return None


# Ejecutar Greedy Search
start_time = time.time()
path_greedy = greedy_search(mars_map, start, goal, max_height_diff)
end_time = time.time()
total_time = end_time - start_time

# Mostrar resultados
if path_greedy:
    print(f"Ruta encontrada por Greedy Search: {path_greedy}")
    distancia = calcular_distancia_recorrida(path_greedy, escala)
    print(f"Distancia recorrida por Greedy Search: {distancia:.2f} metros")
    print(f"El tiempo de ejecución del algoritmo fue: {total_time:.2f} segundos")
else:
    print("No se encontró una ruta válida con Greedy Search.")
