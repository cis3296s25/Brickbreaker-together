import pygame
import sys
from brick import Brick  
from settings import *

# Initialize Pygame
pygame.init()
init_screen_dimensions()

# Colors
BACKGROUND_COLOR = (18, 18, 18)
PLAYER1_COLOR = (52, 152, 219)  # Blue
PLAYER2_COLOR = (231, 76, 60)   # Red
BRICK_COLORS = [
    (230, 245, 255),  
    (198, 231, 250), 
    (166, 212, 245),  
    (135, 191, 235),  
    (104, 165, 222),  
    (73, 140, 208),   
    (44, 115, 194),  
    (28, 98, 173),    
    (19, 79, 149),    
    (12, 61, 123)   
]
TEXT_COLOR = (255, 255, 255)    # White
UI_BACKGROUND = (18, 18, 18, 220)

# Game elements dimensions
PADDLE_WIDTH = int(150 * SCALE_FACTOR)
PADDLE_HEIGHT = int(10 * SCALE_FACTOR)
BALL_RADIUS = int(8 * SCALE_FACTOR)
BRICK_WIDTH = int(54 * SCALE_FACTOR)
BRICK_HEIGHT = int(20 * SCALE_FACTOR)
BRICK_ROWS = 10
BRICK_COLS = 15
BRICK_PADDING = int(8 * SCALE_FACTOR)
LIVES = 3

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("BRICKBREAKER TOGETHER")
clock = pygame.time.Clock()
FPS = 60

# Font setup - using scaled fonts from settings
title_font = pygame.font.SysFont('Arial', TITLE_FONT_SIZE, bold=True)
label_font = pygame.font.SysFont('Arial', LABEL_FONT_SIZE, bold=True)
score_font = pygame.font.SysFont('Arial', SCORE_FONT_SIZE, bold=True)
small_font = pygame.font.SysFont('Arial', SMALL_FONT_SIZE)

