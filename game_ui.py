from physics import Physics2D, Vector2D, RigidBody
import json, sys
import threading
import animation
from collision import BoxCollider
from player import Player
from game_settings import Settings
import physics
from gamelogic import GameLogic
from game_bg import Background
from heart import Heart
from spawner import Spawner
import time


add_library('minim')


class GameUI:
    def __init__(self, sketch, minim):
        self.sketch = sketch    
        self.game_logic = GameLogic(self)
        self.minim = minim
    
    def _load_files(self):
        self.intro_song = self.minim.loadFile("intro_screen_music.mp3")
        self.game_song = self.minim.loadFile("game_music.mp3")
        
        self.axe_sound = self.minim.loadSample("axe_swing.mp3")
        self.monster_death_sound = self.minim.loadSample("monster_death.mp3")
        self.heart_collected_sound = self.minim.loadSample("heart_collected.mp3")
    
    def setup_intro_screen(self):
        self.player = Player(loadImage("PlayerIdle1.png"), 500, 100, loadImage("PlayerIdle1.png").width*0.55, 
                                 loadImage("PlayerIdle1.png").height*0.55, 50, 3, self.game_logic)
        self.player_intro_screen = Player(loadImage("PlayerIdle1.png"), 500, 100, loadImage("PlayerIdle1.png").width*0.55, 
                                 loadImage("PlayerIdle1.png").height*0.55, 50, 0, self.game_logic)
        
        self.bg = Background(loadImage("Background.png"), -1000, 0, 3200, 720, self)
        self.fg = Background(loadImage("Ground.png"), -645, 0, 2560, 720, self)
        self.napi_icon = loadImage("napi_icon.png")
        self.spawner = Spawner(-850, 1900, 2, 3.2, self)
        
        self.intro_song.rewind()
        self.intro_song.loop()
        self.bg.display()
        
    def run_intro_screen(self):
        self.bg.display()
        self.fg.display()
        image(self.napi_icon, -40, 250, self.napi_icon.width * 2, self.napi_icon.height * 2)
        self.player_intro_screen.display()
        
        textFont(Settings.game_font, 60)
        textAlign(CENTER)
        fill(0)
        text("Save Napi's Buffalos", Settings.SCREEN_WIDTH // 2, 100)
        
        textFont(Settings.game_font, 35)
        text("Press SPACE to begin", Settings.SCREEN_WIDTH // 2, 450)
        
        fill(255, 0, 0)
        textAlign(RIGHT)
        text("High Score: " + str(self.game_logic.high_score), Settings.SCREEN_WIDTH - 40, 60)
        noFill()
    
    def setup_game_screen(self):        
        self.intro_song.pause()
        self.game_song.rewind()
        self.game_song.loop()
        
        self.fg.add_collider(0, 660, 1280, 50)
        self.bg.add_collider(self.bg.x + 600, 0, 2400, 800)
        self.fg.add_collider(340, 529, 100, 180)
                
        self.spawn_thread = threading.Thread(target=self.spawner.spawn_enemy)
        self.spawn_thread.start()
        
        self.check_enemy_collision_thread = threading.Thread(target=self.spawner.enemies_collided)
        self.check_enemy_collision_thread.start()
        
        self.next_level = False
        self.setup_next_level()
    
    def run_game_screen(self):
        self._manage_bg()
        if self.next_level:
            textFont(createFont("Arial", 16, True), 50)
            textAlign(CENTER)
            fill(255, 0, 0)
            text("Level " + str(self.game_logic.level), Settings.SCREEN_WIDTH // 2, 200)
        
        textFont(Settings.game_font, 30)
        textAlign(RIGHT)
        fill(0)
        text("High Score: " + str(self.game_logic.high_score), Settings.SCREEN_WIDTH - 40, 60)
        text("Level: " + str(self.game_logic.level), Settings.SCREEN_WIDTH - 40, 110)
        noFill()
        
        self._manage_hearts()
        self.player.display()
        
        self._manage_enemies()
        
        self.player.attack()
        self.player.move()
        self.player.hit(self.spawner.enemies)
    
    def setup_end_screen(self):
        self.game_song.pause()
    
    def run_end_screen(self):
        game_end_bg = loadImage("game_end.jpg")
        image(game_end_bg, 0, 0, Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT)
            
    def setup_next_level(self):        
        self.next_level = True
        
        time.sleep(1.5)
        self.next_level = False
        self.game_logic.resume_spawner()
        
    def setup(self):
        self._load_files()
        Settings.initialize_game_font()

        self.setup_intro_screen()

    def draw(self):
        if self.game_logic.screen == 1:
            self.run_intro_screen()
        elif self.game_logic.screen == 2:
            self.run_game_screen()
        elif self.game_logic.screen == 3:
            self.run_end_screen()
    
    def stop(self):
        """Closes all threads and audio UI safely when exiting program"""
        self.game_logic.end_game()
        
        self.spawn_thread.exit()
        self.spawn_thread.join()
        self.check_enemy_collision.exit()
        self.check_enemy_collision.join()
        self.game_logic.game_logic_thread.exit()
        self.game_logic.game_logic_thread.join()
        
        self.game_song.close()
        self.minim.stop()
        super().stop()
    
    def _manage_bg(self):
        """Moves the backgrounds and their colliders, as well as displaying them to the screen"""
        self.bg.rb.vel._x_val = self.fg.rb.vel.x_val * 1.25  # bg moves 25% faster than fg for parallax scrolling effect
        self.fg.move()
        self.bg.move()
        self.fg.colliders[-1].change_pos(self.fg.x + 1240, 529)  # tree trunk collider
        self.bg.colliders[0].change_pos(self.bg.x + 600, 0)  # player boundary collider
        
        self.bg.display()
        self.fg.display()
        
    def _manage_hearts(self):
        """Moves, displays, and checks if the hearts are collected by the player"""
        for heart in Heart.collectables:
            heart.collected()
                
            heart.x += self.fg.rb.vel.x_val
            heart.box_collider.change_pos(heart.x + 35, heart.y + 40)
            heart.display()
    
    def _manage_enemies(self):
        self.spawner.move_enemies()
        
    def keyPressed(self):
        self.game_logic.keys_pressed[key] = True
    
    def keyReleased(self):
        self.game_logic.keys_pressed[key] = False
        self.player.idle()
    
