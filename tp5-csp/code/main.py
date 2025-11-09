import time
import random
import csv
import os
from statistics import mean, stdev
import pandas as pd
import matplotlib.pyplot as plt
#funciones base (tablero.py del tp4)
# =========================================================
# ESTADOS
# =========================================================

def initialize_random_state(n: int = 8):
    """
    Initializes a random state for the N-queens problem.
    Returns a list where each index represents a column
    and the value is the row where the queen is placed.
    """
    return [random.randint(0, n - 1) for _ in range(n)]

def generate_neighbors(state):
    """
    Generates all neighboring states from the current state.
    A neighbor is a state where one queen is moved to a different
    row within its column.
    
    Args:
        state (list): List representing the queen positions.
        
    Returns:
        list: List of neighboring states.

    Para cada columna, prueba mover la reina a todas las filas distintas de la actual.
    Copia el estado actual y modifica la posición para crear un vecino nuevo.
    Devuelve una lista con todos los vecinos posibles.
    """
    n = len(state)
    neighbors = []
    
    for col in range(n):
        current_row = state[col]
        for new_row in range(n):
            if new_row != current_row:
                neighbor = state.copy()
                neighbor[col] = new_row
                neighbors.append(neighbor)
                
    return neighbors
# =========================================================
# COSTO
# =========================================================
def cost(state):
    """
    Calculates the number of pairs of queens that are attacking each other.
    
    Args:
        state (list): A list where state[i] is the row of the queen in column i.
        
    Returns:
        int: Total number of conflicting pairs.
    
    Esta función se usa para:

    Evaluar qué tan buena es una solución actual.
    Comparar varios vecinos y elegir el de menor costo.
    Saber si ya llegamos a una solución (cuando el costo es 0).
    """
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            same_row = state[i] == state[j]
            same_diag = abs(state[i] - state[j]) == abs(i - j)
            if same_row or same_diag:
                conflicts += 1
    return conflicts
# =========================================================
# VISTAS
# =========================================================
#Función de visualización
def print_board_ascii(state: list):
    """
    Prints an ASCII representation of the N-Queens board.
    
    Each index in the input list represents the column,
    and the value at that index represents the row where the queen is placed.

    Args:
        state (list): A list of integers where state[i] is the row of the queen in column i.

    Example:
        For board = [0, 4, 7, 5, 2, 6, 1, 3], prints a visual 8x8 board with queens.
    """
    n = len(state)
    horizontal_border = "+" + "---+" * n
    for row in range(n):
        print(horizontal_border)
        row_str = ""
        for col in range(n):
            if state[col] == row:
                row_str += "| ♛ "
            else:
                row_str += "|   "
        row_str += "|"
        print(row_str)
    print(horizontal_border)

#--------------------------

# =========================================================
# Implementaciones CSP con conteo de nodos
# =========================================================

def is_consistent(assignment, var, value):
    for other_var, other_val in assignment.items():
        if other_val == value:
            return False
        if abs(other_val - value) == abs(other_var - var):
            return False
    return True


def backtracking_csp_with_count(n, seed):
    rng = random.Random(seed)
    nodes = 0

    value_orders = {var: list(range(n)) for var in range(n)}
    for var in value_orders:
        rng.shuffle(value_orders[var])

    def backtrack(assignment):
        nonlocal nodes
        if len(assignment) == n:
            return [assignment[i] for i in range(n)]

        var = len(assignment)
        nodes += 1

        for value in value_orders[var]:
            if is_consistent(assignment, var, value):
                assignment[var] = value
                result = backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]

        return None

    start = time.time()
    sol = backtrack({})
    elapsed = time.time() - start
    success = sol is not None

    return {"solution": sol, "time": elapsed, "nodes": nodes, "success": success}


