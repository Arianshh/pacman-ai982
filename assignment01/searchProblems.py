# searchProblems.py
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
In searchProblems.py, you will implement generic search problems which are called by
Pacman agents (in searchAgents.py).
"""
import math

import util
from game import Actions, Directions


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

    def getNextStates(self, state):
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


class PositionSearchProblem(SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn=lambda x: 1, goal=(1, 1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None:
            self.startState = start

        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize

        if warn and (len(gameState.data.layout.goals) == 0):
            print 'Warning: this does not look like a regular search maze'

        # For display purposes, DO NOT CHANGE!
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display):  # @UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist)  # @UndefinedVariable

        return isGoal

    def getNextStates(self, state):
        """
        Returns next states, the actions they require, and a cost of 1.
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))

        # Bookkeeping for display purposes
        self._expanded += 1  # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x, y = self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x, y))

        return cost


class CounterClockwiseFoodProblem(SearchProblem):
    """
    This search problem finds paths through all foods and final goal location of map layout

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState, goal=(1, 1)):
        """
        Stores the walls, pacman's starting position and foods.
        """
        self.goal = goal  # # DO NOT CHANGE; this attribute is read from the layout file.
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        self.foods = startingGameState.getFood().deepCopy()
        self._expanded = 0  # DO NOT CHANGE; Number of search nodes expanded

        """
        To get started, you might want to try some of these simple commands to
        understand the search problem that is being passed in:

        print self.goal
        print self.foods
        print self.walls
        """

        # Please add any code here which you would like to use
        # in initializing the problem, it's okey if you don't have any additional code
        self.end = False

    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state space)
        """
        "*** YOUR CODE HERE ***"
        return (self.startingPosition, Directions.WEST, self.foods)

    def getFoodStates(self):
        """
        Returns the start state (in your state space, not the full Pacman state space)
        """
        return (self.foods)

    def isGoalState(self, state):
        """
        Returns whether this search state is a goal state of the problem.
        """
        isGoal = (state[0] == self.goal)
        return isGoal and (state[2].count() == 0)

    def getNextStates(self, state):
        if self.end and state[2].count() != 0:
            return []
        s = Directions.SOUTH
        w = Directions.WEST
        n = Directions.NORTH
        e = Directions.EAST
        cost = 1
        successors = []
        valid_moves = {n: w, w: s, s: e, e: n}

        position, direction, foods = state
        for action in [n, s, e, w]:
            if action == direction or action == valid_moves[direction]:
                food = foods.copy()
                x, y = position
                dx, dy = Actions.directionToVector(action)
                nextx, nexty = int(x + dx), int(y + dy)
                if not self.walls[nextx][nexty] and action == direction:
                    food[nextx][nexty] = False
                    nextState = ((nextx, nexty), direction, food)
                    if food.count() == 0:
                        self.end = True
                    successors += [(nextState, action, cost)]
                elif not self.walls[nextx][nexty] and action == valid_moves[direction]:
                    food[nextx][nexty] = False
                    nextState = ((nextx, nexty), valid_moves[direction], food)
                    if food.count() == 0:
                        self.end = True
                    successors += [(nextState, action, cost)]

        # Bookkeeping for display purposes
        self._expanded += 1  # DO NOT CHANGE

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)


class ScaryProblem(PositionSearchProblem):
    """
        This search problem finds paths through map layout while avoids dangerous zones

        You must select a suitable state space and successor function
    """

    def __init__(self, gameState, goal=(1, 1), start=None, warn=True, visualize=True):
        PositionSearchProblem.__init__(self, gameState, self.cost_function, goal, start, warn, visualize)
        self.ghosts = gameState.getGhostPositions()

        """
        To get started, you might want to try some of these simple commands to
        understand the search problem that is being passed in:

        print self.goal
        print self.walls
        print self.ghosts
        """

        # Please add any code here which you would like to use
        # in initializing the problem, it's okey if you don't have any additional code
        "*** YOUR CODE HERE ***"

    def cost_function(self, state):
        """
        Cost of entering this state, should return higher cost if state is in a dangerous zone

        :param state: tuple (x,y)
        :return: int
        """

        "*** YOUR CODE HERE ***"
        x, y = state
        cost = 1
        for ghost in self.ghosts:
            g_x, g_y = ghost
            if x == g_x or x == g_x + 3 \
                    or x == ghost[0] - 3 \
                    and (y == ghost[1] or y == ghost[1] + 3
                         or y == ghost[1] - 3):
                # Euclidean distance
                distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(state, ghost)]))
                cost += 1 / (distance + .1)
        return cost
