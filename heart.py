from random import uniform, choice
import sprite
from collision import BoxCollider


class Heart(sprite.Sprite):
    """A class representing a player's lives"""
    
    collectables = []
    
    def __init__(self, img, x, y, img_width, img_height, player, is_collectable=False):
        super(Heart, self).__init__(img, x, y, img_width, img_height)
        if is_collectable:
            self._box_collider = BoxCollider(x + 35, y + 40, img_width - 80, img_height - 90)
        self._player = player

    @classmethod
    def spawn(cls, l_bound, r_bound, y, player):
        """
        Spawns the heart if it's a collectable at a random location
        between the specified left and right boundary
        :param l_bound: the left boundary
        :param r_bound: the right boundary
        """
        spawn_x = choice((uniform(l_bound, player.x - 100), 
                         uniform(player.x + player.img_width + 100, r_bound)))
        cls.collectables.append(Heart(loadImage("Heart.png"), spawn_x, y, 
                                      loadImage("Heart.png").width * 0.8, loadImage("Heart.png").height * 0.8, 
                                      player, True))
        
    def collected(self):
        """Increments the player lives and destroys the gameobject if collected by the player"""
        if self._box_collider.collided_with(self._player.standing_box_collider) or self._box_collider.collided_with(self._player.run_box_collider):
            self._player.add_life()
            self.collectables.remove(self)
    
    @property
    def box_collider(self):
        return self._box_collider
