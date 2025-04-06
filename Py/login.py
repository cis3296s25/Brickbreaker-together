import pygame
import sys
import hashlib
from settings import *
from ui_constants import (
    PRIMARY_COLOR, SECONDARY_COLOR, BACKGROUND_COLOR,
    TEXT_COLOR, ACCENT_COLOR,
    FloatingBrick
)
from db import get_user_by_username

pygame.init()
pygame.font.init()
pygame.mixer.init()
init_screen_dimensions()


MAIN_COLOR = (243, 156, 18)

class LoginScreen:
    def __init__(self, screen):
        self.screen = screen
        # Use constant screen dimensions from settings.py
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        # Fonts
        self.title_font = pygame.font.SysFont('Segoe UI', TITLE_FONT_SIZE, bold=True)
        self.input_font = pygame.font.SysFont('Segoe UI', LABEL_FONT_SIZE)
        self.button_font = pygame.font.SysFont('Segoe UI', SMALL_FONT_SIZE)

        # Floating bricks for background animation
        self.floating_bricks = [FloatingBrick(self.screen_width, self.screen_height) for _ in range(5)]

        # Input texts
        self.username_text = ""
        self.password_text = ""
        self.active_input = "username"

        # Layout dimensions
        input_width = int(400 * SCALE_FACTOR)
        input_height = int(50 * SCALE_FACTOR)
        button_width = int(160 * SCALE_FACTOR)
        button_height = int(50 * SCALE_FACTOR)
        small_button_height = int(40 * SCALE_FACTOR)

        self.username_box = pygame.Rect(
            self.screen_width // 2 - input_width // 2,
            int(250 * SCALE_FACTOR),
            input_width,
            input_height
        )
        self.password_box = pygame.Rect(
            self.screen_width // 2 - input_width // 2,
            int(320 * SCALE_FACTOR),
            input_width,
            input_height
        )
        self.login_button_rect = pygame.Rect(
            self.screen_width // 2 - button_width // 2,
            int(400 * SCALE_FACTOR),
            button_width,
            button_height
        )
        self.goto_signup_rect = pygame.Rect(
            self.screen_width // 2 - button_width // 2,
            int(460 * SCALE_FACTOR),
            button_width,
            button_height
        )
        self.goto_menu_rect = pygame.Rect(
            self.screen_width // 2 - button_width // 2,
            int(520 * SCALE_FACTOR),
            button_width,
            button_height
        )

        # Hover state flags and alpha values (for animation)
        self.hover_alpha_login = 0
        self.hover_alpha_direction_login = 1
        self.hover_alpha_signup = 0
        self.hover_alpha_direction_signup = 1
        self.hover_alpha_menu = 0
        self.hover_alpha_direction_menu = 1

        self.hover_login = False
        self.hover_signup = False
        self.hover_menu = False

        self.error_message = ""
        self.clock = pygame.time.Clock()

        # For tab-based focus cycling
        self.focus_list = ["username", "password", "login_button"]
        self.login_success_username = None

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_TAB:
                        self.cycle_focus()
                    elif event.key == pygame.K_RETURN:
                        self.try_submit()
                    else:
                        self.handle_key_input(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(mouse_pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(mouse_pos)

            self.draw()
            pygame.display.flip()

            if self.login_success_username:
                return self.login_success_username

        pygame.quit()
        sys.exit()

    def cycle_focus(self):
        idx = self.focus_list.index(self.active_input) if self.active_input in self.focus_list else 0
        idx = (idx + 1) % len(self.focus_list)
        self.active_input = self.focus_list[idx]

    def try_submit(self):
        if self.username_text.strip() and self.password_text.strip():
            status, user_name = self.attempt_login()
            if status == "SUCCESS":
                self.login_success_username = user_name

    def handle_key_input(self, event):
        if self.active_input == "username":
            if event.key == pygame.K_BACKSPACE:
                self.username_text = self.username_text[:-1]
            else:
                self.username_text += event.unicode
        elif self.active_input == "password":
            if event.key == pygame.K_BACKSPACE:
                self.password_text = self.password_text[:-1]
            else:
                self.password_text += event.unicode

    def handle_mouse_click(self, pos):
        if self.username_box.collidepoint(pos):
            self.active_input = "username"
        elif self.password_box.collidepoint(pos):
            self.active_input = "password"
        else:
            self.active_input = None

        if self.login_button_rect.collidepoint(pos):
            status, user_name = self.attempt_login()
            if status == "SUCCESS":
                self.login_success_username = user_name

        if self.goto_signup_rect.collidepoint(pos):
            from signup import SignUpScreen
            signup = SignUpScreen(self.screen)
            signup.run()
            return

        if self.goto_menu_rect.collidepoint(pos):
            self.login_success_username = "BACK_TO_MENU"
            return

    def handle_mouse_motion(self, mouse_pos):
        self.hover_login = self.login_button_rect.collidepoint(mouse_pos)
        self.hover_signup = self.goto_signup_rect.collidepoint(mouse_pos)
        self.hover_menu = self.goto_menu_rect.collidepoint(mouse_pos)

    def attempt_login(self):
        username = self.username_text.strip()
        password = self.password_text.strip()
        
        # Check if both fields are filled out
        if not username or not password:
            self.error_message = "Please fill out all fields."
            return ("ERROR", None)
            
        # Check if username exists
        user = get_user_by_username(username)
        if not user:
            self.error_message = "Incorrect Username or Password."
            return ("ERROR", None)
            
        # Check if password is correct
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        if hashed_input != user['password_hash']:
            self.error_message = "Incorrect Username or Password."
            return ("ERROR", None)
            
        # Login successful
        self.error_message = "Login successful!"
        self.draw()
        pygame.display.flip()
        pygame.time.wait(1000)
        return ("SUCCESS", username)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        for brick in self.floating_bricks:
            brick.update()
            brick.draw(self.screen)

        # Draw title with glow effect
        title_surf = self.title_font.render("LOGIN", True, PRIMARY_COLOR)
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, 150))
        for offset in range(3):
            glow_surf = self.title_font.render("LOGIN", True, (*PRIMARY_COLOR[:3], 100 - offset * 30))
            glow_rect = glow_surf.get_rect(center=(self.screen_width // 2, 150))
            self.screen.blit(glow_surf, glow_rect)
        self.screen.blit(title_surf, title_rect)

        # Draw input boxes
        self.draw_input_box(self.username_box, self.username_text, "Username", active=(self.active_input=="username"))
        masked_pw = "*" * len(self.password_text)
        self.draw_input_box(self.password_box, masked_pw, "Password", active=(self.active_input=="password"))

        # Update hover alphas
        self.update_button_hover("LOGIN", self.hover_login)
        self.update_button_hover("SIGN UP", self.hover_signup)
        self.update_button_hover("BACK", self.hover_menu)

        # Draw buttons with unified style
        self.draw_button(self.login_button_rect, "LOGIN", hovered=self.hover_login)
        self.draw_button(self.goto_signup_rect, "SIGN UP", hovered=self.hover_signup)
        self.draw_button(self.goto_menu_rect, "BACK", hovered=self.hover_menu)

        # Draw error message if exists
        if self.error_message:
            err_surf = self.input_font.render(self.error_message, True, ACCENT_COLOR)
            err_rect = err_surf.get_rect(center=(self.screen_width // 2, 590))
            self.screen.blit(err_surf, err_rect)

    def draw_input_box(self, rect, text, placeholder, active=False):
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill((18, 18, 18, 215))
        self.screen.blit(s, rect)
        border_color = PRIMARY_COLOR if active else (100, 100, 100)
        if active:
            for offset in range(3):
                pygame.draw.rect(self.screen, (*border_color[:3], 100 - offset * 30), rect.inflate(offset*2, offset*2), border_radius=5)
        else:
            pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=5)
        display_text = placeholder if (not text and not active) else text
        font_surf = self.input_font.render(display_text, True, TEXT_COLOR)
        self.screen.blit(font_surf, (rect.x + 10, rect.y + 10))

    def update_button_hover(self, button_text, is_hovered):
        if button_text == "LOGIN":
            if is_hovered:
                self.hover_alpha_login += 5 * self.hover_alpha_direction_login
                if self.hover_alpha_login >= 100:
                    self.hover_alpha_direction_login = -1
                elif self.hover_alpha_login <= 0:
                    self.hover_alpha_direction_login = 1
            else:
                self.hover_alpha_login = max(self.hover_alpha_login - 5, 0)
        elif button_text == "SIGN UP":
            if is_hovered:
                self.hover_alpha_signup += 5 * self.hover_alpha_direction_signup
                if self.hover_alpha_signup >= 100:
                    self.hover_alpha_direction_signup = -1
                elif self.hover_alpha_signup <= 0:
                    self.hover_alpha_direction_signup = 1
            else:
                self.hover_alpha_signup = max(self.hover_alpha_signup - 5, 0)
        elif button_text == "BACK":
            if is_hovered:
                self.hover_alpha_menu += 5 * self.hover_alpha_direction_menu
                if self.hover_alpha_menu >= 100:
                    self.hover_alpha_direction_menu = -1
                elif self.hover_alpha_menu <= 0:
                    self.hover_alpha_direction_menu = 1
            else:
                self.hover_alpha_menu = max(self.hover_alpha_menu - 5, 0)

    def draw_button(self, rect, text, hovered=False):
        if text.upper() == "LOGIN":
            base_color = PRIMARY_COLOR
            alpha = 50 + self.hover_alpha_login
        elif text.upper() == "SIGN UP":
            base_color = SECONDARY_COLOR
            alpha = 50 + self.hover_alpha_signup
        elif text.upper() == "BACK":
            base_color = MAIN_COLOR
            alpha = 50 + self.hover_alpha_menu
        else:
            base_color = TEXT_COLOR
            alpha = 50

        # Draw button background
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        if hovered:
            s.fill((*base_color[:3], alpha))
        else:
            s.fill((18, 18, 18, 215))
        self.screen.blit(s, rect)

        # Draw button border with rounded corners
        pygame.draw.rect(self.screen, base_color, rect, 4, border_radius=5)

        # Draw button text
        text_color = base_color if hovered else TEXT_COLOR
        txt_surf = self.button_font.render(text, True, text_color)
        txt_rect = txt_surf.get_rect(center=rect.center)
        self.screen.blit(txt_surf, txt_rect)