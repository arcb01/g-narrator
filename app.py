
import sys, keyboard, pyautogui
import pygame, win32api, win32con, win32gui
import ctypes
from TTS import Narrator
from OCR import OCR


READ_CONTENT = 'm'
REPEAT_KEY = 'r'



class App:

    def __init__(self, narrator, OCR):
        self.color = (170, 255, 0)
        self.rect_width = 4
        self.narrator = narrator
        self.OCR = OCR
        pygame.init()

    def get_disp_size(self):
        user32 = ctypes.windll.user32
        dwidth, dheight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return dwidth, dheight

    def get_mouse_pos(self):
        x_mouse_pos = pyautogui.position().x
        y_mouse_pos = pyautogui.position().y
        return x_mouse_pos, y_mouse_pos

    def check_events(self):

        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN and event.name == 'esc':
            print("\n ==== Stopping... ====\n")
            self.narrator.say("Quitting")
            # Delete all images
            self.OCR.delete_imgs()
            sys.exit()

        if event.event_type == keyboard.KEY_DOWN and event.name == READ_CONTENT:
            x, y = self.get_mouse_pos()
            switch = False

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


    def load_display(self):
        # https://stackoverflow.com/questions/550001/fully-transparent-windows-in-pygame
        pygame.init()
        w, h = self.get_disp_size()
        self.screen = pygame.display.set_mode((w, h)) # For borderless, use pygame.NOFRAME
        done = False
        fuchsia = (255, 0, 128)  # Transparency color
        # Keep on top
        win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        # Create layered window
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        # Set window transparency color
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

        self.screen.fill(fuchsia)  # Transparent background
        self.clear_screen = lambda : self.screen.fill(fuchsia)

        pygame.display.update()

    def draw_detection(self, detection):
        
        #self.clear_screen()
        #for detection in self.result:
            #self.clear_screen()
        bbox = detection[0]
        self.output_text = detection[1]
        top = bbox[0][0]
        left = bbox[0][1]
        width = bbox[1][0] - bbox[0][0]
        height = bbox[2][1] - bbox[1][1]
        pygame.draw.rect(self.screen, self.color,  pygame.Rect(top, left, 
                                                            width, height), 
                        self.rect_width)
        pygame.display.update()


    def run(self):
        print("\n ==== App is running... ====")
        while True:
            self.check_events()
            
            
if __name__ == "__main__":

    n = Narrator()
    o = OCR()
    a = App(n, o)
    a.run()

    # ========== TODO ==========
    # 3. Join sentences?

    # ========== BUG ==========
    # 4. Pressing m too consistantly causes the program to bug out

    # ========== FIXME ==========
    # 1. Fix the narrator variables

    # ========== FUTURE WORK ==========
    # 2: Only way of speeding up is speeding up EasyOCR.

   # ========== Other ==========
   #1. OCR2
   # https://github.com/nathanaday/RealTime-OCR
