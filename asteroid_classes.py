"""This file is for all Asteroid classes, which generates and tracks asteroids in the game."""

import arcade
import random
import math
import constants
from flying_objects import Flying_Objects
from abc import abstractmethod

class Asteroid(Flying_Objects):
    """An abstract, flying_object class for asteroids."""
    def __init__(self):
        """Calls super; initiazlies radius, spin, speed, and angle."""
        super().__init__()
        self._radius = 0
        self._spin = 0
        self._angle = math.degrees(random.randint(0, 360))
        
    def advance(self):
        """Handles the advancing and rotating of asteroids."""
        super().advance()
        self._angle += self._spin
        
    def draw(self):
        """Draws asteroid based on texture loaded."""
        width, height, alpha, texture = self._texture
        
        arcade.draw_texture_rectangle(self._center.x, self._center.y, width, height, texture, self._angle, alpha)
    
    @abstractmethod
    def break_apart(self):
        """Handles the destruction and breaking apart of asteroids."""
        pass
    
    #Getter and setter properties listed here    
    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius
        
    @property
    def spin(self):
        return self._spin
    
    @spin.setter
    def spin(self, spin):
        self._spin = spin
        
    
class Big_Rock(Asteroid):
    """An asteroid class for a big rock."""
    def __init__(self):
        """Calls the super init method, then sets the rock attributes to the global constants.
        Also sets position of the asteroid to a random location, besides around the ship.
        Initializes velocity based on random angle given, followed by the image texture."""
        super().__init__()
        self._radius = constants.BIG_ROCK_RADIUS
        self._spin = constants.BIG_ROCK_SPIN
        self._speed = constants.BIG_ROCK_SPEED
        # Sets a random location on the screen, except for a square of space in the center, to make room for the ship
        self._center.x = random.choice([i for i in range(0, constants.SCREEN_WIDTH) if i not in \
                range(int(constants.SCREEN_WIDTH / 2 - (self._radius * 2)), int(constants.SCREEN_WIDTH / 2 + (self._radius * 2)))])
        self._center.y = random.choice([i for i in range(0, constants.SCREEN_HEIGHT) if i not in \
                range(int(constants.SCREEN_HEIGHT / 2 - (self._radius * 2)), int(constants.SCREEN_HEIGHT / 2 + (self._radius * 2)))])
        # Sets velocity based on random angle that is initialized
        self._velocity.dx = math.cos(math.radians(self._angle)) * self._speed
        self._velocity.dy = math.sin(math.radians(self._angle)) * self._speed
        self._texture = self.load_texture(":resources:images/space_shooter/meteorGrey_big1.png")
        
    def break_apart(self):
        """Accepts the current list of asteroids from game.
        Breaks into 2 medium rocks, and one small. Sets attributes for each rock.
        Returns asteroids list with new asteroids."""
        medium_rock_1 = Medium_Rock()
        medium_rock_2 = Medium_Rock()
        small_rock = Small_Rock()
        
        # Set first medium rock with current velocity + 2 pixels/frame in the upwards direction
        medium_rock_1.velocity.dy = self._velocity.dy + 2
        medium_rock_1.velocity.dx = self._velocity.dx
        medium_rock_1.center.x = self._center.x
        medium_rock_1.center.y = self._center.y
        
        # Set second medium rock with current velocity + 2 pixels/frame in the downwards direction
        medium_rock_2.velocity.dy = self._velocity.dy - 2
        medium_rock_2.velocity.dx = self._velocity.dx
        medium_rock_2.center.x = self._center.x
        medium_rock_2.center.y = self._center.y
        
        # Set small rock with current velocity + 5 pixels/frame in the right direction
        small_rock.velocity.dy = self._velocity.dy
        small_rock.velocity.dx = self._velocity.dx + 5
        small_rock.center.x = self._center.x
        small_rock.center.y = self._center.y
        
        # Kills asteroid, returns list of new asteroids
        self.alive = False
        return [medium_rock_1, medium_rock_2, small_rock]
    
    # Getter and setter properties listed below
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, speed):
        self._speed = speed
    
class Medium_Rock(Asteroid):
    """An asteroid class for a medium rock."""
    def __init__(self):
        """Calls super init method, followed by setting the appropriate attributes for the medium rock."""
        super().__init__()
        self._spin = constants.MEDIUM_ROCK_SPIN
        self._radius = constants.MEDIUM_ROCK_RADIUS
        self._texture = self.load_texture(":resources:images/space_shooter/meteorGrey_med1.png")
        
    def break_apart(self):
        """Accepts the current list of asteroids from game.
        Breaks into 2 small rocks. Sets attributes for each rock.
        Returns asteroids list with new asteroids."""
        small_rock_1 = Small_Rock()
        small_rock_2 = Small_Rock()
        
        # Set first small rock with current velocity + 1.5 pixels/frame in the up and right directions
        small_rock_1.velocity.dx = self._velocity.dx + 1.5
        small_rock_1.velocity.dy = self._velocity.dy + 1.5
        small_rock_1.center.x = self._center.x
        small_rock_1.center.y = self._center.y
        
        # Set second small rock with current velocity -1.5 pixels/frame in the down and left directions
        small_rock_2.velocity.dx = self._velocity.dx - 1.5
        small_rock_2.velocity.dy = self._velocity.dy - 1.5
        small_rock_2.center.x = self._center.x
        small_rock_2.center.y = self._center.y
        
        # Kills asteroid, returns list of new asteroids
        self._alive = False
        return [small_rock_1, small_rock_2]
        
    
class Small_Rock(Asteroid):
    """An asteroid class for a small rock."""
    def __init__(self):
        """Calls super init method, followed by setting the appropriate attributes for the small rock."""
        super().__init__()
        self._spin = constants.SMALL_ROCK_SPIN
        self._radius = constants.SMALL_ROCK_RADIUS
        self._texture = self.load_texture(":resources:images/space_shooter/meteorGrey_small1.png")
        
    def break_apart(self):
        """Sets alive attribute to False, and returns a list version of the asteroid."""
        self._alive = False
        return [self]