# Trabajo Práctico 6: Satisfacción de restricciones

---

## Ejercicio 1
Una formulación CSP para un Sudoku puede ser de la forma:
- Variables: Cada casillero en el que puede colocarse un número (81 casilleros)
- Dominio: {1, 2, 3, 4, 5, 6, 7, 8, 9}
- Restricciones: Un mismo número no puede estar en la misma fila, misma columna, o misma "caja" de 3x3.

---
## Ejercicio 2
a. Remove SA − WA, delete G from SA.   
b. Remove SA − V , delete R from SA, leaving only B.   
c. Remove NT − WA, delete G from N T .   
d. Remove NT − SA, delete B from N T , leaving only R.   
e. Remove NSW − SA, delete B from N SW .   
f. Remove NSW − V , delete R from N SW , leaving only G.   
g. Remove Q − NT , delete R from Q.   
h. Remove Q − SA, delete B from Q.   
i. Remove Q − NSW , delete G from Q, leaving no domain for Q.

---
## Ejercicio 3
La complejidad en el peor caso cuando se ejecuta AC-3 en un árbol estructurado CSP es de O(E*D), donde E es la cantidad
de edges/aristas y D es el tamaño del dominio más grande.
5


