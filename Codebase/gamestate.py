import random
import math

class GameState:

    '''
    Directory of All Moves:
    L (0) refers to Left Move
    D (1) refers to Down Move
    U (2) refers to Up Move
    R (3) refers to Right Move
    '''


    # BASE FUNCTIONS
    # These Functions anchor the entire Game State

    def row(self, position, number):
        return position[number]
    
    def column(self, position, number):
        return list(map(list, zip(*position)))[number]

    def transpose(self, pos):
        position = pos[:]
        return list(map(list, zip(*position)))

    def flip(self, pos):
        position = pos[:]
        n = []
        for i in position:
            n.append(i[::-1])
        return n

    def base_move(self, pos, calculateScore):
        scoreIncrease = 0
        position = pos[:]
        newPos = []
        
        for i in position:
            i = list(filter(lambda x: bool(x), i))
            for cnt in range(len(i) - 1):
                if i[cnt] == i[cnt+1]:
                    i[cnt] = 2 * i[cnt]
                    i[cnt + 1] = 0
                    scoreIncrease = i[cnt]
            i = list(filter(lambda x: bool(x), i))

            i = i + [ 0 for _ in range(4 - len(i))]

            newPos.append(i)

        if calculateScore:
            return newPos, scoreIncrease
        else:
            return newPos

    # POSITION OBTAINING FUNCTIONS

    def left_position(self, pos, calculateScore):
        position = pos[:]
        return self.base_move(position, calculateScore)

    def right_position(self, pos, calculateScore):
        position = pos[:]
        position = self.flip(position)
        if calculateScore:
            newPosition, scoreIncrease = self.base_move(position, calculateScore)
            return self.flip(newPosition), scoreIncrease
        return self.flip(self.base_move(position, calculateScore))

    def up_position(self, pos, calculateScore):
        position = pos[:]
        position = self.transpose(position)
        if calculateScore:
            newPosition, scoreIncrease = self.base_move(position, calculateScore)
            return self.transpose(newPosition), scoreIncrease
        return self.transpose(self.base_move(position, calculateScore))

    def down_position(self, pos, calculateScore):
        position = pos[:]
        position = self.transpose(position)
        position = self.flip(position)
        if calculateScore:
            position, scoreIncrease = self.base_move(position, calculateScore)
        else:
            position = self.base_move(position, calculateScore)
        position = self.flip(position)
        position = self.transpose(position)
        if calculateScore:
            return position, scoreIncrease
        return position

    # GAME STATE SPECIAL FUNCTIONS

    def list_legal_moves(self, position):
        legal_moves = [0, 1, 2, 3]

        if self.left_position(position[:], False) == position:
            legal_moves.remove(0)

        if self.down_position(position[:], False) == position:
            legal_moves.remove(1)

        if self.up_position(position[:], False) == position:
            legal_moves.remove(2)

        if self.right_position(position[:], False) == position:
            legal_moves.remove(3)

        return legal_moves

    def free_squares(self, position):
        free_squares_list = []

        for r in range(4):
            for c in range(4):
                if position[r][c] == 0:
                    free_squares_list.append((r, c))
        
        return free_squares_list

    def logPerm(self, position):
        
        s = 0
        for i in position: s += sum(i)
        
        return math.log2(s)

    def tilePerm(self, position):

        s = []
        for i in position: s += i

        return math.log2(max(s)) + 0.95


    # TILE ADDING

    def add_specific_tile(self, pos, value, square):

        position = pos[:]

        r, c = square

        position[r][c] = value

        return position

    def add_new_tile(self, pos):

        position = pos[:]

        value = 2 if random.uniform(0, 1) < 0.9 else 4
        free_squares = self.free_squares(position)

        if len(free_squares) == 0:
            return None

        selected_square = free_squares[random.randint(0, len(free_squares) - 1)]
        r, c = selected_square

        position[r][c] = value

        return position