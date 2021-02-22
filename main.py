import random
import sqlite3
import string
import webbrowser

from character import *
from level_create import *
from mouse import *

current_window = 3
LEVELS = 10


def inc_number(v):
    global current_window
    current_window += v
    if v == -4:
        game.player.rect.x = 1000000


buttons_behaviour = {'Credits': lambda x: inc_number(1), 'Return': lambda x: inc_number(-2),
                     'Return to menu': lambda x: inc_number(-1),
                     'Start game': lambda x: inc_number(2),
                     'Return to main menu': lambda x: inc_number(-4), 'Exit': lambda x: exit(),
                     'Tagir Asadullin': lambda x: webbrowser.open_new('t.me/ficusthepottedplant'),
                     'Continue': lambda x: inc_number(-1)}

left, right, up = False, False, False  # camera flags


class Button:
    def __init__(self, button_text: str, x, y, font_size, is_clickable=True, has_border=False,
                 is_locked=False):
        """
            Create new button with button_text in (x,y) by up left corner with size font_size
            :param is_clickable: set not clickable type of button
            :param has_border: set a border to button if var is True
            :param is_locked: set a locked type, so user can't press it
        """
        self.font = pygame.font.Font('data/fonts/8-BIT WONDER.TTF', font_size)
        self.button_text = button_text
        self.is_clickable = is_clickable
        self.has_border = has_border
        self.is_locked = is_locked

        self.color = 'grey' if is_locked else 'white'
        self.text = self.font.render(button_text, True, self.color)
        self.text_x, self.text_y = x, y
        self.text_w, self.text_h = self.text.get_width(), self.text.get_height()
        self.rect = self.text.get_rect()
        self.center_x, self.center_y = (2 * self.text_x + self.text_w) / 2, (2 * self.text_y + self.text_h) / 2

    def render(self):
        """the method that work on game cycle all the time"""
        if self.has_border:
            pygame.draw.rect(screen, self.color, (self.center_x - 30, self.center_y - 30,
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
                pygame.draw.rect(screen, self.color, (self.text_x - 10, self.text_y - 8,
                                                      self.text_w + 15, self.text_h + 20), width=5, border_radius=10)
            else:
                if not self.is_locked:
                    pygame.draw.polygon(screen, self.color,
                                        ((self.center_x, self.center_y + 40), (self.center_x + 25, self.center_y + 50),
                                         (self.center_x - 25, self.center_y + 50)))

    def update(self, pygame_event):
        """the method that get pygame event and define the behaviour of each button"""
        mouse_pos = pygame.mouse.get_pos()
        if self.text_x <= mouse_pos[0] <= self.text_x + self.text_w and \
                self.text_y <= mouse_pos[1] <= self.text_y + self.text_h and self.is_clickable and not self.is_locked:
            if pygame_event.type == pygame.MOUSEBUTTONDOWN:
                global current_window, buttons_behaviour, game
                if self.button_text.isnumeric():
                    current_window = 3
                    game = GameWindow(self.button_text)
                    data[3] = game
                else:
                    buttons_behaviour[self.button_text](None)

    def unlock_button(self):
        """if the button locked, than unlock button by request """
        self.is_locked = False
        self.color = 'white'
        self.text = self.font.render(self.button_text, True, self.color)


class Menu:
    """main menu window"""

    def __init__(self):
        self.font = pygame.font.Font('data/fonts/8-BIT WONDER.TTF', 6)
        self.buttons = [Button('Start game', width // 2 - 200 + 10, height // 2 - 20, 40),
                        Button('Credits', width // 2 - 98 + 10, height // 2 + 15 + 30, 30),
                        Button('Exit', width // 2 - 35 + 10, height // 2 + 10 + 30 * 3, 20)]

        self.matrix = []
        # generating Matrix effect
        for i in range(0, height, 3):
            for j in range(20):
                self.falling_down(i)

    def falling_down(self, y=-6):
        return
        """make a matrix main theme effect
        :param y: y ords of the screen
        """
        text = self.font.render(string.printable[random.randint(0, 99)], True, 'green')
        text_x, text_y = random.randint(0, width), y
        self.matrix.append((text, [text_x, text_y]))

    def update(self, pygame_event):
        """handle events"""
        for i in self.buttons:
            i.update(pygame_event)

    def render(self):
        """what to do on game cycle"""
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
        """handle button events"""
        for i in self.buttons:
            i.on_cursor(pos)


class Credits(Menu):
    """credits window"""

    def __init__(self):
        super().__init__()
        self.buttons = [Button('Made by', width // 2 - 140, height // 2 - 20, 40, False),
                        Button('Alim Mullayanov', width // 2 - 225 + 10, height // 2 + 10 + 30, 30, False),
                        Button('Tagir Asadullin', width // 2 - 202 + 10, height // 2 + 15 + 30 * 3, 30),
                        Button('Return to menu', width // 2 - 135 + 10, height // 2 + 10 + 30 * 9, 20)]

    def render(self):
        """what to do on game cycle"""
        self.matrix = menu.matrix
        super().render()


class LevelChooser(Menu):
    """level chooser window"""

    def __init__(self):
        super().__init__()
        self.buttons = [Button('Return', width // 2 - 60 + 10, height // 2 + 10 + 30 * 9, 20),
                        Button('Choose level', width // 2 - 230 + 10, height // 2 - 20 * 10, 40, False)]
        a = width // 2 - (1 + LEVELS // 2) * 86  # centre button
        self.con = sqlite3.connect("data/config/config.db")
        self.cur = self.con.cursor()
        result = self.cur.execute("SELECT * FROM config").fetchall()
        for i in result:
            if i[0] > LEVELS:
                break
            self.buttons.append(Button(str(i[0]), (a := a + 100), height // 2 - 100, 40, True, True, i[1]))

    def render(self):
        """what to do on game cycle"""
        self.matrix = menu.matrix
        super().render()
        pygame.draw.rect(screen, 'black', (50, 50,
                                           width - 100, height - 100), width=0, border_radius=10)
        pygame.draw.rect(screen, 'white', (50, 50,
                                           width - 100, height - 100), width=5, border_radius=10)
        for i in self.buttons:
            i.render()
        self.do_button_behaviour(pygame.mouse.get_pos())


class GameWindow:
    def __init__(self, which_level):
        global left, right, up
        self.which_level = which_level
        self.player = Hero((164, 1200))
        main_sprite_group.add(self.player)
        self.level = Level(which_level)
        self.level.create_playable_map()
        self.left, self.right, self.up = False, False, False

    def render(self):
        screen.fill('#1d212d')
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.left = True
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.right = True
        if pygame.key.get_pressed()[pygame.K_z]:
            self.up = True
        self.level.render(self.player)
        self.player.update(self.left, self.right, self.up, platforms)

    def update(self, pygame_event):
        if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            global current_window
            current_window = 4
            screen.fill('#1d212d')
        self.left, self.right, self.up = False, False, False


class Pause(Menu):
    """pause menu"""

    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font('data/fonts/8-BIT WONDER.TTF', 6)
        self.buttons = [Button('Continue', width // 2 - 75 + 10, height // 2 - 30, 20),
                        Button('Return to main menu', width // 2 - 180 + 10, height // 2 + 30, 20)]

    def render(self):
        """what to do on game cycle"""
        self.matrix = menu.matrix
        super().render()
        pygame.draw.rect(screen, 'black', (100, 100,
                                           width - 200, height - 200), border_radius=10)
        pygame.draw.rect(screen, 'white', (100, 100,
                                           width - 200, height - 200), width=5, border_radius=10)
        for i in self.buttons:
            i.render()
        super().do_button_behaviour(pygame.mouse.get_pos())

    def update(self, pygame_event):
        """handle pygame events"""
        if pygame_event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            global current_window, game
            current_window = 3
            mouse.display = False
            screen.fill('#1d212d')

        for i in self.buttons:
            i.update(pygame_event)


if __name__ == '__main__':
    pygame.init()
    fps = 30
    clock = pygame.time.Clock()
    running = True
    all_sprites = pygame.sprite.Group()
    menu = Menu()
    titres = Credits()
    level_menu = LevelChooser()
    pause = Pause()
    pygame.mouse.set_visible(False)
    mouse = Mouse(all_sprites)
    game = GameWindow(3)
    data = {0: menu, 1: titres, 2: level_menu, 3: game, 4: pause}
    while running:
        screen.fill('#1d212d')
        mouse.display = False if current_window == 3 else True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            data[current_window].update(event)
            all_sprites.update(event)

        data[current_window].render()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(fps)
