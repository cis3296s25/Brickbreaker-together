from settings import *
import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick
from ui import UI

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.bricks = [Brick(x * (BRICK_WIDTH + 10) + 80, y * (BRICK_HEIGHT + 10) + 150)
                       for x in range(COLS) for y in range(ROWS)]
        self.score = 0
        self.lives = 3
        self.ui = UI()
        self.running = True

    def handle_events(self):
        keys = pygame.key.get_pressed()
        self.paddle.move(keys)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.ball.reset(self.paddle)

    def update(self):
        result = self.ball.move(self.paddle, self.bricks)
        if result == 10:
            self.score += 10
        elif result == -1:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over()
            else:
                self.ball.reset(self.paddle)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
        self.ui.draw(self.screen, self.score, self.lives)

    def start_screen(self):
        font = pygame.font.Font(None, 72)
        start_text = font.render("Press SPACE to Start", True, PRIMARY_COLOR)
        rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        button_rect = pygame.Rect(rect.left - 20, rect.top - 20, rect.width + 40, rect.height + 40)

        while True:
            self.screen.fill(BACKGROUND_COLOR)
            pygame.draw.rect(self.screen, (50, 50, 50), button_rect, border_radius=8)
            self.screen.blit(start_text, rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return

    def game_over(self):
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("GAME OVER", True, PRIMARY_COLOR)
        restart_text = font.render("Press R to Restart", True, PRIMARY_COLOR)
        quit_text = font.render("Press Q to Quit", True, PRIMARY_COLOR)

        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
        self.screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        waiting = False
                    if event.key == pygame.K_q:
                        self.running = False
                        waiting = False

    def reset_game(self):
        self.lives = 3
        self.score = 0
        self.ball.reset(self.paddle)
        self.bricks = [Brick(x * (BRICK_WIDTH + 10) + 80, y * (BRICK_HEIGHT + 10) + 150)
                       for x in range(COLS) for y in range(ROWS)]

    def run(self):
        self.start_screen()  # Show start screen first
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)
