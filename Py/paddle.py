import pygame
from settings import *

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x = max(80, self.rect.x - 7)
        if keys[pygame.K_RIGHT]:
            self.rect.x = min(WIDTH - 80 - PADDLE_WIDTH, self.rect.x + 7)

    def draw(self, screen):
        pygame.draw.rect(screen, PRIMARY_COLOR, self.rect, border_radius=5)
