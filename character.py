import ctypes
import os

import pygame

user32 = ctypes.windll.user32  # get user monitor size
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
width, height = screensize
SPEED = 10
JUMP = 16
GRAVITY = 1
pack = os.path.dirname(__file__)
image_folder = os.path.join(pack, 'Sprites')


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xspeed = 0
        self.yspeed = 7
        self.x_start = x
        self.y_start = y
        self.stay_ground = False

        self.image = pygame.image.load(f'{image_folder}/03-Pig/Fall (34x28).png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def update(self, left: bool, right: bool, up: bool, plat: pygame.sprite.Group, spike: pygame.sprite.Group):
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
        self.collision(0, self.yspeed, plat, spike)
        self.rect.x += self.xspeed
        self.collision(self.xspeed, 0, plat, spike)

    def collision(self, xspeed, yspeed, plat, spike):
        for s in spike:
            if pygame.sprite.collide_mask(self, s):
                self.rect.x = self.x_start
                self.rect.y = self.y_start
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
