from physics import Physics2D, Vector2D, RigidBody
import json, sys
import animation
from collision import BoxCollider
from player import Player
from game_settings import Settings
import physics
from gamelogic import GameLogic
from game_bg import Background
from heart import Heart
from enemy import Enemy


add_library('minim')


class GameUI:
    def __init__(self, sketch):
        self.sketch = sketch
        
        self.game_logic = GameLogic(self)
        self.player = Player(loadImage("PlayerIdle1.png"), 500, 300, loadImage("PlayerIdle1.png").width*0.55, 
                                 loadImage("PlayerIdle1.png").height*0.55, 50, self.game_logic)
        self.bg = Background(loadImage("Background.png"), -1000, 0, 3200, 720, self)
        self.fg = Background(loadImage("Ground.png"), -900, 0, 2560, 720, self)
        self.enemy = Enemy(loadImage("EnemyWalk1.png"), 700, 420, loadImage("EnemyWalk1.png").width * 0.5, 
                           loadImage("EnemyWalk1.png").height * 0.5, 2, self)
    
    def setup(self):
        self.fg.add_collider(0, 660, 1280, 50)
        self.fg.add_collider(340, 529, 100, 130)
        physics.Physics2D.apply_gravity(self.player._rb)
        
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
        
        self.player.attack()
        self.player.move()
        self.enemy.move()
        self.enemy.display()
    
    def _manage_bg(self):
        self.bg.rb.vel._x_val = self.fg.rb.vel.x_val * 1.25  # bg moves 25% faster than fg for parallax scrolling effect
        self.fg.move()
        self.bg.move()
        self.fg.colliders[-1].change_pos(self.fg.x + 1240, 529)  # tree trunk collider
        #print(self.player.standing_box_collider.collided_with(self.fg.colliders[-1]) or self.fg.colliders[-1].collided_with(self.player.run_box_collider) or self.player.run_box_collider.collided_with(self.fg.colliders[-1]))
        
        if self.player.run_box_collider.collided_with(self.fg.colliders[-1]):
            self.player.hit_wall(self.fg.colliders[-1])
        
        self.bg.display()
        self.fg.display()
        self.fg.display_colliders()
        
    def _manage_hearts(self):
        for heart in Heart.collectables:
            heart.collected()
                
            heart.x += self.fg.rb.vel.x_val
            heart.box_collider.change_pos(heart.x + 35, heart.y + 40)
            heart.display()
            heart.box_collider.display()
    
    def mousePressed(self):
        Heart.spawn(self.player.x - 300, self.player.x + self.player.img_width + 300, self.player.y, self.player)
        #self.player.hit(self.bg)
        print(mouseX, mouseY)       
        
    def keyPressed(self):
        self.game_logic.keys_pressed[key] = True
    
    def keyReleased(self):
        self.game_logic.keys_pressed[key] = False
        self.player.idle()
    
