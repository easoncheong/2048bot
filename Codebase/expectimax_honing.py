import gamestate
import expectimax_heuristics
import math

gameState = gamestate.GameState()
heuristics = expectimax_heuristics.heuristics()

def honing_heuristics(position, scale):
    eval = 0
    eval += heuristics.dynamic_mono(position)
    #eval += 100 * heuristics.static_mono(position)
    eval += 2 * heuristics.smoothness(position)
    eval += scale * heuristics.risk(position)

    return eval

def expectimax(position, depth, scale):
    

    if len(gameState.list_legal_moves(position)) == 0 and depth % 2 == 0:
        ev = (10 ** 5) * 3
    

    elif depth == 0:
        ev = honing_heuristics(position, scale)

    elif depth % 2 == 0:
        ev = math.inf
        childNodes = [
            gameState.left_position(position, False),
            gameState.down_position(position, False),
            gameState.up_position(position, False),
            gameState.right_position(position, False)
        ]

        for child in childNodes:
            if gameState.free_squares(child) == []:
                continue
            ev = min(ev, expectimax(child, depth - 1, scale))

    elif depth % 2 == 1:
        ev = 0
        childSquares = gameState.free_squares(position)
        childNodes2 = []
        childNodes4 = []
        for square in childSquares:
            childNodes2.append(gameState.add_specific_tile(position, 2, square))
            childNodes4.append(gameState.add_specific_tile(position, 4, square))
        
        for child in childNodes2:
            ev += 0.9 * expectimax(child, depth - 1, scale)
        
        for child in childNodes4:
            ev += 0.1 * expectimax(child, depth - 1, scale)

        if len(childSquares):
            ev /= len(childSquares)
        else:
            return ev ** 2
    
    return ev

def search(position, move, legal, scale):
    if len(legal) == 1: return legal[0]

    leftPosition = gameState.left_position(position, False)
    downPosition = gameState.down_position(position, False)
    upPosition = gameState.up_position(position, False)
    rightPosition = gameState.right_position(position, False)

    
    fSLen = len(gameState.free_squares(position))
    if fSLen < 3:
        n = 9
    elif fSLen < 6:
        n = 7
    elif fSLen < 9:
        n = 5
    else:
        n = 3

    cIndices, indices = [], []
    
    for i, j in enumerate([leftPosition, downPosition, upPosition, rightPosition]):
        if i in legal:
            cIndices.append(expectimax(j, n, scale))
            indices.append(i)

    while True:
        indexTarget = cIndices.index(min(cIndices))
        if indices[indexTarget] in legal:
            return indices[indexTarget]
        else:
            indices.pop(indexTarget)
            cIndices.pop(indexTarget)
    