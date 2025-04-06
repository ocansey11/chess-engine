import chess

class BaseAgent:
    def analyze_position(self, board: chess.Board, last_move: str = None) -> str:
        """
        Analyze the current board state and return feedback or coaching advice.
        """
        raise NotImplementedError("Must implement analyze_position()")
