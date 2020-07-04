import random
import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.075
SPRITE_SCALING_BOG_ROLL = 0.01
ROLL_COUNT = 25
PATIENT_SCALING = 0.1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Quorontine"

MOVEMENT_SPEED = 1.5


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Welcome! The year is 2020 and a virus\n"
        " from a distant land has reached your nation.\n"
        "As leader of the United Queendom,\n"
        " you must do your utmost to save the nation, Doris Johnson...", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.WHITE, font_size=25, anchor_x="center")
        arcade.draw_text("..but first you need to stock up. Click to advance", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.WHITE_SMOKE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = InstructionView()
        self.window.show_view(game_view)


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Use the arrow keys to collect 20 bog rolls in 30 seconds!", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=25, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class StageTwoView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Well done! You stocked up on essentials.\n"
        "Alas the virus is spreading quickly.\n"
        "Doris, you have to attend several meetings\n"
        " but you must maintain social distancing", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.WHITE, font_size=25, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.WHITE_SMOKE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = StageTwo()
        game_view.setup()
        self.window.show_view(game_view)


class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class GameView(arcade.View):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        self.time_left = 30

        self.game_over = False
        self.success = False
        # Don't show the mouse cursor

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """
        # self.window.set_mouse_visible(False)

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        self.player_sprite = Player("bojo.png",
                                    SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the coins
        for _ in range(ROLL_COUNT):
            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite("bog_roll_2.png",
                                 SPRITE_SCALING_BOG_ROLL)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.coin_list.draw()
        self.player_list.draw()

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.time_left) % 60

        # Figure out our output
        output = f"Time Left: {seconds:02d} days"
        arcade.draw_text(output, 10, 40, arcade.color.BLACK, 14)

        # Output the timer text.

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        # Put the text on the screen.
        output = f"GAME OVER"
        if self.game_over:
            arcade.draw_text(output, 400, 300, arcade.color.RED, 50)

        # Put the text on the screen.
        output = f"SUCCESS! You stocked up on essentials.\n Click to advance!"
        if self.success:
            arcade.draw_text(output,
             SCREEN_HEIGHT/2,
             SCREEN_WIDTH/2,
             arcade.color.BLUE, 15, anchor_x='center')

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
    
    def on_mouse_press(self, *args):
        if self.success:
            stage_two_view = StageTwoView()
            self.window.show_view(stage_two_view)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.coin_list.update()
        self.player_list.update()
        # Generate a list of all sprites that collided with the player.
        coins_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        self.time_left -= delta_time

        if int(self.time_left) % 60 <= 0 and self.score < 20:
            self.game_over = True
        elif int(self.time_left) % 60 > 0 and self.score >= 20:
            self.success = True




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


class StageTwo(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        """ Initialize """

        # Call the parent class initializer
        super().__init__()

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        # file_path = os.path.dirname(os.path.abspath(__file__))
        # os.chdir(file_path)

        self.game_over = False

        # Variables that will hold sprite lists
        self.player_list = None
        self.patient_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        self.level = 1

        # Don't show the mouse cursor
        # self.set_mouse_visible(False)

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
                                           SPRITE_SCALING_PLAYER)
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
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StageTwoView()
    window.show_view(start_view)
    # start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
