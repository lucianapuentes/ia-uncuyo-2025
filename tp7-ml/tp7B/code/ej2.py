import matplotlib.pyplot as plt
import pandas as pd
import os
# ==============================
# Cargar dataset de entrenamiento
# ==============================

base = os.path.dirname(__file__)
csv_path = os.path.join(base, "arbolado-mza-dataset-train.csv")

# Cargar dataset
df = pd.read_csv(csv_path)

# ====================================================
# a) Distribución de la clase inclinacion_peligrosa
# ====================================================

conteo_inclinacion = df["inclinacion_peligrosa"].value_counts()

plt.figure(figsize=(6,4))
conteo_inclinacion.plot(kind="bar")
plt.title("Distribución de inclinación peligrosa")
plt.xlabel("¿Inclinación peligrosa?")
plt.ylabel("Cantidad de árboles")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

print("\nDistribución de la clase inclinacion_peligrosa:")
print(conteo_inclinacion)


# ====================================================
# b) ¿Alguna sección es más peligrosa?
# ====================================================

peligro_por_seccion = df.groupby("nombre_seccion")["inclinacion_peligrosa"].mean().sort_values(ascending=False)

plt.figure(figsize=(10,6))
peligro_por_seccion.plot(kind="bar")
plt.title("Proporción de árboles con inclinación peligrosa por sección")
plt.xlabel("Sección")
plt.ylabel("Proporción de peligro")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

print("\nProporción de peligro por sección:")
print(peligro_por_seccion)


# ====================================================
# c) ¿Alguna especie es más peligrosa?
# ====================================================

peligro_por_especie = df.groupby("especie")["inclinacion_peligrosa"].mean().sort_values(ascending=False)

plt.figure(figsize=(10,6))
peligro_por_especie.plot(kind="bar")
plt.title("Proporción de árboles con inclinación peligrosa por especie")
plt.xlabel("Especie")
plt.ylabel("Proporción de peligro")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

print("\nProporción de peligro por especie:")
print(peligro_por_especie)