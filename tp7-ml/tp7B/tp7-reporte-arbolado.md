
# Informe: Predicción de Inclinación Peligrosa en Arbolado Público

## Objetivo
El código tiene como objetivo entrenar un modelo de **Random Forest** para predecir si un árbol presenta una **inclinación peligrosa** (`inclinacion_peligrosa`) a partir de un conjunto de características del arbolado público de Mendoza, y generar un archivo CSV con las predicciones.

---

## 1. Instalación y carga de librerías
```r
if(!require(readr)) install.packages("readr")
library(randomForest)
library(dplyr)
library(readr)
````

* Se asegura de que `readr` esté instalado para leer archivos CSV de manera eficiente.
* Se cargan las librerías:

  * **`randomForest`**: para entrenar el modelo de Random Forest.
  * **`dplyr`**: para manipulación de datos.
  * **`readr`**: para lectura rápida de CSV.

---

## 2. Carga de datos

```r
data <- read_csv("tp7-ml/tp7B/data/arbolado-mza-dataset.csv")
data_test <- read_csv("tp7-ml/tp7B/data/arbolado-mza-dataset-test.csv")
```

* Se cargan los datos de entrenamiento y prueba desde archivos CSV.
* `data` contiene el conjunto de entrenamiento con la variable de respuesta `inclinacion_peligrosa`.
* `data_test` contiene los datos donde se realizarán las predicciones.

---

## 3. Balanceo de clases

```r
muestra_inclinacion_peligrosa <- filter(data, inclinacion_peligrosa == 1)
set.seed(123)
muestra_inclinacion_no_peligrosa <- data %>%
  filter(inclinacion_peligrosa == 0) %>%
  sample_n(nrow(muestra_inclinacion_peligrosa))
data_filtrado <- bind_rows(muestra_inclinacion_peligrosa, muestra_inclinacion_no_peligrosa)
```

* El dataset original está **desbalanceado** (muchos más árboles sin inclinación peligrosa que con inclinación peligrosa).
* Se filtran los casos con inclinación peligrosa (`1`) y se selecciona una cantidad igual de casos sin inclinación peligrosa (`0`) de manera aleatoria.
* Esto genera un **dataset balanceado**, evitando que el modelo se sesgue hacia la clase mayoritaria.

---

## 4. Selección de predictores y variable de respuesta

```r
predictores <- data_filtrado %>%
  select(-inclinacion_peligrosa, -id, -nombre_seccion, -area_seccion, -seccion, -ultima_modificacion, -circ_tronco_cm)
respuesta <- factor(data_filtrado$inclinacion_peligrosa)
```

* Se eliminan columnas que no aportan información predictiva o podrían filtrar la variable de salida:

  * `id`, `nombre_seccion`, `area_seccion`, `seccion`, `ultima_modificacion`, `circ_tronco_cm`.
* La variable de respuesta `inclinacion_peligrosa` se transforma en factor, como exige **Random Forest** para clasificación.

---

## 5. Entrenamiento del modelo Random Forest

```r
modelo <- randomForest(x = predictores, y = respuesta, ntree = 15000, mtry = 3)
```

* Se entrena un modelo de **Random Forest** con:

  * `ntree = 15000`: número de árboles en el bosque.
  * `mtry = 3`: número de variables consideradas en cada división de nodo.
* Random Forest combina múltiples árboles para reducir **overfitting** y mejorar precisión.

---

## 6. Predicciones en el conjunto de prueba

```r
predictions <- predict(modelo, newdata = data_test)
head(predictions, 30)
summary(predictions)
```

* Se predicen las clases para los árboles en `data_test`.
* Se muestran las primeras 30 predicciones y un resumen estadístico.

---

## 7. Conversión de predicciones a valores binarios

```r
predicciones_transformadas <- as.numeric(predictions) - 1
```

* Convierte las predicciones de factor (`"No"`/`"Sí"`) a **0** y **1**:

  * `"No"` → 0
  * `"Sí"` → 1

---

## 8. Creación de archivo de resultados

```r
resultado <- data.frame(ID = data_test$id, inclinacion_peligrosa = predicciones_transformadas)
head(resultado)
write.csv(resultado, file = "resultados.csv", row.names = FALSE)
```

* Se genera un dataframe con:

  * `ID`: identificador del árbol.
  * `inclinacion_peligrosa`: predicción binaria (0 o 1).
* Se guarda en un CSV llamado `resultados.csv` listo para subir a Kaggle.

---

## 9. Resumen


1. Carga y preparación de datos.
2. Balanceo de clases para evitar sesgo.
3. Selección de predictores y variable de respuesta.
4. Entrenamiento de un modelo Random Forest.
5. Predicción sobre datos nuevos.
6. Conversión y exportación de resultados.

El uso de **Random Forest** es adecuado para datasets con múltiples variables predictivas y relaciones no lineales, proporcionando además medidas de importancia de las variables.

## 10. Resultados en Kaggle 
![RESULTADOS](/tp7-ml/tp7B/images/kaggle.png)