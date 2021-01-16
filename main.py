import ctypes
import random
import string
import webbrowser

import pygame

from mouse import Mouse

user32 = ctypes.windll.user32  # get user monitor size
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# screensize = 900, 600
size = width, height = screensize

screen = pygame.display.set_mode(screensize)

display_menu, display_levels, display_credits, is_playing, on_pause = True, False, False, False, False  # current displaying window
LEVELS = 9


class Button:
    def __init__(self, button_text: str, x: int, y: int, font_size: int, is_clickable=True, has_border=False):
        """
            Create new button with button_text in (x,y) by up left corner with size font_size
            :param is_clickable: set not clickable type of button
        """
        self.font = pygame.font.Font('data/fonts/8-BIT WONDER.TTF', font_size)
        self.button_text = button_text
        self.is_clickable = is_clickable
        self.has_border = has_border
        self.text = self.font.render(button_text, True, 'white')
        self.text_x, self.text_y = x, y
        self.text_w, self.text_h = self.text.get_width(), self.text.get_height()
        # print(self.text_x, self.text_y,
        #       self.text_w, self.text_h)
        self.rect = self.text.get_rect()
        self.center_x, self.center_y = (2 * self.text_x + self.text_w) / 2, (2 * self.text_y + self.text_h) / 2

    def render(self):
        if self.has_border:
            pygame.draw.rect(screen, 'white', (self.center_x - 30, self.center_y - 30,
                                               60, 60), width=5, border_radius=10)
        screen.blit(self.text, (self.text_x, self.text_y))

    def on_cursor(self, mouse_pos):
        """
        behaviour of each button
        :param mouse_pos: position of cursor
        """
        if self.text_x <= mouse_pos[0] <= self.text_x + self.text_w \
                and self.text_y <= mouse_pos[1] <= self.text_y + self.text_h and self.is_clickable:
            if not self.has_border:
                pygame.draw.rect(screen, 'white', (self.text_x - 10, self.text_y - 8,
                                                   self.text_w + 15, self.text_h + 20), width=5, border_radius=10)
            else:
                pygame.draw.polygon(screen, 'white',
                                    ((self.center_x, self.center_y + 40), (self.center_x + 25, self.center_y + 50),
                                     (self.center_x - 25, self.center_y + 50)))

    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.text_x <= mouse_pos[0] <= self.text_x + self.text_w and \
                self.text_y <= mouse_pos[1] <= self.text_y + self.text_h and self.is_clickable:
            if event.type == pygame.MOUSEBUTTONDOWN:
                windows_behaviour = {'Credits': (False, False, True), 'Return': (True, False, False),
                                     'Start game': (False, True, False), 'Return to main menu': (True, False, False)}

                global display_menu, display_credits, display_levels, running, is_playing, on_pause
                if not windows_behaviour.get(self.button_text) and display_levels:
                    display_menu, display_credits, display_levels = False, False, False
                    is_playing = True
                elif self.button_text == 'Exit':
                    running = False
                elif self.button_text == 'Tagir Asadullin':
                    webbrowser.open_new('t.me/ficusthepottedplant')
                elif self.button_text == 'Continue':
                    is_playing = True
                    on_pause = False
                else:
                    try:
                        display_menu, display_levels, display_credits = windows_behaviour[self.button_text]
                    except KeyError:
                        pass


