import libtcodpy as libtcod
from states.event import Event
from interface.gui import Message, MessageLog


class GameState:
    def __init__(self, name_state):
        self.nameState = name_state
    
    def handle_video(self, game):
        pass
    
    def handle_world(self, game):
        pass


class ActiveState(GameState):
    def __init__(self):
        GameState.__init__(self, "Active")
    
    def handle_video(self, game):
        game.currentDrawMap.draw()
        game.player.draw()
        for enemy in game.current_map.entity_list:
            if game.currentDrawMap.is_in_fov(enemy.x, enemy.y):
                enemy.draw()

    def handle_world(self, game):
        for enemy in game.current_map.entity_list:
            action = enemy.act(enemy, game)
            event = Event(action[0], action[1], enemy)
            yield event


class PauseState(GameState):
    def __init__(self):
        GameState.__init__(self, "Pause")
    
    def handle_video(self, game):
        libtcod.console_print_ex(game.game_screen.current_console.console, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, "Pause")

    def handle_world(self, game):
        key = libtcod.console_wait_for_keypress(True)
        if key.vk == libtcod.KEY_ESCAPE:
            event = Event("exit_game")
        elif key.vk == libtcod.KEY_ENTER:
            event = Event("go_active")
        else:
            event = Event("nop")

        yield event


class PopUpState(GameState):
    def __init__(self):
        GameState.__init__(self, "PopUpState")

    def handle_video(self, game):
        width = game.menu.console_wrapper.dimensions.get_width()
        height = game.menu.console_wrapper.dimensions.get_height()
        game.menu.console_wrapper.console.print_frame(1, 1, width-2, height-2, "blablabla")
        libtcod.console_set_default_foreground(game.menu.console_wrapper.console, libtcod.white)
        index = 3
        for message in game.menu.text_lines:
            libtcod.console_print_ex(game.menu.console_wrapper.console, game.menu.x, index, libtcod.BKGND_NONE,
                                     libtcod.LEFT, message)
            index += 1

        index += 1

        for line_index, message in enumerate(game.menu.choice_lines):
            if line_index is game.menu.cursor_position:
                message = "> " + message
            else:
                message = "  " + message
            libtcod.console_print_ex(game.menu.console_wrapper.console, game.menu.x, index, libtcod.BKGND_NONE,
                                     libtcod.LEFT, message)
            index += 1

    def handle_world(self, game):
        key = libtcod.console_wait_for_keypress(True)

        if key.vk == libtcod.KEY_UP:
            event = Event("cursor_movement", -1)
        elif key.vk == libtcod.KEY_DOWN:
            event = Event("cursor_movement", 1)
        elif key.vk == libtcod.KEY_SPACE:
            event = Event("cursor_selection")
        elif key.vk == libtcod.KEY_ESCAPE:
            event = Event("exit_game")
        elif key.vk == libtcod.KEY_ENTER:
            event = Event("go_active")
        else:
            event = Event("nop")

        yield event


class GameOverState(GameState):
    def __init__(self):
        GameState.__init__(self, "Game Over")

    def handle_video(self, game):
        game.game_screen.message_log.clear_list()
        game.game_screen.message_log.add_line(Message("You've met with a terrible fate, haven't you?", libtcod.red))
        libtcod.console_print_ex(game.game_screen.current_console.console, int(game.game_screen_width / 2) - 5,
                                 int(game.game_screen_height / 2), libtcod.BKGND_NONE, libtcod.LEFT, "GAME OVER")

    def handle_world(self, game):
        key = libtcod.console_wait_for_keypress(True)
        if key.vk == libtcod.KEY_ESCAPE:
            event = Event("exit_game")
        else:
            event = Event("nop")

        yield event
