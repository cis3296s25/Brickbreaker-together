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
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.isGameInProgress:
                self.isPaused = not self.isPaused
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.waiting_for_start:
                    # Start the game for the first time
                    self.waiting_for_start = False
                    self.isGameInProgress = True
                    self.isPaused = False
                    self.ball.reset(self.paddle)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                # Check if pause button was clicked using UI method
                if self.ui.check_pause_button_click(mouse_pos) and self.isGameInProgress:
                    self.isPaused = not self.isPaused

                elif self.ui.check_button_click(event.pos) and self.isGameInProgress:
                    self.isPaused = not self.isPaused
                elif self.isPaused:
                    menu_action = self.ui.check_menu_click(event.pos)
                    if menu_action == 'Continue':
                        self.isPaused = False
                    elif menu_action == 'Settings':
                        # settings logic here
                        pass
                    elif menu_action == 'Main Menu':
                        self.running = False

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
        
        # draw the container
        self.ui.draw_container(self.screen)
        
        # if the game is not in progress, show the start screen
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
        
        # draw the UI elements
        self.ui.draw_lives(self.screen, self.lives)
        self.ui.draw_score(self.screen, self.score)
        self.ui.draw_pause_button(self.screen, self.isPaused)
        
        # make sure the pause menu is on top
        if self.isPaused:
            self.ui.pause_menu.draw(self.screen)


    def game_over(self):
        # Use the UI class to draw the game over screen
        self.ui.draw_game_over(self.screen)
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
