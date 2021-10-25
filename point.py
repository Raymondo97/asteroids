"""This file is for the Point class, keeping track of coordinates for an object."""

class Point:
    """A class that stores coordinates."""
    def __init__(self):
        """Initalizes the x and y coordinates."""
        self._x = 0
        self._y = 0
    
    # Getter and Setter properties are listed below
    @property
    def x(self):
        """Returns x value."""
        return self._x
    
    @property
    def y(self):
        """Returns y value."""
        return self._y
    
    @x.setter
    def x(self, x):
        """Sets x value."""
        self._x = x
        
    @y.setter
    def y(self, y):
        """Sets y value."""
        self._y = y