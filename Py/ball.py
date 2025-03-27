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
        Reset the ball position and shoot it nearly vertically upward.
        """
        self.rect.centerx = paddle.rect.centerx
        self.rect.bottom = paddle.rect.top

        MIN_VERTICAL_SPEED = 2  # Prevent near-horizontal bouncing

        while True:
            # Favor near-vertical shots (around 90° or π/2)
            angle = random.uniform(math.pi / 2 - 0.35, math.pi / 2 + 0.35)  # ~70° to 110°
            dx = BALL_SPEED * math.cos(angle)
            dy = -abs(BALL_SPEED * math.sin(angle))  # Always go upward

            if abs(dy) >= MIN_VERTICAL_SPEED:
                break

        self.dx = dx
        self.dy = dy


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
            if self.rect.colliderect(brick.rect): # Check if the brick is colliding
                if self.rect.right >= brick.rect.left and self.rect.left < brick.rect.left:  # Ball hits right side of the brick
                    bricks.remove(brick)
                    self.dx = -self.dx + random.uniform(.1, 1)  # Reverse horizontal direction + speed up
                    return 10  # Score increase
                elif self.rect.left <= brick.rect.right and self.rect.right > brick.rect.right:  # Ball hits left side of the brick
                    bricks.remove(brick)
                    self.dx = -self.dx + random.uniform(.1, 1) # Reverse horizontal direction + speed up
                    return 10  # Score increase
                if self.rect.bottom >= brick.rect.top and self.rect.top < brick.rect.top:  # Ball hits the bottom of the brick
                    bricks.remove(brick)
                    self.dy = -self.dy + random.uniform(.1, 1) # Reverse vertical direction + speed up
                    return 10  # Score increase
                elif self.rect.top <= brick.rect.bottom and self.rect.bottom > brick.rect.bottom:  # Ball hits the top of the brick
                    bricks.remove(brick)
                    self.dy = -self.dy + random.uniform(.1, 1) # Reverse vertical direction + speed up
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
