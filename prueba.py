import pyautogui
import easyocr
import time
import numpy as np

def take_screenshot(region):
        """
        Function that takes a screenshot and save it in imgs_dir
        """
        myScreenshot = pyautogui.screenshot(region=region)
        filename = "./screenshot.png"
        myScreenshot.save(filename)


# Taking a cropped screenshot
import keyboard
import pyautogui

n_pressed = False
start_x, start_y = 0, 0

def on_key_event(event):
    global n_pressed, start_x, start_y

    if event.event_type == keyboard.KEY_DOWN and event.name == "n" and not n_pressed:
        start_x, start_y = pyautogui.position().x, pyautogui.position().y
        print("n pressed")
        n_pressed = True

    if event.event_type == keyboard.KEY_UP and event.name == "n":
        end_x, end_y = pyautogui.position().x, pyautogui.position().y
        print("n released")
        n_pressed = False

        region = (
            min(start_x, end_x),
            min(start_y, end_y),
            abs(end_x - start_x),
            abs(end_y - start_y)
        )

        take_screenshot(region)

        # TODO read text

keyboard.hook(on_key_event)


# TODO: Transforming coordinates

shight, swidth  = 1440, 3440
p_top_reg = (start_x, start_y)

sample_bbox = [[400, 100], [500, 100], [500, 200], [400, 200]]

pi_x = 1700
pi_y = 700

sample_bbox = np.array([[400, 100], [500, 100], [500, 200], [400, 200]])
# mapping
sample_bbox_arr = sample_bbox + np.array([pi_x, pi_y])

print(sample_bbox_arr)

def map_coordinates_to_screen(coord_list, p_top_reg):
    pi_x, pi_y = p_top_reg
    coord_list = np.array(coord_list, dtype=np.int32)
    coord_list = coord_list + np.array([pi_x, pi_y])
    return coord_list

