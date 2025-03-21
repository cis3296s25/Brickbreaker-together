import pygame
import sys

# Initialize pygame
pygame.init()

# Define colors
PRIMARY_COLOR = (52, 152, 219)  # Blue
BACKGROUND_COLOR = (18, 18, 18)  # Dark gray/black
UI_BACKGROUND = (30, 30, 30)  # Slightly lighter black background
TEXT_COLOR = (255, 255, 255)  # White
LIFE_COLOR = (231, 76, 60)  # Red
BRICK_COLOR = (241, 196, 15)  # White

# Set game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BrickBreaker")

# Paddle properties
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
PADDLE_COLOR = PRIMARY_COLOR
PADDLE_Y = HEIGHT - 70

# Ball properties
BALL_RADIUS = 8
BALL_COLOR = (236, 240, 241)  # Light gray

# Brick properties
BRICK_WIDTH, BRICK_HEIGHT = 54, 20
ROWS, COLS =6,10  # Adjusted columns for better centering
BRICKS = []

# Calculate total brick width for centering
total_brick_width = COLS * (BRICK_WIDTH + 10) - 10
start_x = (WIDTH - total_brick_width) // 2

# Load fonts
font_large = pygame.font.Font(None, 42)
font_score = pygame.font.Font(None, 24)
font_small = pygame.font.Font(None, 20)

class Game:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.game_active = False
        self.paddle = pygame.Rect((WIDTH // 2 - PADDLE_WIDTH // 2, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT))
        self.ball = pygame.Rect((self.paddle.centerx - BALL_RADIUS, PADDLE_Y - BALL_RADIUS * 2, BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.create_bricks()
    
    def create_bricks(self):
        global BRICKS
        BRICKS = []
        for row in range(ROWS):
            for col in range(COLS):
                brick_x = start_x + col * (BRICK_WIDTH + 10)
                brick_y = 145 + row * (BRICK_HEIGHT + 10)
                BRICKS.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))
    def move_ball(self):
        if not self.lives:
            return

        self.ball.x += self.ball_dx
        self.ball.y += self.ball_dy

        # Bounce off left and right walls
        if self.ball.left <= 0 or self.ball.right >= WIDTH:
            self.ball_dx = -self.ball_dx

        # Bounce off top wall
        if self.ball.top <= 0:
            self.ball_dy = -self.ball_dy

        # Bounce off paddle
        if self.ball.colliderect(self.paddle):
            self.ball_dy = -self.ball_dy

        # Bounce off bricks
        for brick in self.bricks[:]:
            if self.ball.colliderect(brick):
                self.bricks.remove(brick)
                self.ball_dy = -self.ball_dy
                self.score += 10
                break

        # If ball goes below paddle
        if self.ball.top >= HEIGHT:
            self.lives -= 1
            self.reset_ball()
    def reset_ball(self):
        self.ball.x = WIDTH // 2
        self.ball.y = HEIGHT - 80
        self.ball_dx = 4
        self.ball_dy = -4
        
    def draw_bricks(self):
        for brick in BRICKS:
            pygame.draw.rect(screen, BRICK_COLOR, brick)
    
    def draw_paddle(self):
        pygame.draw.rect(screen, PADDLE_COLOR, self.paddle, border_radius=5)
    
    def draw_ball(self):
        pygame.draw.circle(screen, BALL_COLOR, self.ball.center, BALL_RADIUS)
    
    def draw_ui(self):
        title_text = font_large.render("BRICKBREAKER", True, PRIMARY_COLOR)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        ui_panel = pygame.Rect(80, 100, WIDTH - 160, 40)
        pygame.draw.rect(screen, UI_BACKGROUND, ui_panel, border_radius=0)
        pygame.draw.line(screen, PRIMARY_COLOR, (ui_panel.left, ui_panel.top), 
                         (ui_panel.right, ui_panel.top), 2)
        
        for i in range(self.lives):
            pygame.draw.circle(screen, LIFE_COLOR, (100 + i * 25, ui_panel.centery), 8)
        
        score_text = font_score.render(f"{self.score:05d}", True, PRIMARY_COLOR)
        score_rect = score_text.get_rect(center=(WIDTH // 2, ui_panel.centery))
        screen.blit(score_text, score_rect)
        
        pygame.draw.rect(screen, PRIMARY_COLOR, (WIDTH - 120, ui_panel.centery - 8, 16, 16), border_radius=4)
        
        game_rect = pygame.Rect(80, 140, WIDTH - 160, HEIGHT - 190)
        pygame.draw.rect(screen, (0, 0, 0), game_rect, border_radius=0)
        pygame.draw.rect(screen, (50, 50, 50), game_rect, 2, border_radius=0)
        
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
            # use left and right key to move the paddle
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_LEFT]:
                            self.paddle.x = max(80, self.paddle.x - 7)  # Limit to left game border
                        if keys[pygame.K_RIGHT]:
                            self.paddle.x = min(WIDTH - 160 - PADDLE_WIDTH, self.paddle.x + 7)  # Limit to right game border

                        # ball will stick with paddle before the game start
                        if not self.game_active:
                            self.ball.centerx = self.paddle.centerx
                            self.ball.bottom = self.paddle.top
            screen.fill(BACKGROUND_COLOR)
            self.draw_ui()
            self.draw_bricks()
            self.draw_paddle()
            self.draw_ball()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
