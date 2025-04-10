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
from levels import LEVELS

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.balls = [self.ball]
        self.powerups = []
        self.bomb_ready = False
        self.speed_modifier = 1.0
        self.slow_until = 0
        # Get the absolute path to the audio directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.audio_dir = os.path.join(current_dir, 'audio')
        
        # Load sound effects
        try:
            brick_hit_path = os.path.join(self.audio_dir, 'hit.wav')  # Changed from brick_hit.wav to hit.wav
            self.brick_hit_sound = pygame.mixer.Sound(brick_hit_path)
            self.brick_hit_sound.set_volume(0.7)  # Set volume to 70%
            
            button_click_path = os.path.join(self.audio_dir, 'button_click.wav')
            self.button_click_sound = pygame.mixer.Sound(button_click_path)
            self.button_click_sound.set_volume(0.5)  # Set volume to 50%
            
            paddle_hit_path = os.path.join(self.audio_dir, 'paddle_hit.wav')
            self.paddle_hit_sound = pygame.mixer.Sound(paddle_hit_path)
            self.paddle_hit_sound.set_volume(2)  # Set volume to 200%
            
            # Add powerup collect sound
            powerup_path = os.path.join(self.audio_dir, 'but.wav')
            self.powerup_sound = pygame.mixer.Sound(powerup_path)
            self.powerup_sound.set_volume(0.7)  # Set volume to 70%
            
            # Add crying sound for game over
            crying_sound_path = os.path.join(self.audio_dir, 'eee.wav')
            self.crying_sound = pygame.mixer.Sound(crying_sound_path)
            self.crying_sound.set_volume(0.8)  # Set volume to 80%
        except Exception as e:
            print(f"Could not load sound effects: {e}")
            self.brick_hit_sound = None
            self.button_click_sound = None
            self.paddle_hit_sound = None
            self.powerup_sound = None
            self.crying_sound = None
            
        # Store music paths
        self.game_music_path = os.path.join(self.audio_dir, 'game_music.mp3')
        self.danger_music_path = os.path.join(self.audio_dir, 'danger_music.mp3')
        self.reborn_music_path = os.path.join(self.audio_dir, 'd.mp3')
        self.current_music = 'normal'  # Track current music state ('normal', 'danger', or 'reborn')
            
        try:
            # Initialize the mixer
            pygame.mixer.init()
            # Load and play the game music
            pygame.mixer.music.load(self.game_music_path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        except Exception as e:
            print(f"Could not load game music: {e}")

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

        self.current_level = 0
        self.create_bricks()
        self.score = 0
        self.lives = 3
        self.ui = UI()
        self.running = True
        self.waiting_for_start = True
        self.isGameInProgress = False
        self.isPaused = False
        self.show_level_complete = False

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

                elif event.key == pygame.K_n:
                    self.current_level += 1
                    self.create_bricks()
                    self.waiting_for_start = True
                    self.balls = [Ball(self.paddle)]

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.ui.check_pause_button_click(mouse_pos) and self.isGameInProgress:
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    self.isPaused = not self.isPaused
                    if self.isPaused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif self.ui.check_button_click(event.pos) and self.isGameInProgress:
                    if self.button_click_sound:
                        self.button_click_sound.play()
                    self.isPaused = not self.isPaused
                    if self.isPaused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif self.isPaused:
                    menu_action = self.ui.check_menu_click(event.pos)
                    if menu_action:  # Only play sound if a button was actually clicked
                        if self.button_click_sound:
                            self.button_click_sound.play()
                        if menu_action == 'Continue':
                            self.isPaused = False
                            pygame.mixer.music.unpause()
                        elif menu_action == 'Settings':
                            pass
                        elif menu_action == 'Main Menu':
                            try:
                                menu_music_path = os.path.join(self.audio_dir, 'background_music.mp3')
                                pygame.mixer.music.load(menu_music_path)
                                pygame.mixer.music.play(-1)
                            except Exception as e:
                                print(f"Could not load menu music: {e}")
                            self.running = False
                if self.show_level_complete:
                    if self.level_complete_buttons["next"].collidepoint(event.pos):
                        self.current_level += 1
                        self.create_bricks()
                        self.balls = [Ball(self.paddle)]
                        self.waiting_for_start = True
                        self.isGameInProgress = False
                        self.show_level_complete = False

                    elif self.level_complete_buttons["quit"].collidepoint(event.pos):
                        from mainmenu import BrickBreakerMenu
                        try:
                            pygame.mixer.music.load(os.path.join("Py", "audio", "background_music.mp3"))
                            pygame.mixer.music.play(-1)
                        except:
                            pass
                        menu = BrickBreakerMenu(self.screen)
                        menu.run()

    def update(self):
        if self.isGameInProgress and not self.isPaused:
            for ball in self.balls[:]:
                result = ball.move(self.paddle, self.bricks, self, self.speed_modifier)

                if result == 10:
                    self.score += 10
                    if random.random() < 0.8:
                        self.powerups.append(PowerUp(ball.rect.centerx, ball.rect.centery))

                elif result == -1:
                    self.balls.remove(ball)
                    if len(self.balls) == 0:
                        self.lives -= 1
                          # Check if we need to switch to danger music
                        if self.lives == 1 and self.current_music != 'danger':
                            try:
                                pygame.mixer.music.load(self.danger_music_path)
                                pygame.mixer.music.set_volume(8)  # Increase volume to 80%
                                pygame.mixer.music.play(-1)
                                self.current_music = 'danger'
                            except Exception as e:
                                print(f"Could not load danger music: {e}")
                        # Check if we need to switch back to normal music when losing a life but still above 1
                        elif self.lives > 1 and (self.current_music == 'reborn' or self.current_music == 'danger'):
                            try:
                                pygame.mixer.music.load(self.game_music_path)
                                pygame.mixer.music.set_volume(0.5)  # Back to normal volume
                                pygame.mixer.music.play(-1)
                                self.current_music = 'normal'
                            except Exception as e:
                                print(f"Could not load normal music: {e}")
                                
                        if self.lives <= 0:
                            self.game_over()
                        else:
                            new_ball = Ball(self.paddle)
                            self.balls.append(new_ball)

        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.rect.colliderect(self.paddle.rect):
                if self.powerup_sound:  # Play sound when collecting powerup
                    self.powerup_sound.play()
                powerup.apply(self)
                self.powerups.remove(powerup)
            elif powerup.rect.top > SCREEN_HEIGHT:
                self.powerups.remove(powerup)

        if self.speed_modifier < 1.0 and pygame.time.get_ticks() > self.slow_until:
            self.speed_modifier = 1.0

        if not self.bricks and self.isGameInProgress:
            self.isGameInProgress = False
            self.show_level_complete = True

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.ui.draw_container(self.screen)

        for brick in self.bricks:
            brick.draw(self.screen)

        for powerup in self.powerups:
            powerup.draw(self.screen)

        self.paddle.draw(self.screen)

        for ball in self.balls:
            ball.draw(self.screen)

        self.ui.draw_lives(self.screen, self.lives)
        self.ui.draw_score(self.screen, self.score)
        self.ui.draw_pause_button(self.screen, self.isPaused)

        if self.isPaused:
            self.ui.pause_menu.draw(self.screen)
        if self.show_level_complete:
            self.draw_level_complete()

    def game_over(self):
            # Stop the current music
        pygame.mixer.music.stop()
        # Play crying sound
        if self.crying_sound:
            self.crying_sound.play()
        self.ui.draw_game_over(self.screen)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.crying_sound:
                        self.crying_sound.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if self.button_click_sound:
                            self.button_click_sound.play()
                        # Stop crying sound when restarting
                        if self.crying_sound:
                            self.crying_sound.stop()
                        self.reset_game()
                        waiting = False
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        if self.button_click_sound:
                            self.button_click_sound.play()
                        # Stop crying sound when quitting to menu
                        if self.crying_sound:
                            self.crying_sound.stop()
                        pygame.quit()
                        sys.exit()

    def create_bricks(self):
        layout = LEVELS[self.current_level % len(LEVELS)]

        self.bricks = []
        # Dynamically center based on columns
        num_cols = max(len(row) for row in layout)
        total_width = num_cols * (BRICK_WIDTH + BRICK_PADDING) - BRICK_PADDING
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = int(150 * SCALE_FACTOR)

        for row_idx, row in enumerate(layout):
            for col_idx, brick_type in enumerate(row):
                if brick_type:
                    x = start_x + col_idx * (BRICK_WIDTH + BRICK_PADDING)
                    y = start_y + row_idx * (BRICK_HEIGHT + BRICK_PADDING)
                    color = random.choice(self.brick_colors)
                    self.bricks.append(Brick(x, y, color))

    def reset_game(self):
        self.lives = 3
        self.score = 0
        self.balls = [Ball(self.paddle)]
        self.create_bricks()
        self.powerups.clear()
        self.bomb_ready = False
        self.slow_until = 0

             
        # Reset to normal music
        if self.current_music != 'normal':
            try:
                pygame.mixer.music.load(self.game_music_path)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                self.current_music = 'normal'
            except Exception as e:
                print(f"Could not load normal music: {e}")

    def draw_level_complete(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont("Arial", 60)
        msg = font.render("Level Passed!", True, (255, 255, 255))
        prompt = font.render("Go to next level?", True, (180, 180, 180))

        self.screen.blit(msg, (self.screen_width // 2 - msg.get_width() // 2, 300))
        self.screen.blit(prompt, (self.screen_width // 2 - prompt.get_width() // 2, 380))

        # Draw buttons
        button_font = pygame.font.SysFont("Arial", 40)
        next_btn = pygame.Rect(self.screen_width//2 - 200, 480, 160, 60)
        quit_btn = pygame.Rect(self.screen_width//2 + 40, 480, 160, 60)

        pygame.draw.rect(self.screen, (46, 204, 113), next_btn, border_radius=10)
        pygame.draw.rect(self.screen, (231, 76, 60), quit_btn, border_radius=10)

        next_text = button_font.render("Next", True, (0, 0, 0))
        quit_text = button_font.render("Quit", True, (0, 0, 0))

        self.screen.blit(next_text, next_btn.move(40, 10))
        self.screen.blit(quit_text, quit_btn.move(40, 10))

        self.level_complete_buttons = {"next": next_btn, "quit": quit_btn}

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            if self.isGameInProgress and not self.isPaused and not self.waiting_for_start:
                self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)
