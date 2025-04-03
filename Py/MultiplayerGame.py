import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Get screen info for fullscreen
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
UI_WIDTH = int(SCREEN_WIDTH * 0.15)
GAME_WIDTH = int(SCREEN_WIDTH * 0.65)
GAME_HEIGHT = int(SCREEN_HEIGHT * 0.75)

# Colors and constants
BACKGROUND_COLOR = (18, 18, 18)
PLAYER1_COLOR = (52, 152, 219)
PLAYER2_COLOR = (231, 76, 60)
TEXT_COLOR = (255, 255, 255)
BRICK_COLORS = [
    (230, 245, 255), (198, 231, 250), (166, 212, 245), (135, 191, 235),
    (104, 165, 222), (73, 140, 208), (44, 115, 194), (28, 98, 173),
    (19, 79, 149), (12, 61, 123)
]
FPS = 60
PADDLE_WIDTH = int(150)
PADDLE_HEIGHT = int(10)
BALL_RADIUS = int(8)
BRICK_WIDTH = int(54)
BRICK_HEIGHT = int(20)
BRICK_ROWS = 10
BRICK_COLS = 15
BRICK_PADDING = int(8)
BALL_SPEED = 5
PADDLE_SPEED = 8
LIVES = 3

font_size_scale = min(SCREEN_WIDTH / 1920, SCREEN_HEIGHT / 1080)
title_font = pygame.font.SysFont('Arial', int(62 * font_size_scale), bold=True)
label_font = pygame.font.SysFont('Arial', int(40 * font_size_scale), bold=True)
score_font = pygame.font.SysFont('Arial', int(50 * font_size_scale), bold=True)
small_font = pygame.font.SysFont('Arial', int(32 * font_size_scale))
countdown_font = pygame.font.SysFont('Arial', int(150 * font_size_scale), bold=True)  # 添加倒计时字体

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("BRICKBREAKER TOGETHER")
clock = pygame.time.Clock()

class Paddle:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color
        self.speed = PADDLE_SPEED
        self.score = 0

    def move(self, direction, bounds):
        if direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed
        self.rect.clamp_ip(bounds)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, self.color, self.rect.inflate(4, 4), border_radius=12, width=2)

class Ball:
    def __init__(self, x, y, color, vx, vy, game):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = BALL_RADIUS
        self.color = color
        self.active = True
        self.game = game  # <-- store reference to game instance

    def move(self, speed_modifier=1.0):
        if self.active:
            self.x += self.vx * speed_modifier
            self.y += self.vy * speed_modifier

    @property
    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius+4, width=2)

    def check_collision(self, bounds, top_paddle, bottom_paddle, bricks, is_top):
        # wall
        if self.x - self.radius <= bounds.left or self.x + self.radius >= bounds.right:
            self.vx *= -1
        # top or bottom wall
        if self.y - self.radius <= bounds.top:
            return "hit_top"
        if self.y + self.radius >= bounds.bottom:
            return "hit_bottom"
        # paddle
        if self.rect.colliderect(top_paddle.rect):
            self.vy = abs(self.vy)
            return "paddle"
        if self.rect.colliderect(bottom_paddle.rect):
            self.vy = -abs(self.vy)
            return "paddle"
        # bricks
        for brick in bricks:
            if brick['active'] and self.rect.colliderect(brick['rect']):
                brick['active'] = False
                self.vy *= -1

                if random.random() < 0.2:  # 20% chance to drop power-up
                    self.game.powerups.append(PowerUp(brick['rect'].centerx, brick['rect'].centery))

                return "brick"
            
