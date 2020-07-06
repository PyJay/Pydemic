import random

import arcade
import pkg_resources

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_VIRUS = 0.1
SPRITE_SCALING_BOG_ROLL = 0.1
SPRITE_SCALING_LASER = 0.8
ROLL_COUNT = 25
PATIENT_SCALING = 0.5
BULLET_SPEED = 5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pydemic"

MOVEMENT_SPEED = 1.5

# sprites
bog_roll = pkg_resources.resource_filename("pydemic", "data/bog_roll.png")
virus_sprite = pkg_resources.resource_filename(
    "pydemic", "data/virus_sprite.png")
dojo = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk1.png"

# music
music = pkg_resources.resource_filename("pydemic", "data/music.mp3")

# textures
day = arcade.load_texture(
    pkg_resources.resource_filename("pydemic", "data/day.png"))
night = arcade.load_texture(
    pkg_resources.resource_filename("pydemic", "data/night.png"))
success = arcade.load_texture(
    pkg_resources.resource_filename("pydemic", "data/success.png"))
dystopia = arcade.load_texture(
    pkg_resources.resource_filename("pydemic", "data/dystopia.png"))
virus = arcade.load_texture(
    pkg_resources.resource_filename("pydemic", "data/virus.png"))
sunrise = arcade.load_texture(
    pkg_resources.resource_filename("pydemic", "data/sunrise.png"))


def set_background(texture): return arcade.draw_lrwh_rectangle_textured(
    0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, texture)


