class Sprite(object):
    """A class representing a simple sprite that can render its image"""
    
    def __init__(self, img, x, y, img_width, img_height):
        self._x = x
        self._y = y
        
        self._direction_x = 1
        self._img_width = img_width
        self._img_height = img_height
        self._img = img
    
    def flip_x(self, direction):
        self._x += self._img.width  # necessary for the flip to not translate the sprite
        self._direction_x = direction
    
    def display(self):
        image(self._img, self._x, self._y, self._img_width, self._img_height)
        
    """Getters and setters"""
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, x):
        self._x = x
   
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, y):
        self._y = y
        
    @property
    def img_width(self):
        return self._img_width
    
    @property
    def img_height(self):
        return self._img_height
    
    @property
    def direction_x(self):
        return self._direction_x
    
