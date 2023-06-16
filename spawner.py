import random
import threading

from game_settings import Settings
from enemy import Enemy


class Spawner:
    """A class that spawns an enemy into the game periodically and manages them"""
    
    def __init__(self, l_bound, r_bound, spawn_rate, game_ui):
        self._l_bound = l_bound
        self._r_bound = r_bound
        
        self._spawn_rate = spawn_rate
        self._enemies = []
        
        self._game_ui = game_ui
    
    def spawn_enemy(self):
        """Spawns an enemy in the left or right boundary of the screen periodically"""
        while frameCount < 20 * 60:
            spawn_x = self._l_bound if random.randrange(0, 2) == 0 else self._r_bound + loadImage("EnemyWalk1.png").width
            enemy = Enemy(loadImage("EnemyWalk1.png"), spawn_x, 420, loadImage("EnemyWalk1.png").width * 0.5, 
                            loadImage("EnemyWalk1.png").height * 0.5, 2, self._game_ui)
            self._enemies.append(enemy)
            threading.Event().wait(self._spawn_rate)
        
    def move_enemies(self):
        """Moves all of the enemies toward the player"""
        for enemy in self._enemies:
            enemy.move()
            enemy.display()
    
    def enemies_collided(self):
        for enemy in self._enemies:
            if enemy.box_collider.collided_with(self._game_ui.player.standing_box_collider) \
                    or enemy.box_collider.collided_with(self._game_ui.player.run_box_collider):
                enemy.hit()
                self._enemies.remove(enemy)
    @property
    def spawn_rate(self):
        return self._spawn_rate
    
    @spawn_rate.setter
    def spawn_rate(self, spawn_rate):
        self._spawn_rate = spawn_rate
    
