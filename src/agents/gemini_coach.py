import chess
import google.generativeai as genai
from agents.base_agent import BaseAgent
from agents.config import GEMINI_API_KEY
import os

class GeminiCoach(BaseAgent):
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("models/gemini-1.5-pro")  # ✅ Confirmed working model

    def analyze_position(self, board: chess.Board, last_move: str = None) -> str:
        fen = board.fen()
        print(fen,last_move)
        prompt = self._build_prompt(fen, last_move)

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"[Gemini error]: {e}"

    def _build_prompt(self, fen: str, last_move: str = None) -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), "prompt_templates", "coach_prompt.txt")
        with open(prompt_path, "r") as f:
            template = f.read()
        return template.replace("{FEN}", fen).replace("{LAST_MOVE}", last_move or "None")
