import pytest
import pygame
import os
import sys
import time
import random

# Add parent directory to path so we can import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import necessary modules
from settings import *
from powerup import PowerUp
from paddle import Paddle
from ball import Ball

@pytest.fixture(scope="module")
def pygame_setup():
    """Initialize pygame and mixer for testing"""
    pygame.init()
    pygame.mixer.init()
    
    # Create a screen for testing
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PowerUp Test")
    
    yield screen
    
    # Teardown
    pygame.quit()

@pytest.fixture(scope="module")
def audio_dir():
    """Get the absolute path to the audio directory"""
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(current_dir, 'audio')

@pytest.fixture(scope="module")
def mock_game(audio_dir):
    """Create a mock game object for testing powerups"""
    class MockGame:
        def __init__(self):
            self.paddle = Paddle()
            self.ball = Ball(self.paddle)
            self.balls = [self.ball]
            self.lives = 3
            self.bomb_ready = False
            self.speed_modifier = 1.0
            self.slow_until = 0
            
            # Load sound for powerup
            try:
                powerup_path = os.path.join(audio_dir, 'but.wav')
                self.powerup_sound = pygame.mixer.Sound(powerup_path)
                self.powerup_sound.set_volume(0.7)
            except Exception as e:
                print(f"Could not load powerup sound: {e}")
                self.powerup_sound = None
                
            # Store music paths for extra_life powerup test
            self.reborn_music_path = os.path.join(audio_dir, 'd.mp3')
            self.current_music = 'normal'
    
    return MockGame()

@pytest.fixture(params=['bomb', 'multi_ball', 'extra_life', 'slow_ball'])
def powerup_type(request):
    """Parameterized fixture for testing different powerup types"""
    return request.param

def test_powerup_effects(pygame_setup, mock_game, powerup_type):
    """Test the effects of each type of powerup"""
    screen = pygame_setup
    game = mock_game
    
    # Create a powerup of the specific type
    powerup = PowerUp(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    powerup.type = powerup_type  # Force the type for testing
    
    # Draw the powerup
    screen.fill(BACKGROUND_COLOR)
    powerup.draw(screen)
    pygame.display.flip()
    
    # Record initial state
    initial_balls = len(game.balls)
    initial_lives = game.lives
    initial_speed_modifier = game.speed_modifier
    initial_bomb_ready = game.bomb_ready
    
    # Apply the powerup
    powerup.apply(game)
    
    # Check the effects based on powerup type
    if powerup_type == 'bomb':
        assert game.bomb_ready, "Bomb powerup should activate bomb_ready"
        
    elif powerup_type == 'multi_ball':
        assert len(game.balls) > initial_balls, "Multi-ball powerup should add new balls"
        # Reset for next test
        game.balls = [game.ball]  # Reset to just one ball
        
    elif powerup_type == 'extra_life':
        assert game.lives > initial_lives, "Extra life powerup should increase lives"
        assert game.lives == initial_lives + 1, f"Lives should increase by 1 from {initial_lives} to {game.lives}"
        
    elif powerup_type == 'slow_ball':
        assert game.speed_modifier < initial_speed_modifier, "Slow ball powerup should reduce speed modifier"
        assert game.speed_modifier == 0.8, f"Speed modifier should be 0.8, got {game.speed_modifier}"

def test_powerup_movement(pygame_setup):
    """Test that powerups move down the screen correctly"""
    screen = pygame_setup
    
    # Create a powerup at the top of the screen
    initial_y = 100
    powerup = PowerUp(SCREEN_WIDTH // 2, initial_y)
    initial_position = powerup.rect.y
    
    # Update the powerup to move it down
    powerup.update()
    
    # Check that it moved down by the expected amount
    assert powerup.rect.y > initial_position, "Powerup should move down"
    assert powerup.rect.y == initial_position + powerup.speed, f"Powerup should move down by {powerup.speed} pixels"

def test_powerup_collection(pygame_setup, mock_game):
    """Test that powerups can be collected by the paddle"""
    screen = pygame_setup
    game = mock_game
    
    # Create a powerup higher above the paddle to avoid initial collision
    powerup = PowerUp(SCREEN_WIDTH // 2, PADDLE_Y - 50)  # Increased distance from paddle
    
    # Position paddle to collect the powerup
    game.paddle.rect.centerx = SCREEN_WIDTH // 2
    
    # Initial state - no collision
    assert not powerup.rect.colliderect(game.paddle.rect), "Powerup should not collide with paddle initially"
    
    # Move powerup down until it collides with paddle
    collision_detected = False
    for _ in range(10):  # Increased iterations to account for greater distance
        powerup.update()
        if powerup.rect.colliderect(game.paddle.rect):
            collision_detected = True
            break
    
    # Assert that collision was detected
    assert collision_detected, "Powerup should collide with paddle after moving down"

if __name__ == "__main__":
    pytest.main(['-v', __file__])