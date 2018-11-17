import libtcodpy as libtcod
from states.event import Event
from interface.gui import Message

class GameState():
    def __init__(self, nameState):
        self.nameState = nameState
    
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
        libtcod.console_print_ex(0, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, "Pause")

    def handle_world(self, game):
        key = libtcod.console_wait_for_keypress(True)
        if key.vk == libtcod.KEY_ESCAPE:
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
        libtcod.console_print_ex(0, int(game.game_screen.game_width / 2) - 5, int(game.game_screen.game_height / 2),
                                 libtcod.BKGND_NONE, libtcod.LEFT, "GAME OVER")

    def handle_world(self, game):
        key = libtcod.console_wait_for_keypress(True)
        if key.vk == libtcod.KEY_ESCAPE:
            event = Event("exit_game")
        else:
            event = Event("nop")

        yield event
