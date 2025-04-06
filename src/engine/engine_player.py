import chess.engine
import os

class EnginePlayer:
    def __init__(self, time_limit=0.1):
        # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # engine_path = os.path.join(base_dir, "stockfish", "stockfish_16_x64_avx2.exe")
        # self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        # self.time_limit = time_limit
        engine_path = r"C:\Users\kevin\Desktop\BU\chess-engine\stockfish\stockfish-windows-x86-64-avx2.exe"
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.time_limit = time_limit


    def get_best_move(self, board):
        result = self.engine.play(board, chess.engine.Limit(time=self.time_limit))
        return result.move

    def close(self):
        self.engine.quit()
