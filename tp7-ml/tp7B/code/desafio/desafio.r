if(!require(readr)) install.packages("readr")
library(randomForest)
library(dplyr)
library(readr)  # Usamos readr::read_csv para una carga más rápida de datos

# Cargar los datos de entrenamiento y prueba
data <- read_csv("tp7-ml/tp7B/data/arbolado-mza-dataset.csv")
data_test <- read_csv("tp7-ml/tp7B/data/arbolado-mza-dataset-test.csv")

# Filtrar los árboles con inclinación peligrosa (1)
muestra_inclinacion_peligrosa <- filter(data, inclinacion_peligrosa == 1)

# Filtrar la misma cantidad de árboles con inclinación no peligrosa (0)
set.seed(123)  # Aseguramos la reproducibilidad
muestra_inclinacion_no_peligrosa <- data %>%
  filter(inclinacion_peligrosa == 0) %>%
  sample_n(nrow(muestra_inclinacion_peligrosa))

# Unir ambos conjuntos para tener un dataset balanceado
data_filtrado <- bind_rows(muestra_inclinacion_peligrosa, muestra_inclinacion_no_peligrosa)

# Excluir columnas irrelevantes y preparar los predictores
predictores <- data_filtrado %>%
  select(-inclinacion_peligrosa, -id, -nombre_seccion, -area_seccion, -seccion, -ultima_modificacion, -circ_tronco_cm)

# Asegurarse de que la variable de respuesta sea un factor
respuesta <- factor(data_filtrado$inclinacion_peligrosa)

# Entrenamiento del modelo Random Forest
modelo <- randomForest(x = predictores, y = respuesta, ntree = 15000, mtry = 3)

# Realizar predicciones en el conjunto de prueba
predictions <- predict(modelo, newdata = data_test)

# Ver las primeras 30 predicciones
head(predictions, 30)

# Resumen de las predicciones
summary(predictions)

# Convertir las predicciones a valores binarios (0 o 1)
predicciones_transformadas <- as.numeric(predictions) - 1  # Convierte 'No' a 0 y 'Sí' a 1

# Imprimir el modelo
print(modelo)

# Crear un dataframe de resultados
resultado <- data.frame(ID = data_test$id, inclinacion_peligrosa = predicciones_transformadas)

# Ver las primeras filas del resultado
head(resultado)

# Guardar el resultado en un archivo CSV
write.csv(resultado, file = "resultados.csv", row.names = FALSE)
