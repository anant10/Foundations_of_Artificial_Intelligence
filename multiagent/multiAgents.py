# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.
      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.
        getAction chooses among the best options according to the evaluation function.
        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        weightForFood = 1
        weightForGhost = 10
        weightSumForFood = 0
        weightSumForGhost =0
        capsules = currentGameState.getCapsules()

        newFoodList = newFood.asList()
        numFoodInList = len(newFoodList)
        numFood = currentGameState.getNumFood()


        if numFoodInList == numFood:
            minDis = 99999
            for eachFoodPoint in newFoodList:
                distance1 = util.manhattanDistance(eachFoodPoint, newPos )
                if( distance1 < minDis ):
                    minDis = distance1
            score = minDis
        else:
            score = 0

        for i, row in enumerate(newGhostStates):
            ghost = row.getPosition()
            distance = util.manhattanDistance(ghost, newPos)
            if distance < 4:
                score = 100
            else:
                score += 1 ** (1 - distance)
        return -score


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.
      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.
      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        numberOfAgents = gameState.getNumAgents()
        numberOfGhosts = numberOfAgents - 1

        v, action = self.minimax(self.depth, gameState, True, 0 )

        return action


    def minimax(self, depth, gameState, checkMaxPlayer, index):

        action_final = Directions.STOP
        if gameState.getLegalActions(0) == [] or depth == 0:
            return self.evaluationFunction(gameState), Directions.STOP

        if checkMaxPlayer:
            v = -999999999
            actions = gameState.getLegalActions(0)
            for action in actions:
                successor = gameState.generateSuccessor(0,action)
                if not index == gameState.getNumAgents()-1:
                    val, action1 = self.minimax( depth, successor, False, index+1)
                if val > v :
                    action_final = action
                    v =val
            return v, action_final

        else:
            minEva = +999999999

            ghostActions = gameState.getLegalActions(index)
            for action in ghostActions:
                successor = gameState.generateSuccessor(index, action)
                if index == gameState.getNumAgents()-1:
                    val, action2 = self.minimax( depth - 1, successor, True, 0)
                else:
                    val, action2 = self.minimax(depth, successor, False, index + 1)
                minEva = min(val, minEva)
            return minEva, action_final




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """

        numberOfAgents=gameState.getNumAgents()
        numberOfGhosts = numberOfAgents - 1

        v, action = self.expectimax(self.depth, gameState, True, 0)

        return action

    def expectimax(self, depth, gameState, checkMaxPlayer, index):

        action_final = Directions.STOP
        if gameState.getLegalActions(0) == [] or depth == 0:
            return self.evaluationFunction(gameState), Directions.STOP

        if checkMaxPlayer:
            v = -999999999
            actions = gameState.getLegalActions(0)
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                if not index == gameState.getNumAgents() - 1:
                    val, action1 = self.expectimax(depth, successor, False, index + 1)
                if val > v:
                    action_final = action
                    v = val
            return v, action_final

        else:

            minEva = 0

            ghostActions = gameState.getLegalActions(index)
            prob = 1.0 / len(ghostActions)
            for action in ghostActions:
                successor = gameState.generateSuccessor(index, action)
                if index == gameState.getNumAgents() - 1:
                    val, action2 = self.expectimax(depth - 1, successor, True, 0)
                else:
                    val, action2 = self.expectimax(depth, successor, False, index + 1)
                minEva = val * prob + minEva
            return minEva, action_final

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
      logic:  for every condition, depending on the priority of the feature, the surge is deducted in the score
       with respect to the distance to the priority feature.
    """
    "*** YOUR CODE HERE ***"
    pacmanPosition = currentGameState.getPacmanPosition()
    walls = currentGameState.getWalls()
    capsules = currentGameState.getCapsules()
    food = currentGameState.getFood()
    numOfFood = currentGameState.getNumFood()
    ghostPositions = currentGameState.getGhostPositions()

    minFoodDistance = 999
    for eachFoodPoint in food.asList():
        distance = util.manhattanDistance(pacmanPosition, eachFoodPoint)
        if (distance < minFoodDistance):
            minFoodDistance = distance
    if numOfFood == 0 :
        minFoodDistance = 1

    minDistanceToWall = 999

    for eachWallPos in walls:
        distance = util.manhattanDistance(pacmanPosition, eachWallPos)
        if (distance < minDistanceToWall):
            minDistanceToWall = distance


    minDistanceToCapsule = 999
    if len(capsules)==0:
        minDistanceToCapsule = 1
    else:
        for eachCapsulePos in capsules:
            distance = util.manhattanDistance(pacmanPosition, eachCapsulePos)
            if (distance < minDistanceToCapsule):
                minDistanceToCapsule = distance


    minDistanceToGhost = 999
    if len(ghostPositions) == 0:
        minDistanceToGhost = 1
    else:
        for ghostPosition in ghostPositions:
            distance = util.manhattanDistance(pacmanPosition, ghostPosition)
            if (distance < minDistanceToGhost):
                minDistanceToGhost = distance

   # newGhostStates = currentGameState.getGhostStates()
   # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]





    discount = -(0.01/5)
    if minDistanceToCapsule<3:
        evaluationFunction = currentGameState.getScore() + discount * minFoodDistance + (discount**2) * minDistanceToCapsule  + (discount**3) * minDistanceToGhost+ (discount**4) * minDistanceToWall

    elif minDistanceToGhost > minFoodDistance :
        evaluationFunction = currentGameState.getScore() + discount * minFoodDistance + (discount**2) * minDistanceToCapsule + (discount**3) * minDistanceToWall  + (discount**4) * minDistanceToGhost
    # elif minDistanceToWall == 1:
    #     evaluationFunction = currentGameState.getScore() +  discount * minDistanceToWall + (discount ** 2) * minFoodDistance + (discount ** 3) * minDistanceToGhost + (discount ** 4) * minDistanceToCapsule
    # # elif minDistanceToWall ==1 and minFoodDistance>15 :
    # #     evaluationFunction = currentGameState.getScore() -  discount * minDistanceToWall - discount ** 2 * minFoodDistance + discount ** 3 * minDistanceToGhost + discount ** 4 * minDistanceToCapsule
    #
    elif minDistanceToGhost < minFoodDistance:
            if minDistanceToGhost == 1:
                evaluationFunction = - 6
            else:
                evaluationFunction = currentGameState.getScore() + discount * minFoodDistance + (
                            discount ** 2) * minDistanceToGhost + (discount ** 3) * minDistanceToWall + (
                                                 discount ** 4) * minDistanceToCapsule

    else:
        evaluationFunction = currentGameState.getScore() + discount * minFoodDistance + (discount**2) * minDistanceToCapsule + (discount**3) * minDistanceToWall + (discount**4) * minDistanceToGhost






    return evaluationFunction



# Abbreviation
better = betterEvaluationFunction