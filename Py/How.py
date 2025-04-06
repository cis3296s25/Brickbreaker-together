import pygame
import sys
import os
from settings import *
from ui_constants import (
    PRIMARY_COLOR, SECONDARY_COLOR, BACKGROUND_COLOR,
    TEXT_COLOR, ACCENT_COLOR,
    FloatingBrick
)

pygame.init()
pygame.font.init()
pygame.mixer.init()
init_screen_dimensions()

HOW_TO_PLAY_COLOR = (52, 152, 219)

class HowToPlayScreen:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        # Font sizes based on screen dimensions
        self.base_title_size = 48
        self.base_subtitle_size = 32
        self.base_text_size = 24
        self.base_button_size = 24

        height_scale = min(self.screen_height / 1080, 1.5)

        self.title_font_size = max(int(self.base_title_size * height_scale), 36)
        self.subtitle_font_size = max(int(self.base_subtitle_size * height_scale), 24)
        self.text_font_size = max(int(self.base_text_size * height_scale), 18)
        self.button_font_size = max(int(self.base_button_size * height_scale), 18)

        self.title_font = pygame.font.SysFont('Segoe UI', self.title_font_size, bold=True)
        self.subtitle_font = pygame.font.SysFont('Segoe UI', self.subtitle_font_size, bold=True)
        self.text_font = pygame.font.SysFont('Segoe UI', self.text_font_size)
        self.button_font = pygame.font.SysFont('Segoe UI', self.button_font_size)

        self.floating_bricks = [FloatingBrick(self.screen_width, self.screen_height) for _ in range(5)]

        button_width = int(160 * SCALE_FACTOR)
        button_height = int(50 * SCALE_FACTOR)
        self.back_button_rect = pygame.Rect(
            self.screen_width // 2 - button_width // 2,
            self.screen_height - int(100 * SCALE_FACTOR),
            button_width,
            button_height
        )
        self.hover_back = False
        self.hover_alpha_back = 0
        self.hover_alpha_direction_back = 1

        self.sections = [
            {
                "title": "How to Play",
                "content": [
                    "• Use LEFT and RIGHT arrow keys to move the paddle",
                    "• Break all the bricks to win the level",
                    "• Don't let the ball fall below the paddle",
                    "• Collect power-ups to gain special abilities"
                ]
            },
            {
                "title": "Controls",
                "content": [
                    "• Arrow Keys: Move the paddle left and right",
                    "• P: Pause the game",
                    "• ESC: Exit to main menu",
                    "• Space: Launch the ball (in some game modes)"
                ]
            },
            {
                "title": "Game Modes",
                "content": [
                    "• Single Player: Play against the computer",
                    "• Local Multiplayer: Play with friends on the same device",
                    "• Online Multiplayer: Play with others online (requires account)"
                ]
            },
            {
                "title": "Power-Ups",
                "content": [
                    "• Red Power-Up: Increases paddle size",
                    "• Blue Power-Up: Slows down the ball",
                    "• Green Power-Up: Multiplies the ball",
                    "• Yellow Power-Up: Adds extra lives",
                    "• Purple Power-Up: Shoots lasers from the paddle"
                ]
            }
        ]

        self.top_margin = int(150 * SCALE_FACTOR)
        self.bottom_margin = int(120 * SCALE_FACTOR)
        self.line_spacing = int(8 * SCALE_FACTOR)
        self.section_spacing = int(30 * SCALE_FACTOR)
        self.subtitle_gap = int(15 * SCALE_FACTOR)

        self.column_width = int(400 * SCALE_FACTOR)
        self.col_gap = int(50 * SCALE_FACTOR)
        self.left_column_x = (self.screen_width // 2) - (self.column_width + self.col_gap // 2)
        self.right_column_x = (self.screen_width // 2) + (self.col_gap // 2)
        self.column_top_y = int(180 * SCALE_FACTOR)

        self.maybe_scale_down_fonts()

        self.clock = pygame.time.Clock()

    def measure_column_height(self, sections_list, subtitle_font, text_font):
        total_height = 0
        for section in sections_list:
            total_height += subtitle_font.get_height() + self.subtitle_gap
            for line in section["content"]:
                total_height += text_font.get_height() + self.line_spacing
            total_height += self.section_spacing
        return total_height

    def maybe_scale_down_fonts(self):
        left_sections = [self.sections[i] for i in range(0, len(self.sections), 2)]
        right_sections = [self.sections[i] for i in range(1, len(self.sections), 2)]

        left_height = self.measure_column_height(left_sections, self.subtitle_font, self.text_font)
        right_height = self.measure_column_height(right_sections, self.subtitle_font, self.text_font)
        max_col_height = max(left_height, right_height)

        available_space = self.screen_height - self.top_margin - self.bottom_margin

        if max_col_height > available_space:
            ratio = available_space / max_col_height

            new_subtitle_size = max(int(self.subtitle_font_size * ratio), 14)
            new_text_size = max(int(self.text_font_size * ratio), 12)

            self.subtitle_font = pygame.font.SysFont('Segoe UI', new_subtitle_size, bold=True)
            self.text_font = pygame.font.SysFont('Segoe UI', new_text_size)

            self.line_spacing = max(int(self.line_spacing * ratio), 2)
            self.section_spacing = max(int(self.section_spacing * ratio), 4)
            self.subtitle_gap = max(int(self.subtitle_gap * ratio), 4)

            left_height = self.measure_column_height(left_sections, self.subtitle_font, self.text_font)
            right_height = self.measure_column_height(right_sections, self.subtitle_font, self.text_font)

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
                        running = False
                elif event.type == pygame.MOUSEMOTION:
                    self.hover_back = self.back_button_rect.collidepoint(mouse_pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button_rect.collidepoint(mouse_pos):
                        running = False
            
            self.draw()
            pygame.display.flip()

    def update_button_hover(self, is_hovered):
        if is_hovered:
            self.hover_alpha_back += 5 * self.hover_alpha_direction_back
            if self.hover_alpha_back >= 100:
                self.hover_alpha_direction_back = -1
            elif self.hover_alpha_back <= 0:
                self.hover_alpha_direction_back = 1
        else:
            self.hover_alpha_back = max(self.hover_alpha_back - 5, 0)

    def draw_button(self, rect, text, hovered=False):
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        if hovered:
            s.fill((*HOW_TO_PLAY_COLOR[:3], 50 + self.hover_alpha_back))
        else:
            s.fill((18, 18, 18, 215))
        self.screen.blit(s, rect)

        pygame.draw.rect(self.screen, HOW_TO_PLAY_COLOR, rect, 4, border_radius=5)

        text_color = HOW_TO_PLAY_COLOR if hovered else TEXT_COLOR
        txt_surf = self.button_font.render(text, True, text_color)
        txt_rect = txt_surf.get_rect(center=rect.center)
        self.screen.blit(txt_surf, txt_rect)

    def draw_title_with_glow(self):
        title_y = int(100 * SCALE_FACTOR)
        title_surf = self.title_font.render("HOW TO PLAY", True, PRIMARY_COLOR)
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, title_y))

        for offset in range(3):
            glow_surf = self.title_font.render("HOW TO PLAY", True, (*PRIMARY_COLOR[:3], 100 - offset * 30))
            glow_rect = glow_surf.get_rect(center=(self.screen_width // 2, title_y))
            self.screen.blit(glow_surf, glow_rect)
        self.screen.blit(title_surf, title_rect)

    def draw_columns(self):
        left_sections = [self.sections[i] for i in range(0, len(self.sections), 2)]
        right_sections = [self.sections[i] for i in range(1, len(self.sections), 2)]

        left_y = self.column_top_y
        right_y = self.column_top_y

        for section in left_sections:
            left_y = self.draw_section_in_column(
                section,
                column_x=self.left_column_x,
                start_y=left_y,
                column_width=self.column_width
            )

        for section in right_sections:
            right_y = self.draw_section_in_column(
                section,
                column_x=self.right_column_x,
                start_y=right_y,
                column_width=self.column_width
            )

    def draw_section_in_column(self, section, column_x, start_y, column_width):
        subtitle_surf = self.subtitle_font.render(section["title"], True, HOW_TO_PLAY_COLOR)
        subtitle_rect = subtitle_surf.get_rect(midtop=(column_x + column_width // 2, start_y))
        self.screen.blit(subtitle_surf, subtitle_rect)

        current_y = subtitle_rect.bottom + self.subtitle_gap

        indent_x = column_x + int(10 * SCALE_FACTOR)
        for line in section["content"]:
            line_surf = self.text_font.render(line, True, TEXT_COLOR)
            line_rect = line_surf.get_rect(topleft=(indent_x, current_y))
            self.screen.blit(line_surf, line_rect)
            current_y = line_rect.bottom + self.line_spacing

        current_y += self.section_spacing
        return current_y

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        for brick in self.floating_bricks:
            brick.update()
            brick.draw(self.screen)

        title_surf = self.title_font.render("HOW TO PLAY", True, PRIMARY_COLOR)
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, int(100 * SCALE_FACTOR)))
        for offset in range(3):
            glow_surf = self.title_font.render("HOW TO PLAY", True, (*PRIMARY_COLOR[:3], 100 - offset * 30))
            glow_rect = glow_surf.get_rect(center=(self.screen_width // 2, int(100 * SCALE_FACTOR)))
            self.screen.blit(glow_surf, glow_rect)
        self.screen.blit(title_surf, title_rect)

        column_width = int(400 * SCALE_FACTOR)
        center_x = self.screen_width // 2
        left_column_x = center_x - column_width - int(150 * SCALE_FACTOR)
        right_column_x = center_x + int(150 * SCALE_FACTOR)
        
        left_column_y = int(180 * SCALE_FACTOR)
        right_column_y = int(180 * SCALE_FACTOR)
        
        title_content_spacing = int(15 * SCALE_FACTOR)
        line_spacing = int(8 * SCALE_FACTOR)
        section_spacing = int(30 * SCALE_FACTOR)
        
        max_content_widths = {}
        for section in self.sections:
            max_width = 0
            for line in section["content"]:
                text_surf = self.text_font.render(line, True, TEXT_COLOR)
                max_width = max(max_width, text_surf.get_width())
            max_content_widths[section["title"]] = max_width

        for i, section in enumerate(self.sections):
            is_left_column = i % 2 == 0
            column_x = left_column_x if is_left_column else right_column_x
            current_y = left_column_y if is_left_column else right_column_y
            
            content_height = 0
            for line in section["content"]:
                text_surf = self.text_font.render(line, True, TEXT_COLOR)
                content_height += text_surf.get_height() + line_spacing
            content_height -= line_spacing
            
            subtitle_surf = self.subtitle_font.render(section["title"], True, HOW_TO_PLAY_COLOR)
            subtitle_rect = subtitle_surf.get_rect(midtop=(column_x + column_width // 2, current_y))
            self.screen.blit(subtitle_surf, subtitle_rect)
            
            current_y = subtitle_rect.bottom + title_content_spacing
            
            content_start_x = column_x + (column_width - max_content_widths[section["title"]]) // 2
            
            for line in section["content"]:
                text_surf = self.text_font.render(line, True, TEXT_COLOR)
                text_rect = text_surf.get_rect(midtop=(content_start_x + max_content_widths[section["title"]] // 2, current_y))
                self.screen.blit(text_surf, text_rect)
                current_y = text_rect.bottom + line_spacing
            
            current_y += section_spacing
            
            if is_left_column:
                left_column_y = current_y
            else:
                right_column_y = current_y

        self.update_button_hover(self.hover_back)
        self.draw_button(self.back_button_rect, "BACK", hovered=self.hover_back)

if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    how_to_play = HowToPlayScreen(screen)
    how_to_play.run()