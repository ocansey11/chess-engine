from behave import given, when, then
from src.game_state import GameState
from src.engine.engine_player import EnginePlayer
import chess

@given("the game is initialized")
def step_initialize_game(context):
    context.game = GameState()
    context.engine = EnginePlayer()
    context.board = context.game.board

@given('the player chooses "{color}"')
def step_choose_color(context, color):
    context.player_color = chess.WHITE if color == "white" else chess.BLACK

@when('the player makes the move "{uci_move}"')
def step_make_player_move(context, uci_move):
    success = context.game.make_move(uci_move)
    assert success, f"Move {uci_move} was not legal"

@then("the engine should respond with a legal move")
def step_engine_moves(context):
    move = context.engine.get_best_move(context.board)
    assert move in context.board.legal_moves
    context.game.make_move(move.uci())
    context.last_engine_move = move.uci()

@then("it should be black's turn before the engine moves")
def step_turn_check(context):
    if context.player_color == chess.WHITE:
        assert context.board.turn == chess.BLACK
    else:
        assert context.board.turn == chess.WHITE

# @then("it should be black's turn")
# def step_turn_check(context):
#     expected = chess.BLACK if context.player_color == chess.WHITE else chess.WHITE
#     assert context.board.turn == expected