class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 15, y - 15, 30, 30)
        self.type = random.choice(['slow_ball', 'extra_life'])
        self.speed = 3

        self.color_map = {
            'slow_ball': (241, 196, 15),  # Yellow
            'extra_life': (46, 204, 113), # Green
        }

        self.label_map = {
            'slow_ball': 'S',
            'extra_life': '+',
        }

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color_map[self.type], self.rect)
        font = pygame.font.Font(None, 24)
        text = font.render(self.label_map[self.type], True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def apply(self, game, player):
        if self.type == 'slow_ball':
            if player == 1:
                game.speed_modifier_p1 = 0.8
                game.slow_until_p1 = pygame.time.get_ticks() + 3000
            elif player == 2:
                game.speed_modifier_p2 = 0.8
                game.slow_until_p2 = pygame.time.get_ticks() + 3000
        elif self.type == 'extra_life':
            if player == 1:
                game.lives1 = min(game.lives1 + 1, LIVES)
            elif player == 2:
                game.lives2 = min(game.lives2 + 1, LIVES)

class Game:
    def __init__(self):
        self.bounds = pygame.Rect((SCREEN_WIDTH - GAME_WIDTH)//2, (SCREEN_HEIGHT - GAME_HEIGHT)//2, GAME_WIDTH, GAME_HEIGHT)
        self.player1 = Paddle(self.bounds.centerx - PADDLE_WIDTH//2, self.bounds.top + 20, PLAYER1_COLOR)
        self.player2 = Paddle(self.bounds.centerx - PADDLE_WIDTH//2, self.bounds.bottom - 20 - PADDLE_HEIGHT, PLAYER2_COLOR)
        self.ball1 = Ball(self.bounds.centerx, self.bounds.top + 60, PLAYER1_COLOR, random.choice([-1,1])*BALL_SPEED/2, BALL_SPEED, self)
        self.ball2 = Ball(self.bounds.centerx, self.bounds.bottom - 60, PLAYER2_COLOR, random.choice([-1,1])*BALL_SPEED/2, -BALL_SPEED, self)
        self.bricks = []
        self.create_bricks()
        self.lives1 = LIVES
        self.lives2 = LIVES
        self.winner = None
        self.speed_modifier_p1 = 1.0
        self.speed_modifier_p2 = 1.0
        self.slow_until_p1 = 0
        self.slow_until_p2 = 0
        self.powerups = []
        self.ball1 = Ball(self.bounds.centerx, self.bounds.top + 60, PLAYER1_COLOR, random.choice([-1,1])*BALL_SPEED/2, BALL_SPEED, self)
        self.ball2 = Ball(self.bounds.centerx, self.bounds.bottom - 60, PLAYER2_COLOR, random.choice([-1,1])*BALL_SPEED/2, -BALL_SPEED, self)


        self.countdown = 3
        self.countdown_timer = pygame.time.get_ticks()
        self.countdown_interval = 1000  # 1sec
        self.game_started = False
        self.animation_scale = 0.1  
        self.animation_speed = 0.05 
        
    def create_bricks(self):
        area_width = BRICK_COLS * (BRICK_WIDTH + BRICK_PADDING) - BRICK_PADDING
        sx = self.bounds.centerx - area_width // 2
        sy = self.bounds.centery - (BRICK_ROWS * (BRICK_HEIGHT + BRICK_PADDING)) // 2
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                rect = pygame.Rect(
                    sx + col * (BRICK_WIDTH + BRICK_PADDING),
                    sy + row * (BRICK_HEIGHT + BRICK_PADDING),
                    BRICK_WIDTH,
                    BRICK_HEIGHT
                )
                self.bricks.append({'rect': rect, 'active': True, 'color': BRICK_COLORS[row % len(BRICK_COLORS)]})

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.player1.move("left", self.bounds)
        if keys[pygame.K_d]: self.player1.move("right", self.bounds)
        if keys[pygame.K_LEFT]: self.player2.move("left", self.bounds)
        if keys[pygame.K_RIGHT]: self.player2.move("right", self.bounds)
        if keys[pygame.K_r] and self.winner:
            self.__init__()

    def update(self):
        current_time = pygame.time.get_ticks()

        if not self.game_started:
            if current_time - self.countdown_timer >= self.countdown_interval:
                self.countdown -= 1
                self.countdown_timer = current_time
                self.animation_scale = 0.1

                if self.countdown <= 0:
                    self.game_started = True

            if self.animation_scale < 1.0:
                self.animation_scale += self.animation_speed
            return

        if self.winner:
            return

        # Move balls with speed modifiers
        self.ball1.move(self.speed_modifier_p1)
        self.ball2.move(self.speed_modifier_p2)

        # Update power-ups
        for powerup in self.powerups[:]:
            powerup.update()

            if powerup.rect.colliderect(self.player1.rect):
                powerup.apply(self, player=1)
                self.powerups.remove(powerup)
            elif powerup.rect.colliderect(self.player2.rect):
                powerup.apply(self, player=2)
                self.powerups.remove(powerup)
            elif powerup.rect.top > self.bounds.bottom:
                self.powerups.remove(powerup)

        # Reset speed modifiers after duration
        if self.speed_modifier_p1 < 1.0 and current_time > self.slow_until_p1:
            self.speed_modifier_p1 = 1.0

        if self.speed_modifier_p2 < 1.0 and current_time > self.slow_until_p2:
            self.speed_modifier_p2 = 1.0

        # Ball 1 collision logic
        if self.ball1.active:
            result = self.ball1.check_collision(self.bounds, self.player1, self.player2, self.bricks, True)
            if result == "hit_top":
                self.ball1.active = False
                self.lives1 -= 1
            elif result == "hit_bottom":
                self.ball1.active = False
                self.lives2 -= 1
            elif result == "brick":
                self.player1.score += 10

        # Ball 2 collision logic
        if self.ball2.active:
            result = self.ball2.check_collision(self.bounds, self.player1, self.player2, self.bricks, False)
            if result == "hit_bottom":
                self.ball2.active = False
                self.lives2 -= 1
            elif result == "hit_top":
                self.ball2.active = False
                self.lives1 -= 1
            elif result == "brick":
                self.player2.score += 10

        # Respawn balls if inactive and lives remain
        if not self.ball1.active and self.lives1 > 0:
            self.ball1 = Ball(self.bounds.centerx, self.bounds.top + 60, PLAYER1_COLOR, random.choice([-1, 1]) * BALL_SPEED / 2, BALL_SPEED, self)

        if not self.ball2.active and self.lives2 > 0:
            self.ball2 = Ball(self.bounds.centerx, self.bounds.bottom - 60, PLAYER2_COLOR, random.choice([-1, 1]) * BALL_SPEED / 2, -BALL_SPEED, self)

        # Determine the winner
        # Respawn balls only if inactive and player still has lives
        if not self.ball1.active and self.lives1 > 0:
            self.ball1 = Ball(self.bounds.centerx, self.bounds.top + 60, PLAYER1_COLOR, random.choice([-1, 1]) * BALL_SPEED / 2, BALL_SPEED, self)

        if not self.ball2.active and self.lives2 > 0:
            self.ball2 = Ball(self.bounds.centerx, self.bounds.bottom - 60, PLAYER2_COLOR, random.choice([-1, 1]) * BALL_SPEED / 2, -BALL_SPEED, self)

        # Once a player's lives reach zero, stop spawning their ball
        if self.lives1 <= 0:
            self.ball1.active = False

        if self.lives2 <= 0:
            self.ball2.active = False

        # Determine winner only when both players lost all lives
        if self.lives1 <= 0 and self.lives2 <= 0:
            if self.player1.score > self.player2.score:
                self.winner = "PLAYER 1 WINS"
            elif self.player2.score > self.player1.score:
                self.winner = "PLAYER 2 WINS"
            else:
                self.winner = "DRAW"


    def draw_ui(self):
        # UI panels
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(0, 0, UI_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(SCREEN_WIDTH - UI_WIDTH, 0, UI_WIDTH, SCREEN_HEIGHT))
        pygame.draw.line(screen, PLAYER1_COLOR, (0, 2), (UI_WIDTH, 2), 4)
        pygame.draw.line(screen, PLAYER2_COLOR, (SCREEN_WIDTH - UI_WIDTH, 2), (SCREEN_WIDTH, 2), 4)

        # Title
        title = title_font.render("BRICKBREAKER", True, TEXT_COLOR)
        sub = small_font.render("TOGETHER", True, (180, 180, 180))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))
        screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, 70))

        # Player stats
        def draw_stats(x, y, label, color, score, lives):
            lbl = label_font.render(label, True, color)
            val = score_font.render(f"{score:04d}", True, TEXT_COLOR)
            screen.blit(lbl, (x - lbl.get_width()//2, y))
            screen.blit(val, (x - val.get_width()//2, y + 40))
            for i in range(LIVES):
                clr = color if i < lives else (50, 50, 50)
                pygame.draw.circle(screen, clr, (x - 35 + i * 35, y + 120), 12)

        draw_stats(UI_WIDTH//2, SCREEN_HEIGHT//3, "PLAYER 1", PLAYER1_COLOR, self.player1.score, self.lives1)
        draw_stats(SCREEN_WIDTH - UI_WIDTH//2, SCREEN_HEIGHT//3, "PLAYER 2", PLAYER2_COLOR, self.player2.score, self.lives2)

    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        self.draw_ui()
        pygame.draw.rect(screen, (0, 0, 0), self.bounds, border_radius=12)
        pygame.draw.rect(screen, (40, 40, 40), self.bounds, border_radius=12, width=2)

        self.player1.draw()
        self.player2.draw()
        if self.ball1.active: self.ball1.draw()
        if self.ball2.active: self.ball2.draw()

        for powerup in self.powerups:
            powerup.draw(screen)

        for brick in self.bricks:
            if brick['active']:
                pygame.draw.rect(screen, brick['color'], brick['rect'], border_radius=4)
                pygame.draw.rect(screen, tuple(max(0, c - 40) for c in brick['color']), brick['rect'].inflate(-10, -10), border_radius=2)

        # draw countdown
        if not self.game_started and self.countdown > 0:
            # draw overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            # draw countdown number
            countdown_text = countdown_font.render(str(self.countdown), True, TEXT_COLOR)
            # calculate scaled size
            scaled_width = int(countdown_text.get_width() * self.animation_scale)
            scaled_height = int(countdown_text.get_height() * self.animation_scale)
            # only draw if scaled size is valid
            if scaled_width > 0 and scaled_height > 0:
                scaled_text = pygame.transform.scale(countdown_text, (scaled_width, scaled_height))
                screen.blit(scaled_text, (SCREEN_WIDTH//2 - scaled_width//2, SCREEN_HEIGHT//2 - scaled_height//2))
            

        if self.winner:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            msg = title_font.render("GAME OVER", True, TEXT_COLOR)
            win = score_font.render(self.winner, True, TEXT_COLOR)
            tip = small_font.render("Press R to restart", True, TEXT_COLOR)
            screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, SCREEN_HEIGHT//2 - 60))
            screen.blit(win, (SCREEN_WIDTH//2 - win.get_width()//2, SCREEN_HEIGHT//2))
            screen.blit(tip, (SCREEN_WIDTH//2 - tip.get_width()//2, SCREEN_HEIGHT//2 + 60))

        pygame.display.flip()

def main():
    game = Game()
    while True:
        game.handle_input()
        game.update()
        game.draw()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
