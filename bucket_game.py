import math

State = tuple[int, list[str | int]]  # Tuple of player (whose turn it is),
                                     # and the buckets (as str)
                                     # or the number in a bucket
Action = str | int  # Bucket choice (as str) or choice of number


class Game:
    def initial_state(self) -> State:
        return 0, ['A', 'B', 'C']

    def to_move(self, state: State) -> int:
        player, _ = state
        return player

    def actions(self, state: State) -> list[Action]:
        _, actions = state
        return actions

    def result(self, state: State, action: Action) -> State:
        if action == 'A':
            return (self.to_move(state) + 1) % 2, [-50, 50]
        elif action == 'B':
            return (self.to_move(state) + 1) % 2, [3, 1]
        elif action == 'C':
            return (self.to_move(state) + 1) % 2, [-5, 15]
        assert type(action) is int
        return (self.to_move(state) + 1) % 2, [action]

    def is_terminal(self, state: State) -> bool:
        _, actions = state
        return len(actions) == 1

    def utility(self, state: State, player: int) -> float:
        assert self.is_terminal(state)
        _, actions = state
        assert type(actions[0]) is int
        return actions[0] if player == self.to_move(state) else -actions[0]

    def print(self, state):
        print(f'The state is {state} and ', end='')
        if self.is_terminal(state):
            print(f'P1\'s utility is {self.utility(state, 0)}')
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
game = Game()

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
game = Game()

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






