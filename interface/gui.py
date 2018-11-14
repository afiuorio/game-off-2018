import libtcodpy as libtcod
from textwrap import wrap

class GameScreen:
    def __init__(self, width, height, game_height):
        # FIXME this first part should be read from a config file
        self.screen_width = width
        self.screen_height = height
        self.game_width = width
        self.game_height = game_height
        self.bottom_bar_width = width
        self.bottom_bar_height = height - self.game_height
        libtcod.console_set_custom_font('resources/arial10x10.png',
                                        libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        self.root_console = libtcod.console_init_root(self.screen_width, self.screen_height,
                                                      'jurassic-mendel', False)
        self.game_area = libtcod.console_new(self.game_width, self.game_height)
        libtcod.console_set_default_foreground(self.game_area, libtcod.white)
        self.bottom_bar = libtcod.console_new(self.bottom_bar_width, self.bottom_bar_height)
        libtcod.console_set_default_background(self.bottom_bar, libtcod.darker_grey)
        self.message_log = MessageLog(1, 37, 8)

    def render_all(self, game):
        libtcod.console_clear(self.game_area)
        libtcod.console_blit(self.game_area, 0, 0, self.game_width, self.game_height, self.root_console, 0, 0)
        game.game_state.handle_video(game)

        libtcod.console_set_default_background(self.bottom_bar, libtcod.darker_grey)
        libtcod.console_clear(self.bottom_bar)

        for index, message in enumerate(self.message_log.on_screen_message_list):
            libtcod.console_set_default_foreground(self.bottom_bar, message.color)
            libtcod.console_print_ex(self.bottom_bar, self.message_log.x, index + 1, libtcod.BKGND_NONE,
                                     libtcod.LEFT, message.text)
        libtcod.console_blit(self.bottom_bar, 0, 0, self.bottom_bar_width, self.bottom_bar.height,
                             self.root_console, 0, self.game_height)
        libtcod.console_flush()


class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, lines):
        self.x = x
        self.width = width
        self.lines = lines
        self.on_screen_message_list = list()

    def add_line(self, message):
        wrapped_lines = wrap(message.text, self.width)

        for line in wrapped_lines:
            if len(self.on_screen_message_list) == self.lines:
                del self.on_screen_message_list[0]

            self.on_screen_message_list.append(Message(line, message.color))