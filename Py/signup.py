import pygame
import sys
import hashlib
from ui_constants import (
    PRIMARY_COLOR, SECONDARY_COLOR, BACKGROUND_COLOR,
    TEXT_COLOR, ACCENT_COLOR,
    FloatingBrick
)
from db import get_user_by_username, create_user

pygame.init()
pygame.font.init()
pygame.mixer.init()

class SignUpScreen:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.title_font = pygame.font.SysFont('Segoe UI', 60, bold=True)
        self.input_font = pygame.font.SysFont('Segoe UI', 32)
        self.button_font = pygame.font.SysFont('Segoe UI', 28)

        self.floating_bricks = [FloatingBrick(self.screen_width, self.screen_height) for _ in range(5)]

        self.username_text = ""
        self.password_text = ""
        self.confirm_text = ""

        self.active_input = "username"

        self.username_box = pygame.Rect(self.screen_width//2 - 200, 220, 400, 50)
        self.password_box = pygame.Rect(self.screen_width//2 - 200, 290, 400, 50)
        self.confirm_box = pygame.Rect(self.screen_width//2 - 200, 360, 400, 50)
        
        self.signup_button_rect = pygame.Rect(self.screen_width//2 - 80, 430, 160, 50)
        self.goto_login_rect = pygame.Rect(self.screen_width//2 - 80, 490, 160, 40)

        self.hover_signup = False
        self.hover_login = False
        self.hover_alpha_signup = 0
        self.hover_alpha_direction_signup = 1
        self.hover_alpha_login = 0
        self.hover_alpha_direction_login = 1

        self.error_message = ""
        self.clock = pygame.time.Clock()

        self.focus_list = ["username", "password", "confirm", "signup_button"]

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
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

        pygame.quit()
        sys.exit()

    def cycle_focus(self):
        idx = self.focus_list.index(self.active_input) if self.active_input in self.focus_list else 0
        idx = (idx + 1) % len(self.focus_list)
        self.active_input = self.focus_list[idx]

    def try_submit(self):
        if self.username_text.strip() and self.password_text.strip() and self.confirm_text.strip():
            result = self.attempt_signup()
            if result == "SUCCESS":
                return

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
        elif self.active_input == "confirm":
            if event.key == pygame.K_BACKSPACE:
                self.confirm_text = self.confirm_text[:-1]
            else:
                self.confirm_text += event.unicode

    def handle_mouse_click(self, pos):
        if self.username_box.collidepoint(pos):
            self.active_input = "username"
        elif self.password_box.collidepoint(pos):
            self.active_input = "password"
        elif self.confirm_box.collidepoint(pos):
            self.active_input = "confirm"
        else:
            self.active_input = None

        if self.signup_button_rect.collidepoint(pos):
            result = self.attempt_signup()
            if result == "SUCCESS":
                return

        if self.goto_login_rect.collidepoint(pos):
            from login import LoginScreen
            login = LoginScreen(self.screen)
            login.run()
            return

    def handle_mouse_motion(self, mouse_pos):
        self.hover_signup = self.signup_button_rect.collidepoint(mouse_pos)
        self.hover_login = self.goto_login_rect.collidepoint(mouse_pos)

    def attempt_signup(self):
        username = self.username_text.strip()
        password = self.password_text.strip()
        confirm = self.confirm_text.strip()

        if not username or not password or not confirm:
            self.error_message = "Please fill all fields."
            return ""
        if password != confirm:
            self.error_message = "Passwords do not match."
            return ""

        existing = get_user_by_username(username)
        if existing:
            self.error_message = "Username already taken."
            return ""
        
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        create_user(username, password)
        self.error_message = "Account created!"
        self.draw()
        pygame.display.flip()
        pygame.time.wait(1000)

        from login import LoginScreen
        login = LoginScreen(self.screen)
        login.run()
        return "SUCCESS"

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        for brick in self.floating_bricks:
            brick.update()
            brick.draw(self.screen)

        title_surf = self.title_font.render("SIGN UP", True, PRIMARY_COLOR)
        title_rect = title_surf.get_rect(center=(self.screen_width//2, 150))
        self.screen.blit(title_surf, title_rect)

        masked_pw = "*" * len(self.password_text)
        masked_cf = "*" * len(self.confirm_text)

        self.draw_input_box(self.username_box, self.username_text, "Username", active=(self.active_input=="username"))
        self.draw_input_box(self.password_box, masked_pw, "Password", active=(self.active_input=="password"))
        self.draw_input_box(self.confirm_box, masked_cf, "Confirm", active=(self.active_input=="confirm"))

        self.update_button_hover("signup")
        self.update_button_hover("login")

        self.draw_button(self.signup_button_rect, "SIGN UP", hovered=self.hover_signup, is_signup=True)
        self.draw_button(self.goto_login_rect, "LOGIN", hovered=self.hover_login, is_signup=False)

        if self.error_message:
            err_surf = self.input_font.render(self.error_message, True, ACCENT_COLOR)
            err_rect = err_surf.get_rect(center=(self.screen_width//2, 560))
            self.screen.blit(err_surf, err_rect)

    def draw_input_box(self, rect, text, placeholder, active=False):
        pygame.draw.rect(self.screen, (30,30,30), rect)
        border_color = PRIMARY_COLOR if active else (100,100,100)
        pygame.draw.rect(self.screen, border_color, rect, 2)
        display_text = placeholder if (not text and not active) else text
        font_surf = self.input_font.render(display_text, True, TEXT_COLOR)
        self.screen.blit(font_surf, (rect.x+10, rect.y+10))

    def update_button_hover(self, which):
        if which == "signup":
            if self.hover_signup:
                self.hover_alpha_signup += 5 * self.hover_alpha_direction_signup
                if self.hover_alpha_signup >= 100:
                    self.hover_alpha_direction_signup = -1
                elif self.hover_alpha_signup <= 0:
                    self.hover_alpha_direction_signup = 1
            else:
                self.hover_alpha_signup -= 5
                if self.hover_alpha_signup < 0:
                    self.hover_alpha_signup = 0
        else:
            if self.hover_login:
                self.hover_alpha_login += 5 * self.hover_alpha_direction_login
                if self.hover_alpha_login >= 100:
                    self.hover_alpha_direction_login = -1
                elif self.hover_alpha_login <= 0:
                    self.hover_alpha_login = 1
            else:
                self.hover_alpha_login -= 5
                if self.hover_alpha_login < 0:
                    self.hover_alpha_login = 0

    def draw_button(self, rect, text, hovered=False, is_signup=True):
        alpha_val = 0
        if is_signup:
            alpha_val = 50 + self.hover_alpha_signup if hovered else 50
        else:
            alpha_val = 50 + self.hover_alpha_login if hovered else 50

        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        s.fill((*SECONDARY_COLOR[:3], alpha_val))
        self.screen.blit(s, (rect.x, rect.y))

        if hovered:
            for offset in range(4):
                pygame.draw.line(
                    self.screen,
                    (*SECONDARY_COLOR, 100 - offset * 25),
                    (rect.left - offset, rect.top),
                    (rect.left - offset, rect.bottom),
                    2
                )
        else:
            pygame.draw.line(
                self.screen,
                SECONDARY_COLOR,
                (rect.left, rect.top),
                (rect.left, rect.bottom),
                4
            )

        txt_surf = self.button_font.render(text, True, TEXT_COLOR)
        txt_rect = txt_surf.get_rect(center=rect.center)
        self.screen.blit(txt_surf, txt_rect)