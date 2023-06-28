import sprite
from physics import RigidBody, Vector2D, Physics2D
from animation import Animator
from collision import BoxCollider


class Enemy(sprite.Sprite):
    """
    A class representing a monster that moves at a constant velocity with
    a simple enemy AI that follows the player.
    """
    
    # enemy frames mapped to (their file path, pointer to next animation played, frame_duration)
    animations = {"walking": (["EnemyWalk1.png", "EnemyWalk2.png"], None, 10), "hit": (["EnemyDamage.png"], None, 1)}
    
    def __init__(self, img, x, y, img_width, img_height, vel, game_ui):
        super(Enemy, self).__init__(img, x, y, img_width, img_height)
        
        self._anim = Animator(**{anim: [list(map(lambda file: loadImage(file), info[0])), info[1], info[2]] for anim, info in Enemy.animations.items()})
        self._anim.set_curr_anim("walking")
        self._box_collider = BoxCollider(x + 70, y + 125, img_width - 125, img_height - 100)
        
        self._rb = RigidBody(x, y, 300)
        self._vel = vel
        
        self._death_duration = 0.6
                
        self._game_ui = game_ui
        
    def display(self):
        self._anim.play(self._x, self._y, self._img_width, self._img_height, self._direction_x)
    
    def _change_direction(self):
        """Flips the sprite and velocity to follow the player"""
        direction_x = 1 if self._x < self._game_ui.player.x else -1
        self._rb.vel._x_val = direction_x * self._vel
        self.flip_x(-direction_x)
    
    def move(self):
        """Makes the enemy follow the player"""
        if self._anim.curr_anim == "walking":
            self._change_direction()
            # if the enemy reaches the tree trunk, make it stop
            if self._direction_x == 1 and self._game_ui.fg.colliders[-1].x <= self._box_collider.x \
                    <= self._game_ui.fg.colliders[-1].x + self._game_ui.fg.colliders[-1].w:
                self._rb.vel._x_val += abs(self._rb.vel.x_val)
            elif self._direction_x == -1 and self._game_ui.fg.colliders[-1].x <= self._box_collider.x + self._box_collider.w \
                    <= self._game_ui.fg.colliders[-1].x + self._game_ui.fg.colliders[-1].w:
                self._rb.vel._x_val += -abs(self._rb.vel.x_val)
        else:
            Physics2D.apply_gravity(self._rb)
            self._rb.apply_force()

        self._rb.vel._x_val += self._game_ui.fg.rb.vel.x_val
        self._rb.move()
        
        self._x, self._y = self._rb.get_pos().x_val, self._rb.get_pos().y_val
        self._box_collider.change_pos(self._x + 70, self._y + 125)
        
    def hit(self):
        """Plays its death animation and pushes it back slightly"""
        self._box_collider.set_active(False)
        self._anim.set_curr_anim("hit")
        self._game_ui.monster_death_sound.trigger()
        self._rb.add_force(Vector2D(self._direction_x * 8000, -200), self._death_duration)
    
    @property
    def box_collider(self):
        return self._box_collider
    
    @property
    def death_duration(self):
        return self._death_duration
    
    @death_duration.setter
    def death_duration(self, duration):
        self._death_duration = duration
