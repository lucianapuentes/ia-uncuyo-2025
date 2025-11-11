## Código función create_folds

    create_folds <- function(df, k = 10) {
    
        set.seed(123)  # para reproducibilidad
        
        n <- nrow(df)
        
        indices <- sample(1:n)
        

        folds <- cut(seq(1, n), breaks = k, labels = FALSE)
        

        lista_folds <- list()
        
        for (i in 1:k) {
            lista_folds[[paste0("Fold", i)]] <- indices[which(folds == i)]
        }
        
        return(lista_folds)
    }

## Código función cross_validation

    cross_validation <- function(df, k = 10) {
    

    df$inclinacion_peligrosa <- factor(df$inclinacion_peligrosa)
    

    df$especie <- factor(df$especie)
    df$nombre_seccion <- factor(df$nombre_seccion)
    
    folds <- create_folds(df, k)
    
    train_formula <- formula(
        inclinacion_peligrosa ~ altura + circ_tronco_cm +
        lat + long + nombre_seccion + especie
    )
    
    resultados <- data.frame(
        accuracy = numeric(k),
        precision = numeric(k),
        sensitivity = numeric(k),
        specificity = numeric(k)
    )
    
    for (i in 1:k) {
        
        test_idx <- folds[[i]]
        data_test <- df[test_idx, ]
        data_train <- df[-test_idx, ]
        
        # =======================
        # Normalizar niveles
        # =======================
        data_train$especie <- factor(data_train$especie, levels = levels(df$especie))
        data_test$especie  <- factor(data_test$especie,  levels = levels(df$especie))
        
        data_train$nombre_seccion <- factor(data_train$nombre_seccion, levels = levels(df$nombre_seccion))
        data_test$nombre_seccion  <- factor(data_test$nombre_seccion,  levels = levels(df$nombre_seccion))
        
        # Entrenar árbol
        tree_model <- rpart(train_formula, data = data_train, method = "class")
        
        # Predicción
        pred <- predict(tree_model, data_test, type = "class")
        
        real <- as.numeric(as.character(data_test$inclinacion_peligrosa))
        pred <- as.numeric(as.character(pred))
        
        TP <- sum(real == 1 & pred == 1)
        TN <- sum(real == 0 & pred == 0)
        FP <- sum(real == 0 & pred == 1)
        FN <- sum(real == 1 & pred == 0)
        
        accuracy    <- (TP + TN) / (TP + TN + FP + FN)
        precision   <- ifelse((TP + FP) == 0, 0, TP / (TP + FP))
        sensitivity <- ifelse((TP + FN) == 0, 0, TP / (TP + FN))
        specificity <- ifelse((TN + FP) == 0, 0, TN / (TN + FP))
        
        resultados[i, ] <- c(accuracy, precision, sensitivity, specificity)
        
        cat("Fold", i, "completado.\n")
    }
    
    medias <- colMeans(resultados)
    desvios <- apply(resultados, 2, sd)
    
    return(list(
        metricas_por_fold = resultados,
        medias = medias,
        desvios = desvios
    ))
    }


|             | Media     | Desviación Estándar |
|-------------|-----------|---------------------|
| Accuracy    | 0.8878478 | 0.006052408         |
| Precision   | 0         | 0                   |
| Sensitivity | 0         | 0                   |
| Specificity | 1         | 0                   |