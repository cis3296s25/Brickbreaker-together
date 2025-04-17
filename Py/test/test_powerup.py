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

def test_powerup():
    """Test PowerUp generation and effects"""
    print("\n=== Testing PowerUp System ===\n")
    
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()
    
    # Create a screen for testing
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PowerUp Test")
    
    # Get the absolute path to the audio directory
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    audio_dir = os.path.join(current_dir, 'audio')
    
    # Create a mock game object to test powerups
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
    
    # Create mock game
    game = MockGame()
    
    # Test each type of powerup
    powerup_types = ['bomb', 'multi_ball', 'extra_life', 'slow_ball']
    
    for powerup_type in powerup_types:
        print(f"Testing {powerup_type} powerup...")
        
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
        
        # Check the effects
        if powerup_type == 'bomb':
            if game.bomb_ready:
                print(f"✓ Bomb powerup activated successfully")
            else:
                print(f"✗ Bomb powerup failed to activate")
                
        elif powerup_type == 'multi_ball':
            if len(game.balls) > initial_balls:
                print(f"✓ Multi-ball powerup added {len(game.balls) - initial_balls} new balls")
            else:
                print(f"✗ Multi-ball powerup failed to add new balls")
                
        elif powerup_type == 'extra_life':
            if game.lives > initial_lives:
                print(f"✓ Extra life powerup increased lives from {initial_lives} to {game.lives}")
            else:
                print(f"✗ Extra life powerup failed to increase lives")
                
        elif powerup_type == 'slow_ball':
            if game.speed_modifier < initial_speed_modifier:
                print(f"✓ Slow ball powerup reduced speed modifier to {game.speed_modifier}")
            else:
                print(f"✗ Slow ball powerup failed to reduce speed modifier")
        
        # Reset for next test
        if powerup_type == 'multi_ball':
            game.balls = [game.ball]  # Reset to just one ball
        
        print(f"✓ {powerup_type} powerup test completed\n")
        time.sleep(1)
    
    # Test powerup movement
    print("Testing powerup movement...")
    powerup = PowerUp(SCREEN_WIDTH // 2, 100)
    
    for _ in range(10):
        screen.fill(BACKGROUND_COLOR)
        powerup.update()  # Move the powerup down
        powerup.draw(screen)
        pygame.display.flip()
        time.sleep(0.1)
    
    print(f"✓ Powerup movement test completed")
    
    # Test powerup collection
    print("\nTesting powerup collection...")
    powerup = PowerUp(SCREEN_WIDTH // 2, PADDLE_Y - 20)  # Just above paddle
    game.paddle.rect.centerx = SCREEN_WIDTH // 2  # Center paddle
    
    # Draw initial state
    screen.fill(BACKGROUND_COLOR)
    powerup.draw(screen)
    game.paddle.draw(screen)
    pygame.display.flip()
    time.sleep(1)
    
    # Move powerup to collide with paddle
    for _ in range(5):
        screen.fill(BACKGROUND_COLOR)
        powerup.update()
        powerup.draw(screen)
        game.paddle.draw(screen)
        
        # Check for collision
        if powerup.rect.colliderect(game.paddle.rect):
            print("✓ Powerup collected by paddle")
            if game.powerup_sound:
                game.powerup_sound.play()
                print("✓ Powerup sound played")
            break
            
        pygame.display.flip()
        time.sleep(0.1)
    
    print("PowerUp testing completed.")
    pygame.quit()

if __name__ == "__main__":
    test_powerup()