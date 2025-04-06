from gemini_coach import GeminiCoach
import chess

coach = GeminiCoach()
board = chess.Board()
board.push_uci("e2e4")

feedback = coach.analyze_position(board, last_move="e2e4")

print("\n[Gemini Coach Feedback]")
print(feedback)


# import google.generativeai as genai
# from config import GEMINI_API_KEY

# # Configure Gemini
# genai.configure(api_key=GEMINI_API_KEY)

# # List available models
# print("\n📦 Available Gemini Models:")
# for model in genai.list_models():
#     print(f"- {model.name} | {model.description}")
