import random
import arcade
import os

BOJO_SCALING = 0.075
PATIENT_SCALING = 0.1
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Collect Coins with Different Levels Example"


class FallingPatient(arcade.Sprite):
    """ Simple sprite that falls down """

    def update(self):
        """ Move the coin """
        self.avoided = False
        # Fall down
        self.center_y -= 2

        # Did we go off the screen? If so, pop back to the top.
        if self.top < 0:
            self.avoided = True


class RisingPatient(arcade.Sprite):
    """ Simple sprite that falls up """

    def update(self):
        """ Move the coin """
        self.avoided = False
        # Move up
        self.center_y += 2

        # Did we go off the screen? If so, pop back to the bottom.
        if self.bottom > SCREEN_HEIGHT:
            self.avoided = True


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """ Initialize """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.game_over = False

        # Variables that will hold sprite lists
        self.player_list = None
        self.patient_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        self.level = 1

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Set the background color
        arcade.set_background_color(arcade.color.BALL_BLUE)


    def level_1(self):
        for i in range(30):

            # Create the coin instance
            patient = FallingPatient(
                "patient.png", PATIENT_SCALING)

            # Position the coin
            patient.center_x = random.randrange(SCREEN_WIDTH)
            patient.center_y = random.randrange(
                SCREEN_HEIGHT, SCREEN_HEIGHT * 2)

            # Add the coin to the lists
            self.patient_list.append(patient)

    def level_2(self):
        for i in range(30):

            # Create the coin instance
            patient = RisingPatient(
                "patient.png", PATIENT_SCALING)

            # Position the coin
            patient.center_x = random.randrange(SCREEN_WIDTH)
            patient.center_y = random.randrange(-SCREEN_HEIGHT, 0)

            # Add the coin to the lists
            self.patient_list.append(patient)

    def setup(self):
        """ Set up the game and initialize the variables. """

        self.score = 0
        self.level = 1

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.patient_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite("bojo.png",
                                           BOJO_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.avoided_patients = 0

        self.level_1()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.player_sprite.draw()
        self.patient_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 15)

        output = f"Level: {self.level}"
        arcade.draw_text(output, 10, 35, arcade.color.WHITE, 15)

        # Put the text on the screen.
        output = f"GAME OVER"
        if self.game_over:
            arcade.draw_text(output, 400, 300, arcade.color.RED, 50)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.patient_list.update()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.patient_list)

        if hit_list:
            self.game_over = True
        # Loop through each colliding sprite, remove it, and add to the score.
        for patient in self.patient_list:
            if patient.avoided == True:
                self.avoided_patients += 1
                self.score += 1
                patient.remove_from_sprite_lists()

        # See if we should go to level 2
        if len(self.patient_list) == 0 and self.level == 1:
            self.level += 1
            self.level_1()
        # See if we should go to level 3
        elif len(self.patient_list) == self.avoided_patients and self.level == 1:
            self.level += 1
            self.level_2()


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
