import thread


from gamelogic import GameLogic
from game_settings import Settings

import sprite
import physics
from heart import Heart

from collision import BoxCollider
from animation import Animator


class Player(sprite.Sprite):
    """A class representing a player that can move, jump, and attack."""
    
    # player frames mapped to (their file path, pointer to next animation played, frame_duration)
    animations = {
                  "idle": (["PlayerIdle1.png"] * 3 + ["PlayerIdle2.png"] * 2 + ["PlayerIdle3.png"] * 3 + ["PlayerIdle2.png"] * 2, None, 4),
                  "attack": (["PlayerAttack1.png"] + ["PlayerAttack2.png"] * 2 + ["PlayerAttack3.png"] * 2 + ["PlayerAttack4.png"] * 2, "idle", 3),
                  "run": (["PlayerRun1.png"] * 2 + ["PlayerRun2.png"] * 3, None, 2),
                  "jump": (["PlayerJump.png"], None, 1),
                  "hit": (["PlayerIdle1.png", "PlayerInvisible.png"], None, 3)
                  }
    
    def __init__(self, img, x, y, img_width, img_height, mass, num_lives, game_logic):
        super(Player, self).__init__(img, x, y, img_width, img_height)
        
        self.anim = Animator(**{anim: [list(map(lambda file: loadImage(file), info[0])), info[1], info[2]] for anim, info in Player.animations.items()})
        self.anim.set_curr_anim("idle")

        self._rb = physics.RigidBody(x, y, mass)
        physics.Physics2D.apply_gravity(self._rb)
        
        self._standing_box_collider = BoxCollider(x + 115, y + 65, img_width - 235, img_height - 85)
        self._run_box_collider = BoxCollider(x + 110, y + 65, img_width - 200, img_height - 85)
        self._axe_box_collider = BoxCollider(x + 165, y + 50, 50, img_height - 160)
        self._run_box_collider.set_active(False)
        self._axe_box_collider.set_active(False)
        
        self._space_pressed_cnt = 0
        self._left_key_pressed = False
        self._right_key_pressed = False
        self._direction_key_pressed_cnt = 0
        self._is_attacking = False
        self._is_hit = False
        
        self._mass = mass
        self._lives = [Heart(loadImage("Heart.png"), x + 38 + 25 * i, y, 30, 30, self) for i in range(2, num_lives + 2)]
        self._immunity_duration = 2  # how long immunity lasts when the player is hit in sec
        self._prev_hit_time = 0
        
        self._game_logic = game_logic
    
    def _check_keys(self):
        force_x = 0
        if self._game_logic.keys_pressed['a'] and not self._right_key_pressed \
                and (self._game_logic.game_ui.bg.colliders[0].x < self._run_box_collider.x and self._game_logic.game_ui.bg.colliders[0].x < self._standing_box_collider.x):
            force_x -= 800
            self._direction_key_pressed_cnt += 1
            self._left_key_pressed = True
            self._right_key_pressed = False
            
            if self._direction_key_pressed_cnt == 1:
                # flip player and colliders
                self._axe_box_collider._x = self._x + 165 - self._axe_box_collider.w - self._standing_box_collider.w - 10
                self.flip_x(-1)
        
        if self._game_logic.keys_pressed['d'] and not self._left_key_pressed \
                and (self._run_box_collider.x + self._run_box_collider.w < self._game_logic.game_ui.bg.colliders[0].x + self._game_logic.game_ui.bg.colliders[0].w
                         and self._standing_box_collider.x + self._standing_box_collider.w < self._game_logic.game_ui.bg.colliders[0].x + self._game_logic.game_ui.bg.colliders[0].w):
            force_x += 800
            self._direction_key_pressed_cnt += 1
            self._right_key_pressed = True
            self._left_key_pressed = False
            
            if self._direction_key_pressed_cnt == 1:
                self._axe_box_collider._x = self._x + 165
                self.flip_x(1)
            
        self._game_logic.game_ui.fg.rb.add_force(physics.Vector2D(-force_x, 0), 0.5)
        
    def _horizontal_movement(self):
        if not self._game_logic.keys_pressed['a']:
            self._left_key_pressed = False
        if not self._game_logic.keys_pressed['d']:
            self._right_key_pressed = False
        
        self._check_keys()
        if self._direction_key_pressed_cnt == 1 and self._rb.is_grounded:
            self._run_box_collider.set_active(True)
            self._standing_box_collider.set_active(False)
            self._axe_box_collider.set_active(False)
            
            self.anim.set_curr_anim("run")
    
    def move(self):
        if self.anim.curr_anim != "attack":
            self._is_attacking = False
            self._axe_box_collider.set_active(False)
        if self._is_attacking:
            return

        self._horizontal_movement()
        self.jump()
        self._rb.apply_force()
        self._rb.move()
        
        # set the coordinates of dependencies to the player coordinates (only needed for vertical movement)
        self._x, self._y = self._rb.get_pos().x_val, self._rb.get_pos().y_val
        self._standing_box_collider.change_pos(self._x + 115, self._y + 65)
        self._run_box_collider.change_pos(self._x + 110, self._y + 65)
        self._axe_box_collider._y = self._y + 50  # x coordinates already changed in another function
        for heart in self._lives:
            heart.y = self._y
    
    def idle(self):
        if not self._game_logic.keys_pressed['d'] and not self._game_logic.keys_pressed['a'] and not self._is_attacking:
            self._direction_key_pressed_cnt = 0
            if self._rb.is_grounded:
                self._standing_box_collider.set_active(True)
                self._run_box_collider.set_active(False)
                self._axe_box_collider.set_active(False)
                self.anim.set_curr_anim("idle")

    def jump(self):        
        if self._rb.is_grounded and not self._is_hit:
            if keyPressed and self._game_logic.keys_pressed['w'] and self._space_pressed_cnt == 0:    
                self._rb.add_force(physics.Vector2D(0, -4800), 0.25)
                self.anim.set_curr_anim("jump")
                self._space_pressed_cnt += 1
    
        if not self.is_grounded(*self._game_logic.game_ui.fg.colliders):
            self._rb.is_grounded = False
        if not self._rb.is_grounded and self._rb.vel.y_val < 2:
            physics.Physics2D.apply_gravity(self._rb)
        
        if not self._rb.is_grounded and self.is_grounded(*self._game_logic.game_ui.fg.colliders):
            self._rb.is_grounded = True
            if self._is_hit:
                self.anim.set_curr_anim("hit")
            else:
                self.anim.set_curr_anim("idle") if self._rb.vel.x_val == 0 else self.anim.set_curr_anim("run")
            self._space_pressed_cnt = 0
            physics.Physics2D.remove_gravity(self._rb)
            self._rb._vel._y_val = 0
    
    def attack(self):
        """Makes player swing his axe. When the player attacks, he cannot move"""
        if (keyPressed and key == CODED and keyCode == SHIFT) and \
                self._rb.is_grounded and not self._is_attacking:
            self._run_box_collider.set_active(False)
            self._standing_box_collider.set_active(True)
            self._axe_box_collider.set_active(True)
            
            self.anim.set_curr_anim("attack")
            self._game_logic.game_ui.axe_sound.trigger()
            
            self._is_attacking = True
        
    def display(self):
        for heart in self._lives:
            heart.display()
        self.anim.play(self._x, self._y, self._img_width, self._img_height, self._direction_x)
        
    def hit_wall(self, *walls):
        player_vel = physics.Vector2D(-self._game_logic.game_ui.fg.rb.vel.x_val, 0)  # relative velocity compared to the bg
        for wall in walls:
            if wall.collision_direction(self._standing_box_collider, player_vel) == "horizontal":
                self._rb.vel._x_val = 0
                for force in self._rb.forces_applied:
                    force.force._x_val = 0
    
    def is_grounded(self, *platforms):
        """ 
        Checks if the player is touching any platform, including the ground
        :param platforms: the box colliders of those platforms
        :return: True or False
        """
        player_vel = physics.Vector2D(-self._game_logic.game_ui.fg.rb.vel.x_val, 0)  # relative velocity compared to the bg
        for platform in platforms:
            if (self._standing_box_collider.collided_with(platform) and platform.collision_direction(self._standing_box_collider, player_vel) == "vertical") \
                    or (self._run_box_collider.collided_with(platform) and platform.collision_direction(self._run_box_collider, player_vel) == "vertical"):
                return True
    
    def hit(self, enemies):
        if self._is_hit:
            if frameCount / float(Settings.FRAME_RATE) - self._prev_hit_time >= self._immunity_duration:
                self._is_hit = False
                self.anim.set_curr_anim("idle")
            else:
                return
        
        for enemy in enemies:
            if self._standing_box_collider.collided_with(enemy.box_collider) or \
                    self._run_box_collider.collided_with(enemy.box_collider):
                self._is_hit = True
                self._prev_hit_time = frameCount / float(Settings.FRAME_RATE)
                self.flip_x(enemy.direction_x)  # makes player face the enemy
                
                self._game_logic.game_ui.fg.rb.add_force(physics.Vector2D(self._direction_x * 11000, 0), 0.6)  # push player backwards
                self._rb.add_force(physics.Vector2D(0, -1600), 0.6)
                
                self.anim.set_curr_anim("jump")
                self.lives.pop(-1)
                break
    
    def add_life(self):
        new_life_x = self._lives[-1].x + 25
        self._lives.append(Heart(loadImage("Heart.png"), new_life_x, self._y, 30, 30, self))
    
    """Getters and setters"""
    
    @property
    def space_pressed_cnt(self):
        return self._space_pressed_cnt
    
    @space_pressed_cnt.setter
    def space_pressed_cnt(self, space_pressed_cnt):
        self._space_pressed_cnt = space_pressed_cnt
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def mass(self):
        return self._mass
    
    @property
    def lives(self):
        return self._lives
    
    @lives.setter
    def lives(self, lives):
        self._lives = lives
    
    @property
    def standing_box_collider(self):
        return self._standing_box_collider
    
    @property
    def run_box_collider(self):
        return self._run_box_collider

    @property
    def axe_box_collider(self):
        return self._axe_box_collider
    
    @property
    def rb(self):
        return self._rb
    
    @property
    def hit_wall(self):
        return self._hit_wall
    
