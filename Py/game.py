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
                # Show game over screen instead of quitting
                self.game_over()
            else:
                # Reset ball position if lives are remaining
                self.ball.reset(self.paddle)

    def game_over(self):
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("GAME OVER", True, PRIMARY_COLOR)
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait 2 seconds before quitting
        self.running = False



    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
        self.ui.draw(self.screen, self.score, self.lives)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)
