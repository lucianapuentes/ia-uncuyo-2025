import pandas as pd
import os

# Construir la ruta absoluta basada en donde está este archivo .py
base = os.path.dirname(__file__)
csv_path = os.path.join(base, "arbolado-mza-dataset.csv")

# Cargar dataset
df = pd.read_csv(csv_path)

# Mezclar filas
df = df.sample(frac=1, random_state=42)

# Calcular tamaños
valid_size = int(len(df) * 0.20)

# Dividir
df_valid = df.iloc[:valid_size]
df_train = df.iloc[valid_size:]

# Guardar archivos en la misma carpeta
df_valid.to_csv(os.path.join(base, "arbolado-mza-dataset-validation.csv"), index=False)
df_train.to_csv(os.path.join(base, "arbolado-mza-dataset-train.csv"), index=False)

print("Archivos generados correctamente.")
