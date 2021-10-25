"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
import constants
from ship import Ship
from asteroid_classes import Big_Rock
from ship_lives_display import Ship_Lives

# Global Constants are now contained in constants.py.
# These was done to obtain easier access to constants in all class files.


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()
        
        self.ship = Ship()
        
        # Initializes a list containing Ship_Lives objects to represent the life count
        self.lives_display = [Ship_Lives() for life in range(self.ship.lives)]
        # Count variable and for loop adjusts position of lives so they are spaced out
        count = 0
        for life in self.lives_display:
            life.center.x += (life.texture[0]) * count
            count += 1

        self.bullets = []
        
        # Creates asteroids list, populated based on the INITAL_ROCK_COUNT constant
        self.asteroids = [Big_Rock() for number in range(constants.INITIAL_ROCK_COUNT)]
            
        # A counter for when the ship is destroyed that will delay the ship's respawn
        self.reset_counter = 0
        
        # A list that is used for when the game_over screen needs to be displayed
        self.game_over = []

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        
        for bullet in self.bullets:
            bullet.draw()
            
        for asteroid in self.asteroids:
            asteroid.draw()
        
        self.ship.draw()
        # Draws the lives at the top of the screen
        for life in self.lives_display:
            life.draw()
        
        # Draws the Game Over display, which is hidden until game_over conditions are met
        for game_over in self.game_over:
            game_over.draw()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.check_collisions()
        self.check_off_screen()
        self.check_resets()
        
        self.ship.advance()
        
        for bullet in self.bullets:
            bullet.advance()
        
        for asteroid in self.asteroids:
            asteroid.advance()
    
    def check_collisions(self):
        """A function that checks if anything has collided."""
        # Checks each asteroid against the current ship
        for asteroid in self.asteroids:
            if asteroid.alive and self.ship.alive:
                too_close_ship = self.ship.radius + asteroid.radius
                
                if (abs(self.ship.center.x - asteroid.center.x) < too_close_ship and
                    abs(self.ship.center.y - asteroid.center.y) < too_close_ship):
                    self.ship.hit()
                    self.lives_display.pop()
                    
            # Checks each individual bullet against each individual asteroid
            for bullet in self.bullets:
                
                if bullet.alive and asteroid.alive:
                    too_close_bullet = bullet.radius + asteroid.radius
                    
                    if (abs(bullet.center.x - asteroid.center.x) < too_close_bullet and
                                abs(bullet.center.y - asteroid.center.y) < too_close_bullet):
                        bullet.alive = False
                        # Kills asteroid; adds smaller asteroids based on which asteroid was killed
                        self.asteroids.extend(asteroid.break_apart())
                        
        # Cleans up any destroyed objects
        self.cleanup_zombies()
    
    def check_off_screen(self):
        """A function that check if anything is off_screen."""
        for asteroid in self.asteroids:
            if asteroid.is_off_screen():
                asteroid.loop_object()
        
        for bullet in self.bullets:
            if bullet.is_off_screen():
                bullet.loop_object()

        if self.ship.is_off_screen():
            self.ship.loop_object()
    
    def cleanup_zombies(self):
        """A function to remove dead objects."""
        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)
        
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)
                
    def check_resets(self):
        """If conditions are met, increments the reset_counter, and checks for ship or game reset."""
        #If ship is dead
        if not self.ship.alive:
            self.reset_counter += 1
            # If ship still has lives, prepare a reset of the ship
            if self.reset_counter >= constants.RESET_COUNTER and self.ship.lives > 0:
                self.ship.reset()
                self.reset_counter = 0
            # Checks for game over due to ship's total destruction
            self.try_end_game()
        # If all asteroids are destoyed
        elif len(self.asteroids) == 0:
            self.reset_counter += 1
            # Check for game over due to asteroids' destruction
            self.try_end_game()

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        Parameters are positive to indicate one direction; negative for the opposite.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.turn(1)

        if arcade.key.RIGHT in self.held_keys:
            self.ship.turn(-1)

        if arcade.key.UP in self.held_keys:
            self.ship.thrust(1)

        if arcade.key.DOWN in self.held_keys:
            self.ship.thrust(-1)

        # Machine gun mode...
        if arcade.key.SPACE in self.held_keys:
            # Check if the firing cooldown is good, then fire
            if self.ship.firing_cooldown >= constants.FIRING_COOLDOWN:
                self.bullets.append(self.ship.fire())
                

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
                
        if self.ship.alive:
            self.held_keys.add(key)

            # Fire bullet!
            if key == arcade.key.SPACE:
                self.bullets.append(self.ship.fire())
        # If the ship is completely dead, look for the Enter button being pressed
        elif self.ship.lives == 0:
            if key == arcade.key.ENTER:
                # Clears the game_over screen, and resets major components of the game
                self.game_over.clear()
                self.reset_counter = 0
                self.reset_game()

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
            
            # Causes thrusters to disappear
            if key == arcade.key.UP or key == arcade.key.DOWN:
                self.ship.thrusters_on = False
                
    def try_end_game(self):
        """If reset_counter criteria is reached:
        begins the game over setup, and displays the game over screen."""
        if self.reset_counter >= constants.GAME_RESET_COUNTER:
            # Game over is displayed, and all items cleared
            self.asteroids.clear()
            self.ship.alive = False
            self.ship.lives = 0
            self.game_over.append(Game_Over())
                
    def reset_game(self):
        """Resets ship, life_count, and asteroids for a new game."""
        self.ship.reset()
        
        self.ship.lives = constants.SHIP_LIVES
        self.lives_display = [Ship_Lives() for life in range(self.ship.lives)]
        # Count variable and for loop adjusts position of lives so they are spaced out
        count = 0
        for life in self.lives_display:
            life.center.x += (life.texture[0]) * count
            count += 1
            
        self.asteroids = [Big_Rock() for number in range(constants.INITIAL_ROCK_COUNT)]
    

class Game_Over:
    """A class responsible for creating a game_over screen when either the ship is out of lives,
    or all asteroids are destroyed."""
    
    def draw(self):
        """Draws text at the center of the screen to indicate that the game has ended."""
        arcade.draw_text("Game Over", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 + 10,
                        arcade.color.WHITE, 20, width=200, align="center",
                        anchor_x="center", anchor_y="center")
        arcade.draw_text("Press Enter to Restart", constants.SCREEN_WIDTH / 2,
                        constants.SCREEN_HEIGHT / 2 - 10, arcade.color.WHITE, 14,
                        width=300, align="center", anchor_x="center", anchor_y="center")
    
# Creates the game and starts it going
window = Game(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
arcade.run()