# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    initial_node = (start_state, [])
    frontier = util.Stack()
    frontier.push(tuple(initial_node))
    # frontier.push(initial_node)
    explored = []

    while not frontier.isEmpty():
        current_node = frontier.pop()
        explored.append(current_node[0])

        if problem.isGoalState(current_node[0]):
            return current_node[1]
        else:
            successors = problem.getSuccessors(current_node[0])
            for successor in successors:
                successor_state = successor[0]
                successor_action = successor[1]

                if successor_state not in explored:
                    # list_frontier = frontier.list[:,0:1]
                    # print " frontier list "
                    # print str(list_frontier)
                    frontier.push([successor_state, current_node[1] + [successor_action]])

                    # if successor_state is lastelementstack[0]:
                    #     frontier.push(tuple(successor_state,lastelementstack[1].append()))
                    # else:
                    #     frontier.push(lastelementstack)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    initial_node = (start_state, [])
    frontier = util.Queue()
    frontier_copy = []
    frontier.push(tuple(initial_node))
    frontier_copy.append(start_state)
    explored = []

    while not frontier.isEmpty():
        current_node = frontier.pop()
        frontier_copy.remove(current_node[0])

        current_node_state, current_node_path = current_node

        explored.append(current_node_state)

        if problem.isGoalState(current_node_state):
            return current_node[1]
        else:
            successors = problem.getSuccessors(current_node_state)
            for successor in successors:
                successor_state = successor[0]
                successor_action = successor[1]

                if successor_state not in explored:
                    if successor_state not in frontier_copy:
                        next_state_path = current_node_path + [successor_action]
                        new_state = (successor_state, next_state_path)

                        frontier.push(tuple(new_state))
                        frontier_copy.append(successor_state)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    initial_node = (start_state, [])
    initial_node_priority = (tuple(initial_node), 0)
    frontier = util.PriorityQueue()
    frontier_with_cost_copy = dict()
    frontier.push(initial_node_priority, 0)
    frontier_with_cost_copy[start_state] = 0
    explored = []

    while not frontier.isEmpty():
        current_node, current_node_cost = frontier.pop()
        current_node_state, current_node_path = current_node
        del frontier_with_cost_copy[current_node_state]
        explored.append(current_node_state)
        if problem.isGoalState(current_node_state):
            return current_node_path
        else:
            successors = problem.getSuccessors(current_node_state)
            for successor in successors:
                successor_state = successor[0]
                successor_action = current_node_path + [successor[1]]
                successor_cost = current_node_cost + successor[2]
                if successor_state not in explored:
                    if successor_state not in frontier_with_cost_copy:
                        new_state = (successor_state, successor_action)
                        new_state_priority = (tuple(new_state), successor_cost)
                        frontier.push(new_state_priority, successor_cost)
                        frontier_with_cost_copy[successor_state] = successor_cost
                    elif successor_state in frontier_with_cost_copy and frontier_with_cost_copy[
                        successor_state] > successor_cost:
                        new_state = (successor_state, successor_action)
                        new_state_priority = (tuple(new_state), successor_cost)
                        frontier.update(new_state_priority, successor_cost)
                        frontier_with_cost_copy[successor_state] = successor_cost

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    initial_node = (start_state, [])
    initial_node_priority = (tuple(initial_node), 0)
    frontier = util.PriorityQueue()
    # frontier_with_cost_copy = dict()
    frontier.push(initial_node_priority, heuristic(start_state, problem))
    # frontier_with_cost_copy[start_state] = 0
    explored = []

    while not frontier.isEmpty():
        current_node, current_node_cost = frontier.pop()
        current_node_state, current_node_path = current_node
        # if current_node_state in frontier_with_cost_copy:
        #     del frontier_with_cost_copy[current_node_state]
        explored.append(current_node_state)
        if problem.isGoalState(current_node_state):
            return current_node_path
        else:
            successors = problem.getSuccessors(current_node_state)
            for successor in successors:
                successor_state = successor[0]
                successor_action = current_node_path + [successor[1]]
                successor_cost = current_node_cost + successor[2]
                successor_priority = successor_cost + heuristic(successor_state, problem)
                if successor_state not in explored:
                    flag_frontier_item_update = False
                    new_node = (successor_state, successor_action)
                    new_state_priority = (tuple(new_node), successor_cost)
                    for (priority, count, node) in frontier.heap:
                        node_in_frontier, node_priority = node
                        node_state, node_action = node_in_frontier
                        if node_state == successor_state:
                            flag_frontier_item_update = True
                            break

                    if not flag_frontier_item_update:
                        frontier.push(new_state_priority, successor_priority)
                    else:
                        if node_priority > successor_priority:
                            frontier.update(new_state_priority, successor_priority)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
