def calculate_demand(own_price, rival_price):
    # Calcula la demanda basada en el precio propio y el precio del rival.
    if own_price < rival_price:
        demand = 100  # Demanda alta
    elif own_price == rival_price:
        demand = 50   # Demanda media
    else:
        demand = 10   # Demanda baja
    return demand

def utility_function(own_price, rival_price, cost):
    # Calcula la utilidad (ganancias) dadas los precios y el costo.
    demand = calculate_demand(own_price, rival_price)
    profit = (own_price - cost) * demand
    return profit
