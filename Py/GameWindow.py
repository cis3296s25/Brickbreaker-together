import pygame
import sys

# Initialize pygame
pygame.init()

# Define colors
PRIMARY_COLOR = (52, 152, 219)  # #3498db - Blue
BACKGROUND_COLOR = (18, 18, 18)  # #121212 - Dark gray/black
UI_BACKGROUND = (30, 30, 30)  # Slightly lighter black background
TEXT_COLOR = (255, 255, 255)  # #ffffff - White
LIFE_COLOR = (231, 76, 60)  # #e74c3c - Red

# Set game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BrickBreaker")

# Load fonts
try:
    font_large = pygame.font.SysFont("Segoe UI", 42, bold=True)
    font_score = pygame.font.SysFont("Segoe UI", 24, bold=True)
    font_small = pygame.font.SysFont("Segoe UI", 20)
except:
    # If a specific font is unavailable, use the default font
    font_large = pygame.font.Font(None, 42)
    font_score = pygame.font.Font(None, 24)
    font_small = pygame.font.Font(None, 20)

class Game:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.game_active = False
        
    def draw_ui(self):
        # Draw title
        title_text = font_large.render("BRICKBREAKER", True, PRIMARY_COLOR)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        # Create UI panel background - corresponding to the red box in the image
        ui_panel = pygame.Rect(80, 100, WIDTH - 160, 40)
        pygame.draw.rect(screen, UI_BACKGROUND, ui_panel, border_radius=0)
        
        # Add a blue line at the top of the UI panel
        pygame.draw.line(screen, PRIMARY_COLOR, (ui_panel.left, ui_panel.top), 
                         (ui_panel.right, ui_panel.top), 2)
        
        # Draw lives - on the left side
        for i in range(self.lives):
            pygame.draw.circle(screen, LIFE_COLOR, (100 + i * 25, ui_panel.centery), 8)
        
        # Draw score - centered
        score_text = font_score.render(f"{self.score:05d}", True, PRIMARY_COLOR)
        score_rect = score_text.get_rect(center=(WIDTH // 2, ui_panel.centery))
        screen.blit(score_text, score_rect)
        

        #pause button
        right_icon_x = WIDTH - 120
        pygame.draw.rect(screen, PRIMARY_COLOR, (right_icon_x, ui_panel.centery - 8, 16, 16), border_radius=4)
        
        # Draw game area
        game_rect = pygame.Rect(80, 140, WIDTH - 160, HEIGHT - 190)
        pygame.draw.rect(screen, (0, 0, 0), game_rect, border_radius=0)
        pygame.draw.rect(screen, (50, 50, 50), game_rect, 2, border_radius=0)
        
        if not self.game_active:
            text = font_small.render("GAME SCREEN", True, (80, 80, 80))
            text_rect = text.get_rect(center=(WIDTH // 2, game_rect.centery))
            screen.blit(text, text_rect)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_active = not self.game_active
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Clear screen
            screen.fill(BACKGROUND_COLOR)
            
            # Draw UI
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            
            # Control frame rate
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
