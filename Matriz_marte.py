import numpy as np

mars_map = np.load('mars_map.npy')
nr, nc = mars_map.shape
print(f"Dimensiones del mapa: {nr} filas x {nc} columnas")

def coordenadas_a_indices(x, y, nr, escala):
    r = nr - round(y / escala)
    c = round(x / escala)
    return int(r), int(c)

# Ejemplo de uso
x, y = 1000, 2000  # Coordenadas en metros
r, c = coordenadas_a_indices(x, y, nr=1814, escala=10.0174)
print(f"Coordenadas (x, y) = ({x}, {y}) -> Índices (r, c) = ({r}, {c})")