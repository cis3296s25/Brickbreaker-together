import pygame
import random
from settings import *

class Brick:
    def __init__(self, x, y, color, brick_type='normal'):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color
        self.type = brick_type
        self.active = True  # ✅ Add this line
        self.light_color = (min(color[0]+40,255), min(color[1]+40,255), min(color[2]+40,255))
        self.dark_color = (max(color[0]-40,0), max(color[1]-40,0), max(color[2]-40,0))

    def get_lighter_color(self, color):
        return tuple(min(c + 50, 255) for c in color)

    def get_darker_color(self, color):
        return tuple(max(c - 50, 0) for c in color)

    def draw(self, screen):
        if not self.active:
            return

        # Base rectangle
        pygame.draw.rect(screen, self.color, self.rect)

        # Light top & left border
        pygame.draw.line(screen, self.light_color, self.rect.topleft, self.rect.topright, 2)
        pygame.draw.line(screen, self.light_color, self.rect.topleft, self.rect.bottomleft, 2)

        # Dark bottom & right border
        pygame.draw.line(screen, self.dark_color, self.rect.bottomleft, self.rect.bottomright, 2)
        pygame.draw.line(screen, self.dark_color, self.rect.topright, self.rect.bottomright, 2)

        # Draw 'X' on indestructible bricks
        if self.type == 'indestructible':
            font = pygame.font.Font(None, int(24 * SCALE_FACTOR))
            label = font.render("X", True, (255, 255, 255))
            label_rect = label.get_rect(center=self.rect.center)
            screen.blit(label, label_rect)

