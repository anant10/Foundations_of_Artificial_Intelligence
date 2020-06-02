import copy


# function to check if different conditions of the terminal states
def utility(state):
    X = 'x'
    O = 'o'
    for i in range(3):
        if (state[i][0] == state[i][1] == state[i][2] == X) or (state[0][i] == state[1][i] == state[2][i] == X):
            return 1
        elif (state[i][0] == state[i][1] == state[i][2] == O) or (state[0][i] == state[1][i] == state[2][i] == O):
            return -1

    if (state[0][0] == state[1][1] == state[2][2] == X) or (state[2][0] == state[1][1] == state[0][2] == X):
        return 1
    elif (state[0][0] == state[1][1] == state[2][2] == O) or (state[2][0] == state[1][1] == state[0][2] == O):
        return -1
    elif not any(' ' in sub for sub in state):
        return 0
    else:
        return None



# function to test utility function
def testUtilityFunction():
    stateWhereXWins = [['o', 'x', 'o'],
                       ['x', 'x', 'x'],
                       ['o', ' ', 'o']]
    print utility(stateWhereXWins)
    stateWhereXWinsDiagonally = [['o', 'x', 'x'],
                                 ['x', 'x', 'o'],
                                 ['x', 'o', 'o']]
    print utility(stateWhereXWinsDiagonally)
    stateWhereOWinsDiagonally = [['o', 'x', 'o'],
                                 ['x', 'o', 'x'],
                                 ['o', 'o', 'o']]
    print utility(stateWhereOWinsDiagonally)
    # stateWhereGameNotCompleteWithBlanks = [['o','x','o'],
    #                              ['x',' ','x'],
    #                              ['o',' ','o']]
    # print utility(stateWhereGameNotCompleteWithBlanks)
    stateWhereDraws = [['o', 'x', 'o'],
                       ['x', 'o', 'x'],
                       ['x', 'o', 'x']]
    print utility(stateWhereDraws)


testUtilityFunction()


def getSuccessor(state, player):
    listOfAllSuccessor = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == ' ':
                dummy = []
                dummy = copy.deepcopy(state)
                dummy[i][j] = player
                listOfAllSuccessor.append(dummy)
    return listOfAllSuccessor


stateWhereGameNotCompleteWithBlanks = [['o', 'x', 'o'],
                                       ['x', ' ', ' '],
                                       ['o', ' ', 'o']]
print getSuccessor(stateWhereGameNotCompleteWithBlanks, 'x')


def minimax(state, player):
    if utility(state) is not None:
        return utility(state)
    if player == 'x':
        v = -9
        successors = getSuccessor(state, player)
        for successor in successors:
            val = minimax(successor, 'o')
            v = max(val, v)
        return v
    else:
        v = +9
        successors = getSuccessor(state, player)
        for successor in successors:
            val = minimax(successor, 'x')
            v = min(val, v)
        return v

def testMinimax():
    state0 = [[' ', ' ', ' '],
              [' ', ' ', ' '],
              [' ', ' ', ' ']]
    out = minimax(state0, 'x')
    print "minimax of s0 >>>> " + str(out)
    assert out == 0
    state1 = [[' ', ' ', ' '],
              [' ', ' ', ' '],
              [' ', ' ', 'x']]
    out = minimax(state1, 'o')
    print "minimax of s1 >>>> " + str(out)
    assert out == 0

    state2 = [['o', ' ', ' '],
              [' ', ' ', ' '],
              [' ', ' ', 'x']]
    out = minimax(state2, 'x')
    print "minimax of s2 >>>> " + str(out)
    assert out == 1

    state3 = [['o', ' ', ' '],
              ['x', ' ', ' '],
              [' ', ' ', 'x']]
    out = minimax(state3, 'o')
    print "minimax of s3 >>>> " + str(out)
    assert out == 0
    state4 = [['o', 'o', ' '],
              ['x', ' ', ' '],
              [' ', ' ', 'x']]
    out = minimax(state4, 'x')
    print "minimax of s4 >>>> " + str(out)
    assert out == 1

    state5 = [['o', 'o', 'x'],
              ['x', ' ', ' '],
              [' ', ' ', 'x']]
    out = minimax(state5, 'o')
    print "minimax of s5 >>>> " + str(out)
    assert out == 1

    state6 = [['o', 'o', 'x'],
              ['x', ' ', 'o'],
              [' ', ' ', 'x']]
    out = minimax(state6, 'x')
    print "minimax of s6 >>>> " + str(out)
    assert out == 1



print"hey"
testMinimax()






# Q3. Minimax for blank initial state is 0 i.e. draw. Follow Line number 94 for assertion
#     Minimax for state 6 with x's turn  => (s6, 'x') is 1 i.e. X wins. Follow Line number 134 for assertion.
#
# Q4. In our problem state s2 is sub optimal. MinMax(S2) > MinMax(S` = S3), where action is max i.e, X.
#     Optimal move for the state is [[' ', ' ', ' '],
#                                     [' ', 'o', ' '],
#                                      [' ', ' ', 'x']]
#     also state s3 is sub optimal. MinMax(S3) < MinMax(S` = S4), where action is min i.e, O.
#     Optimal move for the states are [['o', ' ', ' '],
#                                     [' ', ' ', ' '],
#                                      ['x', ' ', 'x']]
#                                     and
#                                     [['o', ' ', 'x'],
#                                     [' ', ' ', ' '],
#                                      [' ', ' ', 'x']]