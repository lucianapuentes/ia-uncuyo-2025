from tablero import *
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from busqueda_local import *
from genetic import *
# =========================================================
# ------------------ experimento principal ------------------

def run_experiments(seeds, sizes, max_states, algorithms):
    rows = []
    run_id = 0
    for size in sizes:
        # ### ARREGLOS APLICADOS ###
        # Desempaquetamos la tupla. 'env_n' ahora es el índice del 0 al 29.
        # '_' se usa para ignorar el valor de la semilla, ya que la inicialización es aleatoria.
        for env_n, _ in enumerate(seeds):
            for alg_name in algorithms:
                run_id += 1
                
                # Mantenemos la inicialización aleatoria sin semilla:
                state=initialize_random_state(size) 
                
                if alg_name == "random":
                    best, h, states, elapsed = random_search(state, max_states)
                elif alg_name == "HC":
                    best, h, states, elapsed = hill_climbing(max_states, state)
                elif alg_name == "SA":
                    best, h, states, elapsed = simulated_annealing(state, t0=1.0, alpha=0.99, tmin=1e-10, max_steps=max_states)
                elif alg_name == "GA":
                    # Nota: El GA usa 'state' para obtener el tamaño, pero internamente genera su población.
                    best, h, states, elapsed = genetic_algorithm(state, pop_size=30, generations=max_states, mutation_rate=0.1)
                else:
                    continue
                rows.append({
                    "algorithm_name": alg_name,
                    "env_n": env_n, # <-- Ahora es el índice (int)
                    "size": size,
                    "best_solution": best,
                    "H": int(h),
                    "states": int(states),
                    "time": float(elapsed)
                })
    df = pd.DataFrame(rows)
    return df

# parámetros experimentales
seeds = list(range(30))  # 30 semillas
sizes = [4,8,10]
max_states = 2000  # el mismo para todos los algoritmos

algorithms = ["random","HC","SA","GA"]
df = run_experiments(seeds, sizes, max_states, algorithms)

# === ARREGLOS APLICADOS: Asegurar tipos numéricos para evitar fallos de filtrado ===
df["env_n"] = df["env_n"].astype(int)
df["size"] = df["size"].astype(int)
df["H"] = df["H"].astype(int)
df["states"] = df["states"].astype(int)
df["time"] = df["time"].astype(float)
# =================================================================================

# guardar CSV
out_csv = "experiments_results.csv"
df.to_csv(out_csv, index=False)
print("Experimentos",df.head()) # Mostrar las primeras filas

# Calcular estadísticas por (algorithm, size)
# ===========================================

summary=[]
for alg in algorithms:
    print("\nProcesando algoritmo:", alg)
    
    # Se añade un head() para no imprimir todo el DataFrame, 
    # pero el filtrado interno es el correcto
    print(df[df.algorithm_name == alg].head()) 
    
    for size in sizes:
        print("   tamaño:", size)
        
       # === ARREGLO FINAL APLICADO: Filtro con .values para evitar problemas de tipo/índice ===
        # Compara directamente los arrays de valores subyacentes.
        filtro = (df.algorithm_name == alg) & (df['size'].values == size)
        sub = df[filtro]
        
        runs = len(sub)
        print("runs: ", runs)
        if runs == 0:
            continue

        solved = sub[sub.H == 0]
        # total=sub.H  # Esta línea no es necesaria para el cálculo, se mantiene comentada
        
        print("solved count: ", len(solved))
        # print("total: ") # Se elimina print irrelevante
        
        pct_solved = 100 * len(solved) / runs
        H_mean = sub["H"].mean()
        H_std = sub["H"].std(ddof=0)
        
        # estadísticas de corridas exitosas
        time_mean = solved["time"].mean() if len(solved) > 0 else float("nan")
        time_std = solved["time"].std(ddof=0) if len(solved) > 0 else float("nan")
        states_mean = solved["states"].mean() if len(solved) > 0 else float("nan")
        states_std = solved["states"].std(ddof=0) if len(solved) > 0 else float("nan")

        summary.append({
            "algorithm": alg,
            "size": size,
            "runs": runs,
            "pct_solved": pct_solved,
            "H_mean": H_mean,
            "H_std": H_std,
            "time_mean_success": time_mean,
            "time_std_success": time_std,
            "states_mean_success": states_mean,
            "states_std_success": states_std
        })

summary_df = pd.DataFrame(summary)
print("\nResumen de experimentos:",summary_df)
summary_csv = "experiments_summary.csv"
summary_df.to_csv(summary_csv, index=False)
# =========================================================
# ------------------ resultados y gráficos ------------------

# Guardar resumen (se repite por limpieza, aunque ya estaba)
summary_csv = "experiments_summary.csv"
summary_df.to_csv(summary_csv, index=False)


