import pygame
import random
import os
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
        
        # Load game music
        try:
            self.game_music_path = os.path.join('Py', 'audio', 'game_music.mp3')
            pygame.mixer.music.load(self.game_music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Could not load game music: {e}")
        
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
                if self.isPaused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.waiting_for_start:
                    self.waiting_for_start = False
                    self.isGameInProgress = True
                    self.isPaused = False
                    self.ball.reset(self.paddle)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.ui.check_pause_button_click(mouse_pos) and self.isGameInProgress:
                    self.isPaused = not self.isPaused
                    if self.isPaused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif self.ui.check_button_click(event.pos) and self.isGameInProgress:
                    self.isPaused = not self.isPaused
                    if self.isPaused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif self.isPaused:
                    menu_action = self.ui.check_menu_click(event.pos)
                    if menu_action == 'Continue':
                        self.isPaused = False
                        pygame.mixer.music.unpause()
                    elif menu_action == 'Settings':
                        pass
                    elif menu_action == 'Main Menu':
                        try:
                            menu_music_path = os.path.join('Py', 'audio', 'background_music.mp3')
                            pygame.mixer.music.load(menu_music_path)
                            pygame.mixer.music.play(-1)
                        except Exception as e:
                            print(f"Could not load menu music: {e}")
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
        
        # Draw everything using the UI's draw method
        self.ui.draw(self.screen, self.score, self.lives, self.isPaused)
        
        # Draw game elements
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
        
        # make sure the pause menu is on top
        if self.isPaused:
            self.ui.pause_menu.draw(self.screen)

    def game_over(self):
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
        available_colors = self.brick_colors.copy()
        random.shuffle(available_colors)
        
        self.bricks = []
        for y in range(ROWS):
            row_color = available_colors[y]
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
