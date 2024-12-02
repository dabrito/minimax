class MinimaxPricing:
    def __init__(self, max_depth=4):
        self.max_depth = max_depth
        self.best_move = None

    def minimax(self, state, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_terminal(state):
            return self.evaluate(state)

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_possible_moves(state):
                new_state = self.apply_move(state, move)
                eval = self.minimax(new_state, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    if depth == self.max_depth:
                        self.best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(state):
                new_state = self.apply_move(state, move)
                eval = self.minimax(new_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_possible_moves(self, state):
        # Generate possible price points based on constraints
        base_price = state['current_price']
        min_price = state['min_price']
        max_price = state['max_price']
        step = (max_price - min_price) / 10
        
        moves = []
        current = min_price
        while current <= max_price:
            moves.append(round(current, 2))
            current += step
        return moves

    def apply_move(self, state, move):
        new_state = state.copy()
        new_state['current_price'] = move
        return new_state

    def is_terminal(self, state):
        # Check if we've reached a terminal state
        return False

    def evaluate(self, state):
        # Calculate utility based on price, demand, and psychological factors
        price = state['current_price']
        cost = state['cost']
        demand = self.calculate_demand(state)
        
        # Basic profit calculation
        profit = (price - cost) * demand
        
        # Apply psychological factors
        psych_factor = self.calculate_psychological_factor(price)
        
        return profit * psych_factor

    def calculate_demand(self, state):
        # Simple linear demand function
        price = state['current_price']
        base_demand = 100  # Base demand at minimum price
        elasticity = 1.5   # Price elasticity
        
        demand = base_demand * (1 - elasticity * (price - state['min_price']) / 
                               (state['max_price'] - state['min_price']))
        return max(0, demand)

    def calculate_psychological_factor(self, price):
        # Apply psychological pricing effects
        # Returns a multiplier between 0.8 and 1.2
        
        # Check for .99 pricing
        if abs(round(price) - price - 0.99) < 0.01:
            return 1.2
        
        # Check for .95 pricing
        if abs(round(price) - price - 0.95) < 0.01:
            return 1.1
        
        return 1.0