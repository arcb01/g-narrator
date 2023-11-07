import ctypes
import pyautogui
import numpy as np


def get_detection_coords(detection : list):
    """
    For a given detection, returns the coordinates of the bounding box
    :param detection: a list containing the bounding box vertices, text, and confidence
    """

    bbox = detection[0]
    top = bbox[0][0]
    left = bbox[0][1]
    width = bbox[1][0] - bbox[0][0]
    height = bbox[2][1] - bbox[1][1]

    return top, left, width, height

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

def app_print():
    """
    Prints that the app is running
    """

    message = "GNarrator is now running. You can minimize this window."
    symbol = "▒"
    width = 60
    padding = (width - len(message)) // 2

    decorative_line = symbol * width
    formatted_message = f"{symbol * padding} {message} {symbol * padding}"
    
    print(decorative_line)
    print(formatted_message)
    print(decorative_line)

def create_arb_reg(cp : tuple, w : int, h : int):
    """
    Creates a rectangle region of arbitrary width
    :param cp: Center point
    :param w: Width
    :returns Region of interest
    """

    top_left = (cp[0] - w/4, cp[1] - w/4)
    region = (top_left[0], top_left[1], w, h)

    return tuple(np.array(region).astype(int))