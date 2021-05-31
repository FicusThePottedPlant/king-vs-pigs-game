import pygame

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
        self.is_flipped = False
        # run animation
        self.run_list = [pygame.image.load(f'data/sprites/run/{i}.png').convert_alpha() for i in range(1, 9)]
        self.run_list = [pygame.transform.scale(i, (i.get_width() * 3, i.get_height() * 3 - 4)) for i in self.run_list]
        from itertools import cycle
        self.run = cycle(self.run_list)

        # jump animation
        self.jump_list = [pygame.image.load(f'data/sprites/jump/{i}.png').convert_alpha() for i in range(1, 8)]
        self.jump_list = [pygame.transform.scale(i, (i.get_width() * 3, i.get_height() * 3)) for i in self.jump_list]
        self.jump = cycle(self.jump_list)

        self.image = self.jump_list[3]
        self.rect = pygame.Rect(x, y, self.image.get_width() - 5, self.image.get_height() - 5)

    def update(self, left: bool, right: bool, up: bool, plat: pygame.sprite.Group, spike: pygame.sprite.Group):
        """hero's behaviour and updates his position
        :param left - if were moved left
        :param right - if were moved right
        :param up - if were moved up
        :param plat - sprites and coordinates of the level
        :param spike - sprites and coordinates of the spikes"""
        from random import randint
        if left:
            self.xspeed = -SPEED
            if up and self.stay_ground:
                self.image = pygame.transform.flip(self.run_list[randint(0, 7)], 180, 0)
            elif self.stay_ground:
                self.image = pygame.transform.flip(next(self.run), 180, 0)
            elif not self.stay_ground:
                self.image = pygame.transform.flip(self.image, 180, 0) if not self.is_flipped else self.image
            self.is_flipped = True
        elif right:
            self.xspeed = SPEED
            if up and self.stay_ground:
                self.image = self.run_list[randint(0, 7)]
            elif self.stay_ground:
                self.image = next(self.run)
            elif not self.stay_ground:
                self.image = pygame.transform.flip(self.image, 180, 0) if self.is_flipped else self.image
            self.is_flipped = False
        else:
            if self.xspeed > 0:
                self.image = self.jump_list[1]
            elif self.xspeed < 0:
                self.image = pygame.transform.flip(self.jump_list[1], 180, 0)
            self.xspeed = 0
            self.is_flipped = False
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
        """handle colliding"""
        for s in spike:  # if player collides with sprite, teleport him into spawn
            if pygame.sprite.collide_mask(self, s):
                self.rect.x = self.x_start
                self.rect.y = self.y_start
        for p in plat:
            if pygame.sprite.collide_rect(self, p):
                # if hero collide with block, for example, his right coordinate will be the same coordinate as left of block
                if xspeed > 0:  # right colliding
                    self.rect.right = p.rect.left
                elif xspeed < 0:  # left colliding
                    self.rect.left = p.rect.right
                elif yspeed > 0:  # bottom colliding
                    self.rect.bottom = p.rect.top
                    self.stay_ground = True
                    self.yspeed = 0
                elif yspeed < 0:  # top colliding
                    self.rect.top = p.rect.bottom
                    self.yspeed = 2
