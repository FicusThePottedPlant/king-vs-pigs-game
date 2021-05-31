import os

import pygame

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screensize = screen.get_size()
self_path = os.path.dirname(__file__)
maps = os.path.join(self_path, 'data')
# pytmx borders' id
borders = [5, 8, *range(12, 23), *range(32, 44), *range(50, 55), 64, 67, 68, *range(77, 89), 99, 100,
           *range(108, 122),
           131, 132, 152, 153, 161, 162,
           *range(168, 171), *range(196, 202), *range(228, 235), *range(256, 260), *range(288, 292), *range(320, 324)]


class Camera:
    """camera which follows a player"""

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    """size of camera and its coordinates"""
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + (screensize[0] - 100) / 2, -t + (screensize[1] - 400)
    return pygame.Rect(l, t, w, h)


class Level:
    """structure of the level and its generation"""
    def __init__(self, level):
        self.platforms = pygame.sprite.Group()
        self.main_sprite_group = pygame.sprite.Group()
        self.background_sprite_group = pygame.sprite.Group()
        self.spike = pygame.sprite.Group()
        from pytmx import load_pygame
        self.map = load_pygame(f'{maps}/levels/tmx_{level}.tmx')
        self.width = self.map.width
        self.height = self.map.height
        self.tile_size = self.map.tilewidth * 4
        self.camera = Camera(camera_configure, self.width * self.tile_size, self.height * self.tile_size)
        self.layer_count = len(self.map.layers)

    def render(self, player):
        """render sprites of the level"""
        self.camera.update(player)
        for s in self.background_sprite_group:
            screen.blit(s.image, self.camera.apply(s))
        for s in self.main_sprite_group:
            screen.blit(s.image, self.camera.apply(s))

    def create_playable_map(self):
        """creating map"""
        for layer in range(self.layer_count):
            for y in range(self.height):
                for x in range(self.width):
                    id_map = self.map.get_tile_gid(x, y, layer)
                    if id_map != 0:  # 0 - empty
                        tile_id = self.map.tiledgidmap[self.map.get_tile_gid(x, y, layer)] - 1
                        image = self.map.get_tile_image(x, y, layer)
                        image = pygame.transform.scale(image, (64, 64))
                        if tile_id in borders:  # borders can collide with player
                            k = Border(x * self.tile_size, y * self.tile_size, self, image)
                            self.main_sprite_group.add(k)
                            self.platforms.add(k)
                        elif tile_id == 76:  # spike sprite
                            k = Border(x * self.tile_size, y * self.tile_size, self, image)
                            self.spike.add(k)
                            self.main_sprite_group.add(k)
                        else:  # can not collide with player
                            k = BackGroundSprites(x * self.tile_size, y * self.tile_size, self, image)
                            self.background_sprite_group.add(k)


class Platform(pygame.sprite.Sprite):
    """platform sprites"""

    def __init__(self, x, y, id):
        pygame.sprite.Sprite.__init__(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_bounding_rects()


class Border(pygame.sprite.Sprite):
    """interactive(collidable) sprites"""

    def __init__(self, x, y, father, image):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, father.tile_size, 64)
        self.mask = pygame.mask.from_surface(image)
        self.image = image


class BackGroundSprites(pygame.sprite.Sprite):
    """non-interactive sprites"""

    def __init__(self, x, y, father, image):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, father.tile_size, father.tile_size)
        self.image = image


class Spike(pygame.sprite.Sprite):
    """spikes sprites"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player(pygame.sprite.Sprite):
    """player sprites"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
