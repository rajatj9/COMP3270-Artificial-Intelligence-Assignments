from util import manhattanDistance
import math
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
        # prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        state_value = successorGameState.getScore()

        # Food Dots Left
        food_dots_left = successorGameState.getNumFood()
        state_value -= math.exp(-food_dots_left*15)

        # Distance to closest food dot
        if len(newFood.asList()) > 0:
            min_value = math.inf
            for food_position in newFood.asList():
                food_dot_distance = manhattanDistance(newPos, food_position)
                if food_dot_distance < min_value:
                    min_value = food_dot_distance
            state_value += math.exp(-min_value)

        # Distance to closest ghost
        if len(newGhostStates) > 0:
            min_distance = math.inf
            for ghost in newGhostStates:
                ghost_position = ghost.getPosition()
                distance_to_ghost = manhattanDistance(newPos, ghost_position)
                if distance_to_ghost < min_distance:
                    min_distance = distance_to_ghost
            state_value -= math.exp(-min_distance)

        return state_value

        

    def scoreEvaluationFunction(currentGameState):
        return currentGameState.getScore()
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """

def scoreEvaluationFunction(currentGameState):
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
    def minimax(self, gameState, depth, agentID):

        if agentID == gameState.getNumAgents():
            return self.minimax(gameState, depth + 1, 0)

        if gameState.isWin() or gameState.isLose() or depth == self.depth or gameState.getLegalActions(agentID) == 0:
            return self.evaluationFunction(gameState)

        state_scores = []
        for action in gameState.getLegalActions(agentID):
            state_scores.append(self.minimax(gameState.generateSuccessor(agentID, action), depth, agentID + 1))
        if agentID % gameState.getNumAgents() == 0:
            return max(state_scores)
        else:
            return min(state_scores)

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
        available_actions = gameState.getLegalActions(0)
        score_action = [(self.minimax(gameState.generateSuccessor(0, action), 0, 1),  action)
                        for action in available_actions]
        action = max(score_action, key=lambda item: item[0])[1]
        return action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        v = alpha = -math.inf
        beta = math.inf
        best_action = None
        available_actions = gameState.getLegalActions(0)
        for action in available_actions:
            temp = self.min_value(gameState.generateSuccessor(0, action), 0, 1, alpha, beta)
            if v < temp:
                v = temp
                best_action = action

            if v > beta:
                return v
            alpha = max(alpha, temp)
        return best_action

    def min_value(self, gameState, depth, ghost, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        v = math.inf
        available_actions = gameState.getLegalActions(ghost)
        for action in available_actions:
            if ghost == gameState.getNumAgents() - 1:
                v = min(v, self.max_value(gameState.generateSuccessor(ghost, action), depth+1, alpha, beta))
            else:
                v = min(v, self.min_value(gameState.generateSuccessor(ghost, action), depth, ghost+1, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v

    def max_value(self, gameState, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        v = -math.inf
        available_actions = gameState.getLegalActions(0)
        for action in available_actions:
            v = max(v, self.min_value(gameState.generateSuccessor(0, action), depth, 1, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v


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
        return self.pacman_plays(gameState, 1)[1]

    def pacman_plays(self,gameState, depth):
        available_actions = gameState.getLegalActions(0)

        if gameState.isWin() or gameState.isLose() or depth > self.depth or not available_actions:
            return self.evaluationFunction(gameState), None

        score_action = [(self.ghost_plays(gameState.generateSuccessor(0, action), depth, 1)[0], action)
                        for action in available_actions]
        best_score_action = max(score_action, key=lambda item: item[0])
        return best_score_action

    def ghost_plays(self,gameState, depth, agent):
        available_actions = gameState.getLegalActions(agent)

        if gameState.isWin() or gameState.isLose() or depth > self.depth or not available_actions:
            return self.evaluationFunction(gameState), None
        scores = []
        for action in available_actions:
            if agent == gameState.getNumAgents() - 1:
                scores.append(self.pacman_plays(gameState.generateSuccessor(agent, action), depth + 1))
            else:
                scores.append(self.ghost_plays(gameState.generateSuccessor(agent, action), depth, agent + 1))
        return sum(map(lambda score_action: float(score_action[0]) / len(available_actions), scores)), None


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: The calculation takes into account the following factors:
      1. Number of food dots left
      2. Distance to closest food dot
      3. Distance to closest ghost
      4. Distance to farthest ghost
      These figures are calculated and the function e^x with tested weights is used to calculate how good a state is.
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()

    if currentGameState.isLose():
        return -math.inf

    if newPos in [g.getPosition() for g in newGhostStates]:
        return -math.inf

    state_value = currentGameState.getScore()

    # Food Dots Left
    food_dots_left = currentGameState.getNumFood()
    state_value -= math.exp(-food_dots_left/20)

    # Distance to closest food dot
    min_value = math.inf
    for food_position in newFood.asList():
        food_dot_distance = manhattanDistance(newPos, food_position)
        if food_dot_distance < min_value:
            min_value = food_dot_distance
    state_value += math.exp(-min_value)*10

    # Distance to closest ghost
    min_distance = math.inf
    max_distance = -math.inf
    for ghost in newGhostStates:
        ghost_position = ghost.getPosition()
        distance_to_ghost = manhattanDistance(newPos, ghost_position)
        if distance_to_ghost < min_distance:
            min_distance = distance_to_ghost
        if distance_to_ghost > max_distance:
            max_distance = distance_to_ghost
    state_value -= math.exp(-min_distance)*10
    state_value += math.exp(-max_distance)*10

    return state_value


better = betterEvaluationFunction

