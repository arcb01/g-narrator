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
        settings: Settings of the application
        reading_engine: Reading engine
        apperance_settings: Apperance settings for the GUI
        app: GUI app

    `Methods:`
        check_events(): Checks for keyboard events
        clear(): Clears the screen and deletes all screenshots taken
        run(): Main loop of the application
        set_keys(): Sets key bindings
        load_apperance_settings(): Loads apperance settings
    """

    def __init__(self, settings):
        self.app_name = "G-Narrator"
        self.path = Path("./gnarrator/")
        self.app_logo = pygame.image.load(self.path / "assets" / "logo.png")
        self.clock = pygame.time.Clock()
        pygame.init()

        # Load settings
        # TODO: Is there a better way to load settings?
        self.settings = settings
        self.load_apperance_settings()
        self.load_key_settings()
        self.settings = {"keys" : {"REGION" : self.REGION, 
                                    "CLEAR" : self.CLEAR_KEY, 
                                    "SMALL_N_QUICK" : self.SMALL_N_QUICK},
                        "apperance" : self.apperance_settings,
                        "capture" : settings}
        self.k_pressed = False
        
        # Load reading engine
        self.reading_engine = ReadingEngine(settings=self.settings["capture"])

        # GUI app
        self.app = QApplication(sys.argv)

    def load_apperance_settings(self):
        with open(self.path / "config" / "apperance.json", encoding="utf-8") as json_file:
            raw = json.load(json_file)
            try:
                tone_settings = raw[self.settings["APPERANCE"]]
                oppacity_settings = raw["oppacity"]
                apperance_settings = {**tone_settings, **oppacity_settings}
            except KeyError:
                print("WARNING: Error when loading apperance settings")

            self.apperance_settings = apperance_settings

    def load_key_settings(self):
        # Read json file containing key bindings
        with open(self.path / "config" / "keys.json", encoding="utf-8") as json_file:
            k = json.load(json_file)
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

        if keyboard.is_pressed(self.CLEAR_KEY):
            self.clear()

        # if key1 + key2 and... key3 are pressed
        if keyboard.is_pressed(self.REGION.split("+")[:1]):
            self.k_pressed = True
        elif keyboard.is_pressed(self.REGION.split("+")[-1]) and self.k_pressed:
            # Create the paint window (mode tunes the oppacity)
            paint_window = Window(settings=self.settings, mode="regional")
            paint_widget = RegionMode(window=paint_window, reading_engine=self.reading_engine, 
                                    settings=self.settings)
            paint_window.setCentralWidget(paint_widget)
            paint_window.show()
            self.app.exec_()
            self.k_pressed = False

        # if key1 + key2 and... key3 are pressed
        if keyboard.is_pressed(self.SMALL_N_QUICK.split("+")[:1]):
            self.k_pressed = True
        elif keyboard.is_pressed(self.SMALL_N_QUICK.split("+")[-1]) and self.k_pressed:
            window = Window(settings=self.settings, mode="snq")
            self.content = self.reading_engine.read_screen(mode="snq", window=window)
            if self.reading_engine.detectionsFound():
                self.content.show()
                self.reading_engine.say_content_immediatly()
                self.app.exec_()
                self.k_pressed = False

    def run(self):
        """
        Main loop of the application
        """
        
        app_print()

        while True:
            self.check_events()
            self.clock.tick(60)  