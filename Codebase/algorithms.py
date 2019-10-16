import gamestate
import random
import math
import algorithmbase

gameState = gamestate.GameState()
algoBase = algorithmbase.AlgoBase()

'''
FUNCTION GUIDELINES

All functions take in 3 arguments:
Position, Move Count, Legal Moves

All functions output an integer 0 to 3
0 > Left
1 > Down
2 > Up
3 > Right
'''



''' Random Function '''

def random_play(position, move, legal):
    return random.choice(legal)

''' Corner Function '''

def corner_play(position, move, legal):
    if move % 2 == 0:
        if 0 in legal: return 0
        elif 1 in legal: return 1
        elif 2 in legal: return 2
        elif 3 in legal: return 3
    
    if move % 2 == 1:
        if 1 in legal: return 1
        elif 0 in legal: return 0
        elif 2 in legal: return 2
        elif 3 in legal: return 3

''' Corner Risk Function '''

def corner_risk(position, move, legal):

    if len(legal) == 1: return legal[0]

    leftPosition = gameState.left_position(position, False)
    downPosition = gameState.down_position(position, False)
    upPosition = gameState.up_position(position, False)
    rightPosition = gameState.right_position(position, False)

    leftRiskIndex = algoBase.risk_position(leftPosition)
    downRiskIndex = algoBase.risk_position(downPosition)
    upRiskIndex = algoBase.risk_position(upPosition)
    rightRiskIndex = algoBase.risk_position(rightPosition)

    riskIndices = [leftRiskIndex, downRiskIndex, upRiskIndex]
    indexList = [0, 1, 2]


    if max(riskIndices + [rightRiskIndex]) < 0.15:
        while True:
            indexTarget = riskIndices.index(min(riskIndices))
            if indexList[indexTarget] in legal:
                return indexList[indexTarget]
            else:
                indexList.pop(indexTarget)
                riskIndices.pop(indexTarget)
    
    if min(riskIndices + [rightRiskIndex]) > 0.15:
        if len(gameState.free_squares(position)) < 3:
            riskIndices.append(rightRiskIndex)
            indexList.append(3)
        while True:
            indexTarget = riskIndices.index(min(riskIndices))
            if indexList[indexTarget] in legal:
                return indexList[indexTarget]
            else:
                indexList.pop(indexTarget)
                riskIndices.pop(indexTarget)

    riskyIndexList = []
    riskyRiskIndexes = []

    for cnt, i in enumerate(riskIndices[:]):
        if i > 0.15:
            indexList.remove(cnt)
            riskyIndexList.append(cnt)
            riskIndices.remove(i)
            riskyRiskIndexes.append(i)

    while indexList:
        indexTarget = riskIndices.index(min(riskIndices))
        if indexList[indexTarget] in legal:
            return indexList[indexTarget]
        else:
            indexList.pop(indexTarget)
            riskIndices.pop(indexTarget)
    
    while riskyIndexList:
        indexTarget = riskyRiskIndexes.index(min(riskyRiskIndexes))
        if riskyIndexList[indexTarget] in legal:
            return riskyIndexList[indexTarget]
        else:
            riskyIndexList.pop(indexTarget)
            riskyRiskIndexes.pop(indexTarget)

    return legal[0]


''' Corner Index '''

def corner_index(position, move, legal):
    
    if len(legal) == 1: return legal[0]

    leftPosition = gameState.left_position(position, False)
    downPosition = gameState.down_position(position, False)
    upPosition = gameState.up_position(position, False)
    rightPosition = gameState.right_position(position, False)

    cIndices = [
        algoBase.corner_index(leftPosition), 
        algoBase.corner_index(downPosition), 
        algoBase.corner_index(upPosition), 
        algoBase.corner_index(rightPosition)
    ]
    indices = [0, 1, 2, 3]

    while True:
        indexTarget = cIndices.index(max(cIndices))
        if indices[indexTarget] in legal:
            return indices[indexTarget]
        else:
            indices.pop(indexTarget)
            cIndices.pop(indexTarget)

''' Dyn Merge Function '''

