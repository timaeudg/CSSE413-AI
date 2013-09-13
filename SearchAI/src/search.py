# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
import heapq

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's actions:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  return genericGraphSearch(problem, Stack())

def genericGraphSearch(problem, openStruct, heuristic=nullHeuristic):
  closed = []
  startState = problem.getStartState()
  if isinstance(openStruct, PriorityQueue):
      openStruct.push((startState, None, 0, None), 0)
  else:
      openStruct.push((startState, None, 0, None))
  while not openStruct.isEmpty():
      fullStateInfo = openStruct.pop()
#      print "Full State: ", fullStateInfo
      currentState = fullStateInfo[0]
#      print "Current State: ", currentState
      closed.append(currentState)
      if(problem.isGoalState(currentState)):
          actionsToReturn = []
          while fullStateInfo[3] is not None:
              actionsToReturn.insert(0, fullStateInfo[1])
              fullStateInfo = fullStateInfo[3]
          return actionsToReturn
      successors = problem.getSuccessors(currentState)
      for successor in successors:
          openSuccessor = (successor[0], successor[1], successor[2], fullStateInfo)
          if successor[0] not in closed:
              inOpen = False
#              print "Open: ", openStruct.getList()
              for item in openStruct.getList():
                  problemState = item[0]
                  if isinstance(openStruct, PriorityQueue):
                      problemState = item[1][0]
                  if problemState == successor[0]:
                      inOpen = True
#                      print "In open: ", item[0]
              if not inOpen:
#                  print "Not in open: ", successor[0]
                  if isinstance(openStruct, PriorityQueue):
#                      print "Pushed: ", openSuccessor
                      heuristicScore = heuristic(successor[0], problem)
                      costSoFar = successor[2] + fullStateInfo[2]
                      priority = costSoFar + heuristicScore
                      openStruct.push(openSuccessor, priority)
                  else:
                      openStruct.push(openSuccessor)
  #Error here, no solution
  util.raiseNotDefined()

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  return genericGraphSearch(problem, Queue())
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  return genericGraphSearch(problem, PriorityQueue())
  util.raiseNotDefined()


def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  return genericGraphSearch(problem, PriorityQueue(), heuristic)
  util.raiseNotDefined()
    
class Stack:
  "A container with a last-in-first-out (LIFO) queuing policy."
  def __init__(self):
    self.list = []
    
  def push(self,item):
    "Push 'item' onto the stack"
    self.list.append(item)

  def pop(self):
    "Pop the most recently pushed item from the stack"
    return self.list.pop()

  def isEmpty(self):
    "Returns true if the stack is empty"
    return len(self.list) == 0

  def getList(self):
    return self.list 
  
class Queue:
  "A container with a first-in-first-out (FIFO) queuing policy."
  def __init__(self):
    self.list = []
  
  def push(self,item):
    "Enqueue the 'item' into the queue"
    self.list.insert(0,item)

  def pop(self):
    """
      Dequeue the earliest enqueued item still in the queue. This
      operation removes the item from the queue.
    """
    return self.list.pop()

  def isEmpty(self):
    "Returns true if the queue is empty"
    return len(self.list) == 0

  def getList(self):
    return self.list

class PriorityQueue:
  """
    Implements a priority queue data structure. Each inserted item
    has a priority associated with it and the client is usually interested
    in quick retrieval of the lowest-priority item in the queue. This
    data structure allows O(1) access to the lowest-priority item.
    
    Note that this PriorityQueue does not allow you to change the priority
    of an item.  However, you may insert the same item multiple times with
    different priorities.
  """  
  def  __init__(self):  
    self.heap = []
    
  def push(self, item, priority):
      pair = (priority,item)
      heapq.heappush(self.heap,pair)

  def pop(self):
      (priority,item) = heapq.heappop(self.heap)
      return item
  
  def isEmpty(self):
    return len(self.heap) == 0

  def getList(self):
    return self.heap

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
