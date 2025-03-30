import pygame
import random
from settings import *

class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = random.choice(['bomb', 'multi_ball', 'extra_life', 'slow_ball'])
        self.speed = 3