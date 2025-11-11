# ============================================================
#   CLASIFICADOR POR CLASE MAYORITARIA + MÉTRICAS
# ============================================================

library(dplyr)

# ------------------------------------------------------------
# a) Función biggerclass_classifier
# ------------------------------------------------------------

biggerclass_classifier <- function(df) {
  
  # Detectar clase mayoritaria
  mayoritaria <- df %>%
    count(inclinacion_peligrosa) %>%
    arrange(desc(n)) %>%
    slice(1) %>%
    pull(inclinacion_peligrosa)
  
  cat("Clase mayoritaria detectada:", mayoritaria, "\n")
  
  # Asignar esa clase como predicción a todas las observaciones
  df$prediction_class <- mayoritaria
  
  return(df)
}

# ------------------------------------------------------------
# b) Aplicar al archivo de validación
# ------------------------------------------------------------

df_val <- read.csv("tp7-ml/tp7B/data/arbolado-mendoza-dataset-validation-random-pred.csv")

df_pred <- biggerclass_classifier(df_val)

# ------------------------------------------------------------
# c) Cálculo de TP, TN, FP, FN
# ------------------------------------------------------------

TP <- df_pred %>% filter(inclinacion_peligrosa == 1 & prediction_class == 1) %>% nrow()
TN <- df_pred %>% filter(inclinacion_peligrosa == 0 & prediction_class == 0) %>% nrow()
FP <- df_pred %>% filter(inclinacion_peligrosa == 0 & prediction_class == 1) %>% nrow()
FN <- df_pred %>% filter(inclinacion_peligrosa == 1 & prediction_class == 0) %>% nrow()

cat("True Positives (TP): ", TP, "\n")
cat("True Negatives (TN): ", TN, "\n")
cat("False Positives (FP): ", FP, "\n")
cat("False Negatives (FN): ", FN, "\n")

# ------------------------------------------------------------
# d) Matriz de confusión
# ------------------------------------------------------------

conf_matrix <- matrix(
  c(TP, FN,
    FP, TN),
  nrow = 2,
  byrow = TRUE
)

colnames(conf_matrix) <- c("Predicho 1", "Predicho 0")
rownames(conf_matrix) <- c("Real 1", "Real 0")

cat("\nMatriz de confusión:\n")
print(conf_matrix)

# ------------------------------------------------------------
# e) Métricas
# ------------------------------------------------------------

accuracy  <- (TP + TN) / (TP + TN + FP + FN)

precision <- ifelse(TP + FP == 0, 0, TP / (TP + FP))

recall    <- ifelse(TP + FN == 0, 0, TP / (TP + FN))  # sensibilidad

specificity <- ifelse(TN + FP == 0, 0, TN / (TN + FP))

f1_score <- ifelse(precision + recall == 0, 0,
                   2 * precision * recall / (precision + recall))

# Mostrar métricas
cat("\n===== MÉTRICAS DEL MODELO =====\n")
cat("Accuracy:     ", round(accuracy, 4), "\n")
cat("Precision:    ", round(precision, 4), "\n")
cat("Recall:       ", round(recall, 4), "\n")
cat("Specificity:  ", round(specificity, 4), "\n")
cat("F1-Score:     ", round(f1_score, 4), "\n")

# ------------------------------------------------------------
# GUARDADO OPCIONAL
write.csv(df_pred, "predicciones_biggerclass.csv", row.names = FALSE)
write.csv(conf_matrix, "matriz_confusion_biggerclass.csv")
