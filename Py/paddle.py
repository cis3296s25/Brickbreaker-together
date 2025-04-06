import pygame
from settings import *

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x = max(int(80 * SCALE_FACTOR), self.rect.x - int(7 * SCALE_FACTOR))
        if keys[pygame.K_RIGHT]:
            self.rect.x = min(SCREEN_WIDTH - int(80 * SCALE_FACTOR) - PADDLE_WIDTH, self.rect.x + int(7 * SCALE_FACTOR))

    def draw(self, screen):
        pygame.draw.rect(screen, PRIMARY_COLOR, self.rect, border_radius=int(5 * SCALE_FACTOR))
