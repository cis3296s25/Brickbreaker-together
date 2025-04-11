import pygame
import os
import json
from settings import *
from ui_constants import (
    PRIMARY_COLOR, SECONDARY_COLOR, BACKGROUND_COLOR,
    UI_BACKGROUND, TEXT_COLOR, ACCENT_COLOR, PINK, TEAL,
    FloatingBrick
)


SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_settings.json')


DEFAULT_SETTINGS = {
    'music_volume': 0.5,
    'sound_volume': 0.5,
    'screen_width': 1440,
    'screen_height': 900,
    'fullscreen': True
}


SCREEN_SIZE_OPTIONS = [
    (1280, 720),  # 720p
    (1440, 900),  # default
    (1920, 1080)  # 1080p
]

class SettingsUI:
    def __init__(self, screen, return_callback=None):
        self.screen = screen
        self.return_callback = return_callback
        self.screen_width, self.screen_height = screen.get_size()
        

        self.settings = self.load_settings()
        self.audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
        try:
            button_click_path = os.path.join(self.audio_dir, 'button_click.wav')
            self.button_click_sound = pygame.mixer.Sound(button_click_path)
            self.button_click_sound.set_volume(self.settings['sound_volume'])
        except Exception as e:
            print(f"Could not load button click sound: {e}")
            self.button_click_sound = None
        
        # Fonts
        self.title_font = pygame.font.SysFont('Segoe UI', TITLE_FONT_SIZE, bold=True)
        self.label_font = pygame.font.SysFont('Segoe UI', LABEL_FONT_SIZE)
        self.small_font = pygame.font.SysFont('Segoe UI', SMALL_FONT_SIZE)
        
        # Settings items
        self.settings_items = [
            "Music Volume",
            "Sound Volume",
            "Screen Size",
            "Fullscreen",
            "Save and Return",
            "Cancel"
        ]
        
        self.selected_item = None
        
        self.current_size_index = self.get_current_size_index()
        

        self.floating_bricks = [FloatingBrick(self.screen_width, self.screen_height) for _ in range(5)]
        
        self.clock = pygame.time.Clock()
        

        self.dragging = None
    
    def get_current_size_index(self):
        """get_current_size_index"""
        current_size = (self.settings['screen_width'], self.settings['screen_height'])
        for i, size in enumerate(SCREEN_SIZE_OPTIONS):
            if size == current_size:
                return i
        return 1  
    
    def load_settings(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    return json.load(f)
            return DEFAULT_SETTINGS.copy()
        except Exception as e:
            print(f"Error loading settings: {e}")
            return DEFAULT_SETTINGS.copy()
    
    def save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def apply_settings(self):
        pygame.mixer.music.set_volume(self.settings['music_volume'])
        if self.button_click_sound:
            self.button_click_sound.set_volume(self.settings['sound_volume'])
        

        if self.settings['fullscreen']:
            self.screen = pygame.display.set_mode(
                (self.settings['screen_width'], self.settings['screen_height']),
                pygame.NOFRAME | pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode(
                (self.settings['screen_width'], self.settings['screen_height'])
            )
        
        global SCREEN_WIDTH, SCREEN_HEIGHT
        SCREEN_WIDTH = self.settings['screen_width']
        SCREEN_HEIGHT = self.settings['screen_height']
        

        init_screen_dimensions()
        

        self.floating_bricks = [FloatingBrick(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(5)]
        
        return self.screen
    
    def draw_background(self):
        self.screen.fill(BACKGROUND_COLOR)
        for brick in self.floating_bricks:
            brick.update()
            brick.draw(self.screen)
    
    def draw_title(self):
        text_surface = self.title_font.render('', True, PRIMARY_COLOR)
        text_rect = text_surface.get_rect(centerx=self.screen_width//2, centery=100)
        self.screen.blit(text_surface, text_rect)
    
    def draw_slider(self, y_pos, value, label, is_selected=False):
        slider_width = 400
        slider_height = 10
        slider_x = (self.screen_width - slider_width) // 2
        
        label_surface = self.label_font.render(label, True, TEXT_COLOR)
        label_rect = label_surface.get_rect(bottomleft=(slider_x, y_pos - 10))
        self.screen.blit(label_surface, label_rect)
        

        slider_rect = pygame.Rect(slider_x, y_pos, slider_width, slider_height)
        pygame.draw.rect(self.screen, (100, 100, 100), slider_rect, 0, 5)
        

        fill_width = int(slider_width * value)
        fill_rect = pygame.Rect(slider_x, y_pos, fill_width, slider_height)
        color = PRIMARY_COLOR if not is_selected else SECONDARY_COLOR
        pygame.draw.rect(self.screen, color, fill_rect, 0, 5)
        

        handle_x = slider_x + fill_width - 10
        handle_y = y_pos - 5
        handle_rect = pygame.Rect(handle_x, handle_y, 20, 20)
        pygame.draw.rect(self.screen, color, handle_rect, 0, 10)
        
        value_text = f"{int(value * 100)}%"
        value_surface = self.small_font.render(value_text, True, TEXT_COLOR)
        value_rect = value_surface.get_rect(midleft=(slider_x + slider_width + 20, y_pos + slider_height//2))
        self.screen.blit(value_surface, value_rect)
        
        return slider_rect, handle_rect
    
    def draw_toggle(self, y_pos, value, label, is_selected=False):

        toggle_width = 80
        toggle_height = 40
        toggle_x = (self.screen_width - toggle_width) // 2
        

        label_surface = self.label_font.render(label, True, TEXT_COLOR)
        label_rect = label_surface.get_rect(bottomleft=(toggle_x - 150, y_pos + toggle_height//2))
        self.screen.blit(label_surface, label_rect)
        

        toggle_rect = pygame.Rect(toggle_x, y_pos, toggle_width, toggle_height)
        bg_color = (100, 100, 100) if not value else (0, 200, 100)
        if is_selected:
            bg_color = SECONDARY_COLOR
        pygame.draw.rect(self.screen, bg_color, toggle_rect, 0, toggle_height//2)
        

        handle_x = toggle_x + 10 if not value else toggle_x + toggle_width - 30
        handle_rect = pygame.Rect(handle_x, y_pos + 5, 30, 30)
        pygame.draw.rect(self.screen, (255, 255, 255), handle_rect, 0, 15)
        

        status_text = "Start" if value else "Close"
        status_surface = self.small_font.render(status_text, True, TEXT_COLOR)
        status_rect = status_surface.get_rect(midleft=(toggle_x + toggle_width + 20, y_pos + toggle_height//2))
        self.screen.blit(status_surface, status_rect)
        
        return toggle_rect
        
    def draw_fullscreen_selector(self, y_pos, is_selected=False):
        selector_width = 400
        selector_height = 50
        selector_x = (self.screen_width - selector_width) // 2
        
        label_surface = self.label_font.render("Fullscreen", True, TEXT_COLOR)
        label_rect = label_surface.get_rect(bottomleft=(selector_x, y_pos - 10))
        self.screen.blit(label_surface, label_rect)
        
        selector_rect = pygame.Rect(selector_x, y_pos, selector_width, selector_height)
        pygame.draw.rect(self.screen, (50, 50, 50), selector_rect, 0, 10)
        if is_selected:
            pygame.draw.rect(self.screen, SECONDARY_COLOR, selector_rect, 2, 10)
        else:
            pygame.draw.rect(self.screen, PRIMARY_COLOR, selector_rect, 2, 10)
        
        left_arrow = "<"
        right_arrow = ">"
        left_surface = self.label_font.render(left_arrow, True, TEXT_COLOR)
        right_surface = self.label_font.render(right_arrow, True, TEXT_COLOR)
        
        left_rect = left_surface.get_rect(midleft=(selector_x + 20, y_pos + selector_height//2))
        right_rect = right_surface.get_rect(midright=(selector_x + selector_width - 20, y_pos + selector_height//2))
        
        self.screen.blit(left_surface, left_rect)
        self.screen.blit(right_surface, right_rect)
        
        display_mode = "Full Screen" if self.settings['fullscreen'] else "Window"
        mode_surface = self.label_font.render(display_mode, True, TEXT_COLOR)
        mode_rect = mode_surface.get_rect(center=(selector_x + selector_width//2, y_pos + selector_height//2))
        self.screen.blit(mode_surface, mode_rect)
        
        return selector_rect, left_rect, right_rect
    
    def draw_size_selector(self, y_pos, is_selected=False):
        selector_width = 400
        selector_height = 50
        selector_x = (self.screen_width - selector_width) // 2
        

        label_surface = self.label_font.render("ScreenSize", True, TEXT_COLOR)
        label_rect = label_surface.get_rect(bottomleft=(selector_x, y_pos - 10))
        self.screen.blit(label_surface, label_rect)
        

        selector_rect = pygame.Rect(selector_x, y_pos, selector_width, selector_height)
        pygame.draw.rect(self.screen, (50, 50, 50), selector_rect, 0, 10)
        if is_selected:
            pygame.draw.rect(self.screen, SECONDARY_COLOR, selector_rect, 2, 10)
        else:
            pygame.draw.rect(self.screen, PRIMARY_COLOR, selector_rect, 2, 10)
        

        left_arrow = "<"
        right_arrow = ">"
        left_surface = self.label_font.render(left_arrow, True, TEXT_COLOR)
        right_surface = self.label_font.render(right_arrow, True, TEXT_COLOR)
        
        left_rect = left_surface.get_rect(midleft=(selector_x + 20, y_pos + selector_height//2))
        right_rect = right_surface.get_rect(midright=(selector_x + selector_width - 20, y_pos + selector_height//2))
        
        self.screen.blit(left_surface, left_rect)
        self.screen.blit(right_surface, right_rect)
        

        current_size = SCREEN_SIZE_OPTIONS[self.current_size_index]
        size_text = f"{current_size[0]} x {current_size[1]}"
        size_surface = self.label_font.render(size_text, True, TEXT_COLOR)
        size_rect = size_surface.get_rect(center=(selector_x + selector_width//2, y_pos + selector_height//2))
        self.screen.blit(size_surface, size_rect)
        
        return selector_rect, left_rect, right_rect
    
    def draw_button(self, y_pos, text, is_selected=False):

        button_width = 300
        button_height = 60
        button_x = (self.screen_width - button_width) // 2
        
        button_rect = pygame.Rect(button_x, y_pos, button_width, button_height)
        

        if is_selected:
            pygame.draw.rect(self.screen, SECONDARY_COLOR, button_rect, 0, 10)
        else:
            pygame.draw.rect(self.screen, PRIMARY_COLOR, button_rect, 0, 10)
        

        text_surface = self.label_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return button_rect
    
    def draw_settings(self):

        start_y = 200
        spacing = 100
        

        music_slider_rect, music_handle_rect = self.draw_slider(
            start_y, 
            self.settings['music_volume'], 
            "Music Volume", 
            self.selected_item == "Music Volume"
        )
        

        sound_slider_rect, sound_handle_rect = self.draw_slider(
            start_y + spacing, 
            self.settings['sound_volume'], 
            "Sound Volume", 
            self.selected_item == "Sound Volume"
        )

        size_selector_rect, left_arrow_rect, right_arrow_rect = self.draw_size_selector(
            start_y + spacing * 2,
            self.selected_item == "Screen Size"
        )
        

        fullscreen_selector_rect, fullscreen_left_rect, fullscreen_right_rect = self.draw_fullscreen_selector(
            start_y + spacing * 3,
            self.selected_item == "Fullscreen"
        )
        

        save_button_rect = self.draw_button(
            start_y + spacing * 4, 
            "Save and Return", 
            self.selected_item == "Save and Return"
        )
        

        cancel_button_rect = self.draw_button(
            start_y + spacing * 5, 
            "Cancel", 
            self.selected_item == "Cancel"
        )
        
        return {
            "Music Volume": (music_slider_rect, music_handle_rect),
            "Sound Volume": (sound_slider_rect, sound_handle_rect),
            "Screen Size": (size_selector_rect, left_arrow_rect, right_arrow_rect),
            "Fullscreen": (fullscreen_selector_rect, fullscreen_left_rect, fullscreen_right_rect),
            "Save and Return": save_button_rect,
            "Cancel": cancel_button_rect
        }
    
    def handle_slider_click(self, pos, slider_rect, value_key):
        if slider_rect[0].collidepoint(pos) or slider_rect[1].collidepoint(pos):
            slider_x = slider_rect[0].x
            slider_width = slider_rect[0].width
            relative_x = max(0, min(pos[0] - slider_x, slider_width))
            new_value = relative_x / slider_width
            

            self.settings[value_key] = new_value
            

            self.dragging = value_key
            
            return True
        return False
    
    def handle_toggle_click(self, pos, toggle_rect, value_key):
        if toggle_rect.collidepoint(pos):

            self.settings[value_key] = not self.settings[value_key]
            
            if self.button_click_sound:
                self.button_click_sound.play()
            
            return True
        return False
    
    def handle_size_selector_click(self, pos, selector_rects):
        """Handle size selector click"""
        selector_rect, left_arrow_rect, right_arrow_rect = selector_rects
        
        if left_arrow_rect.collidepoint(pos):
            self.current_size_index = max(0, self.current_size_index - 1)
            new_size = SCREEN_SIZE_OPTIONS[self.current_size_index]
            self.settings['screen_width'] = new_size[0]
            self.settings['screen_height'] = new_size[1]
            
            if self.button_click_sound:
                self.button_click_sound.play()
            
            return True
        
        elif right_arrow_rect.collidepoint(pos):

            self.current_size_index = min(len(SCREEN_SIZE_OPTIONS) - 1, self.current_size_index + 1)
            new_size = SCREEN_SIZE_OPTIONS[self.current_size_index]
            self.settings['screen_width'] = new_size[0]
            self.settings['screen_height'] = new_size[1]
            

            if self.button_click_sound:
                self.button_click_sound.play()
            
            return True
        
        return False
        
    def handle_fullscreen_selector_click(self, pos, selector_rects):
        """Handle fullscreen selector click"""
        selector_rect, left_arrow_rect, right_arrow_rect = selector_rects
        
        if left_arrow_rect.collidepoint(pos) or right_arrow_rect.collidepoint(pos):

            self.settings['fullscreen'] = not self.settings['fullscreen']
            

            if self.button_click_sound:
                self.button_click_sound.play()
            
            return True
        
        return False
    
    def run(self):
        """Run settings interface"""
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Press ESC to return without saving settings
                        if self.return_callback:
                            return self.return_callback(self.screen)
                        return self.screen
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Get all control rectangles
                    control_rects = self.draw_settings()
                    
                    # Check which control was clicked
                    if self.handle_slider_click(mouse_pos, control_rects["Music Volume"], 'music_volume'):
                        self.selected_item = "Music Volume"
                    elif self.handle_slider_click(mouse_pos, control_rects["Sound Volume"], 'sound_volume'):
                        self.selected_item = "Sound Volume"
                    elif self.handle_size_selector_click(mouse_pos, control_rects["Screen Size"]):
                        self.selected_item = "Screen Size"
                    elif self.handle_fullscreen_selector_click(mouse_pos, control_rects["Fullscreen"]):
                        self.selected_item = "Fullscreen"
                    elif control_rects["Save and Return"].collidepoint(mouse_pos):
                        # Save settings and apply
                        if self.button_click_sound:
                            self.button_click_sound.play()
                        self.save_settings()
                        screen = self.apply_settings()
                        if self.return_callback:
                            return self.return_callback(screen)
                        return screen
                    elif control_rects["Cancel"].collidepoint(mouse_pos):
                        # Cancel and return
                        if self.button_click_sound:
                            self.button_click_sound.play()
                        if self.return_callback:
                            return self.return_callback(self.screen)
                        return self.screen
                
                if event.type == pygame.MOUSEBUTTONUP:
                    # Stop dragging
                    self.dragging = None
                
                if event.type == pygame.MOUSEMOTION and self.dragging:
                    # Handle slider dragging
                    slider_rect = self.draw_settings()["Music Volume" if self.dragging == 'music_volume' else "Sound Volume"][0]
                    slider_x = slider_rect.x
                    slider_width = slider_rect.width
                    relative_x = max(0, min(mouse_pos[0] - slider_x, slider_width))
                    new_value = relative_x / slider_width
                    
                    # Update settings
                    self.settings[self.dragging] = new_value
                    
                    # If it's a volume setting, apply immediately
                    if self.dragging == 'music_volume':
                        pygame.mixer.music.set_volume(new_value)
                    elif self.dragging == 'sound_volume' and self.button_click_sound:
                        self.button_click_sound.set_volume(new_value)
            

            self.draw_background()
            self.draw_title()
            self.draw_settings()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        return self.screen