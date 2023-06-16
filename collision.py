class BoxCollider:
    """A class representing a box collider that can detect collisions with other colliders"""
    
    def __init__(self, x, y, w, h):
        """Initialize dimensions"""
        self._x, self._y = x, y
        self._w, self._h = w, h
        
        self._is_active = True
    
    def collided_with(self, other):
        """
        Checks if the box collider has collided with another collider
        :param other: the other box collider
        :return: True or False
        """
        if self._is_active and other.is_active:
            return ((other.x <= self._x <= other.x + other.w or other.x <= self._x + self._w <= other.x + other.w) \
                and (other.y <= self._y <= other.y + other.h or other.y <= self._y + self._h <= other.y + other.h)) or \
                ((self._x <= other.x <= self._x + self._w or self._x <= other.x + other.w <= self._x + self._w) \
                and (self._y <= other.y <= self._y + self._h or self._y <= other.y + other.h <= self._y + self._h))
    
    def collision_direction(self, other, vel):
        """
        Calculates the direction of the collision (horizontal or vertical). Uses a really simply
        algorithm that works for simple games only since some values are hardcoded.
        :param other: the other box collider
        :param vel: the velocity of the other gameobject
        :return: the direction as a str
        """
        if (other.x + other.w <= self._x <= self._x + 10 and vel.x_val > 0) or \
                (other.x - 10 <= self._x + self._w <= other.x and vel.x_val < 0):
            return "horizontal"
        else:
            return "vertical"

    def change_pos(self, x, y):
        self._x, self._y = x, y
    
    def display(self):
        """Draws the box collider on the canvas"""
        if self._is_active:
            rect(self._x, self._y, self._w, self._h)
    
    def set_active(self, is_active):
        self._is_active = is_active
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y
    
    @property
    def w(self):
        return self._w
    
    @property
    def h(self):
        return self._h
    
    @property
    def is_active(self):
        return self._is_active
    
