import pygame
from settings import *
from paddle import Paddle
from ball import Ball
from brick import Brick
from ui import UI

class Game:
    def __init__(self):
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
                self.running = False

    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)
        self.paddle.draw(screen)
        self.ball.draw(screen)
        for brick in self.bricks:
            brick.draw(screen)
        self.ui.draw(screen, self.score, self.lives)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

