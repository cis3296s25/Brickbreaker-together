#MultiUi.py
import pygame
from settings import UI_WIDTH, TITLE_FONT_SIZE, SCORE_FONT_SIZE, SMALL_FONT_SIZE
from MultiplayerGame import PLAYER1_COLOR, PLAYER2_COLOR, TEXT_COLOR, LIVES
from ui_constants import ACCENT_COLOR
from multiplayer_pause import MultiplayerPauseMenu

class UIElement:
    def __init__(self, screen):
        # Store screen for drawing
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # Fonts
        self.font_large = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.font_score = pygame.font.Font(None, SCORE_FONT_SIZE)
        self.pause_menu = MultiplayerPauseMenu()

    def draw_ui_panels(self, state):
        """Draw left/right side panels: scores and lives."""
        # Left panel (host / player 1)
        pygame.draw.rect(self.screen, (30, 30, 30), (0, 0, UI_WIDTH, self.screen_height))
        # Right panel (client / player 2)
        pygame.draw.rect(self.screen, (30, 30, 30),
                         (self.screen_width - UI_WIDTH, 0, UI_WIDTH, self.screen_height))
        # Divider lines
        pygame.draw.line(self.screen, PLAYER1_COLOR,
                         (UI_WIDTH, 0), (UI_WIDTH, self.screen_height), 4)
        pygame.draw.line(self.screen, PLAYER2_COLOR,
                         (self.screen_width - UI_WIDTH, 0),
                         (self.screen_width - UI_WIDTH, self.screen_height), 4)

        # Draw scores and lives
        def draw_stats(x, y, label, color, score, lives):
            lbl_s = self.font_score.render(label, True, color)
            scr_s = self.font_score.render(f"{score:04d}", True, TEXT_COLOR)
            self.screen.blit(lbl_s, (x - lbl_s.get_width() // 2, y))
            self.screen.blit(scr_s, (x - scr_s.get_width() // 2, y + 40))
            for i in range(LIVES):
                clr = color if i < lives else (50, 50, 50)
                pygame.draw.circle(self.screen, clr, (x - 35 + i * 35, y + 120), 12)

        draw_stats(UI_WIDTH // 2, self.screen_height // 3,
                   "PLAYER 1", PLAYER1_COLOR,
                   state.get('host_score', 0),
                   state.get('host_lives', 0))
        draw_stats(self.screen_width - UI_WIDTH // 2, self.screen_height // 3,
                   "PLAYER 2", PLAYER2_COLOR,
                   state.get('client_score', 0),
                   state.get('client_lives', 0))

    def draw_countdown(self, value):
        """Overlay a big countdown in the center."""
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        text = str(value)
        cnt_s = self.font_large.render(text, True, ACCENT_COLOR)
        cnt_rect = cnt_s.get_rect(center=(self.screen_width // 2,
                                          self.screen_height // 2))
        self.screen.blit(cnt_s, cnt_rect)

    def draw_pause_menu(self):
        """When paused, show the pause menu."""
        self.pause_menu.draw(self.screen)

    def draw_game_over(self, winner, local_id):
        """Overlay at end of game."""
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        go_s = self.font_large.render("GAME OVER", True, TEXT_COLOR)
        win_s = self.font_score.render(winner, True, TEXT_COLOR)
        tip_s = pygame.font.Font(None, SMALL_FONT_SIZE).render("Press R to restart", True, TEXT_COLOR)
        self.screen.blit(go_s, (self.screen_width // 2 - go_s.get_width() // 2,
                                self.screen_height // 2 - 60))
        self.screen.blit(win_s, (self.screen_width // 2 - win_s.get_width() // 2,
                                 self.screen_height // 2))
        self.screen.blit(tip_s, (self.screen_width // 2 - tip_s.get_width() // 2,
                                 self.screen_height // 2 + 60))