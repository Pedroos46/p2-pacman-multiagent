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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

        """
        Note: Remember that newFood has the function asList()
        Note: As features, try the reciprocal of important values (such as distance to food) 
                rather than just the values themselves.
                
        Estrategia 1: fugir del fantasma!
        Estrategia 2: mirar sempre on esta el menjar mes aprop.

        """
        ###print(newGhostStates)

        """scape from ghost"""
        nearfood = 9999999;
        for fantasma in successorGameState.getGhostPositions():
            if (manhattanDistance(newPos, fantasma) < 2):
                return float(-999999)
        """Get the closets food"""
        for food in newFood.asList():
            nearfood = min(nearfood, manhattanDistance(newPos, food))

        return successorGameState.getScore() + 1/float(nearfood)

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        print(gameState)
        action = None
        maxim = float(-9999999)

        for agentState in gameState.getLegalActions(0):
            optim = self.minimax(1, 0, gameState.generateSuccessor(0, agentState))

            """ maximitzation """
            if optim > maxim:
                maxim = optim
                action = agentState

        return action

    def minimax(self, agentIndex, depth, gameState):
        """First: getting number of ghosts + pacman"""
        nAgents = gameState.getNumAgents()

        """COMENTAR"""
        if gameState.isLose() or gameState.isWin() or depth == self.depth:
            return self.evaluationFunction(gameState)

        if agentIndex == 0:  # maximize for pacman. Iteration like we saw in the seminar class.
            v = -99999
            for nextS in gameState.getLegalActions(agentIndex):
                v = max(self.minimax(1, depth, gameState.generateSuccessor(agentIndex, nextS)), v)
            return v

        if agentIndex != 0:  # minimize for ghosts.

            agentSwitch = agentIndex + 1
            if nAgents == agentSwitch:
                depth = depth + 1
                agentSwitch = 0

            v = 99999
            for nextS in gameState.getLegalActions(agentIndex):
                v = min(self.minimax(agentSwitch, depth, gameState.generateSuccessor(agentIndex, nextS)), v)
            return v

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        print(gameState)
        action = None
        maxim = float(-9999999)
        alpha = float(-9999999)
        beta = float(9999999)

        for agentState in gameState.getLegalActions(0):
            optim = self.alphabeta(1, 0, gameState.generateSuccessor(0, agentState), alpha, beta)

            """ maximitzation """
            if optim > maxim:
                maxim = optim
                action = agentState

            if maxim > beta:
                return maxim
            alpha = max(alpha, maxim)

        return action


    def alphabeta(self, agentIndex, depth, gameState, alpha, beta):
        """First: getting number of ghosts + pacman"""
        nAgents = gameState.getNumAgents()

        """COMENTAR"""
        if gameState.isLose() or gameState.isWin() or depth == self.depth:
            return self.evaluationFunction(gameState)

        if agentIndex == 0:  # maximize for pacman.
            v = -999999
            for nextS in gameState.getLegalActions(agentIndex):
                v = max(self.alphabeta(1, depth, gameState.generateSuccessor(agentIndex, nextS), alpha, beta), v)
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v

        if agentIndex != 0:  # minimize for ghosts.

            agentSwitch = agentIndex + 1
            if nAgents == agentSwitch:
                depth = depth + 1
                agentSwitch = 0

            v = 999999
            for nextS in gameState.getLegalActions(agentIndex):
                v = min(self.alphabeta(agentSwitch, depth, gameState.generateSuccessor(agentIndex, nextS), alpha, beta), v)
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

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
        "*** YOUR CODE HERE ***"
        print(gameState)
        action = None
        maxim = float(-9999999)

        for agentState in gameState.getLegalActions(0):
            optim = self.expectimax(1, 0, gameState.generateSuccessor(0, agentState))

            """ maximitzation """
            if optim > maxim:
                maxim = optim
                action = agentState

        return action

    def expectimax(self, agentIndex, depth, gameState):
        """First: getting number of ghosts + pacman"""
        nAgents = gameState.getNumAgents()

        """COMENTAR"""
        if gameState.isLose() or gameState.isWin() or depth == self.depth:
            return self.evaluationFunction(gameState)

        if agentIndex == 0:  # maximize for pacman. Iteration like we saw in the seminar class.
            v = -99999
            for nextS in gameState.getLegalActions(agentIndex):
                v = max(self.expectimax(1, depth, gameState.generateSuccessor(agentIndex, nextS)), v)
            return v


        if agentIndex != 0:  # minimize for ghosts.

            agentSwitch = agentIndex + 1
            if nAgents == agentSwitch:
                depth = depth + 1
                agentSwitch = 0

            v = 0
            for nextS in gameState.getLegalActions(agentIndex):
                v += self.expectimax(agentSwitch, depth, gameState.generateSuccessor(agentIndex, nextS))/ float(len(gameState.getLegalActions(agentIndex)))
            return v

        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()


    """scape from ghost"""
    nearfood = 9999999
    for fantasma in currentGameState.getGhostPositions():
        distance = manhattanDistance(newPos, fantasma)
        if (distance < 2):
            return distance
    """Get the closets food"""
    for food in newFood.asList():
        nearfood = min(nearfood, manhattanDistance(newPos, food))

    return currentGameState.getScore() + 1 / float(nearfood)

# Abbreviation
better = betterEvaluationFunction
