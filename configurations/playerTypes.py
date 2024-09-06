from random import randint

from objects.gameObjects import Token, Board, Outcome
from objects.playerviewcontroller import Player
from AI.minimax import BoardAnalysis
from AI.menace import MENACE

class HumanTerminalPlayer(Player):
    def _getUserInput(self, valueType, errorHelp, options=None):
        for _ in range(3):
            try:
                raw = input()
                processed = valueType(raw)
            except Exception as e:
                print("Failure to read input '{raw}'.", errorHelp)
                continue
            if options and processed not in options:
                continue
            return processed
        print("3 failed attempts. Could not get input")
        return None

    def pickMove(self, board: Board) -> int:
        print("Input the Row you want to pick! (1,2,3)")

        y = self._getUserInput(int, "Please use 1, 2, or 3", options=(1,2,3))
        if not y:
            return None
        print("Input the Column you want to pick! (1,2,3)")
        x = self._getUserInput(int, "Please use 1, 2, or 3", options=(1,2,3))
        if not x:
            return None
        
        x -= 1
        y -= 1

        return x + (y*3)


class RandomAIPlayer(Player):
    def pickMove(self, board: Board) -> int:
        valid_moves = board.valid_moves()
        move_choice = randint(0, len(valid_moves)-1)
        return valid_moves[move_choice]


class SmartAIPlayer(Player):
    def pickMove(self, board: Board) -> int:
        main_index = board.get_board_index()
        best_outcome = BoardAnalysis.board_analysis[main_index]
        next_board_move_index_pairs = [(move, board.board_index_with_move(move)) for move in board.valid_moves()]
        next_move_options = []
        for move, next_index in next_board_move_index_pairs:
            if BoardAnalysis.board_analysis[next_index] == best_outcome:
                next_move_options.append(move)
        
        move_choice = randint(0, len(next_move_options)-1)
        return next_move_options[move_choice]


class SmartAIPlayerRework(Player):
    def pickMove(self, board: Board) -> int:
        best_outcome = Outcome.token_outcome(self.token)
        next_board_move_index_pairs = [(move, board.board_index_with_move(move)) for move in board.valid_moves()]
        win_moves = []
        draw_moves = []
        lose_moves = []
        for move, next_index in next_board_move_index_pairs:
            analysis = BoardAnalysis.board_analysis[next_index]
            if analysis == best_outcome:
                win_moves.append(move)
            elif analysis == Outcome.DRAW:
                draw_moves.append(move)
            else:
                lose_moves.append(move)
        
        if win_moves:
            next_move_options = win_moves 
        elif draw_moves:
            next_move_options = draw_moves 
        elif lose_moves:
            next_move_options = lose_moves 

        move_choice = randint(0, len(next_move_options)-1)
        return next_move_options[move_choice]


class OptimallyBadAIPlayer(Player):
    def pickMove(self, board: Board) -> int:
        best_outcome = Outcome.token_outcome(self.token)
        next_board_move_index_pairs = [(move, board.board_index_with_move(move)) for move in board.valid_moves()]
        win_moves = []
        draw_moves = []
        lose_moves = []
        for move, next_index in next_board_move_index_pairs:
            analysis = BoardAnalysis.board_analysis[next_index]
            if analysis == best_outcome:
                win_moves.append(move)
            elif analysis == Outcome.DRAW:
                draw_moves.append(move)
            else:
                lose_moves.append(move)
        
        if lose_moves:
            next_move_options = lose_moves 
        elif draw_moves:
            next_move_options = draw_moves 
        elif win_moves:
            next_move_options = win_moves 

        move_choice = randint(0, len(next_move_options)-1)
        return next_move_options[move_choice]


class MENACEPlayer(Player):
    # The MENACE state persists between games
    menace = MENACE()
    def __init__(self, token: Token) -> None:
        super().__init__(token)
        self.MENACE = MENACEPlayer.menace
    
    def pickMove(self, board: Board) -> int:
        move = self.MENACE.make_move(board)
        return move

    def end_game(self, outcome: Outcome) -> None:
        return self.MENACE.reinforce(outcome)

