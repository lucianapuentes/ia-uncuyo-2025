import pandas as pd
import matplotlib.pyplot as plt
import os
# ================================
# Cargar dataset
# ================================
base = os.path.dirname(__file__)
csv_path = os.path.join(base, "arbolado-mza-dataset-train.csv")

# Cargar dataset
df = pd.read_csv(csv_path)

# ---------- Ejercicio 3 ----------
# ---- b) y c) Histogramas de circ_tronco_cm -----

def plot_histogram(df, variable, bins_list):
    plt.figure(figsize=(14, 10))

    # Histograma por cantidad de bins
    for i, bins in enumerate(bins_list, start=1):
        plt.subplot(2, 2, i)
        plt.hist(df[variable], bins=bins, color='blue', alpha=0.7)
        plt.title(f'Histograma de {variable} - {bins} bins', fontsize=14)
        plt.xlabel(variable)
        plt.ylabel('Frecuencia')
        plt.tight_layout()
        plt.savefig('../../images/histograma_circ_tronco_cm_bins.png')
    plt.show()
    plt.clf()

def plot_histogram_by_class(df, variable, class_variable, bins_list):
    plt.figure(figsize=(14, 10))
    # Filtrar por cada clase
    for i, bins in enumerate(bins_list, start=1):
        plt.subplot(2, 2, i)
        clase_0 = df[df[class_variable] == 0][variable]
        clase_1 = df[df[class_variable] == 1][variable]
        plt.hist(clase_0, bins=bins, alpha=0.7, label='No peligrosa (0)', color='blue')
        plt.hist(clase_1, bins=bins, alpha=0.7, label='Peligrosa (1)', color='red')
        plt.title(f'Histograma de {variable} por {class_variable} - {bins} bins', fontsize=14)
        plt.xlabel(variable)
        plt.ylabel('Frecuencia')
        plt.legend()
        # Guardar cada gráfico por cantidad de bins
        plt.tight_layout()
        plt.savefig('../../images/histograma_circ_tronco_cm_class_bins.png')
    plt.show()
    plt.clf()

bins_list = [10, 30, 50, 100]
plot_histogram(df, 'circ_tronco_cm', bins_list)
plot_histogram_by_class(df, 'circ_tronco_cm', 'inclinacion_peligrosa', bins_list)


df.to_csv('arbolado-mendoza-dataset-circ_tronco_cm-train.csv', index=False)