import cv2 as cv
import numpy as np

from threading import Lock
from threading import Thread
from time import time, sleep



class Vision:
    # properties
    targets = []
    fps = 1

    # constructor
    def __init__(self):
        self.lock = Lock()

      # gets X and Y coordinates of enemies
    def get_enemy_coordinates(self, screenshot):
        # converting screen to grayscale
        screen = cv.cvtColor(screenshot, cv.COLOR_RGB2GRAY)
        # finding white text (enemies)
        ret, enemies = cv.threshold(screen, 254, 255, cv.THRESH_BINARY)
        # forms a white bar in order to get the X and Y coordinates with the findContours and rectangle cv functions
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (50, 5))
        enemies = cv.morphologyEx(enemies, cv.MORPH_CLOSE, kernel)
        (contours, hierarchy) = cv.findContours(
            enemies, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # extracting enemy x and y coordinates from contours
        targets = []
        append = targets.append
        for c in contours:
            if cv.contourArea(c) > 50:
                x, y, w, h = cv.boundingRect(c)
                target = ((x + w / 2), (y + h / 2))
                append(target)
        return targets

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            start = time()
            targets = self.get_enemy_coordinates()
            with self.lock:
                self.targets = targets
            self.fps = round(1.0 / (time() - start), 1)
            sleep(0.005)

    def draw_circles(self, img, circles):
        # these colors are actually BGR
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (center_x, center_y) in circles:
            # determine the box positions
            #point = (center[0], center[1])
            cv.circle(img, (int(center_x), int(center_y)), 20, line_color, lineType=line_type)

        return img