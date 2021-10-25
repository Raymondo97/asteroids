"""This file is for the Bullet class."""

from flying_objects import Flying_Objects
import math
import arcade
import constants

class Bullet(Flying_Objects):
    """A class for a bullet, which is a flying object."""
    def __init__(self):
        """Calls super; accepts radius, speed, and life to initialize aspects of the bullet."""
        super().__init__()
        self._radius = constants.BULLET_RADIUS
        self._speed = constants.BULLET_SPEED
        self._life = 0
        self._texture = self.load_texture(":resources:images/space_shooter/laserBlue01.png")
        
    def draw(self):
        """Loads the data from self._texture, then draws bullet."""
        width, height, alpha, texture = self._texture
        
        arcade.draw_texture_rectangle(self._center.x, self._center.y, width, height, texture, self._angle, alpha)
        
    def advance(self):
        """Calls super of parent class, and changes alive attribute if life is too high."""
        super().advance()
        self._life += 1
        if self._life >= constants.BULLET_LIFE:
            self._alive = False
        
    def on_fire(self, velocity_x, velocity_y):
        """Changes velocity to match the current movement of the ship, in addition to bullet's speed."""
        self._velocity.dx = (math.cos(math.radians(self._angle)) * self._speed) + velocity_x
        self._velocity.dy = (math.sin(math.radians(self._angle)) * self._speed) + velocity_y
        
    # Getter and setter properties are listed below
    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius
    
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, speed):
        self._speed = speed
        
    @property
    def life(self):
        return self._life
    
    @life.setter
    def life(self, life):
        self._life = life