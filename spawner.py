import random
import threading
import time

from game_settings import Settings
from enemy import Enemy


class Spawner:
    """A class that spawns an enemy into the game periodically and manages them"""
    
    def __init__(self, l_bound, r_bound, spawn_rate, enemy_vel, game_ui):
        self._l_bound = l_bound
        self._r_bound = r_bound
        
        self._spawn_rate = spawn_rate
        self._spawn_cnt = 0
        self._spawn_limit = 3
        
        self._enemies = []
        self._enemy_vel = enemy_vel
        
        self._pause_collision_checking = threading.Event()
        
        self._game_ui = game_ui
    
    def spawn_enemy(self):
        """Spawns an enemy in the left or right boundary of the screen periodically"""
        while self._game_ui.game_logic.screen == 2:
            if not self._game_ui.game_logic.pause_spawn_event.is_set():
                # if the spawner is still spawning enemies
                spawn_x = self._l_bound if random.randrange(0, 2) == 0 else self._r_bound + loadImage("EnemyWalk1.png").width
                enemy = Enemy(loadImage("EnemyWalk1.png"), spawn_x, 420, loadImage("EnemyWalk1.png").width * 0.5, 
                                loadImage("EnemyWalk1.png").height * 0.5, self._enemy_vel, self._game_ui)
                self._enemies.append(enemy)
                self._spawn_cnt += 1
                if self._spawn_cnt == self._spawn_limit:
                    self._game_ui.game_logic.pause_spawner()
            elif not self._enemies:
                # if player killed all alive enemies
                self._spawn_cnt = 0
                self._game_ui.game_logic.next_level()
            
            time.sleep(self._spawn_rate)
        
    def move_enemies(self):
        """
        Moves all of the enemies toward the player and
        displays them onto the screen
        """
        self._l_bound += self._game_ui.bg.rb.vel.x_val
        self._r_bound += self._game_ui.bg.rb.vel.x_val
        for enemy in self._enemies:
            enemy.move()
            enemy.display()
    
    def enemies_collided(self):
        while self._game_ui.game_logic.screen == 2:     
            if not self._pause_collision_checking.is_set():      
                for enemy in self._enemies:
                    if enemy.box_collider.collided_with(self._game_ui.player.axe_box_collider):
                        enemy.hit()
                        time.sleep(enemy.death_duration)
                        self._enemies.remove(enemy)
                        
                        self._pause_collision_checking.set()
            else:
                if self._game_ui.player.anim.curr_anim != "attack":
                    self._pause_collision_checking.clear()
    
            threading.Event().wait(float(1) / 60)
    
    @property
    def spawn_rate(self):
        return self._spawn_rate
    
    @spawn_rate.setter
    def spawn_rate(self, spawn_rate):
        self._spawn_rate = spawn_rate
    
    @property
    def spawn_limit(self):
        return self.spawn_limit
    
    @spawn_rate.setter
    def spawn_limit(self, spawn_limit):
        self.spawn_limit = spawn_limit
    
    @property
    def enemies(self):
        return self._enemies
    
    @property
    def enemy_vel(self):
        return self._enemy_vel
    
    @enemy_vel.setter
    def enemy_vel(self):
        self._enemy_vel = enemy_vel
    
