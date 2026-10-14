import math

State = tuple[int, int] # Tuple of player (whose turn it is),
                        # and the number to be decreased
Action = str  # Decrement (number <- number-1) or halve (number <- number / 2)

class Game:
    def __init__(self, N: int):
        self.N = N

    def initial_state(self) -> State:
        return 0, self.N

    def to_move(self, state: State) -> int:
        player, _ = state
        return player

    def actions(self, state: State) -> list[Action]:
        return ['--', '/2']

    def result(self, state: State, action: Action) -> State:
        _, number = state
        if action == '--':
            return (self.to_move(state) + 1) % 2, number - 1
        else:
            return (self.to_move(state) + 1) % 2, number // 2  # Floored division

    def is_terminal(self, state: State) -> bool:
        _, number = state
        return number == 0

    def utility(self, state: State, player: int) -> float:
        assert self.is_terminal(state)
        return 1 if self.to_move(state) == player else -1

    def print(self, state: State):
        _, number = state
        print(f'The number is {number} and ', end='')
        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print(f'P1 won')
            else:
                print(f'P2 won')
        else:
            print(f'it is P{self.to_move(state)+1}\'s turn')
            
##############################################################################
# YOUR CODE HERE
def max_value(game, state):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -math.inf, -math.inf
        for a in game.actions(state):
            v2, a2 = min_value(game, game.result(state, a))
            if v2>v:
                v, move = v2, a
        return v, move

def min_value(game, state):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = math.inf, math.inf
        for a in game.actions(state):
            v2, a2 = max_value(game, game.result(state, a))
            if v2<v:
                v, move = v2, a
        return v, move
    
def minimax_search(game: Game, state: State) -> Action | None:
    player = game.to_move(state)
    value, move = max_value(game, state)
    return move
##############################################################################
# YOUR CODE HERE
def Max_value(game, state, alpha, beta):
    if game.is_terminal(state):
        return game.utility(state, player), None
    v = -math.inf
    for a in game.actions(state):
        v2, a2 = Min_value(game, game.result(state, a), alpha, beta)
        if v2>v:
            v, move = v2, a
            alpha = max(alpha, v)
        if v>=beta:
            return v, move
    return v, move


def Min_value(game, state, alpha, beta):
    if game.is_terminal(state):
        return game.utility(state, player), None
    v = math.inf
    for a in game.actions(state):
        v2, a2 = Max_value(game, game.result(state, a), alpha, beta)
        if v2<v:
            v, move = v2, a
            beta = min(beta, v)
        if v <= alpha:
            return v, move
    return v, move


def alpha_beta_pruning(game: Game, state: State) -> Action | None:
    player = game.to_move(state)
    value, move = Max_value(game, state, -math.inf, math.inf)
    return move
############################################################################


# Minimax
game = Game(5)

state = game.initial_state()
game.print(state)
while not game.is_terminal(state):
    player = game.to_move(state)
    action = minimax_search(game, state) # The player whose turn it is
                                         # is the MAX player
    print(f'P{player+1}\'s action: {action}')
    assert action is not None
    state = game.result(state, action)
    game.print(state)


# Alpha Pruning
game = Game(5)

state = game.initial_state()
game.print(state)
while not game.is_terminal(state):
    player = game.to_move(state)
    action = alpha_beta_pruning(game, state) # The player whose turn it is
                                             # is the MAX player
    print(f'P{player+1}\'s action: {action}')
    assert action is not None
    state = game.result(state, action)
    game.print(state)



# Expected output:
# The number is 5 and it is P1's turn
# P1's action: --
# The number is 4 and it is P2's turn
# P2's action: --
# The number is 3 and it is P1's turn
# P1's action: /2
# The number is 1 and it is P2's turn
# P2's action: --
# The number is 0 and P1 won


