import pygame
from settings import *

class PauseMenu:
    def __init__(self):
        self.font_menu = pygame.font.Font(None, LABEL_FONT_SIZE)
        self.font_title = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.menu_options = ['Continue', 'Settings', 'Main Menu']
        self.menu_buttons = []
        
    def draw(self, screen):
        # Get screen dimensions from the screen object
        screen_width, screen_height = screen.get_size()
        
        # Create overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  
        screen.blit(overlay, (0, 0))
        
        # Menu panel
        menu_width = int(300 * SCALE_FACTOR)
        menu_height = int(400 * SCALE_FACTOR)
        menu_x = screen_width // 2 - menu_width // 2
        menu_y = screen_height // 2 - menu_height // 2
        
        # Shadow
        shadow_offset = int(10 * SCALE_FACTOR)
        shadow = pygame.Rect(menu_x + shadow_offset, menu_y + shadow_offset, 
                           menu_width, menu_height)
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow, 0, int(12 * SCALE_FACTOR))
        
        # Main menu
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, (30, 30, 30), menu_rect, 0, int(12 * SCALE_FACTOR))  
        pygame.draw.rect(screen, PRIMARY_COLOR, menu_rect, 2, int(12 * SCALE_FACTOR))  
        
        # Title
        title = self.font_title.render("PAUSED", True, PRIMARY_COLOR)
        title_rect = title.get_rect(center=(screen_width // 2, menu_y + int(30 * SCALE_FACTOR)))
        screen.blit(title, title_rect)
        
        # Buttons
        button_height = int(50 * SCALE_FACTOR)
        button_margin = int(20 * SCALE_FACTOR)
        self.menu_buttons = []
        
        for i, option in enumerate(self.menu_options):
            button_y = menu_y + int(100 * SCALE_FACTOR) + i * (button_height + button_margin)  
            button_rect = pygame.Rect(menu_x + int(50 * SCALE_FACTOR), button_y, 
                                    menu_width - int(100 * SCALE_FACTOR), button_height)
            self.menu_buttons.append(button_rect)
            
            # Button shadow
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                # Hover
                pygame.draw.rect(screen, (PRIMARY_COLOR[0], PRIMARY_COLOR[1], PRIMARY_COLOR[2], 200), 
                               button_rect, 0, int(8 * SCALE_FACTOR))  
                pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, int(8 * SCALE_FACTOR))  
            else:
                # Normal
                pygame.draw.rect(screen, PRIMARY_COLOR, button_rect, 0, int(8 * SCALE_FACTOR))  
            
            # Button text
            text = self.font_menu.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
    
    def check_menu_click(self, pos):
        for i, button in enumerate(self.menu_buttons):
            if button.collidepoint(pos):
                return self.menu_options[i]
        return None