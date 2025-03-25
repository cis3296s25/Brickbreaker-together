import pygame
from settings import *


class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 42)
        self.font_score = pygame.font.Font(None, 24)

    def draw(self, screen, score, lives):
        title = self.font_large.render("BRICKBREAKER", True, PRIMARY_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        score_text = self.font_score.render(f"Score: {score}", True, PRIMARY_COLOR)
        screen.blit(score_text, (WIDTH - 150, 50))

        for i in range(lives):
            pygame.draw.circle(screen, LIFE_COLOR, (100 + i * 25, 70), 8)
