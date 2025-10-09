import random
# =========================================================
# ESTADOS
# =========================================================

def initialize_random_state(n: int = 8):
    """
    Initializes a random state for the N-queens problem.
    Returns a list where each index represents a column
    and the value is the row where the queen is placed.
    """
    return [random.randint(0, n - 1) for _ in range(n)]

def generate_neighbors(state):
    """
    Generates all neighboring states from the current state.
    A neighbor is a state where one queen is moved to a different
    row within its column.
    
    Args:
        state (list): List representing the queen positions.
        
    Returns:
        list: List of neighboring states.

    Para cada columna, prueba mover la reina a todas las filas distintas de la actual.
    Copia el estado actual y modifica la posición para crear un vecino nuevo.
    Devuelve una lista con todos los vecinos posibles.
    """
    n = len(state)
    neighbors = []
    
    for col in range(n):
        current_row = state[col]
        for new_row in range(n):
            if new_row != current_row:
                neighbor = state.copy()
                neighbor[col] = new_row
                neighbors.append(neighbor)
                
    return neighbors
# =========================================================
# COSTO
# =========================================================
def cost(state):
    """
    Calculates the number of pairs of queens that are attacking each other.
    
    Args:
        state (list): A list where state[i] is the row of the queen in column i.
        
    Returns:
        int: Total number of conflicting pairs.
    
    Esta función se usa para:

    Evaluar qué tan buena es una solución actual.
    Comparar varios vecinos y elegir el de menor costo.
    Saber si ya llegamos a una solución (cuando el costo es 0).
    """
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            same_row = state[i] == state[j]
            same_diag = abs(state[i] - state[j]) == abs(i - j)
            if same_row or same_diag:
                conflicts += 1
    return conflicts
# =========================================================
# VISTAS
# =========================================================
#Función de visualización
def print_board_ascii(state: list):
    """
    Prints an ASCII representation of the N-Queens board.
    
    Each index in the input list represents the column,
    and the value at that index represents the row where the queen is placed.

    Args:
        state (list): A list of integers where state[i] is the row of the queen in column i.

    Example:
        For board = [0, 4, 7, 5, 2, 6, 1, 3], prints a visual 8x8 board with queens.
    """
    n = len(state)
    horizontal_border = "+" + "---+" * n
    for row in range(n):
        print(horizontal_border)
        row_str = ""
        for col in range(n):
            if state[col] == row:
                row_str += "| ♛ "
            else:
                row_str += "|   "
        row_str += "|"
        print(row_str)
    print(horizontal_border)

