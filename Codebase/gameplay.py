import random
import math
import gamestate

'''
Gameplay Classes
'''

class Game:

    gameState = gamestate.GameState()

    FUNCT_LIST = [
        gameState.left_position,
        gameState.down_position,
        gameState.up_position,
        gameState.right_position
    ]

    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.score = 0
        self.position = [[0 for _ in range(4)] for _ in range(4)]

    def make_move(self, move):
        if move in self.gameState.list_legal_moves(self.position):
            self.position, scoreIncrease = self.FUNCT_LIST[move](self.position, True)
            self.position = self.gameState.add_new_tile(self.position)
            self.score += scoreIncrease
            return True
        else:
            return False

    def game_active(self):
        return self.gameState.list_legal_moves(self.position) != []

    def play_game(self):

        moves_count = 0
        for _ in range(2):
            self.position = self.gameState.add_new_tile(self.position)

        while self.game_active():
            moves_count += 1
            legal_positions = self.gameState.list_legal_moves(self.position)
            move_selected = self.algorithm(self.position, moves_count, legal_positions)
            while not self.make_move(move_selected):
                move_selected = self.algorithm(self.position, moves_count, legal_positions)
        
        log_perm = self.gameState.logPerm(self.position)
        tile_perm = self.gameState.tilePerm(self.position)

        return log_perm, tile_perm, self.position, self.score

    def play_game_scaled(self, scale):

        f = open('DeepSearch.txt', 'w+')

        moves_count = 0
        for _ in range(2):
            self.position = self.gameState.add_new_tile(self.position)

        while self.game_active():
            moves_count += 1
            legal_positions = self.gameState.list_legal_moves(self.position)
            move_selected = self.algorithm(self.position, moves_count, legal_positions, scale)
            while not self.make_move(move_selected):
                move_selected = self.algorithm(self.position, moves_count, legal_positions, scale)
            f.write('Move ' + str(moves_count) + '\n')
            for i in self.position:
                f.write(str(i) + '\n')
            f.write(['Left', 'Down', 'Up', 'Right'][move_selected] + ' Move was made.\n\n')
            print(moves_count)
            for i in self.position:
                print(i)
            print(['Left', 'Down', 'Up', 'Right'][move_selected])
        log_perm = self.gameState.logPerm(self.position)
        tile_perm = self.gameState.tilePerm(self.position)

        f.close()
        
        return log_perm, tile_perm, self.position, self.score

    