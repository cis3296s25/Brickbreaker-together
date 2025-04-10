import pygame
import random

PRIMARY_COLOR = (52, 152, 219)
SECONDARY_COLOR = (46, 204, 113)
BACKGROUND_COLOR = (18, 18, 18)
UI_BACKGROUND = (18, 18, 18, 215)
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (231, 76, 60)
PINK = (255, 105, 180)
TEAL = (0, 128, 128)


class FloatingBrick:
    def __init__(self, screen_width, screen_height):
        self.width = 60
        self.height = 20
        self.x = random.randint(0, screen_width - self.width)
        self.y = screen_height
        self.color = random.choice([
            PRIMARY_COLOR, 
            SECONDARY_COLOR, 
            ACCENT_COLOR, 
            (243, 156, 18)  # Orange color
        ])
        self.speed = random.uniform(0.5, 2)
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)

    def update(self):
        self.y -= self.speed
        self.rotation += self.rotation_speed
        if self.y < -self.height:
            self.y = pygame.display.get_surface().get_height()
            self.x = random.randint(0, pygame.display.get_surface().get_width() - self.width)

    def draw(self, screen):
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surf.fill(self.color + (25,))
        rotated_surf = pygame.transform.rotate(surf, self.rotation)
        screen.blit(rotated_surf, (self.x, self.y))