import pygame
import random
from settings import *
from paddle import Paddle
from ball import Ball
from brick import Brick
from ui import UI

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        
        # brick colors
        self.brick_colors = [
            (231, 76, 60),   # red
            (230, 126, 34),  # orange
            (241, 196, 15),  # yellow
            (46, 204, 113),  # green
            (52, 152, 219),  # light green  
            (41, 128, 185),  # blue
            (155, 89, 182),  # purple
            (243, 104, 224)  # pink
        ]
        
        self.create_bricks()
        self.score = 0
        self.lives = 3
        self.ui = UI()
        self.running = True
        self.waiting_for_start = True
        self.isGameInProgress = False
        self.isPaused = False

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if self.isGameInProgress and not self.isPaused:
            self.paddle.move(keys)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.waiting_for_start:
                    # Start the game for the first time
                    self.waiting_for_start = False
                    self.isGameInProgress = True
                    self.isPaused = False
                    self.ball.reset(self.paddle)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.ui.check_button_click(event.pos) and self.isGameInProgress:
                    self.isPaused = not self.isPaused

    def update(self):
        if self.isGameInProgress and not self.isPaused:
            
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

    def create_bricks(self):
        # copy the brick colors and shuffle them
        available_colors = self.brick_colors.copy()
        random.shuffle(available_colors)
        
        # create bricks,and make sure there is at least one brick of each color in the first 4 rows
        self.bricks = []
        for y in range(ROWS):
            row_color = available_colors[y]  # each row has a different color
            for x in range(COLS):
                self.bricks.append(
                    Brick(x * (BRICK_WIDTH + 10) + 80, 
                         y * (BRICK_HEIGHT + 10) + 150,
                         row_color)
                )

    def reset_game(self):
        self.lives = 3
        self.score = 0
        self.ball.reset(self.paddle)
        self.create_bricks()  

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            if self.isGameInProgress and not self.isPaused and not self.waiting_for_start:
                self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)
