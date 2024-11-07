from utility import utility_function

def minimax(depth, is_maximizing_player, own_price, rival_price, cost, own_price_options, rival_price_options):
    # Implementación del algoritmo Minimax.
    if depth == 0:
        return utility_function(own_price, rival_price, cost)

    if is_maximizing_player:
        max_eval = float('-inf')
        for price in own_price_options:
            eval = minimax(depth - 1, False, price, rival_price, cost, own_price_options, rival_price_options)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for price in rival_price_options:
            eval = minimax(depth - 1, True, own_price, price, cost, own_price_options, rival_price_options)
            min_eval = min(min_eval, eval)
        return min_eval

def find_optimal_price(cost, own_price_options, rival_price_options, rival_current_price):
    # Encuentra el precio óptimo utilizando Minimax.
    best_price = None
    best_profit = float('-inf')

    for price in own_price_options:
        profit = minimax(
            depth=1,
            is_maximizing_player=False,
            own_price=price,
            rival_price=rival_current_price,
            cost=cost,
            own_price_options=own_price_options,
            rival_price_options=rival_price_options
        )
        if profit > best_profit:
            best_profit = profit
            best_price = price

    return best_price, best_profit
