import algorithmbase
import gamestate

algoBase = algorithmbase.AlgoBase()
gameState = gamestate.GameState()

class heuristics:

    def dynamic_mono(self, position):
        return algoBase.dynamic_monotonicity_base(position)

    def static_mono(self, position):
        return algoBase.static_monotonicity_base(position)
    
    def smoothness(self, position):
        return algoBase.smoothness_base(position)

    ''' weak '''

    def greedy(self, position):
        left = gameState.left_position(position, True)[1]
        down = gameState.down_position(position, True)[1]
        return 40000 - left+down

    def dyn_merge(self, position):
        return 40000 - algoBase.merge_position_base(position)

    ''' testing cases '''

    def risk(self, position):
        return 1 if len(gameState.list_legal_moves(position)) < 2 else 0