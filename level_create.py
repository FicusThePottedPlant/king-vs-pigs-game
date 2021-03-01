import pygame
import os
import pytmx
import ctypes
import hero

user32 = ctypes.windll.user32  # get user monitor size
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# screensize = 900, 600
size = WIDTH, HEIGHT = screensize[0] - 100, screensize[1] - 100
screen = pygame.display.set_mode(screensize)
self_path = os.path.dirname(__file__)
maps = os.path.join(self_path, 'data')

borders = [5, 8, *range(12, 23), *range(32, 44), *range(50, 55), 64, 67, 68, *range(77, 89), 99, 100, *range(108, 122),
           131, 132, 152, 153, 161, 162,
           *range(168, 171), *range(196, 202), *range(228, 235), *range(256, 260), *range(288, 292), *range(320, 324)]
final = [425, 426, 458, 459]
platforms = pygame.sprite.Group()
main_sprite_group = pygame.sprite.Group()
background_sprite_group = pygame.sprite.Group()

WIDTH_CHARACTER = 34
HEIGHT_CHARACTER = 28
level_width = 64 * 16
level_height = 64 * 16
som = True
h = pygame.Surface((64, 64))
h.fill(pygame.Color((255, 0, 0)))


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(width, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIDTH / 2, -t + HEIGHT / 2
    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIDTH), l)  # Не движемся дальше правой границы
    t = min(0, t)  # Не движемся дальше верхней границы
    t = max(-(camera.height - HEIGHT), t)  # Не движемся дальше нижней границы

    return pygame.Rect(l, t, w, h)


class Level:
    def __init__(self, level):
        self.map = pytmx.load_pygame(f'{maps}/test.tmx')
        self.width = self.map.width
        self.height = self.map.height
        self.tile_size = self.map.tilewidth * 2
        self.camera = Camera(camera_configure, self.width * self.tile_size, self.height * self.tile_size)
        self.layer_count = len(self.map.layers)

    def render(self, player):
        self.camera.update(player)
        for i in self.hp:
            screen.blit(i.image, (i.x, i.y))
        for s in background_sprite_group:
            screen.blit(s.image, self.camera.apply(s))
        for s in main_sprite_group:
            screen.blit(s.image, self.camera.apply(s))

    def create_playable_map(self):
        self.hp = []
        x = 50
        y = 10
        for i in range(3):
            a = HP(x, y)
            x += 20
            self.hp.append(a)
        for layer in range(self.layer_count):
            for y in range(self.height):
                for x in range(self.width):
                    id_map = self.map.get_tile_gid(x, y, layer)

                    if id_map != 0:
                        id = self.map.tiledgidmap[self.map.get_tile_gid(x, y, layer)] - 1
                        if id in borders:
                            image = self.map.get_tile_image(x, y, layer)
                            image = pygame.transform.scale(image, (64, 64))
                            k = Border(x * self.tile_size, y * self.tile_size, self, image)
                            main_sprite_group.add(k)
                            platforms.add(k)
                        elif id in final:
                            image = self.map.get_tile_image(x, y, layer)
                            image = pygame.transform.scale(image, (64, 64))
                            k = Final_Blolck(x * self.tile_size, y * self.tile_size, image)
                            main_sprite_group.add(k)
                            platforms.add(k)
                        else:
                            image = self.map.get_tile_image(x, y, layer)
                            image = pygame.transform.scale(image, (64, 64))
                            k = BackGround_sprites(x * self.tile_size, y * self.tile_size, self, image)
                            background_sprite_group.add(k)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'{maps}/tiles/0_352.png')
        self.r = self.image.get_rect()
        self.rect = pygame.Rect(x, y, self.r.w, self.r.h)
        self.mask = pygame.mask.from_surface(self.image)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, xseep, yspeed):
        pygame.sprite.Sprite.__init__(self)
        self.xspeed = xseep
        self.yspeed = yspeed
        self.image = pygame.image.load(f'{maps}/tiles/176_256.png')
        self.r = self.image.get_rect()
        self.rect = pygame.Rect(x, y, self.r.w, self.r.h)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed


class HP(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = x, y
        self.image_full = pygame.image.load(f'{maps}/tiles/144_256.png')
        self.image_void = pygame.image.load(f'{maps}/tiles/160_256.png')
        self.image = self.image_full
        self.mask = pygame.mask.from_surface(self.image_full)
        self.i = 0

    def void(self):
        self.mask = pygame.mask.from_surface(self.image_void)


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y, father, image):
        pygame.sprite.Sprite.__init__(self)
        self.type = ''
        self.image = image
        self.r = self.image.get_rect()
        self.rect = pygame.Rect(x, y, self.r.w, self.r.h)
        self.mask = pygame.mask.from_surface(self.image)


class BackGround_sprites(pygame.sprite.Sprite):
    def __init__(self, x, y, father, image):
        pygame.sprite.Sprite.__init__(self)
        self.type = ''
        self.rect = pygame.Rect(x, y, father.tile_size, father.tile_size)
        self.image = image


class Final_Blolck(Border):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'Final'
        self.image = image
        self.r = self.image.get_rect()
        self.rect = pygame.Rect(x, y, self.r.w, self.r.h)
        self.mask = pygame.mask.from_surface(self.image)
