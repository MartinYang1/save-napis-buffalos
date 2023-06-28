import string
import threading
import json
import os


from heart import Heart


class GameLogic:
    """Manages all the in game logic (i.e. behind the scenes calculations)"""
    
    space_pressed_cnt = 0
    keys_pressed = {}
    
    def __init__(self, game_ui):
        GameLogic.keys_pressed = {char: False for char in string.printable}
        
        self.level = 1
        self.high_score = 0
        self.screen = 1
                
        self.game_ui = game_ui
        
        self.game_logic_thread = threading.Thread(target=self.manage_game_logic)
        self.game_logic_thread.start()
        
        self.pause_spawn_event = threading.Event()
        
        self.start_game()
    
    def next_screen(self):
        self.screen += 1
    
    def prev_screen(self):
        self.screen -= 1
    
    def next_level(self):
        self.game_ui.spawner._enemy_vel *= 1.1
        self.game_ui.spawner._spawn_limit += 3
        self.game_ui.spawner._spawn_rate *= 0.9
        self.level += 1
        Heart.spawn(self.game_ui.player.x - 300, self.game_ui.player.x + self.game_ui.player.img_width + 300, self.game_ui.player.y, self.game_ui.player)
        self.game_ui.setup_next_level()
    
    def start_game(self):
        if os.path.exists('game_data.json'):
            with open('game_data.json', 'r') as f:
                self.high_score = json.load(f).get('high score')
    
    def end_game(self):
        if self.level <= self.high_score:
            return
        
        self.high_score = self.level
        with open('game_data.json', 'w') as f:
            json.dump({'high score': self.high_score}, f)
        
    def _restart_game(self):
        self.level = 1
        self.game_ui.setup_intro_screen()
        self.screen = 1
    
    def manage_game_logic(self):
        threading.Event().wait(3)
        while True:
            if self.keys_pressed[' '] and self.screen == 1:
                self.next_screen()
                self.game_ui.setup_game_screen()
            elif len(self.game_ui.player.lives) == 0 and self.screen == 2:
                self.end_game()
                self.next_screen()
                self.game_ui.setup_end_screen()
            elif self.screen == 3:
                threading.Event().wait(3)
                self._restart_game()
            threading.Event().wait(0.01)
    
    def pause_spawner(self):
        self.pause_spawn_event.set()
    
    def resume_spawner(self):
        self.pause_spawn_event.clear()
    
