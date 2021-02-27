import ctypes
import os

import pygame
import pytmx

user32 = ctypes.windll.user32  # get user monitor size
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
size = WIDTH, HEIGHT = screensize[0] - 100, screensize[1] - 400
screen = pygame.display.set_mode(screensize)
self_path = os.path.dirname(__file__)
maps = os.path.join(self_path, 'data')

borders = [5, 8, *range(12, 23), *range(32, 44), *range(50, 55), 64, 67, 68, *range(77, 89), 99, 100,
           *range(108, 122),
           131, 132, 152, 153, 161, 162,
           *range(168, 171), *range(196, 202), *range(228, 235), *range(256, 260), *range(288, 292), *range(320, 324)]
WIDTH_CHARACTER = 34
HEIGHT_CHARACTER = 28
level_width = 16 * 64
level_height = 16 * 64
h = pygame.Surface((64, 64))


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIDTH / 2, -t + HEIGHT * 1.00000
    return pygame.Rect(l, t, w, h)


class Level:
    def __init__(self, level):
        self.platforms = pygame.sprite.Group()
        self.main_sprite_group = pygame.sprite.Group()
        self.background_sprite_group = pygame.sprite.Group()
        self.spike = pygame.sprite.Group()
        self.map = pytmx.load_pygame(f'{maps}/levels/tmx_{level}.tmx')
        self.width = self.map.width
        self.height = self.map.height
        self.tile_size = self.map.tilewidth * 4
        self.camera = Camera(camera_configure, self.width * self.tile_size, self.height * self.tile_size)
        self.layer_count = len(self.map.layers)

    def render(self, player):
        self.camera.update(player)
        for s in self.background_sprite_group:
            screen.blit(s.image, self.camera.apply(s))
        for s in self.main_sprite_group:
            screen.blit(s.image, self.camera.apply(s))

    def create_playable_map(self):
        for layer in range(self.layer_count):
            for y in range(self.height):
                for x in range(self.width):
                    id_map = self.map.get_tile_gid(x, y, layer)
                    if id_map != 0:
                        tile_id = self.map.tiledgidmap[self.map.get_tile_gid(x, y, layer)] - 1
                        image = self.map.get_tile_image(x, y, layer)
                        image = pygame.transform.scale(image, (64, 64))
                        if tile_id in borders:
                            k = Border(x * self.tile_size, y * self.tile_size, self, image)
                            self.main_sprite_group.add(k)
                            self.platforms.add(k)
                        elif tile_id == 76:
                            k = Border(x * self.tile_size, y * self.tile_size, self, image)
                            self.spike.add(k)
                            self.main_sprite_group.add(k)
                        else:
                            k = BackGroundSprites(x * self.tile_size, y * self.tile_size, self, image)
                            self.background_sprite_group.add(k)


class Door(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, id):
        pygame.sprite.Sprite.__init__(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_bounding_rects()


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y, father, image):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, father.tile_size, 64)
        self.mask = pygame.mask.from_surface(image)
        self.image = image


class BackGroundSprites(pygame.sprite.Sprite):
    def __init__(self, x, y, father, image):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, father.tile_size, father.tile_size)
        self.image = image
