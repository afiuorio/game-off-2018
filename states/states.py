import libtcodpy as libtcod
from states.event import Event


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
            action = enemy.act(game)
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

        yield event
