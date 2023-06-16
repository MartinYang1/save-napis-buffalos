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
            return (other.x <= self._x <= other.x + other.w or other.x <= self._x + self._w <= other.x + other.w) \
                and (other.y <= self._y <= other.y + other.h or other.y <= self._y + self._h <= other.y + other.h)
    
    def get_collision_direction(self, other):
        """
        Calculates the direction of the collision (horizontal or vertical). Use a really simply
        algorithm that works for simple games only
        :param other: the other box collider
        :return: the direction as a str
        """
        if self.collided_with(other):
            if other.y <= self._y + self._h <= other.y + 20 or other.y + other.h <= self._y <= other.y + other.h - 20:
                return "vertical"
            else:
                return "horizontal"
        
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
    
