from random import randint

from objects.gameObjects import Board, Token, Outcome
from utils.symmetry_utils import SymmetryUtil
from utils.graph_utils import search_all_boards

class BeadPool:
    def __init__(self) -> None:
        self.beads = [0,0,0,0,0,0,0,0,0]
        self.bead_count = 0
    
    def add_beads(self, pos: int, amount: int = 1) -> None:
        if 0 > pos or 8 < pos:
            return
        if amount <= 0:
            return
        self.beads[pos] += amount
        self.bead_count += amount
    
    def take_bead(self) -> int:
        if self.bead_count <= 0:
            return None
        pick = randint(1,self.bead_count)
        track = 0
        for pos in range(9):
            track += self.beads[pos]
            if track >= pick:
                if self.beads[pos] == self.bead_count:
                    # only one bead type left
                    return pos
                self.beads[pos] -= 1
                self.bead_count -= 1
                return pos


class Matchbox:
    def __init__(self, board: Board) -> None:
        self.board = board
        self.b_index = board.get_board_index()
        self.beads = BeadPool()
        self.setup_beadpool()
        self.recent_bead = -1
        
    def setup_beadpool(self):
        blanks = self.board.blank_count
        beads_to_add = max(1, int(blanks//2))
        valid_moves = self.board.valid_moves()
        for move in valid_moves:
            self.beads.add_beads(move, beads_to_add)

    def take_turn(self) -> int:
        position = self.beads.take_bead()
        self.recent_bead = position
        return position
    
    def reward(self):
        self.beads.add_beads(self.recent_bead, 3)
    
    def punish(self):
        pass

    def draw(self):
        self.beads.add_beads(self.recent_bead, 1)
        

class MENACE:
    def __init__(self):
        self.info_boards = self.menace_boards()
        self.matchboxes = {index: Matchbox(board) for index, board in self.info_boards.items()}
        self.recent_plays = []
        
    def menace_boards(self) -> list[Board]:
        search_all_boards()  # make sure this has run already
        menace_indexes = set()
        for board in Board.board_dict.values():
            if board.turn() is not Token.NAUGHT:
                # NAUGHT TURNS ONLY
                continue
            smallest_index = SymmetryUtil.smallest_symmetric_board(board)
            if smallest_index not in menace_indexes:
                menace_indexes.add(smallest_index)
        return {i: Board.fromIndex(i) for i in menace_indexes}
    
    def make_move(self, board: Board) -> int:
        smallest_index = SymmetryUtil.smallest_symmetric_board(board)
        matchbox: Matchbox = self.matchboxes[smallest_index]
        symmetric_position = matchbox.take_turn()
        self.recent_plays.append(matchbox)

        original_position = SymmetryUtil.restore_position(Board.fromIndex(smallest_index), board, symmetric_position)
        return original_position

    def reinforce(self, outcome: Outcome):
        if outcome is Outcome.NAUGHT:
            for mb in self.recent_plays:
                mb.reward()
        elif outcome is Outcome.CROSS:
            for mb in self.recent_plays:
                mb.punish()
        elif outcome is Outcome.DRAW:
            for mb in self.recent_plays:
                mb.draw()
        else:
            pass
        self.recent_plays = []
