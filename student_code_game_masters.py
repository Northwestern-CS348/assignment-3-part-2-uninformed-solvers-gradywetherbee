from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        out = (
            tuple(self.disksOnPeg("peg1")),
            tuple(self.disksOnPeg("peg2")),
            tuple(self.disksOnPeg("peg3")))

        return out

    # the disks on a peg
    def disksOnPeg(self, peg):
        ask = parse_input("fact: (on ?disk " + str(peg) + ")")
        bindings_of_disks_on_peg = self.kb.kb_ask(ask)
        disks_on_peg = [];
        if bindings_of_disks_on_peg:
            for binding in bindings_of_disks_on_peg.list_of_bindings:
                disks_on_peg.append(int(str(binding[0].bindings_dict["?disk"]).replace("disk", "")))

        return sorted(disks_on_peg)


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        game_state = self.getGameState()

        disk = str(movable_statement.terms[0])
        origin_peg = str(movable_statement.terms[1])
        origin_peg_as_int = int(origin_peg.replace("peg",""))
        target_peg = str(movable_statement.terms[2])
        target_peg_as_int = int(target_peg.replace("peg",""))

        if len(game_state[target_peg_as_int - 1]) < 1:  #  -1 Accounts for 0 indexing
            ### There's no disk on the peg so we need to retract empty
            self.kb.kb_retract(parse_input("fact: (empty " + target_peg + ")"))
        else:
            ### There's at least one disk already on the target peg
            # top_of_target = game_state[target_peg_as_int - 1][0]
            self.kb.kb_retract(parse_input("fact: (topofstack disk" + str(game_state[target_peg_as_int - 1][0]) + " " + target_peg + ")"))

        ### Add new facts concerning target peg
        self.kb.kb_add(parse_input("fact: (on " + disk + " " + target_peg + ")"))
        self.kb.kb_add(parse_input("fact: (topofstack " + disk + " " + target_peg + ")"))

        ### Remove old facts concerning origin peg
        self.kb.kb_retract(parse_input("fact: (on " + disk + " " + origin_peg + ")"))
        self.kb.kb_retract(parse_input("fact: (topofstack " + disk + " " + origin_peg + ")"))



        ## ORIGIN: Check if there's a disk below the one we're moving and make it the top
        if len(game_state[origin_peg_as_int - 1]) < 2:
            ### There's no disk on the peg so we need to mark it empty
            self.kb.kb_add(parse_input("fact: (empty " + origin_peg + ")"))
        else:
            ## There's at least two disks already on the target peg - we'll move one so this
            ## checks if there is a disk below the one we want to move
            second_to_top_of_origin = game_state[origin_peg_as_int - 1][1]
            self.kb.kb_add(parse_input("fact: (topofstack disk" + str(game_state[origin_peg_as_int - 1][1]) + " " + origin_peg + ")"))





    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """

        ### Rewrite with loops later - this is hideous but fine for now
        things = []

        ask = parse_input("fact: (pos ?tile pos1 pos1)")
        bindings_tile = self.kb.kb_ask(ask)
        if bindings_tile:
            for binding in bindings_tile.list_of_bindings:
                things.append(int(str(binding[0].bindings_dict["?tile"]).replace("tile", "").replace("empty", "-1")))

        ask = parse_input("fact: (pos ?tile pos2 pos1)")
        bindings_tile = self.kb.kb_ask(ask)
        if bindings_tile:
            for binding in bindings_tile.list_of_bindings:
                things.append(int(str(binding[0].bindings_dict["?tile"]).replace("tile", "").replace("empty", "-1")))

        ask = parse_input("fact: (pos ?tile pos3 pos1)")
        bindings_tile = self.kb.kb_ask(ask)
        if bindings_tile:
            for binding in bindings_tile.list_of_bindings:
                things.append(int(str(binding[0].bindings_dict["?tile"]).replace("tile", "").replace("empty", "-1")))

        ask = parse_input("fact: (pos ?tile pos1 pos2)")
        bindings_tile = self.kb.kb_ask(ask)
        if bindings_tile:
            for binding in bindings_tile.list_of_bindings:
                things.append(int(str(binding[0].bindings_dict["?tile"]).replace("tile", "").replace("empty", "-1")))

        ask = parse_input("fact: (pos ?tile pos2 pos2)")
        bindings_tile = self.kb.kb_ask(ask)
        if bindings_tile:
            for binding in bindings_tile.list_of_bindings:
                things.append(int(str(binding[0].bindings_dict["?tile"]).replace("tile", "").replace("empty", "-1")))

        ask = parse_input("fact: (pos ?tile pos3 pos2)")
        bindings_tile = self.kb.kb_ask(ask)
        if bindings_tile:
            for binding in bindings_tile.list_of_bindings:
                things.append(int(str(binding[0].bindings_dict["?tile"].replace("tile", "").replace("empty", "-1"))))

        ask = parse_input("fact: (pos ?tile pos1 pos3)")
        bindings_tile = self.kb.kb_ask(ask)
        if bindings_tile:
            for binding in bindings_tile.list_of_bindings:
                things.append(int(str(binding[0].bindings_dict["?tile"]).replace("tile", "").replace("empty", "-1")))

        ask = parse_input("fact: (pos ?tile pos2 pos3)")
        bindings_tile = self.kb.kb_ask(ask)
        if bindings_tile:
            for binding in bindings_tile.list_of_bindings:
                things.append(int(str(binding[0].bindings_dict["?tile"]).replace("tile", "").replace("empty", "-1")))

        ask = parse_input("fact: (pos ?tile pos3 pos3)")
        bindings_tile = self.kb.kb_ask(ask)
        if bindings_tile:
            for binding in bindings_tile.list_of_bindings:
                things.append(int(str(binding[0].bindings_dict["?tile"]).replace("tile", "").replace("empty", "-1")))

        tuple1 = (things[0], things[1], things[2])
        tuple2 = (things[3], things[4], things[5])
        tuple3 = (things[6], things[7], things[8])

        tuple = (tuple1, tuple2, tuple3)

        return tuple

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        tile = movable_statement.terms[0]
        tilex = movable_statement.terms[1]
        tiley = movable_statement.terms[2]
        destx = movable_statement.terms[3]
        desty = movable_statement.terms[4]

        ### Move tile to new position
        self.kb.kb_retract(parse_input("fact: (pos " + str(tile) + " " + str(tilex) + " " + str(tiley) + ")"))
        self.kb.kb_assert(parse_input("fact: (pos " + str(tile) + " " + str(destx) + " " + str(desty) + ")"))

        ### "Move" empty "tile" to actual tile's old position
        self.kb.kb_retract(parse_input("fact: (pos empty " + str(destx) + " " + str(desty) + ")"))
        self.kb.kb_assert(parse_input("fact: (pos empty " + str(tilex) + " " + str(tiley) + ")"))

        return

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
