import random
import heapq
import time
import csv
from collections import deque
import statistics

# =========================================================
# CONFIGURACIÓN
# =========================================================
SIZE = 100
P = 0.92
MAX_PASOS = 1000
REPETICIONES = 30

# =========================================================
# ENTORNO
# =========================================================
def generar_entorno(size=SIZE, p=P, seed=None):
    if seed is not None:
        random.seed(seed)

    grid = [["F" if random.random() < p else "H" for _ in range(size)] for _ in range(size)]
    sx, sy = random.randrange(size), random.randrange(size)
    gx, gy = random.randrange(size), random.randrange(size)
    while (gx, gy) == (sx, sy):
        gx, gy = random.randrange(size), random.randrange(size)

    grid[sx][sy] = "S"
    grid[gx][gy] = "G"
    return grid, (sx, sy), (gx, gy)

def obtener_vecinos(mapa, estado):
    fila, col = estado
    movimientos = {
        "UP": (fila - 1, col),
        "DOWN": (fila + 1, col),
        "LEFT": (fila, col - 1),
        "RIGHT": (fila, col + 1),
    }
    vecinos = []
    for accion, (f, c) in movimientos.items():
        if 0 <= f < len(mapa) and 0 <= c < len(mapa[0]) and mapa[f][c] != "H":
            vecinos.append(((f, c), accion))
    return vecinos

# =========================================================
# COSTOS Y HEURÍSTICA
# =========================================================
def costo_accion(accion, escenario=1):
    if escenario == 1:
        return 1
    if escenario == 2:
        return 1 if accion in ["LEFT", "RIGHT"] else 10

def calcular_costo(camino, escenario=1):
    if not camino or len(camino) < 2:
        return 0
    costo = 0
    for (x1, y1), (x2, y2) in zip(camino[:-1], camino[1:]):
        if x1 == x2:
            costo += 1  # movimiento horizontal
        else:
            costo += 10 if escenario == 2 else 1
    return costo

def heuristica(nodo, objetivo, escenario=1):
    dx = abs(nodo[0] - objetivo[0])
    dy = abs(nodo[1] - objetivo[1])
    if escenario == 1:
        return dx + dy
    if escenario == 2:
        return dx * 10 + dy * 1

# =========================================================
# ALGORITMOS
# =========================================================
def reconstruir_camino(padres, objetivo):
    camino = []
    estado = objetivo
    while estado is not None:
        camino.append(estado)
        estado = padres.get(estado, None)
    return list(reversed(camino))

def busqueda_aleatoria(mapa, inicio, objetivo, escenario):
    camino = [inicio]
    estado = inicio
    explorados = 0
    for _ in range(MAX_PASOS):
        if estado == objetivo:
            return camino, calcular_costo(camino, escenario), explorados
        vecinos = [v for v, _ in obtener_vecinos(mapa, estado)]
        if not vecinos:
            break
        estado = random.choice(vecinos)
        camino.append(estado)
        explorados += 1
    return None, None, explorados

def bfs(mapa, inicio, objetivo, escenario):
    cola = deque([inicio])
    padres = {inicio: None}
    explorados = 0
    while cola:
        estado = cola.popleft()
        explorados += 1
        if estado == objetivo:
            camino = reconstruir_camino(padres, objetivo)
            return camino, calcular_costo(camino, escenario), explorados
        for vecino, _ in obtener_vecinos(mapa, estado):
            if vecino not in padres:
                padres[vecino] = estado
                cola.append(vecino)
    return None, None, explorados

def dfs(mapa, inicio, objetivo, escenario, limite=None):
    pila = [(inicio, 0)]
    padres = {inicio: None}
    explorados = 0
    while pila:
        estado, prof = pila.pop()
        explorados += 1
        if estado == objetivo:
            camino = reconstruir_camino(padres, objetivo)
            return camino, calcular_costo(camino, escenario), explorados
        if limite is not None and prof >= limite:
            continue
        for vecino, _ in obtener_vecinos(mapa, estado):
            if vecino not in padres:
                padres[vecino] = estado
                pila.append((vecino, prof + 1))
    return None, None, explorados

def ucs(mapa, inicio, objetivo, escenario):
    frontera = [(0, inicio)]
    padres = {inicio: None}
    costos = {inicio: 0}
    explorados = 0
    while frontera:
        costo, estado = heapq.heappop(frontera)
        explorados += 1
        if estado == objetivo:
            camino = reconstruir_camino(padres, objetivo)
            return camino, costo, explorados
        for vecino, accion in obtener_vecinos(mapa, estado):
            nuevo_costo = costo + costo_accion(accion, escenario)
            if vecino not in costos or nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                padres[vecino] = estado
                heapq.heappush(frontera, (nuevo_costo, vecino))
    return None, None, explorados

def a_star(mapa, inicio, objetivo, escenario):
    frontera = [(heuristica(inicio, objetivo, escenario), 0, inicio)]
    padres = {inicio: None}
    costos = {inicio: 0}
    explorados = 0
    while frontera:
        f, g, estado = heapq.heappop(frontera)
        explorados += 1
        if estado == objetivo:
            camino = reconstruir_camino(padres, objetivo)
            return camino, g, explorados
        for vecino, accion in obtener_vecinos(mapa, estado):
            nuevo_g = g + costo_accion(accion, escenario)
            if vecino not in costos or nuevo_g < costos[vecino]:
                costos[vecino] = nuevo_g
                padres[vecino] = estado
                f = nuevo_g + heuristica(vecino, objetivo, escenario)
                heapq.heappush(frontera, (f, nuevo_g, vecino))
    return None, None, explorados

# =========================================================
# EXPERIMENTOS
# =========================================================
def correr_experimentos():
    algoritmos = {
        "Aleatoria": busqueda_aleatoria,
        "BFS": bfs,
        "DFS": lambda m, i, g, e: dfs(m, i, g, e),
        "DFS50": lambda m, i, g, e: dfs(m, i, g, e, 50),
        "DFS75": lambda m, i, g, e: dfs(m, i, g, e, 75),
        "DFS100": lambda m, i, g, e: dfs(m, i, g, e, 100),
        "UCS": ucs,
        "A_star": a_star,
    }

    resultados = {alg: [] for alg in algoritmos}

    for run in range(REPETICIONES):
        seed = run
        mapa, inicio, objetivo = generar_entorno(SIZE, P, seed)

        for escenario in [1, 2]:
            for nombre, funcion in algoritmos.items():
                inicio_t = time.time()
                camino, costo, explorados = funcion(mapa, inicio, objetivo, escenario)
                fin_t = time.time()
                tiempo = fin_t - inicio_t
                pasos = len(camino) if camino else 0
                resultados[nombre].append([
                    run + 1, escenario, len(mapa), P,
                    1 if camino else 0,
                    explorados, pasos, costo if costo else 0,
                    tiempo,
                    camino if camino else []
                ])

    # Guardar CSVs
    for nombre, datos in resultados.items():
        with open(f"{nombre}_resultados.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Run", "Escenario", "Tamano", "Probabilidad",
                "Exito", "Explorados", "Pasos", "Costo", "Tiempo", "Camino"
            ])
            writer.writerows(datos)

# =========================================================
# MAIN
# =========================================================

correr_experimentos()
print("✅ Experimentos completados. Archivos CSV generados.")

