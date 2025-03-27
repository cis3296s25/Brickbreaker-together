import pygame
import random
import math
from settings import *


class Ball:
    def __init__(self, paddle):
        """
        Initialize the ball object at the position of the paddle.
        Args
            paddle (Paddle): The paddle object to position the ball correctly at the start.
        """
        # Create a rectangle representing the ball's position and size.
        # Initially position it at the center of the paddle.
        self.rect = pygame.Rect(paddle.rect.centerx - BALL_RADIUS, paddle.rect.top - BALL_RADIUS * 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        # Call reset to set initial ball movements
        self.reset(paddle)

    def reset(self, paddle):
        """
        Reset the ball position and shoot it at a random angle.
        Args
            paddle (Paddle): The paddle object to position the ball correctly.
        """
        # Center the ball on the paddle.
        self.rect.centerx = paddle.rect.centerx
        self.rect.bottom = paddle.rect.top
        # Generate a random angle between -45° and +45° for launching the ball.
        angle = random.uniform(-math.pi / 4, math.pi / 4)  # -45° to 45°
        # Set the ball's speed based on the calculated angle.
        self.dx = BALL_SPEED * math.cos(angle)
        self.dy = -abs(BALL_SPEED * math.sin(angle))

    def move(self, paddle, bricks):
        """
        Move the ball and handle collisions with walls, paddle, and bricks.
        Args
            paddle (Paddle): The paddle object to detect collision.
            bricks (list): List of Brick objects to detect collision and remove when hit.
        Returns
            int
                10 If a brick is hit (for score increase)
                -1 If the ball is lost (life lost)
                0 If nothing special happens
        """
        # Update the ball's position based on its velocity.
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
        """
        Draw the ball on the screen.
        """
        # Draw a circle at the ball's position.
        pygame.draw.circle(screen, (236, 240, 241), self.rect.center, BALL_RADIUS)
