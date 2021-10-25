"""This file is for the Velocity class, keeping track of the change in coordinates."""

class Velocity:
    """A class that stores the rate of change for coordinates."""
    def __init__(self):
        """Initalizes the change in x and y coordinates."""
        self._dx = 0
        self._dy = 0
    
    # Getter and Setter properties are listed below
    @property
    def dx(self):
        """Returns dx value."""
        return self._dx
    
    @property
    def dy(self):
        """Returns dy value."""
        return self._dy
    
    @dx.setter
    def dx(self, dx):
        """Sets dx value."""
        self._dx = dx
        
    @dy.setter
    def dy(self, dy):
        """Sets dy value."""
        self._dy = dy