import libtcodpy as libtcod
from textwrap import wrap
from utilities.rectangle import Rectangle


class ConsoleWrapper:
    def __init__(self, x, y, w, h, color=libtcod.dark_grey):
        self.dimensions = Rectangle(x, y, w, h)
        self.console = libtcod.console_new(w, h)
        self.color = color
        libtcod.console_set_default_background(self.console, self.color)


class GameScreen:
    def __init__(self, width, height, game_height):
        # FIXME this first part should be read from a config file
        self.screen_width = width
        self.screen_height = height
        self.game_console_wrapper = ConsoleWrapper(0, 0, width, game_height, libtcod.black)
        self.bottom_bar_console_wrapper = ConsoleWrapper(0, game_height, width, height - game_height, libtcod.darker_grey)

        libtcod.console_set_custom_font('resources/arial10x10.png',
                                        libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        self.root_console = libtcod.console_init_root(self.screen_width, self.screen_height,
                                                      'jurassic-mendel', False)

        self.message_log = MessageLog(1, 37, 8)

        self.current_console = None

    def render_all(self, game):
        current_console_x = self.current_console.dimensions.x1
        current_console_y = self.current_console.dimensions.y1
        current_console_width = self.current_console.dimensions.get_width()
        current_console_height = self.current_console.dimensions.get_height()

        libtcod.console_clear(self.current_console.console)
        game.game_state.handle_video(game)
        libtcod.console_blit(self.current_console.console, 0, 0, current_console_width, current_console_height,
                             self.root_console, current_console_x, current_console_y)

        bottom_bar_x = self.bottom_bar_console_wrapper.dimensions.x1
        bottom_bar_y = self.bottom_bar_console_wrapper.dimensions.y1
        bottom_bar_width = self.bottom_bar_console_wrapper.dimensions.get_width()
        bottom_bar_height = self.bottom_bar_console_wrapper.dimensions.get_height()

        libtcod.console_set_default_background(self.bottom_bar_console_wrapper.console, self.bottom_bar_console_wrapper.color)
        libtcod.console_clear(self.bottom_bar_console_wrapper.console)

        for index, message in enumerate(self.message_log.on_screen_message_list):
            libtcod.console_set_default_foreground(self.bottom_bar_console_wrapper.console, message.color)
            libtcod.console_print_ex(self.bottom_bar_console_wrapper.console, self.message_log.x, index + 1, libtcod.BKGND_NONE,
                                     libtcod.LEFT, message.text)
        libtcod.console_blit(self.bottom_bar_console_wrapper.console, 0, 0, bottom_bar_width, bottom_bar_height,
                             self.root_console, bottom_bar_x, bottom_bar_y)

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

    def clear_list(self):
        self.on_screen_message_list = list()