from objects.gameObjects import Board


class SymmetryUtil:
    @staticmethod
    def rotate(board: Board, n:int = 1) -> Board:
        def rotate_once(b: Board) -> Board:
            indexes = (2,5,8,1,4,7,0,3,6)
            return Board.fromList([b.board[i] for i in indexes])
        for _ in range(n % 4):
            board = rotate_once(board)
        return board

    @staticmethod
    def flip(b: Board) -> Board:
        indexes = (2,1,0,5,4,3,8,7,6)
        return Board.fromList([b.board[i] for i in indexes])

    @staticmethod
    def smallest_symmetric_board(board: Board) -> int:
        flipped = SymmetryUtil.flip(board)
        boards = [board, SymmetryUtil.rotate(board, 1),  SymmetryUtil.rotate(board, 2),  SymmetryUtil.rotate(board, 3),
                flipped, SymmetryUtil.rotate(flipped, 1),  SymmetryUtil.rotate(flipped, 2),  SymmetryUtil.rotate(flipped, 3)]
        smallest_index = min([b.get_board_index() for b in boards])
        return smallest_index

    @staticmethod
    def restore_position(src_board: Board, dest_board: Board, src_pos: int) -> int:    
        rotation_matrix = (2,5,8,1,4,7,0,3,6)
        dest_index = dest_board.get_board_index()
        if dest_index == src_board.get_board_index():
            return src_pos
        if dest_index == SymmetryUtil.rotate(src_board, 1).get_board_index():
            return rotation_matrix.index(src_pos)
        if dest_index == SymmetryUtil.rotate(src_board, 2).get_board_index():
            return rotation_matrix.index(rotation_matrix.index(src_pos))
        if dest_index == SymmetryUtil.rotate(src_board, 3).get_board_index():
            return rotation_matrix.index(rotation_matrix.index(rotation_matrix.index(src_pos)))
        flip_matrix = (2,1,0,5,4,3,8,7,6)
        flipped_pos = flip_matrix.index(src_pos)
        flipped_src_board = SymmetryUtil.flip(src_board)
        if dest_index == flipped_src_board.get_board_index():
            return flipped_pos
        if dest_index == SymmetryUtil.rotate(flipped_src_board, 1).get_board_index():
            return rotation_matrix.index(flipped_pos)
        if dest_index == SymmetryUtil.rotate(flipped_src_board, 2).get_board_index():
            return rotation_matrix.index(rotation_matrix.index(flipped_pos))
        if dest_index == SymmetryUtil.rotate(flipped_src_board, 3).get_board_index():
            return rotation_matrix.index(rotation_matrix.index(rotation_matrix.index(flipped_pos)))
