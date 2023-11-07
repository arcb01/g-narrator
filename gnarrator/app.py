from os import environ
import keyboard
import json
from pathlib import Path
# Remove pygame welcome message
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from gnarrator.utils.utils import app_print
from gnarrator.reading_engine import ReadingEngine



class App:
    """
    Class that runs the entire application

    `Attributes:`
        clock: Pygame clock object
        app_name: Name of the application
        path: Path to the application folder
        app_logo: Application logo

    `Methods:`
        check_events(): Checks for keyboard events
        clear(): Clears the screen and deletes all screenshots taken
        run(): Main loop of the application
        set_keys(): Sets key bindings
    """

    def __init__(self, settings):
        self.app_name = "G-Narrator"
        self.path = Path("./gnarrator/")
        self.app_logo = pygame.image.load(self.path / "assets" / "logo.png")
        self.clock = pygame.time.Clock()
        self.set_keys()
        pygame.init()

        self.reading_engine = ReadingEngine(settings)

    def set_keys(self):
        """
        Set key bindings
        """

        # Read json file containing key bindings
        with open(self.path / "config" / "keys.json", encoding="utf-8") as json_file:
            k = json.load(json_file)
            self.FULL_SCREEN = k["FULL_SCREEN"]
            self.REGION = k["REGION"]
            self.CLEAR_KEY = k["CLEAR"]
            self.SMALL_N_QUICK = k["SMALL_N_QUICK"]

    def clear(self):
        try:
            # Clear screen
            self.reading_engine.window.clear_screen()
        except:
            # if window is not yet loaded, ignore
            pass  

    def check_events(self):
        """
        Captures any keyboard events
        """

        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.CLEAR_KEY:
            self.clear()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.REGION:
            self.reading_engine.read_screen_regional()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.FULL_SCREEN:
            self.reading_engine.read_screen()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.SMALL_N_QUICK:
            # NOTE: This mode is usually used for small regions
            self.reading_engine.read_screen_small_n_quick()

    def run(self):
        """
        Main loop of the application
        """
        
        app_print()

        while True:
            self.check_events()
            self.clock.tick(60)  