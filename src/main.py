import pygame
import chess
from interactive_board import InteractiveBoard
from game_state import GameState
from engine.engine_player import EnginePlayer
from agents.gemini_coach import GeminiCoach

WHITE = (238, 238, 210)

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()

        self.player_color = self.show_color_selection()
        self.engine = EnginePlayer()
        self.game = GameState()
        self.coach = GeminiCoach()
        self.board = InteractiveBoard(
            screen=self.screen,
            clock=self.clock,
            game=self.game,
            player_color=self.player_color,
            engine=self.engine,
            coach = self.coach

        )
        

    def show_color_selection(self):
        font = pygame.font.SysFont(None, 48)
        while True:
            self.screen.fill((0, 0, 0))
            white_text = font.render('Press W for White', True, WHITE)
            black_text = font.render('Press B for Black', True, WHITE)
            self.screen.blit(white_text, (150, 200))
            self.screen.blit(black_text, (150, 300))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        return chess.WHITE
                    elif event.key == pygame.K_b:
                        return chess.BLACK

    def run(self):
        self.board.run()

if __name__ == "__main__":
    manager = GameManager()
    manager.run()
