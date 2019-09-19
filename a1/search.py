"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    frontier = util.Stack()
    for element in problem.getSuccessors(start_state):
        frontier.push([element])
    explored_set = {start_state}

    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node[-1][0]):
            result = [element[1] for element in node]
            return result
        elif node[-1][0] not in explored_set:
            explored_set.add(node[-1][0])
            for element in problem.getSuccessors(node[-1][0]):
                frontier.push(node + [element])


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    frontier = util.Queue()
    for element in problem.getSuccessors(start_state):
        frontier.push([element])
    explored_set = {start_state}

    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node[-1][0]):
            print("Found the goal..")
            result = [element[1] for element in node]
            return result
        elif node[-1][0] not in explored_set:
            print(explored_set)
            explored_set.add(node[-1][0])
            for element in problem.getSuccessors(node[-1][0]):
                frontier.push(node + [element])


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    frontier = util.PriorityQueue()
    for element in problem.getSuccessors(start_state):
        frontier.push([element], element[2])
    explored_set = {start_state}

    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node[-1][0]):
            result = [element[1] for element in node]
            return result
        elif node[-1][0] not in explored_set:
            explored_set.add(node[-1][0])
            for element in problem.getSuccessors(node[-1][0]):
                cost = sum([state[2] for state in node])  # Cost upto this node
                cost += element[2]   # Cost for new Node
                frontier.push(node + [element], cost)
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    frontier = util.PriorityQueue()
    for element in problem.getSuccessors(start_state):
        frontier.push([element], element[2] + heuristic(element[0], problem))
    explored_set = {start_state}

    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node[-1][0]):
            print("Found the goal..")
            result = [element[1] for element in node]
            return result
        elif node[-1][0] not in explored_set:
            explored_set.add(node[-1][0])
            for element in problem.getSuccessors(node[-1][0]):
                cost = sum([state[2] for state in node])  # Cost upto this Node
                cost += element[2]  # Path Cost for New Node
                cost += heuristic(element[0], problem)  # Heuristic from this Node
                frontier.push(node + [element], cost)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
