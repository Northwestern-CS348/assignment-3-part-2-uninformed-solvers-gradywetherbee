
from solver import *

import queue

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        if self.victoryCondition == self.currentState.state:
            return True

        # Faster to check or not check if there are already children?
        # if self.gm.getMovables() and not self.currentState.children:
        self.findChildren(self.currentState)

        # If we haven't found any children we need to go back
        if not self.currentState.children:
            self.gm.reverseMove(self.currentState.requiredMovable)
            parent = self.currentState.parent
            self.currentState = parent

            # Need to find where the last place is that we have unvisited children
            found = False
            while parent and not found:
                for i in range(0, len(parent.children) - 1):

                    # Check out the unvisited children and mark them as visited
                    if parent.children[i] not in self.visited.keys():
                        self.gm.makeMove(parent.children[i].requiredMovable)
                        self.visited[parent.children[i]] = True
                        self.currentState = parent.children[i]
                        found = True
                        break

                # Keep going back up if all the children have been visited
                if parent:
                    self.gm.reverseMove(parent.requiredMovable)
                    parent = parent.parent
                    self.currentState = parent
                # If there's no parent then we're at the root and there's nothing to be done
                else:
                    break
        # If there is a child we're going to look at it and mark it visited
        else:
            child_state = self.currentState.children[0]
            self.gm.makeMove(child_state.requiredMovable)
            self.visited[child_state] = True
            self.currentState = child_state

        return False

    # If we need to find the children we can go through all the potential moves
    # and investigate them if we haven't seen that state before
    def findChildren(self, gameState):
        for move in self.gm.getMovables():
            self.gm.makeMove(move)
            childState = self.gm.getGameState()
            if gameState.parent and childState == gameState.parent.state:
                self.gm.reverseMove(move)
            else:
                newState = GameState(childState, gameState.depth + 1, move)
                if newState not in self.visited.keys():
                    newState.parent = gameState
                    gameState.children.append(newState)
                self.gm.reverseMove(move)

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

        # queue (FIFO) is what makes a BFS work
        self.search_queue = queue.Queue()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.victoryCondition == self.currentState.state:
            return True

        if self.currentState not in self.visited:
            self.visited[self.currentState] = True

        if self.gm.getMovables() and not self.currentState.children:
            self.findChildren(self.currentState)

        path = []

        always = 123 ### runs until we break this loop ourselves
        while always == 123:
            next = self.search_queue.get()

            if not next in self.visited:
                #create the path back to the top
                while next.requiredMovable:
                    path.append(next.requiredMovable)
                    next = next.parent

                # reverse the actual states
                while self.currentState.requiredMovable:
                    self.gm.reverseMove(self.currentState.requiredMovable)
                    self.currentState = self.currentState.parent

                # navigate back down and go to the children to mark them as visited and keep searching
                num = len(path) - 1
                while path:

                     # get last element of path and the remove it
                    move = path[num]
                    path.remove(path[num])
                    self.gm.makeMove(move)
                    new_state = self.gm.getGameState()
                    num = num - 1

                    for child in self.currentState.children:
                        if child.state == new_state:
                            self.currentState = child
                            self.visited[self.currentState] = True # set visited flag to make sure we don't visit again
                            break
                break

        return False
    
    def findChildren(self, gameState):
            for move in self.gm.getMovables():
                self.gm.makeMove(move)
                child_state = self.gm.getGameState()

                # if the child state is the same as the grandparent we don't want to go there - it's a duplicate
                if gameState.parent and child_state == gameState.parent.state:
                    self.gm.reverseMove(move)
                else:

                    # it's a new state that we'll add to the queue and look at later
                    child_state = GameState(child_state, self.currentState.depth + 1, move)
                    child_state.parent = self.currentState
                    gameState.children.append(child_state)
                    self.search_queue.put(child_state)
                    self.gm.reverseMove(move)