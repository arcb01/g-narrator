import ctypes
import pyautogui
import pygame
import numpy as np
from sklearn.neighbors import KDTree


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

def loading_screen(screen):
    """
    Loading screen while OCR is running
    """

    font = pygame.font.SysFont("couriernew", 90)
    text = []
    text.append((font.render("Reading screen", 0, (0, 255, 0)), (25, 25)))
    for t in text:
        screen.blit(t[0], t[1])
    pygame.display.update()

def clear_screen(screen):
    """
    Clears the screen
    """
    transparent = (255, 0, 128)
    screen.fill(transparent)
    pygame.display.update()

def closest_nodes(node: tuple, nodes: list):
    """
    Given a node, in this case the mouse position, this function
    returns the k nearest points from all detections.
    :param node: Tuple containing the x and y coordinates of the mouse position
    :param nodes: List of tuples containing the x and y coordinates for 
                all points of every detection
    """

    neighbours = 4

    kdtree = KDTree(np.asarray(nodes).reshape(-1, 2))
    _, ind = kdtree.query(np.asarray(node).reshape(1, -1), k=neighbours)

    return np.squeeze(np.asarray(nodes)[ind]).tolist()

def app_print():
    """
    Prints that the app is running
    """

    message = "Gaming Narrator is now running"
    symbol = "▒"
    width = 60
    padding = (width - len(message)) // 2

    decorative_line = symbol * width
    formatted_message = f"{symbol * padding} {message} {symbol * padding}"
    
    print(decorative_line)
    print(formatted_message)
    print(decorative_line)


