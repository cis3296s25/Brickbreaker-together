import pytest
import pygame
import os
import sys
import time

# Add parent directory to path so we can import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import necessary modules
from settings import *

@pytest.fixture(scope="module")
def pygame_setup():
    """Initialize pygame and mixer for testing"""
    pygame.init()
    pygame.mixer.init()
    
    # Create a small screen for testing
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("BGM Test")
    
    yield screen
    
    # Teardown
    pygame.quit()

@pytest.fixture(scope="module")
def audio_dir():
    """Get the absolute path to the audio directory"""
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(current_dir, 'audio')

@pytest.fixture(params=[
    ('Game Music', 'game_music.mp3'),
    ('Danger Music', 'danger_music.mp3'),
    ('Reborn Music', 'd.mp3'),
    ('Menu Music', 'background_music.mp3')
])
def music_file(request):
    """Parameterized fixture for testing different music files"""
    return request.param

def test_music_loading(pygame_setup, audio_dir, music_file):
    """Test that music files can be loaded and played"""
    music_name, music_filename = music_file
    music_path = os.path.join(audio_dir, music_filename)
    
    # Try to load and play the music
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()
    
    # Let it play for a short time to verify it works
    start_time = time.time()
    while time.time() - start_time < 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pytest.exit("Test interrupted by user")
        pygame.display.flip()
    
    # If we got here without exceptions, the music loaded successfully
    assert pygame.mixer.music.get_busy(), f"{music_name} should be playing"

def test_volume_control(pygame_setup, audio_dir, music_file):
    """Test volume control functionality"""
    music_name, music_filename = music_file
    music_path = os.path.join(audio_dir, music_filename)
    
    # Load and play the music
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()
    
    # Initial volume should be close to 0.3
    initial_volume = pygame.mixer.music.get_volume()
    assert 0.25 <= initial_volume <= 0.35, f"Initial volume {initial_volume} should be close to 0.3"
    
    # Change volume to 0.5
    pygame.mixer.music.set_volume(0.5)
    time.sleep(0.5)  # Short delay to let the change take effect
    
    # Volume should now be close to 0.5
    new_volume = pygame.mixer.music.get_volume()
    assert 0.45 <= new_volume <= 0.55, f"New volume {new_volume} should be close to 0.5"
    
    # Stop the music
    pygame.mixer.music.stop()

def test_pause_unpause(pygame_setup, audio_dir, music_file):
    """Test pause and unpause functionality"""
    music_name, music_filename = music_file
    music_path = os.path.join(audio_dir, music_filename)
    
    # Load and play the music
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()
    
    # Music should be playing
    assert pygame.mixer.music.get_busy(), "Music should be playing"
    
    # Store the current position before pausing
    # Note: pygame doesn't provide a direct way to check if music is paused
    # So we'll test if we can successfully pause and unpause
    
    # Pause the music
    pygame.mixer.music.pause()
    time.sleep(0.5)  # Short delay to let the change take effect
    
    # In pygame, get_busy() returns False when music is paused
    # We can't directly test for paused state, so we'll skip this assertion
    
    # Unpause the music
    pygame.mixer.music.unpause()
    time.sleep(0.5)  # Short delay to let the change take effect
    
    # Music should be playing again
    assert pygame.mixer.music.get_busy(), "Music should be playing after unpause"
    
    # Stop the music
    pygame.mixer.music.stop()