def forward_checking_csp_with_count(n, seed):
    rng = random.Random(seed)
    nodes = 0

    domains_init = {var: list(range(n)) for var in range(n)}
    for var in domains_init:
        rng.shuffle(domains_init[var])

    def forward_check(var, value, domains):
        new_domains = {v: d.copy() for v, d in domains.items()}

        for other_var in range(n):
            if other_var == var:
                continue

            if value in new_domains[other_var]:
                new_domains[other_var].remove(value)

            dist = abs(other_var - var)
            diag1 = value + dist
            diag2 = value - dist

            if diag1 in new_domains[other_var]:
                new_domains[other_var].remove(diag1)
            if diag2 in new_domains[other_var]:
                new_domains[other_var].remove(diag2)

            if len(new_domains[other_var]) == 0:
                return None

        return new_domains

    def backtrack(assignment, domains):
        nonlocal nodes
        if len(assignment) == n:
            return [assignment[i] for i in range(n)]

        var = len(assignment)
        nodes += 1

        for value in list(domains[var]):
            new_domains = forward_check(var, value, domains)
            if new_domains is not None:
                assignment[var] = value
                result = backtrack(assignment, new_domains)
                if result is not None:
                    return result
                del assignment[var]

        return None

    start = time.time()
    sol = backtrack({}, domains_init)
    elapsed = time.time() - start

    success = sol is not None

    return {"solution": sol, "time": elapsed, "nodes": nodes, "success": success}


# =========================================================
# EJECUCIÓN DEL EXPERIMENTO 
# =========================================================

def ejecutar_experimento():
    ns = [4, 8, 10,12,15]   # cambiar si querés agregar 12 y 15
    num_seeds = 30

    rows = []

    for n in ns:
        for alg in ["backtracking", "forward_checking"]:
            for seed in range(num_seeds):

                full_seed = (n * 1000) + seed

                if alg == "backtracking":
                    res = backtracking_csp_with_count(n, full_seed)
                else:
                    res = forward_checking_csp_with_count(n, full_seed)

                rows.append({
                    "n": n,
                    "algorithm": alg,
                    "seed": seed,
                    "success": int(res["success"]),
                    "time": res["time"],
                    "nodes": res["nodes"],
                    "solution": res["solution"]
                })

    os.makedirs("output", exist_ok=True)

    df = pd.DataFrame(rows)
    df.to_csv("tp5-csp/nqueens_results.csv", index=False)

    # ------------------ resumen estadístico ------------------
    summary_rows = []

    for (n, alg), group in df.groupby(["n", "algorithm"]):
        total = len(group)
        success_count = int(group["success"].sum())
        success_pct = 100 * success_count / total

        times_success = group[group["success"] == 1]["time"].tolist()
        nodes_success = group[group["success"] == 1]["nodes"].tolist()

        time_mean = mean(times_success) if times_success else float("nan")
        time_std = stdev(times_success) if len(times_success) > 1 else float("nan")

        nodes_mean = mean(nodes_success) if nodes_success else float("nan")
        nodes_std = stdev(nodes_success) if len(nodes_success) > 1 else float("nan")

        summary_rows.append({
            "n": n,
            "algorithm": alg,
            "success_pct": success_pct,
            "time_mean": time_mean,
            "time_std": time_std,
            "nodes_mean": nodes_mean,
            "nodes_std": nodes_std
        })

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv("tp5-csp/nqueens_summary.csv", index=False)

    # ------------------ boxplots ------------------
    for n in ns:
        subset = df[df["n"] == n]

        # tiempos
        plt.figure(figsize=(8, 5))
        plt.boxplot([
            subset[subset["algorithm"]=="backtracking"]["time"].tolist(),
            subset[subset["algorithm"]=="forward_checking"]["time"].tolist()
        ], labels=["backtracking", "forward checking"])
        plt.title(f"Boxplot tiempos - N={n}")
        plt.ylabel("Tiempo (s)")
        plt.savefig(f"tp5-csp/images/boxplot_tiempos_n{n}.png")
        plt.close()

        # nodos
        plt.figure(figsize=(8, 5))
        plt.boxplot([
            subset[subset["algorithm"]=="backtracking"]["nodes"].tolist(),
            subset[subset["algorithm"]=="forward_checking"]["nodes"].tolist()
        ], labels=["backtracking", "forward checking"])
        plt.title(f"Boxplot nodos - N={n}")
        plt.ylabel("Nodos explorados")
        plt.savefig(f"tp5-csp/images/boxplot_nodos_n{n}.png")
        plt.close()

    print("Experimento finalizado. Resultados en carpeta /output")



ejecutar_experimento()
