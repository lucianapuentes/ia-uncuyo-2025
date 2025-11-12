import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Archivos CSV (solo nombres, estarán en la misma carpeta que el script)
CSV_FILES = {
    "Random": "agent_random.csv",
    "Reflexivo": "agent_reflex.csv"
}

def parse_size(size_str):
    x, y = size_str.split("x")
    return int(x), int(y), int(x) * int(y)

def main():
    # Carpeta donde está el script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Leer y combinar CSVs
    dfs = []
    for agent, file in CSV_FILES.items():
        file_path = os.path.join(script_dir, file)
        if not os.path.exists(file_path):
            print(f"❌ No se encontró el archivo: {file_path}")
            continue
        df = pd.read_csv(file_path)
        df["Agent"] = agent
        dfs.append(df)

    if not dfs:
        print("❌ No se cargó ningún CSV. Revisá que los archivos existan en la carpeta del script.")
        return

    df = pd.concat(dfs, ignore_index=True)

    # Parsear tamaño y calcular tierra total
    df[["size_x", "size_y", "total_cells"]] = df["size"].apply(lambda s: pd.Series(parse_size(s)))
    df["total_dirt"] = df["dirt_rate"] * df["total_cells"]
    
    # Obtener los valores únicos de total_cells para los ticks
    cell_counts = sorted(df["total_cells"].unique())

    # --- Gráfico 1: Performance promedio (CORREGIDO) ---
    plt.figure()
    perf = df.groupby(["Agent", "total_cells", "dirt_rate"])["performance"].mean().reset_index()
    for agent in perf["Agent"].unique():
        subset_agent = perf[perf["Agent"] == agent]
        for dirt in sorted(subset_agent["dirt_rate"].unique()):
            subset = subset_agent[subset_agent["dirt_rate"] == dirt]
            plt.plot(subset["total_cells"], subset["performance"], marker="o", label=f"{agent} - Dirt {dirt}")

    plt.title("Performance promedio por agente y suciedad")
    plt.xlabel("Cantidad de celdas en el entorno")
    plt.ylabel("Performance promedio (celdas limpiadas)")
    
    # 🚀 CORRECCIÓN: Aplicar escala logarítmica para separar los puntos en X
    plt.xscale('log', base=2)
    # Establecer los ticks con los valores originales
    plt.xticks(cell_counts, cell_counts)
    
    plt.legend()
    # Usar which="both" para que el grid funcione con la escala logarítmica
    plt.grid(True, which="both", linestyle="--", alpha=0.7) 
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, "performance_comparison.png"))
    plt.clf()

    # --- Gráfico 2: Acciones promedio (APLICADA LA CORRECCIÓN DE ESCALA) ---
    plt.figure()
    actions = df.groupby(["Agent", "total_cells", "dirt_rate"])["total_actions"].mean().reset_index()
    for agent in actions["Agent"].unique():
        subset_agent = actions[actions["Agent"] == agent]
        for dirt in sorted(subset_agent["dirt_rate"].unique()):
            subset = subset_agent[subset_agent["dirt_rate"] == dirt]
            plt.plot(subset["total_cells"], subset["total_actions"], marker="o", label=f"{agent} - Dirt {dirt}")

    plt.title("Acciones promedio por agente y suciedad")
    plt.xlabel("Cantidad de celdas en el entorno")
    plt.ylabel("Acciones promedio")
    
    # 🚀 CORRECCIÓN: Aplicar escala logarítmica en X al igual que en los otros gráficos
    plt.xscale('log', base=2)
    plt.xticks(cell_counts, cell_counts)
    
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, "actions_comparison.png"))
    plt.clf()

    # --- Gráfico 3: Tiempo promedio (YA ESTABA CORREGIDO) ---
    plt.figure()
    times = df.groupby(["Agent", "total_cells", "dirt_rate"])["execution_time"].mean().reset_index()
    for agent in times["Agent"].unique():
        subset_agent = times[times["Agent"] == agent]
        for dirt in sorted(subset_agent["dirt_rate"].unique()):
            subset = subset_agent[subset_agent["dirt_rate"] == dirt]
            plt.plot(subset["total_cells"], subset["execution_time"], marker="o", label=f"{agent} - Dirt {dirt}")

    plt.title("Tiempo promedio por agente y suciedad")
    plt.xlabel("Cantidad de celdas en el entorno")
    plt.ylabel("Tiempo (segundos)")
    plt.xscale('log', base=2)  # <- Esto ya estaba y es correcto
    plt.xticks(cell_counts, cell_counts)
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, "times_comparison.png"))
    plt.clf()


    # --- Gráfico 4: Tierra total vs limpiada (barras lado a lado) ---
    dirt_stats = df.groupby(["Agent", "total_cells", "dirt_rate"])[["total_dirt", "performance"]].mean().reset_index()
    for dirt in sorted(dirt_stats["dirt_rate"].unique()):
        plt.figure(figsize=(10,5))
        subset_dirt = dirt_stats[dirt_stats["dirt_rate"] == dirt]
        agents = subset_dirt["Agent"].unique()
        # Se calcula la posición de los grupos de barras
        x_ticks = sorted(subset_dirt["total_cells"].unique())
        x = np.arange(len(x_ticks))
        width = 0.35

        # Se asume que solo hay 2 agentes ("Random" y "Reflexivo")
        num_agents = len(agents)
        if num_agents == 2:
             # Ajuste de posición: el centro de los dos grupos estará en x
            pos = [x - width/2, x + width/2] 
        elif num_agents == 1:
            pos = [x]
        else: # Si hay más de dos agentes, se requiere un ajuste más complejo, pero asumimos 2.
             pos = [x + (i - (num_agents-1)/2)*width for i in range(num_agents)]

        for i, agent in enumerate(agents):
            sub = subset_dirt[subset_dirt["Agent"] == agent]
            # Usar la misma posición para las barras de Total y Limpiada de cada agente
            bar_pos = pos[i]
            
            # Gráfico de barras Total (transparente)
            plt.bar(bar_pos, sub["total_dirt"], width, label=f"{agent} - Total", alpha=0.5, edgecolor='black')
            # Gráfico de barras Limpiada (opaco, encima de la de Total)
            plt.bar(bar_pos, sub["performance"], width, label=f"{agent} - Limpiada", alpha=1.0)
            
        plt.xticks(x, x_ticks)
        plt.xlabel("Cantidad de celdas en el entorno")
        plt.ylabel("Celdas")
        plt.title(f"Tierra total vs limpiada (Dirt Rate: {dirt})")
        
        # Ajuste de leyenda para evitar duplicados si se llamó al .bar múltiples veces
        handles, labels = plt.gca().get_legend_handles_labels()
        # Filtrar solo entradas únicas, manteniendo el orden
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        plt.legend(*zip(*unique))
        
        plt.grid(axis="y")
        plt.tight_layout()
        plt.savefig(os.path.join(script_dir, f"dirt_comparison_dirt{dirt}.png"))
        plt.clf()

    print("✅ Gráficos comparativos generados en la carpeta del script.")

if __name__ == "__main__":
    main()