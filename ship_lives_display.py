"""This file contains a class to keep track of the ship's lives, and displaying them on the screen."""

from point import Point
import constants
import math
import arcade

class Ship_Lives:
    """This class is responsible for displaying the number of lives the ship has left on the screen."""
    def __init__(self):
        """Initializes the count of little ships to display on the screen."""
        self._center = Point()
        self._center.y = constants.SCREEN_HEIGHT - 30
        self._center.x = 30
        self._texture = self.load_texture(":resources:images/space_shooter/playerLife1_orange.png")
    
    def draw(self):
        """Draws a few little ships, based on the current life count."""
        width, height, alpha, texture = self._texture
        angle = math.degrees(0)
        
        arcade.draw_texture_rectangle(self._center.x, self._center.y, width, height, texture, angle, alpha)
            
    def load_texture(self, img):
        """A method to load the texture of the flying object."""
        texture = arcade.load_texture(img)
        
        width = texture.width
        height = texture.height
        alpha = 255
        return width, height, alpha, texture
                
        
    # Getter and Setter properties are listed below
    @property
    def life_count(self):
        return self._life_count
    
    @life_count.setter
    def life_count(self, life_count):
        self._life_count = life_count
        
    @property
    def texture(self):
        return self._texture
    
    @texture.setter
    def texture(self, texture):
        self._texture = texture
        
    @property
    def center(self):
        return self._center
    
    @center.setter
    def center(self, center):
        self._center = center