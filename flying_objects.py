"""This file is for the Flying_Objects class,
containing the necessary attributes and methods that a moving object would need."""

import math
import constants
import arcade
from velocity import Velocity
from point import Point
from abc import ABC, abstractmethod

class Flying_Objects(ABC):
    """A class for flying objects."""
    def __init__(self):
        """Initalizes point and velocity objects, as well as life."""
        self._center = Point()
        self._velocity = Velocity()
        self._alive = True
        self._angle = math.degrees(0)
        
    def load_texture(self, img):
        """A method to load the texture of the flying object."""
        texture = arcade.load_texture(img)
        
        width = texture.width
        height = texture.height
        alpha = 255
        return width, height, alpha, texture
        
    def advance(self):
        """Handles the advancement of the objects center based on velocity."""
        self._center.x += self._velocity.dx
        self._center.y += self._velocity.dy
        
    def loop_object(self):
        """Changes object location to the opposite edge of the screen if it moves beyond."""
        if self.center.x >= constants.SCREEN_WIDTH:
            self.center.x = 0
        elif self.center.x <= 0:
            self.center.x = constants.SCREEN_WIDTH
        elif self.center.y >= constants.SCREEN_HEIGHT:
            self.center.y = 0
        elif self.center.y <= 0:
            self.center.y = constants.SCREEN_HEIGHT
        
    def is_off_screen(self):
        """Returns true if object exits screen parameters."""
        off_screen = False
        # If statement checks if objects goes off any side of screen
        if self._center.x > constants.SCREEN_WIDTH or 0 > self._center.x or \
           self._center.y > constants.SCREEN_HEIGHT or 0 > self._center.y:
            off_screen = True
        return off_screen
        
    @abstractmethod
    def draw(self):
        """An abstract drawing method, to be defined by child classes."""
        pass
    
    # Getter and setter properties are listed below
    @property
    def center(self):
        return self._center
    
    @center.setter
    def center(self, center):
        self._center = center
        
    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, velocity):
        self._velocity = velocity
        
    @property
    def alive(self):
        return self._alive
    
    @alive.setter
    def alive(self, alive):
        self._alive = alive
        
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, angle):
        self._angle = angle