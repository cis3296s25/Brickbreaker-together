import pygame
from settings import *

class MultiplayerPauseMenu:
    def __init__(self):
        self.font_menu = pygame.font.Font(None, 36)
        self.font_title = pygame.font.Font(None, 48)
        self.menu_options = ['Continue', 'Settings', 'Main Menu']
        self.menu_buttons = []
        
    def draw(self, screen):
        # Get screen dimensions from the screen object
        screen_width, screen_height = screen.get_size()
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Same opacity as single player
        screen.blit(overlay, (0, 0))
        
        # Menu panel
        menu_width = 300
        menu_height = 400  # Same height as single player for three options
        menu_x = screen_width // 2 - menu_width // 2
        menu_y = screen_height // 2 - menu_height // 2
        
        # Shadow
        shadow_offset = 10
        shadow = pygame.Rect(menu_x + shadow_offset, menu_y + shadow_offset, 
                           menu_width, menu_height)
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow, 0, 12)
        
        # Main menu panel
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, (30, 30, 30), menu_rect, 0, 12)
        pygame.draw.rect(screen, PRIMARY_COLOR, menu_rect, 2, 12)
        
        # Title
        title = self.font_title.render("PAUSED", True, PRIMARY_COLOR)
        title_rect = title.get_rect(center=(screen_width // 2, menu_y + 30))
        screen.blit(title, title_rect)
        
        # Buttons
        button_height = 50
        button_margin = 20
        self.menu_buttons = []
        
        for i, option in enumerate(self.menu_options):
            button_y = menu_y + 100 + i * (button_height + button_margin)
            button_rect = pygame.Rect(menu_x + 50, button_y, menu_width - 100, button_height)
            self.menu_buttons.append(button_rect)
            
            # Button shadow and hover effect
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (PRIMARY_COLOR[0], PRIMARY_COLOR[1], PRIMARY_COLOR[2], 200),
                               button_rect, 0, 8)
                pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, 8)
            else:
                pygame.draw.rect(screen, PRIMARY_COLOR, button_rect, 0, 8)
            
            # Button text
            text = self.font_menu.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
    
    def check_menu_click(self, pos):
        for i, button in enumerate(self.menu_buttons):
            if button.collidepoint(pos):
                return self.menu_options[i]
        return None