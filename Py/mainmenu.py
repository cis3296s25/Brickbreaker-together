import pygame
import sys
import os
from game import Game

# Import colors and FloatingBrick from ui_constants.py
from ui_constants import (
    PRIMARY_COLOR, SECONDARY_COLOR, BACKGROUND_COLOR,
    UI_BACKGROUND, TEXT_COLOR, ACCENT_COLOR, PINK, TEAL,
    FloatingBrick
)

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()  # Initialize the mixer module

# Screen Dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

class BrickBreakerMenu:
    def __init__(self, screen):
        self.screen = screen  # Store the screen object

        pygame.display.set_caption("BrickBreaker Together")
        
        # Load and play menu music
        try:
            music_path = os.path.join('Py', 'audio', 'background_music.mp3')
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Could not load menu music: {e}")
        
        global SCREEN_WIDTH, SCREEN_HEIGHT
        SCREEN_WIDTH = screen.get_width()
        SCREEN_HEIGHT = screen.get_height()
        
        # Fonts
        self.title_font = pygame.font.SysFont('Segoe UI', 80, bold=True)
        self.tagline_font = pygame.font.SysFont('Segoe UI', 24)
        self.menu_font = pygame.font.SysFont('Segoe UI', 32)
        
        # Menu items
        self.menu_items = [
            "Login/Sign Up",
            "Single Player",
            "Multiple Player", 
            "Settings", 
            "Quit"
        ]
        
        # Colors for menu item borders
        self.menu_colors = [
            PINK,                 # For Login/Sign Up
            PRIMARY_COLOR,        # Single Player
            SECONDARY_COLOR,      # Multiple Player
            (243, 156, 18),       # Settings (Orange)
            ACCENT_COLOR          # Quit
        ]
        
        # Floating bricks
        self.floating_bricks = [FloatingBrick(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(5)]
        
        self.clock = pygame.time.Clock()
        self.hovered_item = None
        
        # For hover animation on menu items
        self.hover_alpha = 0
        self.hover_alpha_direction = 1

        # Track currently logged-in user
        self.current_user = None

    def draw_background(self):
        self.screen.fill(BACKGROUND_COLOR)
        for brick in self.floating_bricks:
            brick.update()
            brick.draw(self.screen)

    def draw_title(self):
        text_surface = self.title_font.render('BRICKBREAKER', True, PRIMARY_COLOR)
        tagline_surface = self.tagline_font.render('TOGETHER', True, TEXT_COLOR)
        
        text_rect = text_surface.get_rect(centerx=SCREEN_WIDTH//2, centery=100)
        tagline_rect = tagline_surface.get_rect(centerx=SCREEN_WIDTH//2, top=text_rect.bottom + 10)
        
        self.screen.blit(text_surface, text_rect)
        self.screen.blit(tagline_surface, tagline_rect)

    def draw_menu(self):
        # If a user is logged in, replace the first item text with the username
        if self.current_user:
            self.menu_items[0] = self.current_user.capitalize()
            self.menu_colors[0] = TEAL
        else:
            self.menu_items[0] = "Login/Sign Up"
            self.menu_colors[0] = PINK

        menu_width = 500
        menu_start_y = 250
        menu_item_height = 70
        
        self.hover_alpha += 5 * self.hover_alpha_direction
        if self.hover_alpha >= 100:
            self.hover_alpha_direction = -1
        elif self.hover_alpha <= 0:
            self.hover_alpha_direction = 1
        
        for i, item in enumerate(self.menu_items):
            menu_rect = pygame.Rect(
                (SCREEN_WIDTH - menu_width) // 2, 
                menu_start_y + i * (menu_item_height + 20), 
                menu_width, 
                menu_item_height
            )
            
            # Semi-transparent background
            s = pygame.Surface((menu_width, menu_item_height), pygame.SRCALPHA)
            if i == self.hovered_item:
                hover_color = (*self.menu_colors[i][:3], 50 + self.hover_alpha)
                s.fill(hover_color)
            else:
                s.fill(UI_BACKGROUND)
            self.screen.blit(s, menu_rect)
            
            # Border with glow effect if hovered
            border_color = self.menu_colors[i]
            if i == self.hovered_item:
                for offset in range(4):
                    pygame.draw.line(
                        self.screen,
                        (*border_color[:3], 100 - offset * 25),
                        (menu_rect.left - offset, menu_rect.top),
                        (menu_rect.left - offset, menu_rect.bottom),
                        2
                    )
            else:
                pygame.draw.line(
                    self.screen,
                    border_color,
                    (menu_rect.left, menu_rect.top),
                    (menu_rect.left, menu_rect.bottom),
                    4
                )
            
            # Text with color change on hover
            text_color = self.menu_colors[i] if i == self.hovered_item else TEXT_COLOR
            text_surface = self.menu_font.render(item, True, text_color)
            text_rect = text_surface.get_rect(midleft=(menu_rect.left + 20, menu_rect.centery))
            self.screen.blit(text_surface, text_rect)

    def open_login_signup(self):
        print("Transition to Login/Sign Up screen")
        from login import LoginScreen
        login_screen = LoginScreen(self.screen)
        username = login_screen.run()
        if username:
            self.current_user = username

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEMOTION:
                    menu_width = 500
                    menu_start_y = 250
                    menu_item_height = 70
                    
                    self.hovered_item = None
                    for i, item in enumerate(self.menu_items):
                        menu_rect = pygame.Rect(
                            (SCREEN_WIDTH - menu_width) // 2,
                            menu_start_y + i * (menu_item_height + 20),
                            menu_width,
                            menu_item_height
                        )
                        if menu_rect.collidepoint(mouse_pos):
                            self.hovered_item = i
                            break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    menu_width = 500
                    menu_start_y = 250
                    menu_item_height = 70
                    for i, item in enumerate(self.menu_items):
                        menu_rect = pygame.Rect(
                            (SCREEN_WIDTH - menu_width) // 2,
                            menu_start_y + i * (menu_item_height + 20),
                            menu_width,
                            menu_item_height
                        )
                        if menu_rect.collidepoint(mouse_pos):
                            if i == 0:
                                if self.current_user:
                                    print(f"Clicked user button for {self.current_user.capitalize()}")
                                else:
                                    self.open_login_signup()
                            elif item == "Single Player":
                                pygame.mixer.music.stop()
                                game = Game(self.screen)
                                game.run()
                                try:
                                    music_path = os.path.join('Py', 'audio', 'background_music.mp3')
                                    pygame.mixer.music.load(music_path)
                                    pygame.mixer.music.set_volume(0.5)
                                    pygame.mixer.music.play(-1)
                                except Exception as e:
                                    print(f"Could not reload menu music: {e}")
                            elif item == "Multiple Player":
                                pygame.mixer.music.stop()
                                from MultiplayerGame import run_game
                                run_game(self.screen)
                                try:
                                    music_path = os.path.join('Py', 'audio', 'background_music.mp3')
                                    pygame.mixer.music.load(music_path)
                                    pygame.mixer.music.set_volume(0.5)
                                    pygame.mixer.music.play(-1)
                                except Exception as e:
                                    print(f"Could not reload menu music: {e}")
                            elif item == "Quit":
                                running = False

            self.draw_background()
            self.draw_title()
            self.draw_menu()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()