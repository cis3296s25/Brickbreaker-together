import pygame
import random
import math
from settings import *

class Ball:
    def __init__(self, paddle):
        self.rect = pygame.Rect(paddle.rect.centerx - BALL_RADIUS, paddle.rect.top - BALL_RADIUS * 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.reset(paddle)

    def reset(self, paddle):
        self.rect.centerx = paddle.rect.centerx
        self.rect.bottom = paddle.rect.top
        angle = random.uniform(-math.pi / 4, math.pi / 4)  # -45° to 45°
        self.dx = BALL_SPEED * math.cos(angle)
        self.dy = -abs(BALL_SPEED * math.sin(angle))

    def move(self, paddle, bricks):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off left and right walls
        if self.rect.left <= 80 or self.rect.right >= WIDTH - 80:
            self.dx = -self.dx

        # Bounce off top wall
        if self.rect.top <= 140:
            self.dy = -self.dy

        # Bounce off paddle
        if self.rect.colliderect(paddle.rect):
            self.dy = -self.dy

        # Bounce off bricks
        for brick in bricks[:]:
            if self.rect.colliderect(brick.rect):
                bricks.remove(brick)
                self.dy = -self.dy
                return 10  # Score increase

        # If ball falls below paddle
        if self.rect.top >= HEIGHT:
            return -1  # Lose life
        
        return 0

    def draw(self, screen):
        pygame.draw.circle(screen, (236, 240, 241), self.rect.center, BALL_RADIUS)
