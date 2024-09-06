from objects.gameObjects import Board, Outcome
from objects.graph import Graph, Node

from utils.graph_utils import search_all_boards

class BoardAnalysis:
    def calculate_best_play(graph: Graph) -> dict:
        board_analysis = {}  # {int: Outcome, ... }  # index: better player

        start_node = graph.get_start()

        # Depth first search, otherwise we will be loading literally every single node at once

        def best_play_at_node(node: Node) -> Outcome:
            if node.value in board_analysis:
                return board_analysis[node.value]
            
            board = Board.fromIndex(node.value)
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

    board_analysis = calculate_best_play(search_all_boards())
