import string


class GameLogic:
    """Manages all the in game logic (i.e. behind the scenes calculations)"""
    
    space_pressed_cnt = 0
    keys_pressed = {}
    
    def __init__(self, game_ui):
        GameLogic.keys_pressed = {char: False for char in string.printable}
        self.game_ui = game_ui
        
