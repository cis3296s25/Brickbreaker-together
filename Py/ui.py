import pygame
from settings import *
from pause import PauseMenu


class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 42)
        self.font_score = pygame.font.Font(None, 24)
        self.pause_menu = PauseMenu()

    def draw(self, screen, score, lives, is_paused=False):
        score_text = self.font_score.render(str(score), True, PRIMARY_COLOR)
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//8))
        screen.blit(score_text, score_rect)

        for i in range(lives):
            pygame.draw.circle(screen, LIFE_COLOR, (100 + i * 25, 70), 8)
            
        self.draw_button(screen)
        
        if is_paused:
            self.pause_menu.draw(screen)
    
    def draw_button(self, screen):
        button_width = 30
        button_height = 30
        button_x = screen.get_width() - button_width - 20
        button_y = screen.get_height() //10
        self.button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (52, 152, 219), self.button_rect)
        
        # Add button border effect
        pygame.draw.rect(screen, (41, 128, 185), self.button_rect, 2)
    
    def check_button_click(self, pos):
        if hasattr(self, 'button_rect'):
            return self.button_rect.collidepoint(pos)
        return False
    
    def check_menu_click(self, pos):
        return self.pause_menu.check_menu_click(pos)
