# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    currentFood = currentGameState.getFood()
    currentPos = currentGameState.getPacmanPosition()
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    #print "Scared Times: ", newScaredTimes
    ghostScore = 0
    combinedGhostDistance = 0
    caredGhosts = 0
    for ghostState in newGhostStates:
        distance = manhattanDistance(ghostState.getPosition(), newPos)
        if distance < 2:
            combinedGhostDistance += distance
            caredGhosts += 1
    if combinedGhostDistance == 0 and caredGhosts > 0:
        ghostScore = -9999999
    elif combinedGhostDistance ==0:
        ghostScore = 0
    else:
        ghostScore = -1/(combinedGhostDistance)
    #print "Ghost Score: ", ghostScore
    foodScore = 0
    for food in currentFood.asList():
        if currentPos[0] < newPos[0]:
            if food[0] > currentPos[0]:
                foodScore = 1
        elif currentPos[0] > newPos[0]:
            if food[0] < currentPos[0]:
                foodScore = 1
        elif currentPos[1] < newPos[1]:
            if food[1] > currentPos[1]:
                foodScore = 1
        elif currentPos[1] > newPos[1]:
            if food[1] < currentPos[1]:
                foodScore = 1
            
    if len(newFood.asList()) == 0:
        foodScore = 99999
    else:
        foodScore += 1.0/(len(newFood.asList()))
    #print "Food Score: ", foodScore
    return foodScore + ghostScore

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
  
  def miniMax(self, gameState, iteration, agentsLeft, evalFunction):
    "Iteration is the number of cycles for the agents we need to do still, agents left are the # of agents in the cycle"
    if iteration == 0 and agentsLeft == 0:
      value = evalFunction(gameState)
      return value, None
    else:
      newIteration = None
      newAgentsLeft = None
      if agentsLeft == 0:
        newIteration = iteration - 1
        newAgentsLeft = gameState.getNumAgents()
      else:
        newIteration = iteration
        newAgentsLeft = agentsLeft
      agentIndex = gameState.getNumAgents() - newAgentsLeft
      agentActions = gameState.getLegalActions(agentIndex)
      bestAction = None
      bestValue = None
      values = []
      for action in agentActions:
        if action is Directions.STOP and agentIndex == 0:
          continue
        if bestAction is None:
          bestAction = action
        successor = gameState.generateSuccessor(agentIndex, action)
        value, minMaxAction = self.miniMax(successor, newIteration, newAgentsLeft - 1, evalFunction)
        values.append((value, minMaxAction))
        if bestValue is None:
          bestValue = value
        elif agentIndex == 0 and value > bestValue:
          bestValue = value
          bestAction = action
        elif value < bestValue and agentIndex != 0:
          bestValue = value
          bestAction = action
          
      if bestAction is None or bestValue is None:
        bestValue = evalFunction(gameState)
        
      return bestValue, bestAction
        

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    value, action = self.miniMax(gameState, self.depth, 0, self.evaluationFunction)
    #print "Best Action: ", action, " Best Value: ", value
    return action
    util.raiseNotDefined()
    

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  def alphaBeta(self, gameState, iteration, agentsLeft, evalFunction, greater, less):
    "Iteration is the number of cycles for the agents we need to do still, agents left are the # of agents in the cycle"
    if iteration == 0 and agentsLeft == 0:
      value = evalFunction(gameState)
      return value, None
    else:
      newIteration = None
      newAgentsLeft = None
      if agentsLeft == 0:
        newIteration = iteration - 1
        newAgentsLeft = gameState.getNumAgents()
      else:
        newIteration = iteration
        newAgentsLeft = agentsLeft
      agentIndex = gameState.getNumAgents() - newAgentsLeft
      agentActions = gameState.getLegalActions(agentIndex)
      bestAction = None
      bestValue = None
      passedGreater = greater
      passedLess = less
      for action in agentActions:
        if action is Directions.STOP and agentIndex == 0:
          continue
        if bestAction is None:
          bestAction = action
        successor = gameState.generateSuccessor(agentIndex, action)
        if passedGreater is not None and agentIndex == 0:
          if bestValue is not None:
            passedGreater = max(passedGreater, bestValue)
        if passedLess is not None and agentIndex != 0:
          if bestValue is not None:
            passedLess = min(passedLess, bestValue)
        
        value, minMaxAction = self.alphaBeta(successor, newIteration, newAgentsLeft - 1, evalFunction, passedGreater, passedLess)

        if bestValue is None:
          bestValue = value
        elif agentIndex == 0 and value > bestValue:
          bestValue = value
          bestAction = action
        elif value < bestValue and agentIndex != 0:
          bestValue = value
          bestAction = action
        
        if agentIndex == 0:
          if passedGreater is None or bestValue > passedGreater:
            passedGreater = bestValue
          if bestValue > passedLess and passedLess is not None:
            return bestValue, bestAction
        else:
          if passedLess is None or bestValue < passedLess:
            passedLess = bestValue
          if bestValue < passedGreater and passedGreater is not None:
            return bestValue, bestAction
          
      if bestAction is None or bestValue is None:
        bestValue = evalFunction(gameState)
        
      return bestValue, bestAction

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    value, action = self.alphaBeta(gameState, self.depth, 0, self.evaluationFunction, None, None)
    return action

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """
  
  def expectiMax(self, gameState, iteration, agentsLeft, evalFunction):
    "Iteration is the number of cycles for the agents we need to do still, agents left are the # of agents in the cycle"
    if iteration == 0 and agentsLeft == 0:
      value = evalFunction(gameState)
      return value, None
    else:
      newIteration = None
      newAgentsLeft = None
      if agentsLeft == 0:
        newIteration = iteration - 1
        newAgentsLeft = gameState.getNumAgents()
      else:
        newIteration = iteration
        newAgentsLeft = agentsLeft
      agentIndex = gameState.getNumAgents() - newAgentsLeft
      agentActions = gameState.getLegalActions(agentIndex)          
      bestAction = None
      bestValue = None
      values = []
      for action in agentActions:
        if action == Directions.STOP and agentIndex == 0:
          continue
        if bestAction is None:
          bestAction = action
        successor = gameState.generateSuccessor(agentIndex, action)
        value, minMaxAction = self.expectiMax(successor, newIteration, newAgentsLeft - 1, evalFunction)
        values.append((value, minMaxAction))
        if bestValue is None:
          bestValue = value
        elif agentIndex == 0 and value > bestValue:
          bestValue = value
          bestAction = action
        elif value < bestValue and agentIndex != 0:
          bestValue = value
          bestAction = action
          
      if bestAction is None or bestValue is None:
        bestValue = evalFunction(gameState)
        return bestValue, bestAction
      if agentIndex != 0:
        total = 0
        for tuple in values:
#          print tuple[0]
          total += tuple[0]
#          print "Total: ", total
        return total / len(values), bestAction
      return bestValue, bestAction

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    value, action = self.expectiMax(gameState, self.depth, 0, self.evaluationFunction)
    return action

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  foodGrid = currentGameState.getFood()
  currentPos = currentGameState.getPacmanPosition()
  #print "Food Length: ", foodGrid.height
  #print "Food Row Length: ", foodGrid.width
  maximumPossibleManhattanDistance = foodGrid.height + foodGrid.width
  if len(foodGrid.asList()) == 0:
    foodLeftScore = 9999
  else:
    foodLeftScore = 1.0/(maximumPossibleManhattanDistance * len(foodGrid.asList()))
  foodDistanceScore = 0
  minDistance = maximumPossibleManhattanDistance
  for food in foodGrid.asList():
    distance = euclideanDistance(currentPos, food)
    if distance < minDistance:
      minDistance = distance
  foodDistanceScore = 1.0/(minDistance)
#  scaredGhostsScore = 0.0
#  newScaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]
#  for scaredTime in newScaredTimes:
#    scaredGhostScore += scaredTime
  return currentGameState.getScore() + 2*foodLeftScore + 2*foodDistanceScore

def euclideanDistance(start, end):
  "The Euclidean distance heuristic for a PositionSearchProblem"
  return ( (start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2 ) ** 0.5
  
# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

