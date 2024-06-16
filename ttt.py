from enum import IntEnum
from typing import Any


class Token(IntEnum):
    BLANK = 0
    CROSS = 1
    NAUGHT = 2

    def tokenFromIndex(value):
        if value == 0:
            return Token.BLANK
        elif value == 1:
            return Token.CROSS
        elif value == 2:
            return Token.NAUGHT
        else:
            raise Exception(f"Cannot create Token Object from {value}, must be 0, 1, 2")
    

class Position:
    def __init__(self, index: int) -> None:
        self.x = index % 3
        self.y = index // 3
        self.validate()

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.validate()

    def validate(self):
        if not (self._validCoord(self.x) and self._validCoord(self.y)):
            raise Exception("x, y values must be values of 1,2,3 ")

    def _validCoord(self, x: Any) -> bool:
        return x in (1, 2, 3)

    def getIndex(self) -> int:
        return (self.x - 1) + 3 * (self.y - 1)


class Node:
    def __init__(self, value: Any, edges) -> None:
        self.value = value
        self.edges = edges

    def addEdge(self, other) -> None:
        if other and other not in self.edges:
            self.edges.append(other)


class Graph:
    def __init__(self, nodes: list[Node]) -> None:
        self.nodes = nodes


class Board:
    def __init__(self, table: list[list[Token]]) -> None:
        self.table = table
        self.index: int # = self._calculateIndex()
        self.turn = self._calculateTurn()

    def getSpaceCoords(self, x: int, y: int) -> Token:
        return self.table[y][x]
    
    def getSpacePosition(self, where: Position) -> Token:
        return self.table[where.y-1][where.x-1]
        # return self.getSpaceIndex(where.getIndex())

    def getSpaceIndex(self, i: int) -> Token:
        return self.table[i // 3][i % 3]
    
    def _setSquareCoord(self, who: Token, where: Position) -> None:
        self.table[where.y-1][where.x-1] = who
    
    def _valueGenerator(self):
        return (self.getSpaceIndex(i) for i in range(9))
    
    def getBoardValueList(self) -> list[Token]:
        return list(self._valueGenerator())

    def _calculateIndex(self) -> int:
        return sum(
            token ** (index)
            for index, token in enumerate(self._valueGenerator(), start=1)
        )
    
    def _getNumPlayer(self, player: Token) -> int:
        return len([token for token in self._valueGenerator() if token == player])
    
    def _calculateTurn(self) -> Token:
        naughtNum = self._getNumPlayer(Token.NAUGHT)
        crossNum = self._getNumPlayer(Token.CROSS)
        # Assuming Naughts goes first
        if naughtNum == crossNum:
            return Token.NAUGHT
        elif naughtNum > crossNum:
            return Token.CROSS
        elif naughtNum < crossNum:
            raise Exception(
                "Invalid board state: Should always be at least as many "
                "Naughts as there are Crosses (Remember: NAUGHTS GO FIRST!)"
            )
    
    def getIndex(self) -> int:
        self.index = self._calculateIndex()
        return self.index

    def getTurn(self) -> Token:
        return self._calculateTurn()
    
    def playSquare(self, where: Position) -> bool:
        if self.getSpacePosition(where) is not Token.BLANK:
            return False
        self._setSquareCoord(self._calculateTurn(), where)
        return True

    def copy(self):
        return Board(self.table)

    def validMove(self, position: Position):
        return position and self.getSpacePosition(position) == Token.BLANK
    
    def validNextMoves(self):
        return [Position(index) for index in range(9) if self.validMove(Position(index))]

    def isBoardFull(self):
        for token in self._valueGenerator():
            if token == Token.BLANK:
                return False
        return True
    
    def tokenHasWin(self, token: Token):
        # columns
        if token == self.getSpaceCoords(0,0) ==  self.getSpaceCoords(0,1) ==  self.getSpaceCoords(0,2):
            return True
        if token == self.getSpaceCoords(1,0) ==  self.getSpaceCoords(1,1) ==  self.getSpaceCoords(1,2):
            return True
        if token == self.getSpaceCoords(2,0) ==  self.getSpaceCoords(2,1) ==  self.getSpaceCoords(2,2):
            return True
        # rows
        if token == self.getSpaceCoords(0,0) ==  self.getSpaceCoords(1,0) ==  self.getSpaceCoords(2,0):
            return True
        if token == self.getSpaceCoords(0,1) ==  self.getSpaceCoords(1,1) ==  self.getSpaceCoords(2,1):
            return True
        if token == self.getSpaceCoords(0,2) ==  self.getSpaceCoords(1,2) ==  self.getSpaceCoords(2,2):
            return True
        # diagonals
        if token == self.getSpaceCoords(0,0) ==  self.getSpaceCoords(1,1) ==  self.getSpaceCoords(2,2):
            return True
        if token == self.getSpaceCoords(0,2) ==  self.getSpaceCoords(1,1) ==  self.getSpaceCoords(2,0):
            return True
        return False


class BoardFactory:
    def __init__(self) -> None:
        self.boardType = Board

    def newStartBoard(self):
        return self.boardType([[Token.BLANK for _ in range(3)] for _ in range(3)])

    def makeBoardFromIndex(self):
        # values = []
        # self.boardType()
        print("NOTHING")
        pass

    def createBoardWithMove(self, board: Board, position: Position) -> Board:
        newBoard = board.copy()
        newBoard.playSquare(position)
        return newBoard


class Player:
    def __init__(self, token: Token) -> None:
        self.token = token
    
    def pickMove(self, board: Board) -> Position:
        pass


class BoardView:
    def __init__(self, board: Board) -> None:
        self.board = board

    def showBoard(self):
        pass

    def showWin(self, player: Player):
        pass

    def showDraw(self):
        pass


class TerminalBoardView(BoardView):
    def __init__(self, board: Board) -> None:
        self.board = board
        self.pieces = {
            Token.BLANK: " ",
            Token.NAUGHT: "O",
            Token.CROSS: "X",
        }

    def showBoard(self):
        board_str = (
            "{}|{}|{}\n"
            "-----\n"
            "{}|{}|{}\n"
            "-----\n"
            "{}|{}|{}\n"
            ).format(*[self.pieces[piece] for piece in self.board._valueGenerator()])
        print(board_str)
    
    def showWin(self, player: Player):
        print(f"CONGRATS, {self.pieces[player.token]} wins!")

    def showDraw(self):
        print("DRAW")


class BoardReference:
    def __init__(self) -> None:
        self.tables = dict()

    def addBoard(self, board: Board):
        index = board.getIndex()
        if index not in self.tables:
            self.tables[board.getIndex()] = board


class HumanTerminalPlayer(Player):
    def _getUserInput(self, valueType, errorHelp):
        for _ in range(3):
            try:
                raw = input()
                processed = valueType(raw)
            except Exception as e:
                print("Failure to read input '{raw}'.", errorHelp)
                continue
            return processed
        print("3 failed attempts. Could not get input")
        return None

    def pickMove(self, board: Board) -> Position:
        print("Input the Row you want to pick! (1,2,3)")

        y = self._getUserInput(int, "Please use 1, 2, or 3")
        if not y:
            return None
        print("Input the Column you want to pick! (1,2,3)")
        x = self._getUserInput(int, "Please use 1, 2, or 3")
        if not x:
            return None

        return Position(x,y)



def main():
    turn = Token.NAUGHT

    bf = BoardFactory()
    board = bf.newStartBoard()
    b_view = TerminalBoardView(board)
    b_view.showBoard()

    players = {
        Token.NAUGHT: HumanTerminalPlayer(Token.NAUGHT),
        Token.CROSS: HumanTerminalPlayer(Token.CROSS)
    }

    while True:
        move = players[turn]

        if not move or not board.validMove(move):
            print("Invalid move! Try again")
        else:
            board.playSquare(move)
        b_view.showBoard()

        if board.tokenHasWin(turn):
            b_view.showWin(turn)
        if board.isBoardFull():
            b_view.showDraw()
        turn = board.getTurn()


if __name__ == "__main__":
    main()
