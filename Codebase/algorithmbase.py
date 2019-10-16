import math
import random
import gamestate

gameState = gamestate.GameState()

class AlgoBase:

    ''' Merge ''' 

    def merge_row(self, row):
        mergeIX = 0
        i = row[:]
        i = list(filter(lambda x: bool(x), i))
        for cnt in range(len(i) - 1):
            if i[cnt] == i[cnt+1]:
                i[cnt] = 2 * i[cnt]
                i[cnt + 1] = 0
                mergeIX += math.log2(i[cnt]) ** 2
        i = list(filter(lambda x: bool(x), i))
        return mergeIX

    def merge_position_base(self, pos):
        mergeIX = 0
        position = pos[:]
        for n in range(4):
            row = gameState.row(position, n)
            mergeIX += self.merge_row(row)
            col = gameState.column(position, n)
            mergeIX += self.merge_row(col)

        return mergeIX

    def merge_position(self, position):
        mergeIX = 0
        possibleSpawns = gameState.free_squares(position)
        for spawn in possibleSpawns:
            possiblePosition = gameState.add_specific_tile(position, 2, spawn)
            mergeIX += 0.9 * self.merge_position_base(possiblePosition)
            possiblePosition = gameState.add_specific_tile(position, 4, spawn)
            mergeIX += 0.1 * self.merge_position_base(possiblePosition)
        if len(possibleSpawns):
            mergeIX /= len(possibleSpawns)
        else:
            mergeIX = 0
        return mergeIX



    def risk_position(self, pos):
        position = pos[:]
        riskIndex = 0
        possibleSpawns = gameState.free_squares(position)
        for spawn in possibleSpawns:
            rightPossiblePosition = gameState.add_specific_tile(position, 2, spawn)
            if len(gameState.list_legal_moves(rightPossiblePosition)) < 2:
                riskIndex += 0.9
            rightPossiblePosition = gameState.add_specific_tile(position, 4, spawn)
            if len(gameState.list_legal_moves(rightPossiblePosition)) < 2:
                riskIndex += 0.1
        if len(possibleSpawns):
            riskIndex /= len(possibleSpawns)
        else:
            riskIndex = 2

        return riskIndex

    
    ''' Static Monotonicity '''
    
    def monotonicity_core(self, n1, n2):
        if n1 == n2:
            return '='
        if n1 > n2:
            return '>'
        if n1 < n2:
            return '<'

    def static_monotonicity_row(self, pos):
        position = pos[:]
        string = ''
        for cnt, i in enumerate(position[:len(position) - 1]):
            string += self.monotonicity_core(i, position[cnt+1])
        return min(string.count('>'), string.count('<'))

    def static_monotonicity_base(self, pos):
        monotonicity_index = 0
        position = pos[:]
        for n in range(4):
            row = gameState.row(position, n)
            monotonicity_index += self.static_monotonicity_row(row)
            col = gameState.column(position, n)
            monotonicity_index += self.static_monotonicity_row(col)

        return monotonicity_index

    def static_monotonicity(self, pos):
        position = pos[:]
        monotonicity = 0
        possibleSpawns = gameState.free_squares(position)
        for spawn in possibleSpawns:
            possiblePosition = gameState.add_specific_tile(position, 2, spawn)
            monotonicity += 0.9 * self.static_monotonicity_base(possiblePosition)
            possiblePosition = gameState.add_specific_tile(position, 4, spawn)
            monotonicity += 0.1 * self.static_monotonicity_base(possiblePosition)
        if len(possibleSpawns):
            monotonicity /= len(possibleSpawns)
        else:
            monotonicity = 100
        return monotonicity

    
    ''' Dynamic Monotonicity '''

    def zeroIfNeg(self, N):
        if N < 0:
            return 0
        else:
            return N

    def dynamic_monotonicity_row(self, pos):
        position = pos[:]
        m1 = self.zeroIfNeg(position[1] - position[0]) + self.zeroIfNeg(position[2] - position[1]) \
            + self.zeroIfNeg(position[3] - position[2])
        m2 = self.zeroIfNeg(position[0] - position[1]) + self.zeroIfNeg(position[1] - position[2]) \
            + self.zeroIfNeg(position[2] - position[3])

        return min(m1, m2)
        
    def dynamic_monotonicity_base(self, pos):
        monotonicity_index = 0
        position = pos[:]
        for n in range(4):
            row = gameState.row(position, n)
            monotonicity_index += self.dynamic_monotonicity_row(row)
            col = gameState.column(position, n)
            monotonicity_index += self.dynamic_monotonicity_row(col)

        return monotonicity_index

    def dynamic_monotonicity(self, pos):
        position = pos[:]
        monotonicity = 0
        possibleSpawns = gameState.free_squares(position)
        for spawn in possibleSpawns:
            possiblePosition = gameState.add_specific_tile(position, 2, spawn)
            monotonicity += 0.9 * self.dynamic_monotonicity_base(possiblePosition)
            possiblePosition = gameState.add_specific_tile(position, 4, spawn)
            monotonicity += 0.1 * self.dynamic_monotonicity_base(possiblePosition)
        if len(possibleSpawns):
            monotonicity /= len(possibleSpawns)
        else:
            monotonicity = 10 ** 8
        return monotonicity

    
    ''' Smoothness '''

    def smoothness_row(self, pos):
        return abs(pos[0]-pos[1]) + abs(pos[1] - pos[2]) + abs(pos[2] - pos[3])
    
    def smoothness_base(self, pos):
        smoothness_index = 0
        position = pos[:]
        for n in range(4):
            row = gameState.row(position, n)
            smoothness_index += self.smoothness_row(row)
            col = gameState.column(position, n)
            smoothness_index += self.smoothness_row(col)
        return smoothness_index
    
    def smoothness(self, pos):
        position = pos[:]
        smoothness = 0
        possibleSpawns = gameState.free_squares(position)
        for spawn in possibleSpawns:
            possiblePosition = gameState.add_specific_tile(position, 2, spawn)
            smoothness += 0.9 * self.smoothness_base(possiblePosition)
            possiblePosition = gameState.add_specific_tile(position, 4, spawn)
            smoothness += 0.1 * self.smoothness_base(possiblePosition)
        if len(possibleSpawns):
            smoothness /= len(possibleSpawns)
        else:
            smoothness = 10 ** 8
        return smoothness


    ''' Corner Index '''

    CORNER_INDEX = [
        [6.5, 3, -2, -3],
        [7, 1, -1.8, -3.5],
        [8, 0.7, -1.5, -3.7],
        [10, 0.5, -0.5, -3.8]
    ]

    def corner_index_base(self, pos):
        cIndex = 0
        for i in range(3):
            for j in range(3):
                cIndex += self.CORNER_INDEX[i][j] * pos[i][j]
        return cIndex
    
    def corner_index(self, pos):
        position = pos[:]
        cIndex = 0
        possibleSpawns = gameState.free_squares(position)
        for spawn in possibleSpawns:
            possiblePosition = gameState.add_specific_tile(position, 2, spawn)
            cIndex += 0.9 * self.corner_index_base(possiblePosition)
            possiblePosition = gameState.add_specific_tile(position, 4, spawn)
            cIndex += 0.1 * self.corner_index_base(possiblePosition)
        if len(possibleSpawns):
            cIndex /= len(possibleSpawns)
        else:
            cIndex = 10 ** 8
        return cIndex