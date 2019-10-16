import gameplay
import expectimax_honing

'''
This is the command centre where algorithms are tested.
'''

N_GAMES = 5

VN = 'Expectimax Final Test'

lowerBound = 0
upperBound = 0
skip = 100



def honing(scale):

    f = open(VN + ' ' +  str(scale) + '.txt', "w+")

    f.write(VN + ' ' +  str(scale) + '\n')

    results_list = []
    scores_list = []
    for n in range(N_GAMES):
        game = gameplay.Game(expectimax_honing.search)
        resultFull = game.play_game_scaled(scale)
        result = min(resultFull[0:2])
        scores_list.append(resultFull[3])
        print(scale, n, result, resultFull[3])
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

    return sum(results_list) / N_GAMES

def main():

    ovr_results = []
    best_result = 0
    best_algorithm = None
    scale=lowerBound
    while scale <= upperBound:
        result = honing(scale)
        ovr_results.append((scale, result))
        if result > best_result:
            best_algorithm = scale
            best_result = result
        scale += skip
    for n in ovr_results:
        print(n)
    print(best_result, best_algorithm)


main()