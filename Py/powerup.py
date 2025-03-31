import pygame
import random
from settings import *

class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = random.choice(['bomb', 'multi_ball', 'extra_life', 'slow_ball'])
        self.speed = 3

        self.color_map = {
            'bomb': (231, 76, 60),        # Red
            'multi_ball': (52, 152, 219), # Blue
            'extra_life': (46, 204, 113), # Green
            'slow_ball': (241, 196, 15),  # Yellow
        }

        self.label_map = {
            'bomb': 'B',
            'multi_ball': 'M',
            'extra_life': '+',
            'slow_ball': 'S',
        }
    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        # Draw the power-up circle
        pygame.draw.ellipse(screen, self.color_map[self.type], self.rect)

        # Draw the label text
        font = pygame.font.Font(None, 24)
        label = self.label_map[self.type]
        text = font.render(label, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def apply(self, game):
        if self.type == 'bomb':
            game.bomb_ready = True

        elif self.type == 'multi_ball':
            from ball import Ball
            new_balls = []
            for b in game.balls:
                for _ in range(2):
                    new_ball = Ball(game.paddle)
                    new_ball.rect.center = b.rect.center  # Start from existing ball
                    new_ball.dx = b.dx + random.uniform(-1, 1)
                    new_ball.dy = b.dy + random.uniform(-1, 1)
                    new_balls.append(new_ball)
            game.balls.extend(new_balls)

        elif self.type == 'extra_life':
            game.lives = min(game.lives + 1, 5)

        elif self.type == 'slow_ball':
            game.speed_modifier = 0.8  # Reduce ball speed to 80%
            game.slow_until = pygame.time.get_ticks() + 3000  # for 3 seconds
