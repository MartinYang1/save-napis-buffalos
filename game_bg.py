import sprite
from physics import RigidBody
from collision import BoxCollider


class Background(sprite.Sprite):
    """A class representing the background of the game that can move"""
    
    def __init__(self, img, x, y, img_width, img_height, game_ui):
        super(Background, self).__init__(img, x, y, img_width, img_height)
        
        player = game_ui.player
        self.rb = RigidBody(x, y, player.mass)
        self._colliders = []
    
    def add_collider(self, x, y, w, h):
        self._colliders.append(BoxCollider(x, y, w, h))
    
    def display_colliders(self):
        for collider in self._colliders:
            collider.display()
    
    def move(self):
        self.rb.move()
        self.rb.apply_force()
        self._x, self._y = self.rb.get_pos().x_val, self.rb.get_pos().y_val
    
    @property
    def colliders(self):
        return self._colliders
