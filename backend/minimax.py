import math

def evaluacion(costo, precio_propio, precio_rival, estrategia_propia, estrategia_rival):
    if precio_propio < costo:
        return -1000

    # Base de utilidad: Ganancia bruta (precio propio - costo)
    utilidad = (1+precio_propio - costo) * 10

    # Modificar utilidad según estrategias propias
    if estrategia_propia == "Agresivo":
        utilidad += (precio_rival - precio_propio) * 10  # Fomenta precios competitivos
    elif estrategia_propia == "Moderado":
        utilidad += (precio_propio - costo) * 5  # Prioriza ganancia sobre competencia
    elif estrategia_propia == "Conservador":
        utilidad += (precio_propio - costo) * 1  # Prioriza márgenes seguros

    # Ajustar utilidad según estrategias rivales
    if estrategia_rival == "Agresivo":
        utilidad -= (precio_propio - precio_rival) * 3  # Penaliza por no competir
    elif estrategia_rival == "Moderado":
        utilidad += 1  # Neutral
    elif estrategia_rival == "Conservador":
        utilidad += (precio_propio - precio_rival) * 3  # Beneficio por no competir

    # Penalización por estar fuera del rango razonable
    if precio_propio < precio_rival * 0.8:
        utilidad -= 20  # Penalización por precios demasiado bajos
    elif precio_propio > precio_rival * 1:
        utilidad -= 20  # Penalización por precios demasiado altos

    return utilidad




# Algoritmo Minimax
def minimax(nodo, profundidad, maximizador, costo, precio_min, precio_max, precio_rival, estrategia_propia, estrategia_rival):
    print(f"Minimax -> Nodo: {nodo}, Profundidad: {profundidad}, Maximizador: {maximizador}")
    if profundidad == 0 or es_terminal(nodo, precio_min, precio_max):
        return evaluacion(costo, nodo, precio_rival, estrategia_propia, estrategia_rival), nodo

    if maximizador:
        mejor_valor = -math.inf
        mejor_precio = None
        for precio in generar_sucesores(precio_min, precio_max):
            valor, _ = minimax(precio, profundidad - 1, False, costo, precio_min, precio_max, precio_rival, estrategia_propia, estrategia_rival)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_precio = precio
        return mejor_valor, max(precio_min, min(mejor_precio, precio_max))
    else:
        mejor_valor = math.inf
        mejor_precio = None
        for precio in generar_sucesores(precio_min, precio_max):
            valor, _ = minimax(precio, profundidad - 1, True, costo, precio_min, precio_max, precio_rival, estrategia_propia, estrategia_rival)
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_precio = precio
        return mejor_valor, max(precio_min, min(mejor_precio, precio_max))

# Algoritmo Alpha-Beta
def alpha_beta(nodo, profundidad, alfa, beta, maximizador, costo, precio_min, precio_max, precio_rival, estrategia_propia, estrategia_rival):
    if profundidad == 0 or es_terminal(nodo, precio_min, precio_max):
        return evaluacion(costo, nodo, precio_rival, estrategia_propia, estrategia_rival), nodo

    if maximizador:
        mejor_valor = -math.inf
        mejor_precio = None
        for precio in generar_sucesores(precio_min, precio_max):
            valor, _ = alpha_beta(precio, profundidad - 1, alfa, beta, False, costo, precio_min, precio_max, precio_rival, estrategia_propia, estrategia_rival)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_precio = precio
            alfa = max(alfa, valor)
            if alfa >= beta:
                break
        return mejor_valor, max(precio_min, min(mejor_precio, precio_max))
    else:
        mejor_valor = math.inf
        mejor_precio = None
        for precio in generar_sucesores(precio_min, precio_max):
            valor, _ = alpha_beta(precio, profundidad - 1, alfa, beta, True, costo, precio_min, precio_max, precio_rival, estrategia_propia, estrategia_rival)
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_precio = precio
            beta = min(beta, valor)
            if alfa >= beta:
                break
        return mejor_valor, max(precio_min, min(mejor_precio, precio_max))

# Función para determinar si un estado es terminal
def es_terminal(precio_actual, precio_min, precio_max):
    return precio_actual < precio_min or precio_actual > precio_max

def generar_sucesores(precio_min, precio_max, pasos=0.1):
    sucesores = []
    precio_actual = precio_min
    while precio_actual <= precio_max + 1: 
    # while precio_actual <= precio_max + 1e-9: 
        sucesores.append(round(precio_actual, 2))
        precio_actual += pasos
    print(f"Generando sucesores: {sucesores}")
    return sucesores

def validar_precio_optimo(precio_optimo, precio_min, precio_max):
    if precio_optimo < precio_min:
        return precio_min
    elif precio_optimo > precio_max:
        return precio_max
    return precio_optimo