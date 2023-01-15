import ctypes
import pyautogui


def get_disp_size():
    """
    Returns the width and height of the display
    """

    user32 = ctypes.windll.user32
    dwidth, dheight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    
    return dwidth, dheight

def get_mouse_pos():
    """
    Returns the x and y coordinates of the mouse position
    """

    x_mouse_pos = pyautogui.position().x
    y_mouse_pos = pyautogui.position().y

    return x_mouse_pos, y_mouse_pos