import pygame
from settings import *
from pause import PauseMenu


class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.font_score = pygame.font.Font(None, SCORE_FONT_SIZE)
        self.pause_menu = PauseMenu()
        
        # Container dimensions will be set in draw_container
        self.container_width = None
        self.container_height = None
        self.container_x = None
        self.container_y = None
        
        # Game area dimensions will be set in draw_container
        self.game_area_width = None
        self.game_area_height = None
        self.game_area_x = None
        self.game_area_y = None
        
        # Pause button dimensions will be set in draw_container
        self.pause_btn_radius = int(20 * SCALE_FACTOR)
        self.pause_btn_x = None
        self.pause_btn_y = None

    def draw(self, screen, score, lives, is_paused=False):
        # draw the container first
        self.draw_container(screen)
        
        # then draw the UI elements
        self.draw_lives(screen, lives)
        self.draw_score(screen, score)
        self.draw_pause_button(screen, is_paused)
        
        # pause menu
        if is_paused:
            self.pause_menu.draw(screen)
    
    def draw_container(self, screen):
        # Get screen dimensions
        screen_width, screen_height = screen.get_size()
        
        # Update container dimensions
        self.container_width = screen_width - int(100 * SCALE_FACTOR)
        self.container_height = screen_height - int(100 * SCALE_FACTOR)
        self.container_x = (screen_width - self.container_width) // 2
        self.container_y = (screen_height - self.container_height) // 2
        
        # Update game area dimensions
        self.game_area_width = self.container_width - int(4 * SCALE_FACTOR)
        self.game_area_height = self.container_height - int(60 * SCALE_FACTOR)  # Space for top UI
        self.game_area_x = self.container_x + int(2 * SCALE_FACTOR)
        self.game_area_y = self.container_y + int(56 * SCALE_FACTOR)
        
        # Update pause button position
        self.pause_btn_x = self.container_x + self.container_width - int(40 * SCALE_FACTOR)
        self.pause_btn_y = self.container_y + int(28 * SCALE_FACTOR)
        
        # Draw the game container
        container_rect = pygame.Rect(
            int(60 * SCALE_FACTOR), 
            int(50 * SCALE_FACTOR), 
            screen_width - int(120 * SCALE_FACTOR), 
            screen_height - int(100 * SCALE_FACTOR)
        )
        pygame.draw.rect(screen, (30, 30, 30), container_rect)  # Dark background
        pygame.draw.rect(screen, PRIMARY_COLOR, container_rect, 2)  # Border
    
    def draw_lives(self, screen, lives):
        """Draw the player's remaining lives"""
        if self.container_x is None:
            return
            
        for i in range(lives):
            pygame.draw.circle(screen, LIFE_COLOR, 
                             (self.container_x + int(30 * SCALE_FACTOR) + i * int(30 * SCALE_FACTOR), 
                              self.container_y + int(28 * SCALE_FACTOR)), 
                             int(10 * SCALE_FACTOR))
    
    def draw_score(self, screen, score):
        """Draw the player's current score"""
        if self.container_x is None:
            return
            
        screen_width = screen.get_width()
        score_text = self.font_score.render(f"{score:05d}", True, PRIMARY_COLOR)
        score_rect = score_text.get_rect(center=(screen_width // 2, self.container_y + int(28 * SCALE_FACTOR)))
        screen.blit(score_text, score_rect)
    
    def draw_pause_button(self, screen, is_paused):
        """Draw the pause/play button"""
        if self.pause_btn_x is None:
            return
            
        # Draw button background
        pygame.draw.circle(screen, (50, 50, 50), 
                         (self.pause_btn_x, self.pause_btn_y), self.pause_btn_radius)
        
        if not is_paused:
            # Draw pause icon (two vertical bars)
            pygame.draw.rect(screen, (255, 255, 255), 
                           (self.pause_btn_x - int(5 * SCALE_FACTOR), 
                            self.pause_btn_y - int(8 * SCALE_FACTOR), 
                            int(3 * SCALE_FACTOR), 
                            int(16 * SCALE_FACTOR)), 0)
            pygame.draw.rect(screen, (255, 255, 255), 
                           (self.pause_btn_x + int(2 * SCALE_FACTOR), 
                            self.pause_btn_y - int(8 * SCALE_FACTOR), 
                            int(3 * SCALE_FACTOR), 
                            int(16 * SCALE_FACTOR)), 0)
        else:
            # Draw play icon (triangle)
            pygame.draw.polygon(screen, (255, 255, 255), 
                             [(self.pause_btn_x - int(5 * SCALE_FACTOR), self.pause_btn_y - int(8 * SCALE_FACTOR)), 
                              (self.pause_btn_x - int(5 * SCALE_FACTOR), self.pause_btn_y + int(8 * SCALE_FACTOR)), 
                              (self.pause_btn_x + int(7 * SCALE_FACTOR), self.pause_btn_y)])
    
    def draw_button(self, screen):
        """Draw the UI button in the corner (separate from pause button)"""
        button_width = int(30 * SCALE_FACTOR)
        button_height = int(30 * SCALE_FACTOR)
        button_x = screen.get_width() - button_width - int(20 * SCALE_FACTOR)
        button_y = screen.get_height() // 10
        self.button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (52, 152, 219), self.button_rect)
        
        # Add button border effect
        pygame.draw.rect(screen, (41, 128, 185), self.button_rect, 2)
    
    def check_button_click(self, pos):
        """Check if the UI button was clicked"""
        if hasattr(self, 'button_rect'):
            return self.button_rect.collidepoint(pos)
        return False
    
    def check_pause_button_click(self, pos):
        """Check if the pause button was clicked"""
        if self.pause_btn_x is None:
            return False
            
        distance = ((pos[0] - self.pause_btn_x) ** 2 + (pos[1] - self.pause_btn_y) ** 2) ** 0.5
        return distance <= self.pause_btn_radius
    
    def check_menu_click(self, pos):
        """Check if any menu item was clicked"""
        return self.pause_menu.check_menu_click(pos)
        
    def draw_game_over(self, screen):
        """Draw the game over screen"""
        screen_width, screen_height = screen.get_size()
        font = pygame.font.Font(None, TITLE_FONT_SIZE)
        game_over_text = font.render("GAME OVER", True, PRIMARY_COLOR)
        restart_text = font.render("Press R to Restart", True, PRIMARY_COLOR)
        quit_text = font.render("Press Q to Quit", True, PRIMARY_COLOR)

        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - int(50 * SCALE_FACTOR)))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2))
        screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 + int(50 * SCALE_FACTOR)))
