import pygame
import load


class Mouse(pygame.sprite.Sprite):
    image = load.load_image("arrow.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Mouse.image
        self.image = pygame.transform.smoothscale(Mouse.image, (32, 32))
        self.rect = self.image.get_rect()

    def update(self, ev):
        if ev.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_focused():
                self.rect.x = ev.pos[0]
                self.rect.y = ev.pos[1]
            else:
                self.rect.x = -1000
                self.rect.y = -1000
