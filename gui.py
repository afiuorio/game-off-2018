import libtcodpy as libtcod


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
        libtcod.console_set_default_foreground(self.root_console, libtcod.white)
        self.bottom_bar = libtcod.console_new(self.bottom_bar_width, self.bottom_bar_height)
        libtcod.console_set_default_background(self.bottom_bar, libtcod.desaturated_blue)

    def render_all(self, game):
        libtcod.console_clear(self.root_console)
        game.game_state.handle_video(game)
        libtcod.console_clear(self.bottom_bar)
        libtcod.console_blit(self.bottom_bar, 0, 0, self.bottom_bar_width, self.bottom_bar.height,
                             self.root_console, 0, self.game_height, 255)
        libtcod.console_flush()
