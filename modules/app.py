from os import environ
import sys, keyboard, pyautogui
import win32gui, win32com.client, json
import win32api, win32con, win32gui
# Remove pygame welcome message
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

from ocr import OCR
from TTS import Narrator
from utils.utils import get_disp_size, app_print


class App:
    """
    Class that runs the entire application

    `Attributes:`
        rect_width: width of the bounding box
        narrator: An object of the Narrator class that is used to read the text
        OCR: An object of the OCR class that is used to detect text
        clock: Pygame clock object
        switch_detection: Boolean that enables swtiching between detections
        det_idx: Index of the current detection
        highlighted_color: Color that highlights the current bounding box
        dimmed_color: Color of the unselected bounding boxes

    `Methods:`
        check_events(): Checks for keyboard events
        load_display(): Loads the display window
        draw_detection(detection): For a given detection, draw a bounding box around the text
        quit(): Clears the screen and deletes all screenshots taken
        end_of_list(): Checks if the current detection is the last one
        read_screen(): Main reading function. 
        read_out_loud(slow: bool): TTS
        run(): Main loop of the application
        set_keys(): Sets key bindings
    """

    def __init__(self, narrator: object, OCR: object):
        self.app_name = "Gaming Narrator"
        self.app_logo = pygame.image.load('./assets/logo.png')
        self.rect_width = 4
        self.narrator = narrator
        self.OCR = OCR
        self.clock = pygame.time.Clock()
        self.switch_detection = False
        self.engaging = False
        self.dimmed_color = (70, 96, 0)
        self.highlighted_color = (170, 255, 0)
        self.set_keys()
        pygame.init()

    def set_keys(self):
        """
        Set key bindings
        """

        # Read json file containing key bindings
        with open('./config/keys.json') as json_file:
            k = json.load(json_file)
            self.CAPTURE = k["CAPTURE"]
            self.SWITCH_DET_FORWARD = k["SWITCH_FORWARD"]
            self.SWITCH_DET_BACKWARD = k["SWITCH_BACKWARD"]
            self.REPEAT_KEY = k["REPEAT"]
            self.READ_NEAREST = k["READ_NEAREST"]
            self.READ_OUT_LOUD = k["READ_OUT_LOUD"]
            self.QUIT_KEY = k["QUIT"]

    def quit(self):
        try:
            if len(self.OCR.get_all_detections()) > 0:
                self.OCR.empty_results()
                self.narrator.say("Clearing screen.")
                self.clear_screen()
                pygame.display.update()
                # Delete all images 
                self.OCR.delete_imgs()
        except:
            pass

    def end_of_list(self):
        return True if self.det_idx == len(self.OCR.get_all_detections()) - 1 else False

    def read_screen(self):
        """
        Main function that reads the screen content using OCR.
        """

        self.det_idx = 0
        self.engaging = True
        # Load pygame window 
        self.load_display()
        # Start OCR
        self.OCR.send_screen(self.screen) # Used for adding a loading screen.
        self.OCR.start()
        if len(self.OCR.get_all_detections()) > 0:
            # For every detection found, draw a colored bounding box around it.
            for detection in self.OCR.get_all_detections():
                self.draw_detection(detection, color=self.dimmed_color)
            # Highlight first detection
            self.draw_detection(self.OCR.get_all_detections()[self.det_idx], color=self.highlighted_color)

    def read_out_loud(self, slow=False):
        """
        Text to speech function that reads out loud the text inside the 
        selected detection.
        :param slow: If True, the text will be read out loud slowly.
        """
        
        assert len(self.OCR.get_all_detections()) > 0, "No detections found yet. Please start scanning first."
        text = self.OCR.get_all_detections()[self.det_idx][1]

        if not slow:
            self.narrator.say(text)
        else:
            self.narrator.slower_saying(text)

    def check_events(self):
        """
        Captures any keyboard events
        """

        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.QUIT_KEY:
            self.quit()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.READ_NEAREST:
            pass
            # NOTE: This is not implemented yet. Code in alternative branch.

        if event.event_type == keyboard.KEY_DOWN and event.name == self.CAPTURE:
            self.read_screen()

        if event.event_type == keyboard.KEY_DOWN and event.name in [self.SWITCH_DET_FORWARD, self.SWITCH_DET_BACKWARD]:
            assert len(self.OCR.get_all_detections()) > 0, "No detections found yet. Please start scanning first."

            if not self.end_of_list():
                if event.name == self.SWITCH_DET_BACKWARD:
                    if self.det_idx == 0: # The first bbox
                        self.draw_detection(self.OCR.get_all_detections()[self.det_idx], color=self.dimmed_color)
                        self.det_idx = len(self.OCR.get_all_detections()) - 1
                        self.draw_detection(self.OCR.get_all_detections()[self.det_idx], color=self.highlighted_color)
                    elif self.det_idx > 0: # Not the first bbox
                        self.draw_detection(self.OCR.get_all_detections()[self.det_idx], color=self.dimmed_color)
                        self.draw_detection(self.OCR.get_all_detections()[self.det_idx - 1], color=self.highlighted_color)
                        self.det_idx  -= 1
                elif event.name == self.SWITCH_DET_FORWARD:
                    self.draw_detection(self.OCR.get_all_detections()[self.det_idx], color=self.dimmed_color)
                    self.draw_detection(self.OCR.get_all_detections()[self.det_idx + 1], color=self.highlighted_color)
                    self.det_idx  += 1
            else:
                if event.name == self.SWITCH_DET_FORWARD:
                    # Loop back to start
                    self.draw_detection(self.OCR.get_all_detections()[self.det_idx], color=self.dimmed_color)
                    self.det_idx = 0
                    self.draw_detection(self.OCR.get_all_detections()[self.det_idx], color=self.highlighted_color)
                else:
                    self.draw_detection(self.OCR.get_all_detections()[self.det_idx], color=self.dimmed_color)
                    self.draw_detection(self.OCR.get_all_detections()[self.det_idx - 1], color=self.highlighted_color)
                    self.det_idx  -= 1

        if event.event_type == keyboard.KEY_DOWN and event.name == self.READ_OUT_LOUD:
            self.read_out_loud()

        if event.event_type == keyboard.KEY_DOWN and event.name == self.REPEAT_KEY:
            self.read_out_loud(slow=True)

    def load_display(self):
        """
        Loads the display window
        """

        pygame.init()
        w, h = get_disp_size()
        self.screen = pygame.display.set_mode((w, h)) # For borderless, use pygame.NOFRAME
        pygame.display.set_caption(self.app_name)
        pygame.display.set_icon(self.app_logo)
        fuchsia = (255, 0, 128)  # Transparency bbox_color
        # Lock window on top
        win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        # Create layered window
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        # Set window transparency bbox_color
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

        self.screen.fill(fuchsia)  # Transparent background
        self.clear_screen = lambda : self.screen.fill(fuchsia)

        pygame.display.update()


    def draw_detection(self, detection : list, color : tuple = (170, 255, 0)):
        """
        For a given detection, draw a bounding box around the text
        :param detection: a list containing the bounding box vertices, text, and confidence
        :param color: the color of the bounding box
        """
    
        #self.clear_screen()
        bbox = detection[0]
        self.output_text = detection[1]
        top = bbox[0][0]
        left = bbox[0][1]
        width = bbox[1][0] - bbox[0][0]
        height = bbox[2][1] - bbox[1][1]
        pygame.draw.rect(self.screen, color,  pygame.Rect(top, left, 
                                                            width, height), 
                        self.rect_width)
        pygame.display.update()

    def run(self):
        """
        Main loop of the application
        """
        
        self.OCR.delete_imgs() # Clear folder
        
        app_print()

        while True:
            self.check_events()
            self.clock.tick(60)


def settings(lang : str, gpu : bool, voice_speed : int):

    en_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
    es_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"

    if lang == "en":
        voice = en_voice
    elif lang == "es":
        voice = es_voice

    tts = Narrator(voice=voice, voice_speed=voice_speed)
    ocr = OCR(lang=lang, gpu=gpu)

    return tts, ocr
