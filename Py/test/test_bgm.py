import pygame
import os
import sys
import time

# Add parent directory to path so we can import game modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import necessary modules
from settings import *

def test_bgm():
    """Test background music loading and playing functionality"""
    print("\n=== Testing Background Music (BGM) ===\n")
    
    # Initialize pygame and mixer
    pygame.init()
    pygame.mixer.init()
    
    # Create a small screen for testing
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("BGM Test")
    
    # Get the absolute path to the audio directory
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    audio_dir = os.path.join(current_dir, 'audio')
    
    # List of music files to test
    music_files = [
        ('Game Music', 'game_music.mp3'),
        ('Danger Music', 'danger_music.mp3'),
        ('Reborn Music', 'd.mp3'),
        ('Menu Music', 'background_music.mp3')
    ]
    
    # Test each music file
    for music_name, music_file in music_files:
        music_path = os.path.join(audio_dir, music_file)
        print(f"Testing {music_name} ({music_file})...")
        
        try:
            # Try to load and play the music
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()
            
            print(f"✓ Successfully loaded and playing {music_name}")
            print("  Listening for 3 seconds...")
            
            # Let it play for 3 seconds
            start_time = time.time()
            while time.time() - start_time < 3:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        
                # Update display to keep window responsive
                pygame.display.flip()
            
            # Test volume control
            print("  Testing volume control (50%)...")
            pygame.mixer.music.set_volume(0.5)
            time.sleep(1)
            
            # Test pause/unpause
            print("  Testing pause functionality...")
            pygame.mixer.music.pause()
            time.sleep(1)
            pygame.mixer.music.unpause()
            time.sleep(1)
            
            # Stop the music
            pygame.mixer.music.stop()
            print(f"✓ {music_name} test completed successfully\n")
            
        except Exception as e:
            print(f"✗ Error with {music_name}: {e}\n")
    
    print("BGM testing completed.")
    pygame.quit()

if __name__ == "__main__":
    test_bgm()