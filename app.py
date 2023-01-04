import sys, keyboard, pyautogui
import pygame, win32api, win32con, win32gui
import ctypes

from TTS import Narrator
from ocr import OCR


READ_CONTENT = 'm'
QUICK_READ = 'º'
REPEAT_KEY = 'r'
QUIT_KEY = 'esc'


class App:
    """
    Class that runs the entire application

    `Attributes:`
        bbox_color: color of the bounding box that is drawn around the text
        rect_width: width of the bounding box
        narrator: An object of the Narrator class that is used to read the text
        OCR: An object of the OCR class that is used to detect text
        clock: Pygame clock object

    `Methods:`
        get_disp_size(): Get the width and height of the display
        get_mouse_pos(): Returns the x and y coordinates of the mouse position
        check_events(): Checks for keyboard events
        load_display(): Loads the display window
        draw_detection(detection): For a given detection, draw a bounding box around the text
        run(): Main loop of the application
    """

    def __init__(self, narrator: object, OCR: object):
        self.bbox_color = (170, 255, 0)
        self.rect_width = 4
        self.narrator = narrator
        self.OCR = OCR
        self.clock = pygame.time.Clock()
        pygame.init()

    def get_disp_size(self):
        """
        Returns the width and height of the display
        """

        user32 = ctypes.windll.user32
        dwidth, dheight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return dwidth, dheight

    def get_mouse_pos(self):
        """
        Returns the x and y coordinates of the mouse position
        """

        x_mouse_pos = pyautogui.position().x
        y_mouse_pos = pyautogui.position().y
        return x_mouse_pos, y_mouse_pos

    def check_events(self):
        """
        Captures any keyboard events
        """

        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN and event.name == QUIT_KEY:
            print("\n ==== Stopping... ====\n")

            self.narrator.say("Quitting")

            # Delete all images and quit
            self.OCR.delete_imgs()
            sys.exit()

        if event.event_type == keyboard.KEY_DOWN and event.name == READ_CONTENT:
            # Get mouse position
            x, y = self.get_mouse_pos()
            # Load display
            self.load_display()
            # Start OCR
            if self.OCR.check_start():
                self.OCR.start()
            else:
                pass
            # Find nearest detection from the mouse position
            nearest_detection = self.OCR.find_nearest_detection(x, y)
            # Draw detection
            self.draw_detection(nearest_detection)
            # Text to speech
            self.narrator.say(self.output_text)
            
        if event.event_type == keyboard.KEY_DOWN and event.name == REPEAT_KEY:
            # Repeat text a little bit slower
            self.narrator.slower_saying(self.output_text)

        if event.event_type == keyboard.KEY_DOWN and event.name == QUICK_READ:
            # Load display
            self.load_display()
            # Start OCR
            self.OCR.start()
            # Get all detections
            for detection in self.OCR.get_all_detections():
                # Draw detection
                self.draw_detection(detection)
                # Text to speech
                self.narrator.say(self.output_text)

    def load_display(self):
        """
        Loads the display window
        """
        # https://stackoverflow.com/questions/550001/fully-transparent-windows-in-pygame

        pygame.init()
        w, h = self.get_disp_size()
        self.screen = pygame.display.set_mode((w, h)) # For borderless, use pygame.NOFRAME
        fuchsia = (255, 0, 128)  # Transparency bbox_color
        # Lock window to top
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

    def draw_detection(self, detection : list):
        """
        For a given detection, draw a bounding box around the text
        :param detection: a list containing the bounding box vertices, text, and confidence
        """
    
        self.clear_screen()
        bbox = detection[0]
        self.output_text = detection[1]
        top = bbox[0][0]
        left = bbox[0][1]
        width = bbox[1][0] - bbox[0][0]
        height = bbox[2][1] - bbox[1][1]
        pygame.draw.rect(self.screen, self.bbox_color,  pygame.Rect(top, left, 
                                                            width, height), 
                        self.rect_width)
        pygame.display.update()


    def run(self):
        """
        Main loop of the application
        """

        print("\n ==== App is running... ====")
        while True:
            self.clock.tick(60)
            self.check_events()
            
            
if __name__ == "__main__":

    lang = "en"
    en_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
    es_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"

    if lang == "en":
        voice = en_voice
    elif lang == "es":
        voice = es_voice

    tts = Narrator(voice=voice)
    ocr = OCR(lang=lang)
    a = App(tts, ocr)
    a.run()


    # ========== TODO ==========
    # Paragraph detection
    #   1. New OCR? New detection algorithm?
    #   2. Test all cases with paragraph=True. See results


    # ========== BUG ==========
    # 4. Pressing m too consistantly causes the program to bug out

    # ========== FIXME ==========
    # 2. Display issues with the calling order

    # ========== FUTURE WORK ==========
    # 1. Add a GUI
    # 2. Only way of speeding up is speeding up EasyOCR or replacing it.
    #   OCR Alternatives:
            # 1. https://github.com/PaddlePaddle/PaddleOCR
            # 2. https://github.com/mindee/doctr

    # 3. Language understanding for bulding sentences

   # ========== References ==========
   # 1. https://github.com/nathanaday/RealTime-OCR