class StageMenuBase(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        arcade.start_render()
        set_background(night)
        arcade.draw_text(self.main_text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=25, anchor_x="center")
        arcade.draw_text(self.sub_text,
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_view(self.instruction_view())


class StageInstructionsBase(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(self.main_text,
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=25, anchor_x="center")
        arcade.draw_text(self.sub_text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_view = self.game_view()
            game_view.setup()
            self.window.show_view(game_view)


class FinalMenu(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        arcade.start_render()
        set_background(sunrise)
        arcade.draw_text("You have fully recovered from the infection.\n"
                         "The rates have started to drop \n"
                         "and things are looking promising.\n"
                         "Congratulations Doris!", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.AZURE, font_size=25, anchor_x="center")
        arcade.draw_text("Press Enter to restart", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.AZURE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            menu_view = StageOneMenu()
            self.window.show_view(menu_view)


class SuccessView(arcade.View):
    def __init__(self, next_stage_view):
        super().__init__()
        sound = arcade.load_sound(":resources:sounds/upgrade1.wav")
        arcade.play_sound(sound)
        self.next_stage_menu = next_stage_view

    def on_show(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

    def on_draw(self):
        arcade.start_render()
        set_background(success)
        arcade.draw_text("Success!", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.FOLLY, font_size=35, anchor_x="center")
        arcade.draw_text("Press Enter to advance", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.FOLLY, font_size=30, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_view(self.next_stage_menu())


class GameOverView(arcade.View):
    # TODO: you can reset variables in the init
    # TODO: you can add some context about where you were killed
    def __init__(self):
        sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        arcade.play_sound(sound)
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        set_background(dystopia)
        arcade.draw_text("Game Over - you were infected", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.CANARY_YELLOW, font_size=35, anchor_x="center")
        arcade.draw_text("Press Enter to restart",
                         SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75, arcade.color.CANARY_YELLOW, font_size=30, anchor_x="center")
        # TODO: show scores here

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            menu_view = StageOneMenu()
            self.window.show_view(menu_view)

# Sprite Players


class Player(arcade.Sprite):

    def update(self, up_pressed, down_pressed, left_pressed, right_pressed):
        self.change_x = 0
        self.change_y = 0

        if up_pressed and not down_pressed:
            self.change_y = MOVEMENT_SPEED
        elif down_pressed and not up_pressed:
            self.change_y = -MOVEMENT_SPEED
        if left_pressed and not right_pressed:
            self.change_x = -MOVEMENT_SPEED
        elif right_pressed and not left_pressed:
            self.change_x = MOVEMENT_SPEED

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


class FallingPatient(arcade.Sprite):
    """ Simple sprite that falls down """
    speed = 2

    def update(self):
        """ Move the enemy """
        self.avoided = False
        # Fall down
        self.center_y -= self.speed

        # Did we go off the screen? If so, pop back to the top.
        if self.top < 0:
            self.avoided = True


class RisingPatient(arcade.Sprite):
    """ Simple sprite that falls up """

    def update(self):
        """ Move the enemy """
        self.avoided = False
        # Move up
        self.center_y += 2.5

        # Did we go off the screen? If so, pop back to the bottom.
        if self.bottom > SCREEN_HEIGHT:
            self.avoided = True


class StageBase(arcade.View):
    def __init__(self):
        super().__init__()
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


class StageOne(StageBase):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.player_list = None
        self.roll_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        self.time_left = 30
        self.roll_collect_sound = arcade.load_sound(
            ":resources:sounds/coin1.wav")

        # Don't show the mouse cursor

        arcade.set_background_color(arcade.color.BALL_BLUE)

    def setup(self):
        """ Set up the game and initialize the variables. """
        # self.window.set_mouse_visible(False)
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.roll_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        self.player_sprite = Player(
            dojo,
            SPRITE_SCALING_PLAYER
        )
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the rolls
        for _ in range(ROLL_COUNT):
            # Create the roll instance
            roll = arcade.Sprite(bog_roll,
                                 SPRITE_SCALING_BOG_ROLL)

            # Position the roll
            roll.center_x = random.randrange(SCREEN_WIDTH)
            roll.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the roll to the lists
            self.roll_list.append(roll)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        set_background(day)
        self.roll_list.draw()
        self.player_list.draw()

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.time_left) % 60

        # Figure out our output
        output = f"Time Left: {seconds:02d} days"
        arcade.draw_text(output, 10, 40, arcade.color.BLACK, 14)

        # Output the timer text.

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.roll_list.update()
        self.player_sprite.update(
            self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed)
        # Generate a list of all sprites that collided with the player.
        roll_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.roll_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for roll in roll_hit_list:
            roll.remove_from_sprite_lists()
            arcade.play_sound(self.roll_collect_sound)
            self.score += 1

        self.time_left -= delta_time

        if int(self.time_left) % 60 <= 0 and self.score < 20:
            self.window.show_view(GameOverView())
        elif int(self.time_left) % 60 > 0 and self.score >= 20:
            self.window.show_view(SuccessView(StageTwoMenu))


class StageTwo(StageBase):
    """
    Main application class.
    """

    def __init__(self):
        """ Initialize """

        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.player_list = None
        self.patient_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        self.level = 1
        self.avoided_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        # Don't show the mouse cursor
        # self.set_mouse_visible(False)

        # Set the background color
        arcade.set_background_color(arcade.color.BALL_BLUE)

    def level_1(self):
        for i in range(30):

            # Create the patient instance
            patient = FallingPatient(
                ":resources:images/animated_characters/zombie/zombie_walk0.png", PATIENT_SCALING)

            # Position the patient
            patient.center_x = random.randrange(SCREEN_WIDTH)
            patient.center_y = random.randrange(
                SCREEN_HEIGHT, SCREEN_HEIGHT * 2)

            # Add the patients to the lists
            self.patient_list.append(patient)

    def level_2(self):
        for i in range(30):

            # Create the enemy instance
            patient = RisingPatient(
                ":resources:images/animated_characters/zombie/zombie_walk0.png", PATIENT_SCALING)

            # Position the enemy
            patient.center_x = random.randrange(SCREEN_WIDTH)
            patient.center_y = random.randrange(-SCREEN_HEIGHT, 0)

            # Add the enemy to the lists
            self.patient_list.append(patient)

    def setup(self):
        """ Set up the game and initialize the variables. """

        self.score = 0
        self.level = 1

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.patient_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player(dojo,
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
        set_background(day)

        # Draw all the sprites.
        self.player_sprite.draw()
        self.patient_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 15)

        output = f"Level: {self.level}"
        arcade.draw_text(output, 10, 35, arcade.color.BLACK, 15)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.patient_list.update()
        self.player_sprite.update(
            self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed)

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.patient_list)

        if hit_list:
            self.window.show_view(GameOverView())
        # Loop through each colliding sprite, remove it, and add to the score.
        for patient in self.patient_list:
            if patient.avoided == True:
                self.avoided_patients += 1
                arcade.play_sound(self.avoided_sound)
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

        elif self.score == 60 and self.level == 2:
            self.window.show_view(SuccessView(StageThreeInstructions))


class StageThree(StageBase):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.player_list = None
        self.virus_list = None
        self.bullet_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Don't show the mouse cursor
        # self.set_mouse_visible(False)

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.virus_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Set up the player
        self.score = 0

        # Image from kenney.nl
        self.player_sprite = Player(dojo,
                                    SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)

        # Create the enemies
        for i in range(30):

            # Create the enemy instance
            virus = FallingPatient(
                virus_sprite, SPRITE_SCALING_VIRUS)
            virus.speed = 0.5

            # Position the enemy
            virus.center_x = random.randrange(SCREEN_WIDTH)
            virus.center_y = random.randrange(
                SCREEN_HEIGHT, SCREEN_HEIGHT * 2)

            # Add the enemy to the lists
            self.virus_list.append(virus)

        # Set the background color
        arcade.set_background_color(arcade.color.CORAL_RED)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        set_background(virus)
        # Draw all the sprites.
        self.virus_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        super().on_key_press(key, modifiers)
        if key == arcade.key.SPACE:
            # Gunshot sound
            arcade.play_sound(self.gun_sound)
            # Create a bullet
            bullet = arcade.Sprite(
                ":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

            # The image points to the right, and we want it to point up. So
            # rotate it.
            bullet.angle = 90

            # Give the bullet a speed
            bullet.change_y = BULLET_SPEED

            # Position the bullet
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top

            # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on bullet sprites
        self.bullet_list.update()
        self.player_sprite.update(
            self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed)
        self.virus_list.update()
        # Loop through each bullet
        for bullet in self.bullet_list:
            # TODO: create a Bullet Class and put this there
            # Check this bullet to see if it hit a virus
            hit_list = arcade.check_for_collision_with_list(
                bullet, self.virus_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every virus we hit, add to the score and remove the virus
            for virus in hit_list:
                virus.remove_from_sprite_lists()
                self.score += 1

                # Hit Sound
                arcade.play_sound(self.hit_sound)

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.virus_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        infected = False
        for virus in self.virus_list:
            if virus.avoided == True:
                infected = True
                virus.remove_from_sprite_lists()

        if hit_list or infected:
            self.window.show_view(GameOverView())

        if self.score >= 30:
            self.window.show_view(SuccessView(FinalMenu))


class GameWindow(arcade.Window):

    def __init__(self, *args):
        super().__init__(*args)
        self.music = arcade.Sound(music, streaming=True)

    def setup(self):
        self.music.play(volume=0.1)


class StageOneInstructions(StageInstructionsBase):
    def __init__(self):
        super().__init__()
        self.main_text = "Use the arrow keys to collect 20 bog rolls in 30 days!"
        self.sub_text = "Press Enter to advance"
        self.game_view = StageOne


class StageTwoInstructions(StageInstructionsBase):
    def __init__(self):
        super().__init__()
        self.main_text = "Use the arrow keys to avoid the infected!"
        self.sub_text = "Press Enter to advance"
        self.game_view = StageTwo


class StageThreeInstructions(StageInstructionsBase):
    def __init__(self):
        super().__init__()
        self.main_text = ("Use the arrow keys to move and space bar to shoot\n"
                          "Do not touch the virus or let it pass your defences.")
        self.sub_text = "Press Enter to advance"
        self.game_view = StageThree


class StageOneMenu(StageMenuBase):
    def __init__(self):
        super().__init__()
        self.main_text = ("Welcome! The year is 2020 and a virus\n"
        " from a distant land has reached your nation.\n\n"
        "As leader of the United Queendom,\n"
        " you must do your utmost to save the nation, Doris...")
        self.sub_text = "..but first you need to stock up. Press Enter to advance"
        self.instruction_view = StageOneInstructions


class StageTwoMenu(StageMenuBase):
    def __init__(self):
        super().__init__()
        self.main_text = ("Well done! You stocked up on essentials.\n\n"
        "The pydemic is spreading quickly.\n"
        "Doris, you have to attend several meetings\n"
        " but you must maintain social distancing")
        self.sub_text = "Press Enter to advance"
        self.instruction_view = StageTwoInstructions


class StageThreeMenu(StageMenuBase):
    def __init__(self):
        super().__init__()
        self.main_text = ("You have tried very hard to avoid people\n"
        "Alas, you have still been infected.\n\n"
        "Doris, you must fight the disease\n"
        " your nation depends on you")
        self.sub_text = "Press Enter to advance"
        self.instruction_view = StageThreeInstructions


def main():
    """ Main method """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    start_view = StageOneMenu()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
