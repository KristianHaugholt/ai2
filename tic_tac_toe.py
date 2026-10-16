import math
import time

from copy import deepcopy

State = tuple[int, list[list[int | None]]]  # Tuple of player (whose turn it is),
                                            # and board
Action = tuple[int, int]  # Where to place the player's piece

class Game:
    def initial_state(self) -> State:
        return (0, [[None, None, None], [None, None, None], [None, None, None]])

    def to_move(self, state: State) -> int:
        player_index, _ = state
        return player_index

    def actions(self, state: State) -> list[Action]:
        _, board = state
        actions = []
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    actions.append((row, col))
        return actions

    def result(self, state: State, action: Action) -> State:
        _, board = state
        row, col = action
        next_board = deepcopy(board)
        next_board[row][col] = self.to_move(state)
        return (self.to_move(state) + 1) % 2, next_board

    def is_winner(self, state: State, player: int) -> bool:
        _, board = state
        for row in range(3):
            if all(board[row][col] == player for col in range(3)):
                return True
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        return all(board[i][2 - i] == player for i in range(3))

    def is_terminal(self, state: State) -> bool:
        _, board = state
        if self.is_winner(state, (self.to_move(state) + 1) % 2):
            return True
        return all(board[row][col] is not None for row in range(3) for col in range(3))

    def utility(self, state, player):
        assert self.is_terminal(state)
        if self.is_winner(state, player):
            return 1
        if self.is_winner(state, (player + 1) % 2):
            return -1
        return 0

    def print(self, state: State):
        _, board = state
        print()
        for row in range(3):
            cells = [
                ' ' if board[row][col] is None else 'x' if board[row][col] == 0 else 'o'
                for col in range(3)
            ]
            print(f' {cells[0]} | {cells[1]} | {cells[2]}')
            if row < 2:
                print('---+---+---')
        print()
        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print(f'P1 won')
            elif self.utility(state, 1) > 0:
                print(f'P2 won')
            else:
                print('The game is a draw')
        else:
            print(f'It is P{self.to_move(state)+1}\'s turn to move')
            
            
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

import time
# Minimax
game = Game()
first=True

state = game.initial_state()
game.print(state)
while not game.is_terminal(state):
    player = game.to_move(state)
    start = time.perf_counter()
    action = minimax_search(game, state) # The player whose turn it is
                                         # is the MAX player
    end = time.perf_counter()
    if first: firstMiniMax = (end - start)                                 
    print(f'P{player+1}\'s action: {action}')
    assert action is not None
    state = game.result(state, action)
    game.print(state)
    first=False



# Alpha Pruning
game = Game()
first=True
state = game.initial_state()
game.print(state)
while not game.is_terminal(state):
    player = game.to_move(state)
    start = time.perf_counter()
    action = alpha_beta_pruning(game, state) # The player whose turn it is
                                             # is the MAX player
    end = time.perf_counter()
    if first: firstAlphaBeta = (end - start)
    print(f'P{player+1}\'s action: {action}')
    assert action is not None
    state = game.result(state, action)
    game.print(state)
    first=False

print(f"Elapsed first move (Minimax): {firstMiniMax} s")
print(f"Elapsed first move (Alpha-Beta): {firstAlphaBeta} s")
print(f"Speedup: {firstMiniMax/firstAlphaBeta:.2f}x faster with Alpha-Beta pruning")


##############################################################################
# Non-mandatory (Section 4.1): Prioritizing quicker wins
class FastWinGame(Game):
    def utility(self, state: State, player: int) -> float:
        assert self.is_terminal(state)
        empty = sum(row.count(None) for row in state[1])
        if self.is_winner(state, player):
            return 1 + empty
        if self.is_winner(state, (player + 1) % 2):
            return -(1 + empty)
        return 0


print("\n--- Non-mandatory: Standard Game ---")
game = Game()
state: State = (0, [[0, 1, 1], [0, None, None], [None, None, None]])
game.print(state)
while not game.is_terminal(state):
    player = game.to_move(state)
    action = minimax_search(game, state)
    print(f'P{player+1}\'s action: {action}')
    assert action is not None
    state = game.result(state, action)
    game.print(state)

print("\n--- Non-mandatory: FastWinGame ---")
fast_game = FastWinGame()
state = (0, [[0, 1, 1], [0, None, None], [None, None, None]])
fast_game.print(state)
while not fast_game.is_terminal(state):
    player = fast_game.to_move(state)
    action = minimax_search(fast_game, state)
    print(f'P{player+1}\'s action: {action}')
    assert action is not None
    state = fast_game.result(state, action)
    fast_game.print(state)