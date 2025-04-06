import chess

class GameState:
    """
    Manages chess game state, PGN tracking, and move validation.
    """
    def __init__(self):
        self.board = chess.Board()

    def is_legal_move(self, move):
        return chess.Move.from_uci(move) in self.board.legal_moves

    def make_move(self, move):
        chess_move = chess.Move.from_uci(move)
        if chess_move in self.board.legal_moves:
            self.board.push(chess_move)
            return True
        return False

    def get_turn(self):
        return "white" if self.board.turn else "black"

    def get_legal_moves(self, from_square):
        return [move.uci() for move in self.board.legal_moves if move.uci().startswith(from_square)]

    def reset(self):
        self.board.reset()
