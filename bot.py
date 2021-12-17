import pyautogui
import keyboard
from pynput.mouse import Button, Controller

from time import time, sleep

class BotAction:
    offset_x = 0
    offset_y = 0
    window_w = 0
    window_h = 0
    mouse = Controller()

    def __init__ (self, offset_x, offset_y, window_w, window_h):
        self.x = 6
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.window_w = window_w
        self.window_h = window_h

    def turn_camera(self, distance):
            x = (self.offset_x + self.window_w / 2)
            y = (self.offset_y + self.window_h / 2)
            pyautogui.moveTo(x, y)
            self.mouse.press(Button.right)
            pyautogui.moveTo(distance, 0)
            self.mouse.release(Button.right)
            sleep(0.2)