class UIElement:
    def __init__(self):
        # Use constant screen dimensions from settings.py
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        
        # Calculate positions
        self.game_rect = pygame.Rect(
            (self.screen_width - GAME_WIDTH) // 2, 
            (self.screen_height - GAME_HEIGHT) // 2 + int(20 * SCALE_FACTOR), 
            GAME_WIDTH, 
            GAME_HEIGHT
        )
        
        # Create static paddles
        self.player1_paddle = pygame.Rect(
            self.game_rect.centerx - PADDLE_WIDTH // 2,
            self.game_rect.top + int(20 * SCALE_FACTOR),
            PADDLE_WIDTH,
            PADDLE_HEIGHT
        )
        
        self.player2_paddle = pygame.Rect(
            self.game_rect.centerx - PADDLE_WIDTH // 2,
            self.game_rect.bottom - int(20 * SCALE_FACTOR) - PADDLE_HEIGHT,
            PADDLE_WIDTH,
            PADDLE_HEIGHT
        )
        
        # Static ball positions
        self.ball1_pos = (
            self.game_rect.centerx,
            self.game_rect.top + int(60 * SCALE_FACTOR)
        )
        
        self.ball2_pos = (
            self.game_rect.centerx,
            self.game_rect.bottom - int(60 * SCALE_FACTOR)
        )
        

        self.bricks = []
        self.create_bricks()
        
        # Static scores and lives
        self.player1_score = 0
        self.player2_score = 0
        self.player1_lives = LIVES
        self.player2_lives = LIVES
        
    def create_bricks(self):
        self.BRICK_COLORS = [
            (230, 245, 255),  
            (198, 231, 250), 
            (166, 212, 245),  
            (135, 191, 235),  
            (104, 165, 222),  
            (73, 140, 208),   
            (44, 115, 194),  
            (28, 98, 173),    
            (19, 79, 149),    
            (12, 61, 123)   
        ]
        brick_area_width = BRICK_COLS * (BRICK_WIDTH + BRICK_PADDING) - BRICK_PADDING
        start_x = self.game_rect.centerx - brick_area_width // 2
        start_y = self.game_rect.centery - ((BRICK_ROWS * (BRICK_HEIGHT + BRICK_PADDING)) // 2)
        
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + BRICK_PADDING)
                y = start_y + row * (BRICK_HEIGHT + BRICK_PADDING)
                self.bricks.append(Brick(x, y, self.BRICK_COLORS[row]))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    def draw(self):
        # Clear screen
        screen.fill(BACKGROUND_COLOR)
        
        # Draw UI backgrounds
        player1_ui_rect = pygame.Rect(0, 0, UI_WIDTH, self.screen_height)
        player2_ui_rect = pygame.Rect(self.screen_width - UI_WIDTH, 0, UI_WIDTH, self.screen_height)
        
        pygame.draw.rect(screen, (30, 30, 30), player1_ui_rect)
        pygame.draw.rect(screen, (30, 30, 30), player2_ui_rect)
        
        # Top border decorations for UI panels
        pygame.draw.line(screen, PLAYER1_COLOR, (0, 2), (UI_WIDTH, 2), 4)
        pygame.draw.line(screen, PLAYER2_COLOR, (self.screen_width - UI_WIDTH, 2), (self.screen_width, 2), 4)
        
        # Draw title
        title_text = title_font.render("BRICKBREAKER", True, (255, 255, 255))
        tagline_text = small_font.render("TOGETHER", True, (180, 180, 180))
        
        screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, int(20 * SCALE_FACTOR)))
        screen.blit(tagline_text, (self.screen_width // 2 - tagline_text.get_width() // 2, int(100 * SCALE_FACTOR)))
        
        # Draw game background
        pygame.draw.rect(screen, (0, 0, 0), self.game_rect, border_radius=12)
        pygame.draw.rect(screen, (40, 40, 40), self.game_rect, border_radius=12, width=2)
        
        # Draw player UIs
        # Player 1
        player1_label = label_font.render("PLAYER 1", True, PLAYER1_COLOR)
        player1_score = score_font.render(f"{self.player1_score:04d}", True, TEXT_COLOR)
        
        screen.blit(player1_label, (UI_WIDTH // 2 - player1_label.get_width() // 2, self.screen_height // 3))
        screen.blit(player1_score, (UI_WIDTH // 2 - player1_score.get_width() // 2, self.screen_height // 3 + int(50 * SCALE_FACTOR)))
        
        # Player 1 lives
        for i in range(LIVES):
            life_color = PLAYER1_COLOR if i < self.player1_lives else (50, 50, 50)
            pygame.draw.circle(screen, life_color, 
                              (UI_WIDTH // 2 - int(35 * SCALE_FACTOR) + i * int(35 * SCALE_FACTOR), 
                               self.screen_height // 3 + int(150 * SCALE_FACTOR)), 
                              int(12 * SCALE_FACTOR))
        
        # Player 2
        player2_label = label_font.render("PLAYER 2", True, PLAYER2_COLOR)
        player2_score = score_font.render(f"{self.player2_score:04d}", True, TEXT_COLOR)
        
        screen.blit(player2_label, (self.screen_width - UI_WIDTH // 2 - player2_label.get_width() // 2, self.screen_height // 3))
        screen.blit(player2_score, (self.screen_width - UI_WIDTH // 2 - player2_score.get_width() // 2, self.screen_height // 3 + int(50 * SCALE_FACTOR)))
        
        # Player 2 lives
        for i in range(LIVES):
            life_color = PLAYER2_COLOR if i < self.player2_lives else (50, 50, 50)
            pygame.draw.circle(screen, life_color, 
                              (self.screen_width - UI_WIDTH // 2 - int(35 * SCALE_FACTOR) + i * int(35 * SCALE_FACTOR), 
                               self.screen_height // 3 + int(150 * SCALE_FACTOR)), 
                              int(12 * SCALE_FACTOR))
        
        # Draw paddles with glow effect
        pygame.draw.rect(screen, PLAYER1_COLOR, self.player1_paddle, border_radius=10)
        pygame.draw.rect(screen, PLAYER1_COLOR, self.player1_paddle.inflate(4, 4), border_radius=12, width=2)
        
        pygame.draw.rect(screen, PLAYER2_COLOR, self.player2_paddle, border_radius=10)
        pygame.draw.rect(screen, PLAYER2_COLOR, self.player2_paddle.inflate(4, 4), border_radius=12, width=2)
        
        # Draw balls with glow effect
        pygame.draw.circle(screen, PLAYER1_COLOR, self.ball1_pos, BALL_RADIUS)
        pygame.draw.circle(screen, PLAYER1_COLOR, self.ball1_pos, BALL_RADIUS + 4, width=2)
        
        pygame.draw.circle(screen, PLAYER2_COLOR, self.ball2_pos, BALL_RADIUS)
        pygame.draw.circle(screen, PLAYER2_COLOR, self.ball2_pos, BALL_RADIUS + 4, width=2)
        
        # Draw brick
        for brick in self.bricks:
            brick.draw(screen)
        
        # Update the display
        pygame.display.flip()

def main():
    ui = UIElement()
    
    # Main loop
    while True:
        ui.handle_events()
        ui.draw()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
