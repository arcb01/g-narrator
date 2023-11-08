from os import environ
import keyboard
import json
from pathlib import Path
# Remove pygame welcome message
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from gnarrator.utils.utils import app_print
from gnarrator.reading_engine import ReadingEngine
from gnarrator.windows import Window, RegionMode
import sys
from PyQt5.QtWidgets import QApplication


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
        self.settings = settings
        self.set_keys()
        pygame.init()

        # Load settings
        self.settings = settings
        self.load_apperance_settings()

        self.reading_engine = ReadingEngine(settings=self.settings)
        self.app = QApplication(sys.argv)

    def load_apperance_settings(self):
        # FIXME
        with open(self.path / "config" / "apperance.json", encoding="utf-8") as json_file:
            raw = json.load(json_file)
            try:
                apperance_settings = raw[self.settings["APPERANCE"]]
            except KeyError:
                print("WARNING: Apperance setting not found, using light as default")
                apperance_settings = raw["light"]

            self.apperance_settings = apperance_settings

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
            self.content.clear_screen()
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
            paint_window = Window(settings=self.apperance_settings, mode="regional")
            paint_widget = RegionMode(paint_window, self.reading_engine)
            paint_window.setCentralWidget(paint_widget)
            paint_window.show()
            self.app.exec_()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.FULL_SCREEN:
            window = Window(settings=self.apperance_settings, mode="full")
            self.content = self.reading_engine.read_screen(mode="full", window=window)
            self.content.show()
            self.app.exec_()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.SMALL_N_QUICK:
            # NOTE: This mode is usually used for small regions
            # FIXME:
            self.reading_engine.read_screen_small_n_quick()

    def run(self):
        """
        Main loop of the application
        """
        
        app_print()

        while True:
            self.check_events()
            self.clock.tick(60)  