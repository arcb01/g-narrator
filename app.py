import sys, keyboard, pyautogui
import pygame, win32api, win32con, win32gui
import win32gui, win32com.client

from TTS import Narrator
from ocr import OCR
from utils import *

# Key bindings
START_READING = 'º'
SWITCH_DETECTION = 'n'
REPEAT_KEY = 'r'
READ_NEAREST = 'h'
READ_OUT_LOUD = '-'
QUIT_KEY = 'q'


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
        run(): Main loop of the application
    """

    def __init__(self, narrator: object, OCR: object):
        self.rect_width = 4
        self.narrator = narrator
        self.OCR = OCR
        self.clock = pygame.time.Clock()
        self.switch_detection = False
        self.engaging = False
        self.dimmed_color = (65, 94, 0)
        self.highlighted_color = (170, 255, 0)


    def quit(self):
        print("\n ==== Stopping... ====\n")

        self.narrator.say("Quitting Narrator")
        # Delete all images and quit
        self.OCR.delete_imgs()
        sys.exit()


    def end_of_list(self):
        return True if self.det_idx == len(self.OCR.get_all_detections()) - 1 else False


    def check_events(self):
        """
        Captures any keyboard events
        """

        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN and event.name == QUIT_KEY:
            self.quit()

        if event.event_type == keyboard.KEY_DOWN and event.name == READ_NEAREST:
            # Get mouse position
            x, y = get_mouse_pos()
            # Load display
            self.load_display()
            # Start OCR
            #if self.OCR.check_start():
            self.OCR.start()
            #else:
                #pass
            # Find nearest detection from the mouse position
            nearest_detection = self.OCR.find_nearest_detection(x, y)
            # Draw detection
            self.draw_detection(nearest_detection)
            # Text to speech
            self.narrator.say(self.output_text)
            
        if event.event_type == keyboard.KEY_DOWN and event.name == REPEAT_KEY:
            # Repeat text a little bit slower
            self.narrator.slower_saying(self.output_text)

        if event.event_type == keyboard.KEY_DOWN and event.name == START_READING:
            self.load_display(bring_to_foreground=True)
            self.det_idx = 0
            self.engaging = True
            # Start OCR
            self.OCR.start()
            if len(self.OCR.get_all_detections()) > 0:
                # Draw all possible OCR detections
                for detection in self.OCR.get_all_detections():
                    self.draw_detection(detection, color=self.dimmed_color)
                # Highlight first detection
                self.draw_detection(self.OCR.get_all_detections()[self.det_idx], color=self.highlighted_color)

        if event.event_type == keyboard.KEY_DOWN and event.name == SWITCH_DETECTION:
            if not self.end_of_list():
                self.det_idx  += 1
                # Apply highlighted color to current detection
                self.draw_detection(self.OCR.get_all_detections()[self.det_idx], color=self.highlighted_color)
                # Apply dimmed color to previous detection
                self.draw_detection(self.OCR.get_all_detections()[self.det_idx - 1], color=self.dimmed_color)
            else:
                # Apply dimmed color to previous detection
                self.draw_detection(self.OCR.get_all_detections()[self.det_idx], color=self.dimmed_color)
                self.det_idx = 0
                # Apply highlighted color to current detection
                self.draw_detection(self.OCR.get_all_detections()[self.det_idx], color=self.highlighted_color)


        if event.event_type == keyboard.KEY_DOWN and event.name == READ_OUT_LOUD:
            # Read text of current detection
            self.narrator.say(self.OCR.get_all_detections()[self.det_idx][1])


    def load_display(self, bring_to_foreground=False):
        """
        Loads the display window
        """
        # https://stackoverflow.com/questions/550001/fully-transparent-windows-in-pygame
        pygame.init()
        w, h = get_disp_size()
        self.screen = pygame.display.set_mode((w, h)) # For borderless, use pygame.NOFRAME
        fuchsia = (255, 0, 128)  # Transparency bbox_color
        # Lock window to top
        # win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        # Create layered window
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        # Set window transparency bbox_color
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

        self.screen.fill(fuchsia)  # Transparent background
        self.clear_screen = lambda : self.screen.fill(fuchsia)

        if bring_to_foreground:
            # Bring window to foregorund (to be able to see the bboxes)
            toplist = []
            winlist = []

            def enum_callback(hwnd, results):
                winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

            win32gui.EnumWindows(enum_callback, toplist)
            window = [(hwnd, title) for hwnd, title in winlist if 'pygame' in title.lower()]
            window_id = window[0]
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            win32gui.SetForegroundWindow(window_id[0])
        
        pygame.display.update()


    def draw_detection(self, detection : list, color : tuple = (170, 255, 0)):
        """
        For a given detection, draw a bounding box around the text
        :param detection: a list containing the bounding box vertices, text, and confidence
        """
    
        #self.clear_screen()
        bbox = detection[0]
        self.output_text = detection[1]
        top = bbox[0][0]
        left = bbox[0][1]
        width = bbox[1][0] - bbox[0][0]
        height = bbox[2][1] - bbox[1][1]

        #s = pygame.Surface((width,height), pygame.SRCALPHA, 32)   # per-pixel alpha
        #s.fill((255, 0, 128, 80))                         # notice the alpha value in the color
        #self.screen.blit(s, (top, left))

        pygame.draw.rect(self.screen, color,  pygame.Rect(top, left, 
                                                            width, height), 
                        self.rect_width)
        pygame.display.update()


    def run(self):
        """
        Main loop of the application
        """

        print("\n ==== App is running... ====")
        while True:
            self.check_events()
            self.clock.tick(60)

            pygame.display.flip()
            
            

        
        
if __name__ == "__main__":

    lang = "es"
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
    # 1. Play the game and see what is needed


    # ========== BUG ==========
    # When clicking º for second time, bboxes flashes

    # ========== FIXME ==========
    # 1. Able to press esc at any time to exit. Fails while tts is reading something
    # 2. Check what key binding errors before presseing the start button (º)

    # ========== FUTURE WORK ==========
    # 1. Add a GUI
    # 2. Only way of speeding up is speeding up EasyOCR or replacing it.
    #   OCR Alternatives:
            # 1. https://github.com/PaddlePaddle/PaddleOCR
            # 2. https://github.com/mindee/doctr

    # 3. Language understanding for bulding sentences

   # ========== References ==========
   # 1. https://github.com/nathanaday/RealTime-OCR
