import util

from game import Directions

UNREACHABLE_GOAL_STATE = [Directions.STOP]
n = Directions.NORTH
s = Directions.SOUTH
w = Directions.WEST
e = Directions.EAST


def tinyMazeSearch(problem):
    """
    Run to get familiar with directions.
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    Run this function to get familiar with how navigations works using Directions enum.
    """
    to_goal_easy_directions = [s, s, w, s, w, w, s, w]
    return to_goal_easy_directions


def simpleMazeSearch(problem):
    """
    Q1:
    Search for the goal using right-hand or left-hand method explained in docs.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getNextStates(problem.getStartState())
    Dont forget to take a look at handy classes implemented in util.py.
    """

    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    direction = n
    path = []
    left_hand_directions = {n: w, w: s, e: n, s: e}
    right_hand_directions = {n: e, w: n, s: w, e: s}

    while not problem.isGoalState(state):
        next_valid_states = problem.getNextStates(state)
        next_valid_actions = [action for node, action, _ in next_valid_states]
        if right_hand_directions[direction] in next_valid_actions:
            new_direction = right_hand_directions[direction]
            path += [new_direction]
            direction = new_direction
            state = next_valid_states[next_valid_actions.index(new_direction)][0]
            continue
        if direction in next_valid_actions:
            path += [direction]
            direction = direction
            state = next_valid_states[next_valid_actions.index(direction)][0]
            continue
        if left_hand_directions[direction] in next_valid_actions:
            new_direction = left_hand_directions[direction]
            path += [new_direction]
            direction = new_direction
            state = next_valid_states[next_valid_actions.index(new_direction)][0]
            continue
        if left_hand_directions[left_hand_directions[direction]] in next_valid_actions:
            new_direction = left_hand_directions[left_hand_directions[direction]]
            path += [new_direction]
            state = next_valid_states[next_valid_actions.index(new_direction)][0]
            continue
    return path

    "*** YOUR EXPLANATION HERE***"
    """Mentioned algorithm doesn't always return an answer to the goal. for example consider a map which has no 
    inner walls and the goal is in the center of the maze """


def dfs(problem):
    """
    Q2:
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal.
    Make sure to implement a graph search algorithm.
    Dont forget to take a look at handy classes implemented in util.py.
    """

    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    path = []
    stack.push((problem.getStartState(), path))
    visited = [problem.getStartState()]
    while not stack.isEmpty():
        current_node, path = stack.pop()

        for next_node, action, _ in problem.getNextStates(current_node):
            if next_node not in visited:
                if problem.isGoalState(next_node):
                    return path + [action]
                else:
                    stack.push((next_node, path + [action]))
                    visited.append(next_node)
    return path + [Directions.STOP]

    "*** YOUR EXPLANATION HERE***"
    """ """


def bfs(problem):
    """
    Q3:
    Search the shallowest nodes in the search tree first.
    Dont forget to take a look at handy classes implemented in util.py.
    """

    queue = util.Queue()
    queue.push((problem.getStartState(), []))
    visited = [problem.getStartState()]
    while not queue.isEmpty():
        current_node, path = queue.pop()
        nextStates = problem.getNextStates(current_node)
        for next_node, action, cost in nextStates:
            if next_node not in visited:
                if problem.isGoalState(next_node):
                    return path + [action]
                else:
                    queue.push((next_node, path + [action]))
                    visited.append(next_node)


def deadend_bfs(problem, startState, goalState):
    """
    Q3:
    Search the shallowest nodes in the search tree first.
    Dont forget to take a look at handy classes implemented in util.py.
    """

    queue = util.Queue()
    queue.push((startState, []))
    visited = [startState]
    while not queue.isEmpty():
        current_node, path = queue.pop()
        nextStates = problem.getNextStates(current_node)
        for next_node, action, cost in nextStates:
            if next_node not in visited:
                if next_node == goalState:
                    return path + [action]
                else:
                    queue.push((next_node, path + [action]))
                    visited.append(next_node)
    return path


def isDeadend(direction, next_nodes):
    return len(next_nodes) == 1 and next_nodes[0][1] != direction


def deadend(problem):
    """
    Q5: Search for all dead-ends and then go for goal state.
    Dont forget to take a look at handy classes implemented in util.py.
    """

    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    queue.push(problem.getStartState())
    visited = [problem.getStartState()]
    deadends = []
    goalState = None
    while not queue.isEmpty():
        current_node = queue.pop()
        nextStates = problem.getNextStates(current_node)
        for next_node, action, cost in nextStates:
            if next_node not in visited:
                if isDeadend(action, problem.getNextStates(next_node)):
                    deadends += [next_node]
                if problem.isGoalState(next_node):
                    goalState = next_node
                else:
                    queue.push(next_node)
                    visited.append(next_node)
    path = []
    deadends = [problem.getStartState()] + deadends
    for index, deadend in enumerate(deadends):
        if index == len(deadends) - 1:
            break
        path += deadend_bfs(problem, deadend, deadends[index + 1])
    path += deadend_bfs(problem, deadends[len(deadends) - 1], goalState)
    return path


def ucs(problem):
    """
    Q7: Search the node of least total cost first.
    Dont forget to take a look at handy classes implemented in util.py.
    """

    "*** YOUR CODE HERE ***"
    p_queue = util.PriorityQueue()
    p_queue.push((problem.getStartState(), []), 0)
    visited = [problem.getStartState()]
    while not p_queue.isEmpty():
        current_node, path = p_queue.pop()
        nextStates = problem.getNextStates(current_node)
        for next_node, action, cost in nextStates:
            if next_node not in visited:
                if problem.isGoalState(next_node):
                    return path + [action]
                else:
                    p_queue.push((next_node, path + [action]), cost)
                    visited.append(next_node)

    "*** YOUR EXPLANATION HERE***"
    """ """
