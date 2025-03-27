import pygame
from settings import *
from pause import PauseMenu


class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 42)
        self.font_score = pygame.font.Font(None, 60)  # Updated font size to match game.py
        self.pause_menu = PauseMenu()
        
        # Container dimensions
        self.container_width = WIDTH - 100
        self.container_height = HEIGHT - 100
        self.container_x = (WIDTH - self.container_width) // 2
        self.container_y = (HEIGHT - self.container_height) // 2
        
        # Game area dimensions
        self.game_area_width = self.container_width - 4
        self.game_area_height = self.container_height - 60  # Space for top UI
        self.game_area_x = self.container_x + 2
        self.game_area_y = self.container_y + 56
        
        # Pause button dimensions
        self.pause_btn_radius = 20
        self.pause_btn_x = self.container_x + self.container_width - 40
        self.pause_btn_y = self.container_y + 28

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
        """Draw the game container with borders and background"""
        # Draw border
        pygame.draw.rect(screen, PRIMARY_COLOR, 
                        (self.container_x, self.container_y, self.container_width, self.container_height), 
                        2, 12)
        
        # Draw game area background (black)
        pygame.draw.rect(screen, (0, 0, 0), 
                        (self.game_area_x, self.game_area_y, self.game_area_width, self.game_area_height), 
                        0)
        
        # Draw top UI background
        ui_height = 80
        pygame.draw.rect(screen, (18, 18, 18), 
                        (self.container_x + 2, self.container_y + 2, self.container_width - 4, ui_height), 
                        0, 12)
    
    def draw_lives(self, screen, lives):
        """Draw the player's remaining lives"""
        for i in range(lives):
            pygame.draw.circle(screen, (231, 76, 60), 
                             (self.container_x + 30 + i * 30, self.container_y + 28), 10)
    
    def draw_score(self, screen, score):
        """Draw the player's current score"""
        score_text = self.font_score.render(f"{score:05d}", True, PRIMARY_COLOR)
        score_rect = score_text.get_rect(center=(WIDTH // 2, self.container_y + 28))
        screen.blit(score_text, score_rect)
    
    def draw_pause_button(self, screen, is_paused):
        """Draw the pause/play button"""
        # Draw button background
        pygame.draw.circle(screen, (50, 50, 50), 
                         (self.pause_btn_x, self.pause_btn_y), self.pause_btn_radius)
        
        if not is_paused:
            # Draw pause icon (two vertical bars)
            pygame.draw.rect(screen, (255, 255, 255), 
                           (self.pause_btn_x - 5, self.pause_btn_y - 8, 3, 16), 0)
            pygame.draw.rect(screen, (255, 255, 255), 
                           (self.pause_btn_x + 2, self.pause_btn_y - 8, 3, 16), 0)
        else:
            # Draw play icon (triangle)
            pygame.draw.polygon(screen, (255, 255, 255), 
                             [(self.pause_btn_x - 5, self.pause_btn_y - 8), 
                              (self.pause_btn_x - 5, self.pause_btn_y + 8), 
                              (self.pause_btn_x + 7, self.pause_btn_y)])
    
    def draw_button(self, screen):
        """Draw the UI button in the corner (separate from pause button)"""
        button_width = 30
        button_height = 30
        button_x = screen.get_width() - button_width - 20
        button_y = screen.get_height() //10
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
        distance = ((pos[0] - self.pause_btn_x) ** 2 + (pos[1] - self.pause_btn_y) ** 2) ** 0.5
        return distance <= self.pause_btn_radius
    
    def check_menu_click(self, pos):
        """Check if any menu item was clicked"""
        return self.pause_menu.check_menu_click(pos)
        
    def draw_game_over(self, screen):
        """Draw the game over screen"""
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("GAME OVER", True, PRIMARY_COLOR)
        restart_text = font.render("Press R to Restart", True, PRIMARY_COLOR)
        quit_text = font.render("Press Q to Quit", True, PRIMARY_COLOR)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))
