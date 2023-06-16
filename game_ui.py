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


add_library('minim')


class GameUI:
    def __init__(self, sketch, minim):
        self.sketch = sketch    
        self.game_logic = GameLogic(self)
        self.minim = minim
        
        self.player = Player(loadImage("PlayerIdle1.png"), 500, 300, loadImage("PlayerIdle1.png").width*0.55, 
                                 loadImage("PlayerIdle1.png").height*0.55, 50, self.game_logic)
        self.bg = Background(loadImage("Background.png"), -1000, 0, 3200, 720, self)
        self.fg = Background(loadImage("Ground.png"), -900, 0, 2560, 720, self)
        self.spawner = Spawner(-100, 1380, 2, self)
    
    def _load_files(self):
        self.game_song = self.minim.loadFile("game_music.mp3")
        self.axe_sound = self.minim.loadSample("axe_sound2.wav")
        self.axe_sound.trigger()
        # self.axe_sound.trigger()
        # self.axe_sound.trigger()
        # self.axe_sound.trigger()
        
    def setup(self):
        self.fg.add_collider(0, 660, 1280, 50)
        self.bg.add_collider(150, 0, 2600, 800)
        self.fg.add_collider(340, 529, 100, 180)
        
        physics.Physics2D.apply_gravity(self.player._rb)
        
        spawn_thread = threading.Thread(target=self.spawner.spawn_enemy)
        spawn_thread.start()
        
        self._load_files()
        #self.game_song.loop()
        
        smooth()
        frameRate(Settings.FRAME_RATE)

    def draw(self):
        self._manage_bg()
        
        self._manage_hearts()
        self.player.display()
        noFill()
        self.player.standing_box_collider.display()
        self.player.run_box_collider.display()
        self.player.axe_box_collider.display()
        
        self._manage_enemies()
        
        self.player.attack()
        self.player.move()
    
    def stop(self):
        self.game_song.close()
        self.minim.stop()
        super().stop()
    
    def _manage_bg(self):
        self.bg.rb.vel._x_val = self.fg.rb.vel.x_val * 1.25  # bg moves 25% faster than fg for parallax scrolling effect
        self.fg.move()
        self.bg.move()
        self.fg.colliders[-1].change_pos(self.fg.x + 1240, 529)  # tree trunk collider
        self.bg.colliders[0].change_pos(self.bg.x + 150, 0)  # player boundary collider
        
        self.bg.display()
        self.fg.display()
        self.fg.display_colliders()
        self.bg.display_colliders()
        
    def _manage_hearts(self):
        for heart in Heart.collectables:
            heart.collected()
                
            heart.x += self.fg.rb.vel.x_val
            heart.box_collider.change_pos(heart.x + 35, heart.y + 40)
            heart.display()
            heart.box_collider.display()
    
    def _manage_enemies(self):
        self.spawner.move_enemies()
        self.spawner.enemies_collided()
    
    def mousePressed(self):
        #Heart.spawn(self.player.x - 300, self.player.x + self.player.img_width + 300, self.player.y, self.player)
        #self.player.hit(self.bg)
        pass
        
    def keyPressed(self):
        self.game_logic.keys_pressed[key] = True
    
    def keyReleased(self):
        self.game_logic.keys_pressed[key] = False
        self.player.idle()
    
