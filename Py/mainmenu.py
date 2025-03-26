import pygame
import sys
import random
from game import Game

# Initialize Pygame
pygame.init()
pygame.font.init()

# Screen Dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

# Colors
PRIMARY_COLOR = (52, 152, 219)
SECONDARY_COLOR = (46, 204, 113)
BACKGROUND_COLOR = (18, 18, 18)
UI_BACKGROUND = (18, 18, 18, 215)
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (231, 76, 60)

class FloatingBrick:
    def __init__(self, screen_width, screen_height):
        self.width = 60
        self.height = 20
        self.x = random.randint(0, screen_width - self.width)
        self.y = screen_height
        self.color = random.choice([
            PRIMARY_COLOR, 
            SECONDARY_COLOR, 
            ACCENT_COLOR, 
            (243, 156, 18)  # Orange color
        ])
        self.speed = random.uniform(0.5, 2)
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)

    def update(self):
        self.y -= self.speed
        self.rotation += self.rotation_speed
        if self.y < -self.height:
            self.y = pygame.display.get_surface().get_height()
            self.x = random.randint(0, pygame.display.get_surface().get_width() - self.width)

    def draw(self, screen):
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surf.fill(self.color + (25,))  # Low opacity
        rotated_surf = pygame.transform.rotate(surf, self.rotation)
        screen.blit(rotated_surf, (self.x, self.y))

class BrickBreakerMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("BrickBreaker Together")
        
        # Fonts
        self.title_font = pygame.font.SysFont('Segoe UI', 80, bold=True)
        self.tagline_font = pygame.font.SysFont('Segoe UI', 24)
        self.menu_font = pygame.font.SysFont('Segoe UI', 32)
        
        # Menu items
        self.menu_items = [
            "Single Player",
            "Multiple Player", 
            "Settings", 
            "Quit"
        ]
        
        # Colors for menu item borders
        self.menu_colors = [
            PRIMARY_COLOR, 
            SECONDARY_COLOR, 
            (243, 156, 18),  # Orange
            ACCENT_COLOR
        ]
        
        # Floating bricks
        self.floating_bricks = [FloatingBrick(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(5)]
        
        self.clock = pygame.time.Clock()
        self.hovered_item = None
        self.hover_alpha = 0
        self.hover_alpha_direction = 1

    def draw_background(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw floating bricks
        for brick in self.floating_bricks:
            brick.update()
            brick.draw(self.screen)

    def draw_title(self):
        # Gradient text effect
        text_surface = self.title_font.render('BRICKBREAKER', True, PRIMARY_COLOR)
        tagline_surface = self.tagline_font.render('TOGETHER', True, TEXT_COLOR)
        
        text_rect = text_surface.get_rect(centerx=SCREEN_WIDTH//2, centery=100)
        tagline_rect = tagline_surface.get_rect(centerx=SCREEN_WIDTH//2, top=text_rect.bottom + 10)
        
        self.screen.blit(text_surface, text_rect)
        self.screen.blit(tagline_surface, tagline_rect)

    def draw_menu(self):
        menu_width = 500
        menu_start_y = 250
        menu_item_height = 70
        
        # Update hover animation
        self.hover_alpha += 5 * self.hover_alpha_direction
        if self.hover_alpha >= 100:
            self.hover_alpha_direction = -1
        elif self.hover_alpha <= 0:
            self.hover_alpha_direction = 1
        
        for i, item in enumerate(self.menu_items):
            # Menu item background
            menu_rect = pygame.Rect(
                (SCREEN_WIDTH - menu_width) // 2, 
                menu_start_y + i * (menu_item_height + 20), 
                menu_width, 
                menu_item_height
            )
            
            # Semi-transparent background
            s = pygame.Surface((menu_width, menu_item_height), pygame.SRCALPHA)
            if i == self.hovered_item:
                hover_color = (*self.menu_colors[i][:3], 50 + self.hover_alpha)
                s.fill(hover_color)
            else:
                s.fill(UI_BACKGROUND)
            self.screen.blit(s, menu_rect)
            
            # Border with glow effect for hovered item
            border_color = self.menu_colors[i]
            if i == self.hovered_item:
                # Draw multiple lines for glow effect
                for offset in range(4):
                    pygame.draw.line(
                        self.screen,
                        (*border_color[:3], 100 - offset * 25),
                        (menu_rect.left - offset, menu_rect.top),
                        (menu_rect.left - offset, menu_rect.bottom),
                        2
                    )
            else:
                pygame.draw.line(
                    self.screen,
                    border_color,
                    (menu_rect.left, menu_rect.top),
                    (menu_rect.left, menu_rect.bottom),
                    4
                )
            
            # Text with color change on hover
            text_color = self.menu_colors[i] if i == self.hovered_item else TEXT_COLOR
            text_surface = self.menu_font.render(item, True, text_color)
            text_rect = text_surface.get_rect(midleft=(menu_rect.left + 20, menu_rect.centery))
            self.screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    menu_width = 500
                    menu_start_y = 250
                    menu_item_height = 70
                    
                    self.hovered_item = None
                    for i, item in enumerate(self.menu_items):
                        menu_rect = pygame.Rect(
                            (SCREEN_WIDTH - menu_width) // 2,
                            menu_start_y + i * (menu_item_height + 20),
                            menu_width,
                            menu_item_height
                        )
                        if menu_rect.collidepoint(mouse_pos):
                            self.hovered_item = i
                            break
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    menu_width = 500
                    menu_start_y = 250
                    menu_item_height = 70
                    
                    for i, item in enumerate(self.menu_items):
                        menu_rect = pygame.Rect(
                            (SCREEN_WIDTH - menu_width) // 2,
                            menu_start_y + i * (menu_item_height + 20),
                            menu_width,
                            menu_item_height
                        )
                        
                        if menu_rect.collidepoint(mouse_pos):
                            if item == "Single Player":
                                game = Game(self.screen)
                                game.run()
                                running = False
                            elif item == "Quit":
                                running = False

            # Draw everything
            self.draw_background()
            self.draw_title()
            self.draw_menu()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

