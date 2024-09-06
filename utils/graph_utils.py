from objects.gameObjects import Board
from objects.graph import Graph, Node


def createBoardNode(board: Board) -> Node:
    if board.complete():
        return Node(board.get_board_index(), None)
    moves = board.valid_moves()
    next_board_indicies = [board.board_index_with_move(move) for move in moves]
    edges = set()
    for index in next_board_indicies:
        Board.board_dict[index] = Board.fromIndex(index)
        edges.add(index)

    return Node(board.get_board_index(), edges)


def makeNodeFromIndex(index: int) -> Node:
    board = Board.fromIndex(index)
    node = createBoardNode(board)
    return node


def search_all_boards() -> Graph:
    start_node = makeNodeFromIndex(0)

    graph = Graph(start_node)
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
