from enum import IntEnum
from typing import Any
from random import randint

import click

## TIC TAC TOE MODEL 

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
    def __init__(self, a:Token,b:Token,c:Token,d:Token,e:Token,f:Token,g:Token,h:Token,i:Token):
        self.board = (a,b,c,d,e,f,g,h,i)
        self.index = -1
        self.blank_count = sum(True for c in self.board if c is Token.BLANK)
        self.naught_count = sum(True for c in self.board if c is Token.NAUGHT)
        self.cross_count = sum(True for c in self.board if c is Token.CROSS)
    
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


class Node:
    def __init__(self, value: int, edges: set =None):
        self.value = value
        self.out_edges = edges if edges else set()
    
    def add_edge(self, edge: int):
        self.out_edges.add(edge)
    
    def __str__(self) -> str:
        if len(self.out_edges) == 0:
            return f"{self.value}:"
        return f"{self.value}:" + ",".join((str(edge) for edge in self.out_edges))


class Graph:
    def __init__(self) -> None:
        self.nodes = {}

    def has_node_by_index(self, index: int) -> bool:
        return index in self.nodes
    
    def add_node(self, node: Node) -> None:
        self.nodes[node.value] = node

    def get_node(self, node_index: int) -> Node:
        if node_index not in self.nodes:
            return None
        return self.nodes[node_index]
    
    def str_out(self) -> str:
        return "\n".join([str(node) for node in self.nodes.values()])


board_dict = {}


def makeBoardFromIndex(index: int) -> Board:
    if index in board_dict:
        return board_dict[index]
    tokens = []
    for power in three_powers:
        tokens.append(Token(int(index // power) % 3))
    board_dict[index] = Board(tokens[0],tokens[1],tokens[2],tokens[3],tokens[4],tokens[5],tokens[6],tokens[7],tokens[8])
    return board_dict[index]


def createBoardNode(board: Board) -> Node:
    if board.complete():
        return Node(board.get_board_index(), None)
    moves = board.valid_moves()
    next_board_indicies = [board.board_index_with_move(move) for move in moves]
    edges = set()
    for index in next_board_indicies:
        board_dict[index] = makeBoardFromIndex(index)
        edges.add(index)

    return Node(board.get_board_index(), edges)


def makeNodeFromIndex(index: int) -> Node:
    board = makeBoardFromIndex(index)
    node = createBoardNode(board)
    return node


## GET ANALYSIS

def search_all_boards():
    start_node = createBoardNode(makeBoardFromIndex(0))

    graph = Graph()
    to_search: list[Node] = [start_node]

    count = 1
    while to_search:
        node: Node = to_search.pop()
        count += 1

        graph.add_node(node)
        
        for edge in node.out_edges:
            edge: int
            if graph.has_node_by_index(edge):
                continue
            new_node = makeNodeFromIndex(edge)
            if not new_node:
                continue
            to_search.append(new_node)
    
    return graph


def write_graph(graph: Graph, filename: str = "graph.txt") -> None:
    text = graph.str_out()
    with open(filename, "w+") as f:
        f.write(text)


def read_graph(filename: str = "graph.txt") -> Graph:
    with open(filename, "r") as f:
        text = f.read().split("\n")
    
    def node_from_line(line:str):
        value_text, edges_text = line.split(":")
        value = int(value_text)
        if edges_text == '':
            edges = None
        else:
            edges = set(int(e) for e in edges_text.split(","))
        return Node(value, edges)
    
    g = Graph()
    for line in text:
        g.add_node(node_from_line(line))
    
    return g


def calculate_best_play(graph: Graph) -> dict:
    board_analysis = {}  # {int: Outcome, ... }  # index: better player

    start_node = graph.get_node(0)

    # Depth first search, otherwise we will be loading literally every single node at once

    def best_play_at_node(node: Node) -> Outcome:
        if node.value in board_analysis:
            return board_analysis[node.value]
        
        board = makeBoardFromIndex(node.value)
        if board.complete():
            board_analysis[node.value] = board.outcome()
            return board_analysis[node.value]
        board_status = board.outcome()
        
        player = Outcome.token_outcome(board.turn())
        opponent = Outcome.token_outcome(board.opponent())

        # Do not break this early, I want to explore all nodes!
        current_best = None
        for edge in node.out_edges:
            edge_best_play = best_play_at_node(graph.get_node(edge))
            if current_best is None:
                current_best = edge_best_play
            elif edge_best_play is Outcome.DRAW:
                if current_best != player:
                    current_best = edge_best_play
            elif edge_best_play == player:
                current_best = edge_best_play
        
        board_analysis[node.value] = current_best
        return current_best

    start_node_best_play = best_play_at_node(start_node)

    return board_analysis


class BoardAnalysis:
    board_analysis = calculate_best_play(search_all_boards())


## HANDLING GAMEPLAY

class Player:
    def __init__(self, token: Token) -> None:
        self.token = token
    
    def pickMove(self, board: Board) -> int:
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


class GameController:
    def __init__(self, players: dict[Token, Player], view: BoardView) -> None:
        self.view = view
        self.players = players

    def runGame(self):
        board = makeBoardFromIndex(0)
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

            if board.outcome() is Outcome.token_outcome(turn):
                b_view.showWin(board, self.players[turn])
                return Outcome.token_outcome(turn)
            elif board.outcome() is Outcome.DRAW:
                b_view.showDraw(board)
                return Outcome.DRAW
            
            turn = board.turn()


## OPTIONS

@click.command()
@click.option("--writegraph", is_flag=True, type=click.BOOL, default=False)
@click.option("--playcross", is_flag=True, type=click.BOOL, default=False)
@click.option("--twoplayer", is_flag=True, type=click.BOOL, default=False)
@click.option("--boteasy", is_flag=True, type=click.BOOL, default=False)
@click.option("--bothard", is_flag=True, type=click.BOOL, default=False)
@click.option("--optimallybad", is_flag=True, type=click.BOOL, default=False)
def main(writegraph, playcross, twoplayer, boteasy, bothard, optimallybad):
    if writegraph:
        write_graph(search_all_boards())

    if playcross:
        human = Token.CROSS
        other = Token.NAUGHT 
    else:
        human = Token.NAUGHT
        other = Token.CROSS 

    if twoplayer:
        players = {
            human: HumanTerminalPlayer(human),
            other: HumanTerminalPlayer(other)
        }
    elif boteasy:
        players = {
            human: HumanTerminalPlayer(human),
            other: RandomAIPlayer(other)
        }
    elif bothard:
        players = {
            human: HumanTerminalPlayer(human),
            other: SmartAIPlayer(other)
        }
    elif optimallybad:
        players = {
            human: HumanTerminalPlayer(human),
            other: OptimallyBadAIPlayer(other)
        }
    else:  # bothard by default
        players = {
            human: HumanTerminalPlayer(human),
            other: SmartAIPlayerRework(other)
        }
    
    controller = GameController(players, TerminalBoardView)
    controller.runGame()


if __name__ == "__main__":
    main()
