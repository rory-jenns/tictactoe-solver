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
    def __init__(self, start=None) -> None:
        self.nodes = {}
        self.start = start

    def has_node_by_index(self, index: int) -> bool:
        return index in self.nodes
    
    def add_node(self, node: Node) -> None:
        self.nodes[node.value] = node

    def get_node(self, node_index: int) -> Node:
        if node_index not in self.nodes:
            return None
        return self.nodes[node_index]
    
    def get_start(self) -> Node:
        if self.start:
            return self.start
        return self.get_node(0)
    
    def str_out(self) -> str:
        return "\n".join([str(node) for node in self.nodes.values()])

