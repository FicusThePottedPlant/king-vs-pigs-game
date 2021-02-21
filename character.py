import pygame
import os
import ctypes
user32 = ctypes.windll.user32  # get user monitor size
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# screensize = 900, 600
size = width, height = screensize
MAIN_WIDTH = width
MAIN_HEIGHT = height
SPEED = 7
COLOR_CHARACTER = 'black'

WIDTH_CHARACTER = 15
HEIGHT_CHARACTER = 20
JUMP = 8.5
GRAVITY = 0.3
pack = os.path.dirname(__file__)
image_folder = os.path.join(pack, 'Sprites')


class Char(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.l = False
        self.xspeed = 0
        self.yspeed = 7
        self.x_start = pos[0]
        self.y_start = pos[1]
        self.stay_ground = False
        self.image = pygame.Surface((WIDTH_CHARACTER, HEIGHT_CHARACTER))
        self.image.fill(pygame.Color(COLOR_CHARACTER))
        self.image = pygame.image.load(f'{image_folder}/03-Pig/Fall (34x28).png').convert()
        self.r = self.image.get_rect()
        self.rect = pygame.Rect(pos[0], pos[1], self.r.width, self.r.height)

    def update(self, left, right, up,plat):
        if left:
            self.xspeed = -SPEED
        elif right:
            self.xspeed = SPEED
        else:
            self.xspeed = 0
        if up:
            if self.stay_ground:
                self.yspeed = -JUMP
        if not self.stay_ground:
            self.yspeed += GRAVITY
        self.stay_ground = False
        self.rect.y += self.yspeed
        self.collision(0, self.yspeed, plat)
        self.rect.x += self.xspeed
        self.collision(self.xspeed, 0, plat)

    def collision(self, xspeed, yspeed, plat):
        for p in plat:
            if pygame.sprite.collide_rect(self, p):
                if xspeed > 0:
                    self.rect.right = p.rect.left
                elif xspeed < 0:
                    self.rect.left = p.rect.right
                elif yspeed > 0:
                    self.rect.bottom = p.rect.top
                    self.stay_ground = True
                    self.yspeed = 0
                elif yspeed < 0:
                    self.rect.top = p.rect.bottom
                    self.yspeed = 2
