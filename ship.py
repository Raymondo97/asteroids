"""This file is for the Ship class, which creates and tracks the ship within the game."""

from flying_objects import Flying_Objects
from bullet import Bullet
import arcade
import constants
import math

class Ship(Flying_Objects):
    """A class for a ship, which is a flying object."""
    def __init__(self):
        """Calls super; accepts radius, turn_amount,
        and thrust_amount to initialize aspects of the ship.
        Also initializes information to keep track of the ship's lives."""
        super().__init__()
        self._center.x = constants.SCREEN_WIDTH / 2
        self._center.y = constants.SCREEN_HEIGHT / 2
        self._radius = constants.SHIP_RADIUS
        self._spin = constants.SHIP_TURN_AMOUNT
        self._speed = constants.SHIP_THRUST_AMOUNT
        self._firing_cooldown = constants.FIRING_COOLDOWN
        self._lives = constants.SHIP_LIVES
        self._thrusters_on = False
        self._thrusters_direction = "forward"
        self._texture = self.load_texture(":resources:images/space_shooter/playerShip1_orange.png")
        self._thrusters_texture = self.load_texture(":resources:images/tiles/torch1.png")
        
    def draw(self):
        """Draws a ship and thrusters from image files."""
        # Draws thrusters
        width2, height2, alpha2, texture2 = self._thrusters_texture
        
        width2 = texture2.width - self._radius
        height2 = texture2.height - self._radius
        alpha2 = 1
        if self._thrusters_on and self._alive:
            alpha2 = 255
        
        # Determines whether to aim the thrusters forward or backward
        if self._thrusters_direction == "forward":
            angle2 = self._angle + 180
            x2 = self._center.x - ((math.cos(math.radians(self._angle + 90))) * self._radius)
            y2 = self._center.y - ((math.sin(math.radians(self._angle + 90))) * self._radius)
        elif self._thrusters_direction == "backward":
            angle2 = self._angle
            # Adjusts the position of the thrusters slightly, to be placed at the correct position
            x2 = self._center.x + ((math.cos(math.radians(self._angle + 90))) * (self._radius - 10))
            y2 = self._center.y + ((math.sin(math.radians(self._angle + 90))) * (self._radius - 10))
        
        arcade.draw_texture_rectangle(x2, y2, width2, height2, texture2, angle2, alpha2)
        
        # Draws ship
        width, height, alpha, texture = self._texture
        if not self._alive:
            alpha = 1
            
        arcade.draw_texture_rectangle(self._center.x, self._center.y, width, height, texture, self._angle, alpha)
        
    def advance(self):
        """Calls super, and increments the firing cooldown."""
        super().advance()
        self._firing_cooldown += 1
    
    def turn(self, direction):
        """A method for changing the angle of the ship."""
        self._angle += direction * self._spin
    
    def thrust(self, direction):
        """A method that handles the thrust of the ship.
        Also instantiates and returns a thrusters object."""
        # Sets the thrusters position to forward or backward, depending on direction given
        if direction > 0:
            self._thrusters_direction = "forward"
        elif direction < 0:
            self._thrusters_direction = "backward"
        
        # Changes velocity for ship, based on direction and speed
        self._velocity.dx += (math.cos(math.radians(self._angle + 90))) * self._speed * direction
        self._velocity.dy += (math.sin(math.radians(self._angle + 90))) * self._speed * direction
        
        # Allows thrusters to be visible
        self._thrusters_on = True
                
    def fire(self):
        """If firing cooldown is cleared, resets firing cooldown.
        Fires a bullet from the bullet class.
        Sets bullet attributes to ship's attributes, and returns bullet."""
        self._firing_cooldown = 0
        bullet = Bullet()
        # Centers bullet slightly in front of ship
        bullet.center.x = self._center.x + ((math.cos(math.radians(self._angle + 90))) * ((self._radius + bullet.radius) / 2))
        bullet.center.y = self._center.y + ((math.sin(math.radians(self._angle + 90))) * ((self._radius + bullet.radius) / 2))
        
        # Sets bullet attributes based on ship's attributes
        bullet.angle = self._angle + 90
        bullet.on_fire(self._velocity.dx, self._velocity.dy)
        return bullet
    
    def hit(self):
        """A method that keeps track of the ship's lives.
        Removes the ship from the screen momentarily so it can be properly reset"""
        self._center.x = constants.SCREEN_WIDTH * 2
        self._center.y = constants.SCREEN_HEIGHT * 2
        self._lives -= 1
        self._alive = False
            
    def reset(self):
        """Resets the ship when destroyed, if it has life left."""
        if self._lives > 0:
            self._center.x = constants.SCREEN_WIDTH / 2
            self._center.y = constants.SCREEN_HEIGHT / 2
            self._velocity.dx = 0
            self._velocity.dy = 0
            self._angle = math.degrees(0)
            self._alive = True
    
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
    def spin(self):
        return self._spin
    
    @spin.setter
    def spin(self, spin):
        self._spin = spin
        
    @property
    def thrusters_direction(self):
        return self._thrusters_direction
    
    @thrusters_direction.setter
    def thrusters_direction(self, thrusters_direction):
        self._thrusters_direction = thrusters_direction
        
    @property
    def thrusters_on(self):
        return self._thrusters_on
    
    @thrusters_on.setter
    def thrusters_on(self, thrusters_on):
        self._thrusters_on = thrusters_on
        
    @property
    def lives(self):
        return self._lives
    
    @lives.setter
    def lives(self, lives):
        self._lives = lives
        
    @property
    def firing_cooldown(self):
        return self._firing_cooldown
    
    @firing_cooldown.setter
    def firing_cooldown(self, firing_cooldown):
        self._firing_cooldown = firing_cooldown