class Menu:
    def __init__(self):
        self.font = pygame.font.Font('data/fonts/8-BIT WONDER.TTF', 6)
        self.buttons = [Button('Start game', width // 2 - 200, height // 2 - 20, 40),
                        Button('Credits', width // 2 - 100, height // 2 + 15 + 30, 30),
                        Button('Exit', width // 2 - 35, height // 2 + 10 + 30 * 3, 20)]
        self.matrix = []

        for i in range(0, height, 3):
            for j in range(20):
                self.falling_down(i)

    def falling_down(self, y=-9):
        """make a matrix main theme effect
        :param y: y ords of the screen
        """
        text = self.font.render(string.printable[random.randint(0, 99)], True, 'green')
        text_x, text_y = random.randint(0, width), y
        self.matrix.append((text, [text_x, text_y]))

    def update(self, event):
        for i in self.buttons:
            i.update(event)

    def render(self):

        for i in self.matrix:
            screen.blit(*i)
            i[1][1] += 3
            if i[1][1] >= height + 3:
                self.matrix.remove(i)

        for i in range(20):
            self.falling_down()
        for i in self.buttons:
            i.render()
        self.do_button_behaviour(pygame.mouse.get_pos())

    def do_button_behaviour(self, pos):
        """
        handle button events
        """
        for i in self.buttons:
            i.on_cursor(pos)


class Credits(Menu):
    def __init__(self):
        super().__init__()
        self.buttons = [Button('Made by', width // 2 - 140, height // 2 - 20, 40, False),
                        Button('Alim Mullayanov', width // 2 - 225, height // 2 + 10 + 30, 30, False),
                        Button('Tagir Asadullin', width // 2 - 202, height // 2 + 15 + 30 * 3, 30),
                        Button('Return', width // 2 - 60, height // 2 + 10 + 30 * 9, 20)]

    def render(self):
        self.matrix = menu.matrix
        super().render()


class LevelChooser(Menu):
    def __init__(self):
        super().__init__()
        self.buttons = [Button('Return', width // 2 - 60, height // 2 + 10 + 30 * 9, 20),
                        Button('Choose level', width // 2 - 240, height // 2 - 20 * 10, 40, False)]

        a = width // 2 - (1 + LEVELS // 2) * 100
        for i in range(1, LEVELS + 1):
            self.buttons.append(Button(str(i), (a := a + 100), height // 2 - 100, 40, True, True))

    def render(self):
        self.matrix = menu.matrix
        super().render()
        pygame.draw.rect(screen, 'black', (50, 50,
                                           width - 100, height - 100), width=0, border_radius=10)
        pygame.draw.rect(screen, 'white', (50, 50,
                                           width - 100, height - 100), width=5, border_radius=10)
        for i in self.buttons:
            i.render()
        self.do_button_behaviour(pygame.mouse.get_pos())


class Game:
    # TODO integrate a level and game here
    def __init__(self):



    def render(self):
        pygame.draw.rect(screen, 'red', (50, 50,
                                         width - 100, height - 100), width=5, border_radius=10)

    def update(self, event):
        if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            global is_playing, on_pause
            is_playing = False
            on_pause = True


class Pause(Menu):
    def __init__(self):
        self.font = pygame.font.Font('data/fonts/8-BIT WONDER.TTF', 6)
        self.buttons = [Button('Continue', width // 2 - 75, height // 2 - 30, 20),
                        Button('Return to main menu', width // 2 - 180, height // 2 + 30, 20)]

    def render(self):
        pygame.draw.rect(screen, 'white', (100, 100,
                                           width - 200, height - 200), width=5, border_radius=10)
        for i in self.buttons:
            i.render()
        self.do_button_behaviour(pygame.mouse.get_pos())

    def do_button_behaviour(self, pos):
        super(Pause, self).do_button_behaviour(pygame.mouse.get_pos())

    def update(self, event):
        if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            global is_playing, on_pause
            is_playing = True
            on_pause = False

        for i in self.buttons:
            i.update(event)


def all_window_render():
    if display_menu:
        menu.render()
    elif display_credits:
        titres.render()
    elif display_levels:
        level_menu.render()
    elif is_playing:
        game.render()
    elif on_pause:
        pause.render()


def all_window_update():
    if display_menu:
        menu.update(event)
    elif display_credits:
        titres.update(event)
    elif display_levels:
        level_menu.update(event)
    elif is_playing:
        game.update(event)
    elif on_pause:
        pause.update(event)


if __name__ == '__main__':
    pygame.init()
    fps = 30
    clock = pygame.time.Clock()
    running = True
    all_sprites = pygame.sprite.Group()

    menu = Menu()
    titres = Credits()
    level_menu = LevelChooser()
    game = Game()
    pause = Pause()

    pygame.mouse.set_visible(False)
    mouse = Mouse(all_sprites)
    do_clear = True
    while running:
        if do_clear:
            screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            all_window_update()

        all_window_render()
        all_sprites.draw(screen)
        all_sprites.update(event)

        pygame.display.flip()

        clock.tick(fps)
