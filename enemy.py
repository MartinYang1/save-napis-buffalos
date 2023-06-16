import sprite
from physics import RigidBody, Vector2D
from animation import Animator
from collision import BoxCollider


class Enemy(sprite.Sprite):
    """
    A class representing a monster that moves at a constant velocity with
    a simple enemy AI that follows the player.
    """
    
    # enemy frames mapped to (their file path, pointer to next animation played, frame_duration)
    animations = {"walking": (["EnemyWalk1.png", "EnemyWalk2.png"], None, 10)}
    enemies = []
    
    def __init__(self, img, x, y, img_width, img_height, vel, game_ui):
        super(Enemy, self).__init__(img, x, y, img_width, img_height)
        
        self._anim = Animator(**{anim: [list(map(lambda file: loadImage(file), info[0])), info[1], info[2]] for anim, info in Enemy.animations.items()})
        self._anim.set_curr_anim("walking")
        self._box_collider = BoxCollider(x + 40, y + 100, img_width - 110, img_height - 120)
        
        self._rb = RigidBody(x, y, 300)
        self._vel = vel
        
        self._game_ui = game_ui
        
    def display(self):
        self._anim.play(self._x, self._y, self._img_width, self._img_height, self._direction_x)
        self._box_collider.display()
    
    def _change_direction(self):
        """Flips the sprite and velocity"""
        direction_x = 1 if self._x < self._game_ui.player.x else -1
        self._rb.vel._x_val = direction_x * self._vel
        self.flip_x(-direction_x)
    
    def move(self):
        """Makes the enemy follow the player"""
        self._change_direction()    
        self._rb.vel._x_val += self._game_ui.fg.rb.vel.x_val
        self._rb.move()
        
        self._x, self._y = self._rb.get_pos().x_val, self._rb.get_pos().y_val
        self._box_collider.change_pos(self._x + 40, self._y + 100)
        
