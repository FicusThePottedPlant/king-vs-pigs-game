import ctypes
import os
from itertools import cycle
import pygame

user32 = ctypes.windll.user32  # get user monitor size
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
width, height = screensize
SPEED = 10
JUMP = 16
GRAVITY = 1


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xspeed = 0
        self.yspeed = 7
        self.x_start = x
        self.y_start = y
        self.stay_ground = False
        self.run_list = [pygame.image.load(f'data/sprites/run/{i}.png').convert_alpha() for i in range(1, 9)]
        self.run_list = [pygame.transform.scale(i, (i.get_width() * 3, i.get_height() * 3 - 4)) for i in self.run_list]
        self.run = cycle(self.run_list)
        self.image = next(self.run)

        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.jump_list = [pygame.image.load(f'data/sprites/jump/{i}.png').convert_alpha() for i in range(1, 8)]
        self.jump_list = [pygame.transform.scale(i, (i.get_width() * 3, i.get_height() * 3)) for i in self.jump_list]
        self.jump = cycle(self.jump_list)

    def update(self, left: bool, right: bool, up: bool, plat: pygame.sprite.Group, spike: pygame.sprite.Group):
        if left:
            self.xspeed = -SPEED
            if up:
                self.image = pygame.transform.flip(self.run_list[5], 180, 0)
            elif left and self.stay_ground:
                self.image = pygame.transform.flip(next(self.run), 180, 0)
        elif right:
            self.xspeed = SPEED
            if up:
                self.image = self.run_list[5]
            elif right and self.stay_ground:
                self.image = next(self.run)

        else:
            self.xspeed = 0
            self.image = self.jump_list[1]
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
