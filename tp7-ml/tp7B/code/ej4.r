# ============================================================
#  MÉTRICAS PARA EL CLASIFICADOR ALEATORIO
# ============================================================

library(dplyr)

# ------------------------------------------------------------
# Función random_classifier
# ------------------------------------------------------------

random_classifier <- function(df) {
  
  # Generar probabilidad aleatoria
  set.seed(123)  # para reproducibilidad (podés cambiarlo)
  df$prediction_prob <- runif(nrow(df), min = 0, max = 1)
  
  # Clasificar según prob > 0.5
  df$prediction_class <- ifelse(df$prediction_prob > 0.5, 1, 0)
  
  return(df)
}

# ------------------------------------------------------------
# Cargar VALIDATION y aplicar clasificador
# ------------------------------------------------------------

df_val <- read.csv("tp7-ml/tp7B/data/arbolado-mendoza-dataset-validation-random-pred.csv")

df_pred <- random_classifier(df_val)

# ------------------------------------------------------------
# Cálculo de TP, TN, FP, FN
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
# Matriz de confusión
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
# MÉTRICAS
# ------------------------------------------------------------

accuracy  <- (TP + TN) / (TP + TN + FP + FN)

precision <- ifelse(TP + FP == 0, 0, TP / (TP + FP))

recall    <- ifelse(TP + FN == 0, 0, TP / (TP + FN))   # sensibilidad

specificity <- ifelse(TN + FP == 0, 0, TN / (TN + FP))

f1_score <- ifelse(precision + recall == 0, 0,
                   2 * precision * recall / (precision + recall))


cat("\n===== MÉTRICAS DEL CLASIFICADOR ALEATORIO =====\n")
cat("Accuracy:     ", round(accuracy, 4), "\n")
cat("Precision:    ", round(precision, 4), "\n")
cat("Recall:       ", round(recall, 4), "\n")
cat("Specificity:  ", round(specificity, 4), "\n")
cat("F1-Score:     ", round(f1_score, 4), "\n")

# ------------------------------------------------------------
# OPCIONAL: exportar resultados
# write.csv(df_pred, "predicciones_random.csv", row.names = FALSE)
# write.csv(conf_matrix, "matriz_confusion_random.csv")
