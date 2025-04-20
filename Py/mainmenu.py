import pygame
import sys
import os
import subprocess
from game import Game
from settings import *

# UI constants
from ui_constants import (
    PRIMARY_COLOR, SECONDARY_COLOR, BACKGROUND_COLOR,
    UI_BACKGROUND, TEXT_COLOR, ACCENT_COLOR, PINK, TEAL,
    FloatingBrick
)
from settings_ui import SettingsUI
import online_multiplayer_client as omc

# Initialize Pygame modules
pygame.init()
pygame.font.init()
pygame.mixer.init()
init_screen_dimensions()

class BrickBreakerMenu:
    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = SCREEN_WIDTH, SCREEN_HEIGHT
        pygame.display.set_caption("BrickBreaker Together")

        # Audio directory
        base = os.path.dirname(os.path.abspath(__file__))
        self.audio_dir = os.path.join(base, 'audio')
        # Load click sound
        try:
            click = pygame.mixer.Sound(os.path.join(self.audio_dir, 'button_click.wav'))
            click.set_volume(0.5)
            self.click_sound = click
        except:
            self.click_sound = None
        # Music
        try:
            pygame.mixer.music.load(os.path.join(self.audio_dir, 'background_music.mp3'))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except:
            pass

        # Fonts
        self.title_font   = pygame.font.SysFont('Segoe UI', TITLE_FONT_SIZE, bold=True)
        self.tagline_font = pygame.font.SysFont('Segoe UI', SMALL_FONT_SIZE)
        self.menu_font    = pygame.font.SysFont('Segoe UI', LABEL_FONT_SIZE)

        # Menus
        self.menu_items   = ["Login/Sign Up","Single Player","Multiple Player","Settings","How to Play","Quit"]
        self.menu_colors  = [PINK, PRIMARY_COLOR, SECONDARY_COLOR, (243,156,18), (52,152,219), ACCENT_COLOR]
        self.mult_items   = ["Local Multiplayer","Online Multiplayer","Back"]
        self.mult_colors  = [PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR]
        self.online_items = ["Host","Join","Back"]
        self.online_colors= [PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR]

        # UI state
        self.show_mult = False
        self.show_online = False
        self.show_enter = False
        self.enter_text = ""
        self.current_user = None
        self.bricks = [FloatingBrick(self.w,self.h) for _ in range(5)]
        self.clock = pygame.time.Clock()
        self.hover=0; self.dir=1; self.sel=None

    def draw_bg(self):
        self.screen.fill(BACKGROUND_COLOR)
        for b in self.bricks:
            b.update(); b.draw(self.screen)

    def draw_title(self):
        t = self.title_font.render("BRICKBREAKER",True,PRIMARY_COLOR)
        g = self.tagline_font.render("TOGETHER",True,TEXT_COLOR)
        tr = t.get_rect(center=(self.w//2,100))
        gr = g.get_rect(center=(self.w//2,tr.bottom+20))
        self.screen.blit(t,tr); self.screen.blit(g,gr)

    def draw_buttons(self, items, colors, start_y=250):
        w,item_h=500,70; x=(self.w-w)//2
        # hover pulse
        self.hover+=5*self.dir
        if self.hover>=100: self.dir=-1
        if self.hover<=0: self.dir=1
        for i,(txt,col) in enumerate(zip(items,colors)):
            r=pygame.Rect(x,start_y+i*(item_h+20),w,item_h)
            s=pygame.Surface((w,item_h),pygame.SRCALPHA)
            s.fill((*col[:3],50+self.hover) if i==self.sel else UI_BACKGROUND)
            self.screen.blit(s,r)
            bc=(*col[:3],100) if i==self.sel else col
            pygame.draw.rect(self.screen,bc,r,4,border_radius=5)
            tc=col if i==self.sel else TEXT_COLOR
            ts=self.menu_font.render(txt,True,tc)
            tr=ts.get_rect(midleft=(r.left+20,r.centery))
            self.screen.blit(ts,tr)

    def draw_main(self):
        if self.current_user:
            self.menu_items[0]=self.current_user.capitalize(); self.menu_colors[0]=TEAL
        else:
            self.menu_items[0]="Login/Sign Up"; self.menu_colors[0]=PINK
        self.draw_buttons(self.menu_items,self.menu_colors)

    def draw(self):
        if self.show_enter:
            prompt=self.menu_font.render("Enter host username:",True,TEXT_COLOR)
            inp=self.menu_font.render(self.enter_text+"|",True,PRIMARY_COLOR)
            pr=prompt.get_rect(center=(self.w//2,self.h//2-40))
            ir=inp.get_rect(midtop=(self.w//2-100,self.h//2))
            self.screen.blit(prompt,pr); self.screen.blit(inp,ir)
        elif self.show_online:
            self.draw_buttons(self.online_items,self.online_colors)
        elif self.show_mult:
            self.draw_buttons(self.mult_items,self.mult_colors)
        else:
            self.draw_main()

    def open_login(self):
        from login import LoginScreen
        u=LoginScreen(self.screen).run()
        if u and u!="BACK_TO_MENU": self.current_user=u

    def run(self):
        running=True
        while running:
            pos=pygame.mouse.get_pos()
            for e in pygame.event.get():
                if e.type==pygame.QUIT: pygame.quit();sys.exit()
                if e.type==pygame.KEYDOWN:
                    if self.show_enter:
                        if e.key==pygame.K_RETURN and self.enter_text:
                            room=self.enter_text.strip()
                            omc.client_main(room,self.current_user)
                            return
                        elif e.key==pygame.K_BACKSPACE:
                            self.enter_text=self.enter_text[:-1]
                        else:
                            self.enter_text+=e.unicode
                    elif e.key==pygame.K_ESCAPE:
                        pygame.quit();sys.exit()
                if e.type==pygame.MOUSEMOTION:
                    self.sel=None
                    arr=(self.enter_text and []) or (
                        self.online_items if self.show_online else
                        self.mult_items if self.show_mult else
                        self.menu_items)
                    for i in range(len(arr)):
                        r=pygame.Rect((self.w-500)//2,250+i*(70+20),500,70)
                        if r.collidepoint(pos): self.sel=i;break
                if e.type==pygame.MOUSEBUTTONDOWN and not self.show_enter:
                    if self.show_online:
                        it=self.online_items[self.sel]
                        if it=="Host":
                            if not self.current_user: self.open_login()
                            if self.current_user:
                                omc.client_main(self.current_user,self.current_user)
                                return
                        elif it=="Join":
                            if not self.current_user: self.open_login()
                            if self.current_user:
                                self.show_enter=True; self.enter_text=""
                        else: self.show_online=False
                    elif self.show_mult:
                        it=self.mult_items[self.sel]
                        if it=="Local Multiplayer":
                            from MultiplayerGame import run_game; run_game(self.screen)
                        elif it=="Online Multiplayer":
                            self.show_online=True
                        else: self.show_mult=False
                    else:
                        it=self.menu_items[self.sel]
                        if self.click_sound: self.click_sound.play()
                        if it=="Login/Sign Up": self.open_login()
                        elif it=="Single Player":
                            pygame.mixer.music.stop();Game(self.screen).run()
                        elif it=="Multiple Player": self.show_mult=True
                        elif it=="Settings":
                            ui=SettingsUI(self.screen,return_callback=lambda s:s);self.screen=ui.run()
                        elif it=="How to Play":
                            from How import HowToPlayScreen;HowToPlayScreen(self.screen).run()
                        else: running=False

            self.draw_bg();self.draw_title();self.draw();pygame.display.flip();self.clock.tick(60)
        pygame.quit();sys.exit()
