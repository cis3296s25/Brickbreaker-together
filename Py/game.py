import pygame
import random
import os
import sys
from settings import *
from paddle import Paddle
from ball import Ball
from brick import Brick
from ui import UI
from powerup import PowerUp

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.balls = [self.ball] #Now supports multiple balls
        self.powerups = []
        self.bomb_ready = False
        self.speed_modifier = 1.0  # Normal speed initially
        self.slow_until = 0
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
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p and self.isGameInProgress:
                    self.isPaused = not self.isPaused
                    if self.isPaused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif event.key == pygame.K_SPACE:
                    if self.waiting_for_start:
                        self.waiting_for_start = False
                        self.isGameInProgress = True
                        self.isPaused = False
                        for ball in self.balls:
                            ball.reset(self.paddle)
            
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
            for ball in self.balls[:]:
                result = ball.move(self.paddle, self.bricks, self, self.speed_modifier)

                if result == 10:
                    self.score += 10
                    if random.random() < 0.2:
                        self.powerups.append(PowerUp(ball.rect.centerx, ball.rect.centery))

                elif result == -1:
                    self.balls.remove(ball)
                    if len(self.balls) == 0:
                        self.lives -= 1
                        if self.lives <= 0:
                            self.game_over()
                        else:
                            new_ball = Ball(self.paddle)
                            self.balls.append(new_ball)

        # Update powerups
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.rect.colliderect(self.paddle.rect):
                powerup.apply(self)
                self.powerups.remove(powerup)
            elif powerup.rect.top > SCREEN_HEIGHT:
                self.powerups.remove(powerup)
                
        # Reset speed modifier after slow effect ends
        if self.speed_modifier < 1.0 and pygame.time.get_ticks() > self.slow_until:
            self.speed_modifier = 1.0

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        # First draw UI container
        self.ui.draw_container(self.screen)

        # Then draw bricks and other game elements
        for brick in self.bricks:
            brick.draw(self.screen)

        for powerup in self.powerups:
            powerup.draw(self.screen)

        self.paddle.draw(self.screen)

        # NOW draw all balls (on top of UI container)
        for ball in self.balls:
            ball.draw(self.screen)

        # Finally draw UI elements (score, lives, etc.)
        self.ui.draw_lives(self.screen, self.lives)
        self.ui.draw_score(self.screen, self.score)
        self.ui.draw_pause_button(self.screen, self.isPaused)

        if self.isPaused:
            self.ui.pause_menu.draw(self.screen)

    def game_over(self):
        self.ui.draw_game_over(self.screen)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        waiting = False
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def create_bricks(self):
        available_colors = self.brick_colors.copy()
        random.shuffle(available_colors)
        
        # Calculate brick layout dimensions
        total_brick_width = COLS * (BRICK_WIDTH + BRICK_PADDING) - BRICK_PADDING
        total_brick_height = ROWS * (BRICK_HEIGHT + BRICK_PADDING) - BRICK_PADDING
        
        # Calculate starting position to center the brick layout
        start_x = (SCREEN_WIDTH - total_brick_width) // 2
        start_y = int(150 * SCALE_FACTOR)  # Top margin
        
        self.bricks = []
        for y in range(ROWS):
            row_color = available_colors[y]
            for x in range(COLS):
                brick_x = start_x + x * (BRICK_WIDTH + BRICK_PADDING)
                brick_y = start_y + y * (BRICK_HEIGHT + BRICK_PADDING)
                self.bricks.append(Brick(brick_x, brick_y, row_color))

    def reset_game(self):
        self.lives = 3
        self.score = 0
        self.balls = [Ball(self.paddle)]
        self.create_bricks()
        self.powerups.clear()
        self.bomb_ready = False
        self.slow_until = 0

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            if self.isGameInProgress and not self.isPaused and not self.waiting_for_start:
                self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)
