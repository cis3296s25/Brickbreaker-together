import pygame
from settings import *

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            left_limit = int(80 * SCALE_FACTOR)
            self.rect.x = max(left_limit, self.rect.x - int(7 * SCALE_FACTOR))
        if keys[pygame.K_RIGHT]:
            right_limit = SCREEN_WIDTH - int(80 * SCALE_FACTOR) - self.rect.width
            self.rect.x = min(right_limit, self.rect.x + int(7 * SCALE_FACTOR))

    def draw(self, screen):
        pygame.draw.rect(screen, PRIMARY_COLOR, self.rect, border_radius=int(5 * SCALE_FACTOR))
