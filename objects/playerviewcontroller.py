from objects.gameObjects import Board, Token, Outcome


class Player:
    def __init__(self, token: Token) -> None:
        self.token = token
    
    def pickMove(self, board: Board) -> int:
        pass

    def end_game(self, outcome: Outcome) -> None:
        pass


class BoardView:
    def __init__(self, board: Board) -> None:
        pass

    def showBoard(self, board: Board):
        pass

    def showWin(self, board: Board, player: Player):
        pass

    def showDraw(self, board: Board):
        pass

    def player_turn(self, turn: Token):
        pass

    def showOutcome(self, outcome: Outcome):
        pass


class GameController:
    def __init__(self, players: dict[Token, Player], view: BoardView) -> None:
        self.view = view
        self.players = players

    def runGame(self):
        board = Board.fromIndex(0)
        b_view = self.view(board)
        b_view.showBoard(board)

        turn = board.turn()
        while True:
            b_view.player_turn(turn)
            move = self.players[turn].pickMove(board)
            if move is None or move not in board.valid_moves():
                print("Invalid move! Try again")
            else:
                board = board.board_with_move(move)
            
            b_view.showBoard(board)
            
            if board.outcome() is not Outcome.INCOMPLETE:
                break

            turn = board.turn()
        
        for player in self.players.values():
            player.end_game(board.outcome())

        
        if board.outcome() is Outcome.token_outcome(turn):
            b_view.showWin(board, self.players[turn])
            return Outcome.token_outcome(turn)
        elif board.outcome() is Outcome.DRAW:
            b_view.showDraw(board)
            return Outcome.DRAW
            