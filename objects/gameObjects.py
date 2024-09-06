from enum import IntEnum

three_powers = [1,3,9,27,81,243,729,2187,6561]

class Token(IntEnum):
    BLANK = 0
    NAUGHT = 1
    CROSS = 2


class Outcome(IntEnum):
    INCOMPLETE = 0
    DRAW = 1
    NAUGHT = 2
    CROSS = 3

    def token_outcome(token: Token):
        if token is Token.CROSS:
            return Outcome.CROSS
        if token is Token.NAUGHT:
            return Outcome.NAUGHT
        return None


class Board:
    board_dict = {}
    def __init__(self, a:Token,b:Token,c:Token,d:Token,e:Token,f:Token,g:Token,h:Token,i:Token):
        self.board = (a,b,c,d,e,f,g,h,i)
        self.index = -1
        self.blank_count = sum(True for c in self.board if c is Token.BLANK)
        self.naught_count = sum(True for c in self.board if c is Token.NAUGHT)
        self.cross_count = sum(True for c in self.board if c is Token.CROSS)
    
    @staticmethod
    def fromIndex(index: int):
        if index in Board.board_dict:
            return Board.board_dict[index]
        tokens = []
        for power in three_powers:
            tokens.append(Token(int(index // power) % 3))
        Board.board_dict[index] = Board.fromList(tokens)
        return Board.board_dict[index]

    @staticmethod
    def fromList(tokens: list[int]):
        return Board(tokens[0],tokens[1],tokens[2],tokens[3],tokens[4],tokens[5],tokens[6],tokens[7],tokens[8])
    
    def turn(self) -> Token:
        if self.naught_count <= self.cross_count:
            return Token.NAUGHT
        else:
            return Token.CROSS
    
    def opponent(self) -> Token:
        if self.turn() == Token.NAUGHT:
            return Token.CROSS
        else:
            return Token.NAUGHT
        
    def complete(self) -> bool:
        if self.blank_count == 0:
            return True
        if self.naught_count < 3 and self.cross_count < 3:
            return False
        if Token.BLANK != self.board[0] and self.board[0] == self.board[1] == self.board[2]:
            return True
        if Token.BLANK != self.board[3] and self.board[3] == self.board[4] == self.board[5]:
            return True
        if Token.BLANK != self.board[6] and self.board[6] == self.board[7] == self.board[8]:
            return True
        if Token.BLANK != self.board[0] and self.board[0] == self.board[3] == self.board[6]:
            return True
        if Token.BLANK != self.board[1] and self.board[1] == self.board[4] == self.board[7]:
            return True
        if Token.BLANK != self.board[2] and self.board[2] == self.board[5] == self.board[8]:
            return True
        if Token.BLANK != self.board[0] and self.board[0] == self.board[4] == self.board[8]:
            return True
        if Token.BLANK != self.board[2] and self.board[2] == self.board[4] == self.board[6]:
            return True
        return False
    
    def outcome(self) -> bool:
        if not self.complete():
            return Outcome.INCOMPLETE
        
        for token in (Token.NAUGHT, Token.CROSS):
            if token == self.board[0] and self.board[0] == self.board[1] == self.board[2]:
                return Outcome.token_outcome(token)
            if token == self.board[3] and self.board[3] == self.board[4] == self.board[5]:
                return Outcome.token_outcome(token)
            if token == self.board[6] and self.board[6] == self.board[7] == self.board[8]:
                return Outcome.token_outcome(token)
            if token == self.board[0] and self.board[0] == self.board[3] == self.board[6]:
                return Outcome.token_outcome(token)
            if token == self.board[1] and self.board[1] == self.board[4] == self.board[7]:
                return Outcome.token_outcome(token)
            if token == self.board[2] and self.board[2] == self.board[5] == self.board[8]:
                return Outcome.token_outcome(token)
            if token == self.board[0] and self.board[0] == self.board[4] == self.board[8]:
                return Outcome.token_outcome(token)
            if token == self.board[2] and self.board[2] == self.board[4] == self.board[6]:
                return Outcome.token_outcome(token)
        
        return Outcome.DRAW

    def board_with_move(self, index:int):
        tokens = [t for t in self.board]
        tokens[index] = self.turn()
        return Board(tokens[0],tokens[1],tokens[2],tokens[3],tokens[4],tokens[5],tokens[6],tokens[7],tokens[8])

    def board_index_with_move(self, move_index:int) -> int:
        if self.board[move_index] != Token.BLANK:
            Exception(f"Invalid move, token already present. Board index: {self.get_board_index()}. Move attempt: {move_index}.")
        return self.get_board_index() + three_powers[move_index] * self.turn()

    def get_board_index(self):
        if self.index == -1:
            index = 0
            for i, t in enumerate(self.board):
                index += t * three_powers[i]
            self.index = index
        return self.index
    
    def valid_moves(self):
        return tuple(i for i, t in enumerate(self.board) if t is Token.BLANK)
