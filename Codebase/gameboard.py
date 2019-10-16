import algorithms
import gameplay

'''
This is the command centre where algorithms are tested.
'''

# The Algorithm Used
ALGORITHM = algorithms.dynamic_monotonicity
ALGORITHM_NAME = 'Dynamic Monotonicity'

# The Number of Games
N_GAMES = 500


def main():

    f = open(ALGORITHM_NAME + '.txt', "w+")

    f.write('Algorithm: ' + ALGORITHM_NAME + '\n')

    results_list = []
    positions_list = []
    scores_list = []

    for n in range(N_GAMES):
        game = gameplay.Game(ALGORITHM)
        resultFull = game.play_game()
        scores_list.append(resultFull[3])
        positions_list.append(resultFull[2])
        result = min(resultFull[0:2])
        print(n, result, resultFull[3])
        results_list.append(result)

        f.write('\nGame ' + str(n) + ':')
        f.write('\nFinal Score: ' + str(resultFull[3]))
        f.write('\nLogarithmic Performance: ' + str(resultFull[0]))
        f.write('\nMax Tile Performance: ' + str(resultFull[1]))
        f.write('\nDeath Position:\n')
        for row in resultFull[2]:
            f.write(str(row) + '\n')

    f.write('\nAverage PR: ' + str(sum(results_list) / N_GAMES))
    f.write('\nMaximum PR: ' + str(max(results_list)))
    f.write('\nMinimum PR: ' + str(min(results_list)))

    f.write('\n\nAverage Score: ' + str(sum(scores_list) / N_GAMES))
    f.write('\nMaximum Score: ' + str(max(scores_list)))
    f.write('\nMinimum Score: ' + str(min(scores_list)))

    f.close()

main()