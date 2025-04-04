import pygame
import sys
import hashlib
from ui_constants import (
    PRIMARY_COLOR, SECONDARY_COLOR, BACKGROUND_COLOR,
    TEXT_COLOR, ACCENT_COLOR,
    FloatingBrick
)
from db import get_user_by_username

pygame.init()
pygame.font.init()
pygame.mixer.init()

class LoginScreen:
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
        self.active_input = "username"
        self.username_box = pygame.Rect(self.screen_width//2 - 200, 250, 400, 50)
        self.password_box = pygame.Rect(self.screen_width//2 - 200, 320, 400, 50)
        self.login_button_rect = pygame.Rect(self.screen_width//2 - 70, 400, 140, 50)
        self.goto_signup_rect = pygame.Rect(self.screen_width//2 - 70, 470, 140, 40)
        self.hover_login = False
        self.hover_signup = False
        self.hover_alpha_login = 0
        self.hover_alpha_direction_login = 1
        self.hover_alpha_signup = 0
        self.hover_alpha_direction_signup = 1
        self.error_message = ""
        self.clock = pygame.time.Clock()
        self.focus_list = ["username", "password", "login_button"]
        self.login_success_username = None

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

    def handle_mouse_motion(self, mouse_pos):
        self.hover_login = self.login_button_rect.collidepoint(mouse_pos)
        self.hover_signup = self.goto_signup_rect.collidepoint(mouse_pos)

    def attempt_login(self):
        username = self.username_text.strip()
        password = self.password_text.strip()
        if not username or not password:
            return ("ERROR", None)
        user = get_user_by_username(username)
        if not user:
            self.error_message = "Username not found."
            return ("ERROR", None)
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        if hashed_input != user['password_hash']:
            self.error_message = "Incorrect password."
            return ("ERROR", None)
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
        title_surf = self.title_font.render("LOGIN", True, PRIMARY_COLOR)
        title_rect = title_surf.get_rect(center=(self.screen_width//2, 150))
        self.screen.blit(title_surf, title_rect)
        self.draw_input_box(self.username_box, self.username_text, "Username", active=(self.active_input=="username"))
        masked_pw = "*" * len(self.password_text)
        self.draw_input_box(self.password_box, masked_pw, "Password", active=(self.active_input=="password"))
        self.update_button_hover("login")
        self.update_button_hover("signup")
        self.draw_button(self.login_button_rect, "LOGIN", hovered=self.hover_login, is_login=True)
        self.draw_button(self.goto_signup_rect, "SIGN UP", hovered=self.hover_signup, is_login=False)
        if self.error_message:
            err_surf = self.input_font.render(self.error_message, True, ACCENT_COLOR)
            err_rect = err_surf.get_rect(center=(self.screen_width//2, 540))
            self.screen.blit(err_surf, err_rect)

    def draw_input_box(self, rect, text, placeholder, active=False):
        pygame.draw.rect(self.screen, (30,30,30), rect)
        border_color = PRIMARY_COLOR if active else (100,100,100)
        pygame.draw.rect(self.screen, border_color, rect, 2)
        display_text = placeholder if (not text and not active) else text
        font_surf = self.input_font.render(display_text, True, TEXT_COLOR)
        self.screen.blit(font_surf, (rect.x+10, rect.y+10))

    def update_button_hover(self, which):
        if which == "login":
            if self.hover_login:
                self.hover_alpha_login += 5 * self.hover_alpha_direction_login
                if self.hover_alpha_login >= 100:
                    self.hover_alpha_direction_login = -1
                elif self.hover_alpha_login <= 0:
                    self.hover_alpha_direction_login = 1
            else:
                self.hover_alpha_login -= 5
                if self.hover_alpha_login < 0:
                    self.hover_alpha_login = 0
        else:
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

    def draw_button(self, rect, text, hovered=False, is_login=True):
        alpha_val = 50
        if is_login:
            alpha_val = 50 + self.hover_alpha_login if hovered else 50
        else:
            alpha_val = 50 + self.hover_alpha_signup if hovered else 50
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