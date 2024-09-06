from objects.gameObjects import Board, Token, Outcome
from objects.playerviewcontroller import BoardView, Player


class TerminalBoardView(BoardView):
    pieces = {
        Token.BLANK: " ",
        Token.NAUGHT: "O",
        Token.CROSS: "X",
    }

    def showBoard(self, board: Board):
        board_str = (
            "{}|{}|{}\n"
            "-----\n"
            "{}|{}|{}\n"
            "-----\n"
            "{}|{}|{}\n"
            ).format(*[TerminalBoardView.pieces[piece] for piece in board.board])
        print(board_str)
    
    def showWin(self, board: Board, player: Player):
        print(f"CONGRATS, {TerminalBoardView.pieces[player.token]} wins!")

    def showDraw(self, board: Board):
        print("DRAW")
        
    def player_turn(self, turn: Token):
        print(f"Turn now: {TerminalBoardView.pieces[turn]} ")

    def showOutcome(self, outcome: Outcome):
        winner = "X" if outcome is Outcome.CROSS else "O" if outcome is Outcome.NAUGHT else "DRAW"
        print(f"WINNER IS {winner}")


