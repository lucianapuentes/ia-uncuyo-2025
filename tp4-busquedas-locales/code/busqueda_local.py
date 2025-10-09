from  tablero import *
import time
import math

# =========================================================
# ALGORITMOS
# =========================================================

'''
HILL CLIMBING (descenso del gradiente)
Estructura general del algoritmo

1.Evaluar el costo del estado actual.
2.Generar todos sus vecinos.
3.Elegir el vecino con menor costo.
4.Si es mejor que el actual, avanzar a ese estado.
5.Si no hay mejora posible → nos quedamos en un óptimo local.
'''
def hill_climbing(max_steps,current):
    """
    Hill Climbing algorithm to solve the N-Queens problem.
    
    Args:
        max_steps (int): Maximum number of steps before giving up.
        current (list): A list where current[i] is the row of the queen in column i.

    Returns:
        tuple: (final_state, final_cost,final_steps,final_time)
    """
    inicio=time.time()
    # Calcular el costo del estado actual
    current_cost=cost(current)
    print("Estado inicial:", current)
    print("Costo:", current_cost)
    print_board_ascii(current)
    print("------------")
    steps=0
    for step in range(max_steps):
        steps+=1
        #Generar vecinos y calcular sus costos
        neighbors=generate_neighbors(current)
        neighbors_costs=[cost(neighbor) for neighbor in neighbors]
        #Buscar el vecino de costo mínimo
        min_cost=min(neighbors_costs)
        #Si todos los vecinos tienen el mismo valor o mayor, la solución actual es la mejor
        if min_cost>=current_cost:
            last_step=step
            break
        #Elegimos el vecino con menor costo
        best_index=neighbors_costs.index(min_cost)
        current=neighbors[best_index]
        current_cost=min_cost
    if current_cost==0:
        print("Se encontró una solución")
    print("Iteraciones ejecutadas:", steps)
    print("Estado final:", current)
    print("Costo final:", current_cost)
    print_board_ascii(current)
    fin=time.time()
    tiempo=fin-inicio
    print("tiempo: ",tiempo)
    return current,current_cost,steps,tiempo
'''
SIMULATED ANNEALING 
Estructura general del algoritmo

1.Calcular costo del estado actual
2.Si la temperatura actual no es menor a la temperatura mínima,
elegir al azar un vecino del estado actual
3.Si el vecino tiene menor costo, se acepta
4.Sino, se acepta con probabilidad decreciente
5."Enfriar" la temperatura
'''
def simulated_annealing(current,t0,alpha,tmin,max_steps:int | None):
    """
    Simulated Annealing algorithm to solve the N-Queens problem.
    
    Args:
        current (list): A list where current[i] is the row of the queen in column i.
        t0 (float): Initial temperature
        alpha (float): Cooling rate for geometrical schedule
        tmin (float): Minimum temperature
        max_steps (int|None): Maximum number of steps before giving up.

    Returns:
        tuple: (final_state, final_cost,final_steps,final_time)
    """
    inicio=time.time()
    #Calcular el costo del estado actual
    current_cost=cost(current)
    temperature=t0
    steps=0
    #Criterio de finalización
    while temperature>tmin:
        steps+=1
        if max_steps!=None:
            if steps==max_steps:
                print("Iteraciones máximas alcanzadas")
                break
        if current_cost==0:
            print("Se encontró una solución")
            break
        #Elegir un vecino al azar y calcular su costo
        neighbor=random.choice(generate_neighbors(current))
        neighbor_cost=cost(neighbor)
        cost_dif=neighbor_cost-current_cost
        if cost_dif<0:
            #El vecino tiene costo menor, entonces se acepta
            current=neighbor
            current_cost=neighbor_cost
        else:
            #Si el vecino tiene costo igual o peor al actual, se acepta con probabilidad decreciente
            prob=math.exp(-cost_dif/temperature)
            if random.random()<prob:
                current=neighbor
                current_cost=neighbor_cost
        #"Enfriar" la temperatura, función de schedule
        temperature*=alpha
    if temperature<=tmin:
        print("Se alcanzó la temperatura mínima")
    fin=time.time()
    tiempo=fin-inicio
    print("Iteraciones:", steps)
    print("Estado final:", current)
    print("Costo final:", current_cost)
    print("tiempo: ",tiempo)
    print_board_ascii(current)
    return current,current_cost,steps,tiempo

