import os
import pygame
import chess
from game_state import GameState

WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)

ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))

class InteractiveBoard:
    def __init__(self, screen, clock, game, player_color, engine, coach):
        self.screen = screen
        self.clock = clock
        self.game = game
        self.player_color = player_color
        self.engine = engine
        self.coach = coach
        self.feedback = ""
        self.selected_square = None
        self.running = True
        self.load_images()

    def load_images(self):
        self.piece_images = {}
        for piece in ["wP", "wN", "wB", "wR", "wQ", "wK", "p", "n", "b", "r", "q", "k"]:
            file_path = os.path.join(ASSETS_DIR, f"{piece}.svg")
            if os.path.exists(file_path):
                self.piece_images[piece] = pygame.transform.scale(
                    pygame.image.load(file_path), (SQUARE_SIZE, SQUARE_SIZE)
                )

    def get_board_representation(self):
        board_matrix = []
        for rank in range(8):
            row = []
            for file in range(8):
                actual_rank = rank if self.player_color == chess.WHITE else 7 - rank
                actual_file = file if self.player_color == chess.WHITE else 7 - file
                square = chess.square(actual_file, 7 - actual_rank)
                piece = self.game.board.piece_at(square)
                if piece:
                    symbol = piece.symbol()
                    row.append(f"w{symbol}" if symbol.isupper() else symbol)
                else:
                    row.append(".")
            board_matrix.append(row)
        return board_matrix

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        if self.feedback:
            self.display_feedback()

    def display_feedback(self):
        font = pygame.font.SysFont(None, 20)
        lines = self.feedback.split('\n')
        y_offset = HEIGHT - 80
        for line in lines[:3]:  # Limit to 3 lines
            text = font.render(line.strip(), True, (255, 255, 255))
            self.screen.blit(text, (10, y_offset))
            y_offset += 20

    def draw_pieces(self):
        board_matrix = self.get_board_representation()
        for row in range(8):
            for col in range(8):
                piece = board_matrix[row][col]
                if piece in self.piece_images:
                    self.screen.blit(self.piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def get_square_clicked(self, pos):
        x, y = pos
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        actual_col = col if self.player_color == chess.WHITE else 7 - col
        actual_row = row if self.player_color == chess.WHITE else 7 - row
        return chess.square(actual_col, 7 - actual_row)

    def handle_click(self, pos):
        clicked_square = self.get_square_clicked(pos)
        if self.selected_square is None:
            piece = self.game.board.piece_at(clicked_square)
            if piece and ((self.game.board.turn and piece.color == chess.WHITE) or 
                          (not self.game.board.turn and piece.color == chess.BLACK)):
                self.selected_square = clicked_square
        else:
            move_uci = chess.Move(self.selected_square, clicked_square)
            if self.game.is_legal_move(move_uci.uci()):
                self.game.make_move(move_uci.uci())
                self._maybe_trigger_coach(move_uci.uci())
            self.selected_square = None

    def _maybe_trigger_coach(self, last_move_uci: str):
        fullmove = self.game.board.fullmove_number
        if self.game.board.turn == chess.WHITE and fullmove % 5 == 0:
            print(f"[Gemini Coach] Triggered after Black's move {fullmove}")
            self.feedback = self.coach.analyze_position(self.game.board, last_move_uci)
        else:
            self.feedback = ""

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.draw_board()
            self.draw_pieces()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (self.player_color == chess.WHITE and self.game.board.turn == chess.WHITE) or \
                       (self.player_color == chess.BLACK and self.game.board.turn == chess.BLACK):
                        self.handle_click(event.pos)

            # Engine move
            if (self.player_color == chess.WHITE and self.game.board.turn == chess.BLACK) or \
               (self.player_color == chess.BLACK and self.game.board.turn == chess.WHITE):
                pygame.time.wait(300)
                move = self.engine.get_best_move(self.game.board)
                self.game.make_move(move.uci())
                self._maybe_trigger_coach(move.uci())

            self.clock.tick(60)

        self.engine.close()
        pygame.quit()
