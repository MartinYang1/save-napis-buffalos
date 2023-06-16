import sys
from functools import reduce

from game_settings import Settings


class Physics2D:
    GRAVITY_FORCE = 160  # N/kg^2
        
    @classmethod
    def apply_gravity(cls, gameobj):
        """Applies gravity to a gameobject"""
        gameobj.add_force(Vector2D(0, cls.GRAVITY_FORCE), sys.maxsize)
    
    @classmethod
    def remove_gravity(cls, gameobj):
        """Removes gravity from a gameobject"""
        gameobj.remove_force(force=Vector2D(0, cls.GRAVITY_FORCE))
    
    @staticmethod
    def get_current_time():
        return frameCount / Settings.FRAME_RATE


class EnactedForce:
    """A class representing a 2D Force that is applied to a rigid body"""
    
    def __init__(self, force, duration, type):
        self.force = force
        self.duration = duration
        self.type = type
        
        self.begin_time = frameCount / float(Settings.FRAME_RATE)  # start time in num of seconds


class RigidBody:
    """A class representing a 2D rigid body that can experience forces"""

    def __init__(self, x, y, mass, drag=450):
        """
        Initializes the vector and scalar properties of a rigid body
        :param mass: mass in kg
        """
        self._pos = Vector2D(x, y)
        self._mass = mass
        self._vel = Vector2D(0, 0)
        self._drag = drag

        # variables used to know when to stop the force of friction
        self._prev_vel_x = 0
        
        self._is_grounded = True
        self._is_moving = False
        self._forces_applied = []
    
    def add_force(self, force, duration, type="applied"):
        """
        Adds a EnactedForce object to the list of forces being applied to the rigidbody
        :param force: a Vector2D object in Newtons
        :param duration: the duration the force is applied in sec
        :param type: the type of force as a str
        """
        self._forces_applied.append(EnactedForce(force, duration, type))
    
    def remove_force(self, force=None):
        """
        Removes a force from the force applied list once it has been 
        applied for its specified duration
        :param force: if specified, removes a specific force from the force applied list
        regardless of its duration
        """
        if force:
            for enacted_force in self._forces_applied[:]:
                if enacted_force.force == force:
                    self._forces_applied.remove(enacted_force)

        for force in self._forces_applied[:]:
            if frameCount / float(Settings.FRAME_RATE) - force.begin_time >= force.duration:
                self._forces_applied.remove(force)
    
    def _calculate_net_force(self):
        if len(self._forces_applied) == 0:
            net_force = Vector2D(0, 0)
        elif len(self._forces_applied) == 1:
            net_force = self._forces_applied[0].force
        else:
            try:
                net_force = reduce(lambda f1, f2: f1.force + f2.force, self._forces_applied)
            except AttributeError:
                net_force = Vector2D(0, 0)
                for i in range(0, len(self._forces_applied)-1, 2):
                    net_force += self._forces_applied[i].force + self._forces_applied[i+1].force
        # cnt = 0
        # for enacted_force in self._forces_applied:
        #     if enacted_force.force == Vector2D(0, -1000):
        #         cnt += 1
        net_force += self._calculate_drag()
        return net_force
    
    def apply_force(self):
        """Applies the net force (sum of all the forces) to the rigid body's velocity"""
        self.remove_force()  # removes forces that are no longer present
        
        # net force does not include friction
        net_force = self._calculate_net_force()
        acceleration = net_force / float(self._mass)
        self._prev_vel_x = self._vel.x_val
        
        #self._vel += acceleration * (1.0 / Settings.FRAME_RATE)
        # if abs(self._vel.x_val) <= 5:
        #     self._vel._x_val = 0
        #print(abs(self._vel.x_val) <= 5)
        #print(acceleration.x_val < 0 and 0 <= self._vel.x_val < 5)
        if (acceleration.x_val < 0 and 0 < self._vel.x_val < 5) or (acceleration.x_val > 0 and -5 < self._vel.x_val < 0):
            self._vel._x_val = 0
            acceleration._x_val = 0
        self._vel += acceleration * (1.0 / Settings.FRAME_RATE)
    
    def _calculate_drag(self):
        """
        Calculates the drag force experienced by the rigid body
        by the velocity it is travelling at
        :return: a Vector2D object representing the drag force
        """
        drag_force_x = self._vel.x_val**2 * self._drag
        drag_force_y = self._vel.y_val**2 * self._drag
        
        drag_force_x = -drag_force_x if self._vel.x_val > 0 else drag_force_x
        drag_force_y = -drag_force_y if self._vel.y_val > 0 else drag_force_y
        
        # just have drag_force_y be 0 for now since it is not needed
        drag_force_y = 0
        return Vector2D(drag_force_x, drag_force_y)

    def _calculate_friction(self, friction_coefficient):
        """
        Calculates the force of kinetic friction experienced by the rigid body
        :param friction_coefficient: the coefficient of friction between the two
        surfaces
        :return: a Vector2D object representing the friction force
        """
        force_friction = friction_coefficient * self._mass * Physics2D.GRAVITY_FORCE
        if self._vel.x_val == 0:
            return Vector2D(0, 0)
        elif self._vel.x_val > 0:
            return Vector2D(-force_friction, 0)
        else:
            return Vector2D(force_friction, 0)
    
    def move(self):
        self._pos += self._vel
    
    def get_pos(self):
        return self._pos
    
    def change_pos(self, x, y):
        self._pos = Vector2D(x, y)
    
    @property
    def vel(self):
        return self._vel
    
    @vel.setter
    def vel(self, vel):
        self._vel = vel
    
    @property
    def is_grounded(self):
        return self._is_grounded
    
    @is_grounded.setter
    def is_grounded(self, is_grounded):
        self._is_grounded = is_grounded
    
    def forces_applied(self):
        return self._forces_applied


class Vector2D:
    """A class representing a 2D vector with its x and y component in the
     cartesian coordinate system"""
    def __init__(self, x_val, y_val):
        self._x_val = x_val
        self._y_val = y_val
    
    def __add__(self, v2):
        return Vector2D(self._x_val + v2._x_val, self._y_val + v2._y_val)
    
    def __mul__(self, scalar):
        return Vector2D(self._x_val * scalar, self._y_val * scalar)
    
    def __div__(self, scalar):
        return Vector2D(self._x_val / scalar, self._y_val / scalar)            
    
    def __repr__(self):
        return "({}, {})".format(self.x_val, self.y_val)        
    
    def __eq__(self, v2):
        return self._x_val == v2._x_val and self._y_val == v2._y_val

    @property
    def magnitude(self):
        return (self._x_val ** 2 + self._y_val ** 2) ** 0.5
    
    @property
    def x_val(self):
        return self._x_val
    
    @x_val.setter
    def x_val(self, x_val):
        self._x_val = x_val

    @property
    def y_val(self):
        return self._y_val

    @y_val.setter
    def y_val(self, y_val):
        self._y_val = y_val
    
