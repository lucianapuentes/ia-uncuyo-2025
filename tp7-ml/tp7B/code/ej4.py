import pandas as pd
import os
import numpy as np
# ================================
# Cargar dataset
# ================================
base = os.path.dirname(__file__)
csv_path = os.path.join(base, "arbolado-mza-dataset-validation.csv")

def add_random_prob(df):
    df["prediction_prob"] = np.random.rand(len(df))
    return df
def random_classifier(df):
    df["prediction_class"] = df["prediction_prob"].apply(lambda x: 1 if x > 0.5 else 0)
    return df
df = pd.read_csv(csv_path)

df = add_random_prob(df)
df = random_classifier(df)


df.to_csv("arbolado-mendoza-dataset-validation-random-pred.csv", index=False)
