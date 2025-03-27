import pygame
from settings import *

class PauseMenu:
    def __init__(self):
        self.font_menu = pygame.font.Font(None, 36)
        self.menu_options = ['Continue', 'Settings', 'Main Menu']
        self.menu_buttons = []
        
    def draw(self, screen):
        # overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # menu options
        menu_width = 300
        menu_height = 400
        menu_x = WIDTH // 2 - menu_width // 2
        menu_y = HEIGHT // 2 - menu_height // 2
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, (30, 30, 30), menu_rect)
        pygame.draw.rect(screen, PRIMARY_COLOR, menu_rect, 2)
        
        # buttons
        button_height = 50
        button_margin = 20
        self.menu_buttons = []
        
        for i, option in enumerate(self.menu_options):
            button_y = menu_y + 50 + i * (button_height + button_margin)
            button_rect = pygame.Rect(menu_x + 50, button_y, menu_width - 100, button_height)
            self.menu_buttons.append(button_rect)
            
            # button background
            pygame.draw.rect(screen, PRIMARY_COLOR, button_rect)
            
            # button text
            text = self.font_menu.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
    
    def check_menu_click(self, pos):
        for i, button in enumerate(self.menu_buttons):
            if button.collidepoint(pos):
                return self.menu_options[i]
        return None