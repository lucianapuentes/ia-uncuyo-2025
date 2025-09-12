import pandas as pd
import matplotlib.pyplot as plt
import glob

# =========================================================
# LEER TODOS LOS CSVs
# =========================================================
def cargar_datos():
    archivos = glob.glob("*_resultados.csv")
    dfs = {}
    for archivo in archivos:
        nombre = archivo.replace("_resultados.csv", "")
        dfs[nombre] = pd.read_csv(archivo)
    return dfs

# =========================================================
# BOXPLOTS
# =========================================================
def graficar_boxplots(dfs, metrica="Costo", escenario=1):
    datos = []
    etiquetas = []
    for nombre, df in dfs.items():
        subset = df[df["Escenario"] == escenario]
        if not subset.empty:
            datos.append(subset[metrica].values)
            etiquetas.append(nombre)

    plt.figure(figsize=(10, 6))
    plt.boxplot(datos, labels=etiquetas)
    plt.title(f"Distribución de {metrica} por algoritmo (Escenario {escenario})")
    plt.ylabel(metrica)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

# =========================================================
# GRÁFICO LINEAL COMPARATIVO
# =========================================================
def graficar_lineal(dfs, metrica="Tiempo", escenario=1):
    plt.figure(figsize=(10, 6))
    for nombre, df in dfs.items():
        subset = df[df["Escenario"] == escenario]
        if not subset.empty:
            plt.plot(subset["Run"], subset[metrica], marker="o", label=nombre)

    plt.title(f"Evolución de {metrica} por repetición (Escenario {escenario})")
    plt.xlabel("Repetición")
    plt.ylabel(metrica)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

# =========================================================
# MAIN
# =========================================================

dfs = cargar_datos()

# Boxplots de varias métricas
for metrica in ["Explorados", "Pasos", "Costo", "Tiempo"]:
    graficar_boxplots(dfs, metrica, escenario=1)
    graficar_boxplots(dfs, metrica, escenario=2)

# Gráfico lineal comparativo
for metrica in ["Costo", "Tiempo"]:
    graficar_lineal(dfs, metrica, escenario=1)
    graficar_lineal(dfs, metrica, escenario=2)
