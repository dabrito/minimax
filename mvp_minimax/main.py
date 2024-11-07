# main.py

import json
from minimax import find_optimal_price

def main():
    # Cargar datos del producto y del rival
    with open('mvp_minimax/data/product_data.json', 'r') as f:
        product_data = json.load(f)

    with open('mvp_minimax/data/rival_data.json', 'r') as f:
        rival_data = json.load(f)

    # Extraer información relevante
    COST = product_data['cost']
    MIN_PRICE = product_data['min_price']
    MAX_PRICE = product_data['max_price']
    PRICE_STEP = 10  # Incrementos de precio

    OWN_PRICE_OPTIONS = list(range(MIN_PRICE, MAX_PRICE + PRICE_STEP, PRICE_STEP))

    RIVAL_CURRENT_PRICE = rival_data['price']
    RIVAL_PRICE_STEP = 10  # Suponemos el mismo incremento para el rival
    RIVAL_PRICE_OPTIONS = [
        RIVAL_CURRENT_PRICE - RIVAL_PRICE_STEP,
        RIVAL_CURRENT_PRICE,
        RIVAL_CURRENT_PRICE + RIVAL_PRICE_STEP
    ]

    # Asegurar que los precios del rival están dentro de un rango válido
    RIVAL_PRICE_OPTIONS = [price for price in RIVAL_PRICE_OPTIONS if price > 0]

    # Encontrar el precio óptimo
    optimal_price, expected_profit = find_optimal_price(
        cost=COST,
        own_price_options=OWN_PRICE_OPTIONS,
        rival_price_options=RIVAL_PRICE_OPTIONS,
        rival_current_price=RIVAL_CURRENT_PRICE
    )

    # Mostrar resultados
    print(f"Precio óptimo sugerido: ${optimal_price}")
    print(f"Ganancias esperadas: ${expected_profit}")

if __name__ == "__main__":
    main()
