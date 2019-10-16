import expectimax_heuristics
import gamestate
import math

gameState = gamestate.GameState()
heuristics = expectimax_heuristics.heuristics()

def primary_heuristics(position):
    pass

def honing_heuristics(position, scale):
    eval = 0
    return eval

def expectimax(position, depth):
    
    if len(gameState.list_legal_moves(gameState)) == 0 and depth % 2 == 0:
        return (10 ** 7) * 7
    elif depth == 0:
        return primary_heuristics(position)

    elif depth % 2 == 0:
        ev = math.inf
        childNodes = [
            gameState.left_position(position, False),
            gameState.down_position(position, False),
            gameState.up_position(position, False),
            gameState.right_position(position, False)
        ]

        for child in childNodes:
            if gameState.free_squares(position) == []:
                continue
            ev = min(ev, expectimax(child, depth - 1))
        
    elif depth % 2 == 1:
        ev = 0
        childSquares = gameState.free_squares(position)
        childNodes2 = []
        childNodes4 = []
        for square in childSquares:
            childNodes2.append(gameState.add_specific_tile(position, 2, square))
            childNodes4.append(gameState.add_specific_tile(position, 4, square))
        
        for child in childNodes2:
            ev += (0.9 / len(childSquares)) * expectimax(child, depth - 1)
        
        for child in childNodes4:
            ev += (0.9 / len(childSquares)) * expectimax(child, depth - 1)

    return ev