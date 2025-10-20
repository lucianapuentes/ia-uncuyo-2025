import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Asegurar que el directorio actual sea el del script ---
# Se mantiene comentado por seguridad, descomentar si se usa como script standalone
# os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- Cargar los CSV ---
summary = pd.read_csv("experiments_summary.csv")
results = pd.read_csv("experiments_results.csv")

# --- Estilo general ---
sns.set(style="whitegrid", palette="Set2")

# Aseguramos que 'size' sea una etiqueta para las gráficas
results["size_label"] = results["size"].astype(str)

# Definimos el directorio de salida (Asegúrate de que exista o créalo antes)
IMAGE_DIR = "boxplots_individuales"
os.makedirs(IMAGE_DIR, exist_ok=True) 

# ========================================
# 1️⃣ BOXPLOTS INDIVIDUALES POR (ALGORITMO, TAMAÑO)
# ========================================

# ----------------------------------------------------
# A. Boxplot: Calidad Final de la Solución (H)
# ----------------------------------------------------

# Creamos una cuadrícula para generar un gráfico por cada combinación (algoritmo, tamaño)
g_h = sns.FacetGrid(
    data=results, 
    col="algorithm_name",  # Columnas separadas por algoritmo
    row="size_label",      # Filas separadas por tamaño
    sharex=False,          # Ejes X independientes
    sharey=False,          # Ejes Y independientes
    height=4,              # Altura de cada gráfico
    aspect=1.2             # Relación de aspecto
)

# En cada subtrama, trazamos el boxplot de la métrica H
g_h.map(sns.boxplot, "algorithm_name", "H", order=results["algorithm_name"].unique())

# Ajustamos títulos y etiquetas para cada gráfico
g_h.set_axis_labels("Algoritmo", "Conflictos (H)")
g_h.set_titles(col_template="{col_name}", row_template="Tamaño $N={row_name}$")
g_h.fig.suptitle("Distribución de Conflictos Finales (H) por Run", y=1.02, fontsize=16)

plt.tight_layout()
g_h.fig.savefig(os.path.join(IMAGE_DIR, "boxplot_H_individual_alg_size.png"))
plt.show()

# ----------------------------------------------------
# B. Boxplot: Tiempo de Ejecución (Solo Corridas Exitosas)
# ----------------------------------------------------

# Filtramos solo las soluciones encontradas (H=0)
successful_runs = results[results['H'] == 0].copy()

if not successful_runs.empty:
    
    # Creamos una cuadrícula para el tiempo de ejecución (solo runs exitosos)
    g_time = sns.FacetGrid(
        data=successful_runs, 
        col="algorithm_name", 
        row="size_label", 
        sharex=False, 
        sharey=False, 
        height=4, 
        aspect=1.2
    )

    # En cada subtrama, trazamos el boxplot del tiempo
    g_time.map(sns.boxplot, "algorithm_name", "time", order=successful_runs["algorithm_name"].unique())

    # Ajustamos títulos y etiquetas
    g_time.set_axis_labels("Algoritmo", "Tiempo (segundos)")
    g_time.set_titles(col_template="{col_name}", row_template="Tamaño $N={row_name}$")
    g_time.fig.suptitle("Tiempo de Ejecución para Soluciones Exitosas (H=0)", y=1.02, fontsize=16)
    
    plt.tight_layout()
    g_time.fig.savefig(os.path.join(IMAGE_DIR, "boxplot_time_success_individual_alg_size.png"))
    plt.show()
else:
    print("No hay corridas exitosas (H=0) para graficar el tiempo de forma individual.")

# ========================================
# 2️⃣ EVOLUCIÓN DE H() EN UNA EJECUCIÓN (Se mantiene, con un ejemplo)
# ========================================
# Este tipo de gráfica muestra TODOS los puntos finales de H vs States para un N específico
# y sigue siendo una buena forma de visualizar el comportamiento.

size_ejemplo = 8 

plt.figure(figsize=(10, 6))
for alg in results["algorithm_name"].unique():
    subset = results[(results["algorithm_name"] == alg) & (results["size"] == size_ejemplo)].sort_values("states")
    plt.scatter(subset["states"], subset["H"], label=alg, s=20, alpha=0.6)

plt.title(f"Resultado Final H() vs. Iteraciones (n={size_ejemplo})", fontsize=16)
plt.xlabel("Iteraciones Totales (states)", fontsize=12)
plt.ylabel("Conflictos Finales (H)", fontsize=12)
plt.legend(title="Algoritmo")
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "scatter_H_vs_states.png"))
plt.show()