def dynamic_merge(position, move, legal):

    if len(legal) == 1: return legal[0]

    leftPosition = gameState.left_position(position, False)
    downPosition = gameState.down_position(position, False)
    upPosition = gameState.up_position(position, False)
    rightPosition = gameState.right_position(position, False)

    mergeIndices = [
        algoBase.merge_position(leftPosition), 
        algoBase.merge_position(downPosition), 
        algoBase.merge_position(upPosition), 
        algoBase.merge_position(rightPosition)
    ]
    indices = [0, 1, 2, 3]

    while True:
        indexTarget = mergeIndices.index(max(mergeIndices))
        if indices[indexTarget] in legal:
            return indices[indexTarget]
        else:
            indices.pop(indexTarget)
            mergeIndices.pop(indexTarget)
    

''' Greedy '''

def greedy_score(position, move, legal):
    left = gameState.left_position(position, True)[1]
    down = gameState.down_position(position, True)[1]
    up = gameState.up_position(position, True)[1]
    right = gameState.right_position(position, True)[1]

    scores = [left, down, up, right]
    indices = [0, 1, 2, 3]

    while True:
        indexTarget = scores.index(max(scores))
        if indices[indexTarget] in legal:
            return indices[indexTarget]
        else:
            indices.pop(indexTarget)
            scores.pop(indexTarget)


''' Static Monotonicity '''

def static_monotonicity(position, move, legal):

    if len(legal) == 1: return legal[0]

    leftPosition = gameState.left_position(position, False)
    downPosition = gameState.down_position(position, False)
    upPosition = gameState.up_position(position, False)
    rightPosition = gameState.right_position(position, False)

    monotonicity_indices = [
        algoBase.static_monotonicity(leftPosition), 
        algoBase.static_monotonicity(downPosition), 
        algoBase.static_monotonicity(upPosition), 
        algoBase.static_monotonicity(rightPosition)
    ]
    indices = [0, 1, 2, 3]

    while True:
        indexTarget = monotonicity_indices.index(min(monotonicity_indices))
        if indices[indexTarget] in legal:
            return indices[indexTarget]
        else:
            indices.pop(indexTarget)
            monotonicity_indices.pop(indexTarget)


def dynamic_monotonicity(position, move, legal):

    if len(legal) == 1: return legal[0]

    leftPosition = gameState.left_position(position, False)
    downPosition = gameState.down_position(position, False)
    upPosition = gameState.up_position(position, False)
    rightPosition = gameState.right_position(position, False)

    monotonicity_indices = [
        algoBase.dynamic_monotonicity(leftPosition), 
        algoBase.dynamic_monotonicity(downPosition), 
        algoBase.dynamic_monotonicity(upPosition), 
        algoBase.dynamic_monotonicity(rightPosition)
    ]
    indices = [0, 1, 2, 3]

    while True:
        indexTarget = monotonicity_indices.index(min(monotonicity_indices))
        if indices[indexTarget] in legal:
            return indices[indexTarget]
        else:
            indices.pop(indexTarget)
            monotonicity_indices.pop(indexTarget)


''' Smoothness Index '''

def smoothness(position, move, legal):

    if len(legal) == 1: return legal[0]

    leftPosition = gameState.left_position(position, False)
    downPosition = gameState.down_position(position, False)
    upPosition = gameState.up_position(position, False)
    rightPosition = gameState.right_position(position, False)

    sIndices = [
        algoBase.smoothness(leftPosition), 
        algoBase.smoothness(downPosition), 
        algoBase.smoothness(upPosition), 
        algoBase.smoothness(rightPosition)
    ]
    indices = [0, 1, 2, 3]

    while True:
        indexTarget = sIndices.index(min(sIndices))
        if indices[indexTarget] in legal:
            return indices[indexTarget]
        else:
            indices.pop(indexTarget)
            sIndices.pop(indexTarget)


''' Free Squares '''

def free_squares(position, move, legal):
    left = gameState.free_squares(gameState.left_position(position, False))
    down = gameState.free_squares(gameState.down_position(position, False))
    up = gameState.free_squares(gameState.up_position(position, False))
    right = gameState.free_squares(gameState.right_position(position, False))

    scores = [len(left), len(down), len(up), len(right)]
    indices = [0, 1, 2, 3]

    while True:
        indexTarget = scores.index(max(scores))
        if indices[indexTarget] in legal:
            return indices[indexTarget]
        else:
            indices.pop(indexTarget)
            scores.pop(indexTarget)