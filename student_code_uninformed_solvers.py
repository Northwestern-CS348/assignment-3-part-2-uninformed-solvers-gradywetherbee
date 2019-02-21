
from solver import *

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
        if self.currentState == self.victoryCondition:
            return True

        moves = self.gm.getMovables()

        if not self.currentState.children and not moves:
            print("no children:" + self.currentState.children)
            self.findChildren(self.currentState)
            print("after findChildren:" + self.currentState.children)

        if moves and self.currentState.children:
            for move in moves:
                print(move)

        if not self.currentState.children and not moves:
            self.gm.reverseMove()
        print(self)


    def findChildren(self, gameState):
        moves = self.getMovables()
        for move in moves:
            self.gm.makeMove(move)
            childState = self.gm.getGameState()
            if gameState.parent and childState == gameState.parent:
                self.gm.reverseMove()
            else:
                newState = GameState(childState, gameState.depth + 1, move)
                if newState not in self.visited.keys():
                    gameState.children.append(newState)
                    newState.parent = gameState
                    self.gm.reverseMove()

class SolverBFS(UninformedSolver):
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
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True
