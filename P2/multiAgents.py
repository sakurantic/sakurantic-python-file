import util
import math

from game import Agent

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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        super().__init__()
        self.index = 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        return self.maxValue(gameState, 1)[1]

    def maxValue(self, gameState, depth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None
        v = - math.inf
        actionBest = None
        for action in gameState.getLegalActions(self.index):
            successorGameState = gameState.generateSuccessor(self.index, action)
            value =self.minValue(successorGameState, self.index + 1, depth) # TODO self.minValue(successorGameState, self.index + 1, depth) or self.maxValue(successorGameState, depth + 1)[0]
            if value > v:
                v = value
                actionBest = action
        return v, actionBest

    def minValue(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        v = math.inf
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex < gameState.getNumAgents() - 1:
                value = self.minValue(successorGameState, agentIndex + 1, depth)
            else:
                if depth < self.depth:
                    value = self.maxValue(successorGameState, depth + 1)[0] # TODO self.minValue(successorGameState, agentIndex + 1, depth) or self.maxValue(successorGameState, depth + 1)[0]
                else:
                    value = self.evaluationFunction(successorGameState)
            v = min(v, value)
        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        return self.maxValue(gameState, 1, True)[1]

    def maxValue(self, gameState, depth, alpha=-math.inf, beta=math.inf):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None
        v = - math.inf
        actionBest = None
        for action in gameState.getLegalActions(self.index):
            successorGameState = gameState.generateSuccessor(self.index, action)
            value =self.minValue(successorGameState, self.index + 1, depth, alpha, beta) # TODO self.minValue(successorGameState, self.index + 1, depth, alpha, beta) or self.maxValue(successorGameState,depth + 1, alpha, beta)[0]
            if value > v:
                v = value
                actionBest = action
            if v >= beta: # TODO v >= beta or v <= beta
                return v, None
            alpha = max(alpha, v)
        return v, actionBest

    def minValue(self, gameState, agentIndex, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        v = math.inf
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex < gameState.getNumAgents() - 1:
                value = self.minValue(successorGameState, agentIndex + 1, depth, alpha, beta)
            else:
                if depth < self.depth:
                    value = self.maxValue(successorGameState,depth + 1, alpha, beta)[0]  # TODO self.minValue(successorGameState, agentIndex + 1, depth, alpha, beta) or self.maxValue(successorGameState,depth + 1, alpha, beta)[0]
                else:
                    value = self.evaluationFunction(successorGameState)
            v = min(v, value)
            if v <= alpha:# TODO v >= alpha or v <= alpha
                return v
            beta = min(beta, v)
        return v
