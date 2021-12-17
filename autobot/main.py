from re import S
import cv2 as cv
import numpy as np
import os
from time import time
from botcapture import WindowCapture
from botvision import Vision
from botutils import Utils
import configparser
from botaction import BotActions, BotState

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

path = os.path.dirname(os.path.abspath(__file__)) + '/settings.ini'
Config = configparser.ConfigParser()
Config.read(path)
UI_info = Config.get('Settings', 'UI_info')
abilities = Config.get('Settings', 'Abilities').split(",")

# initialize the WindowCapture class
wincap = WindowCapture('RPG HF : CannaDruid')
vis = Vision()
utils = Utils(wincap.offset_x, wincap.offset_y, wincap.w, wincap.h,
                  UI_info)
bot = BotActions(wincap.offset_x, wincap.offset_y, wincap.w, wincap.h, 5, abilities)
bot.start()
loop_time = time()
while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    bot.update_targets(vis.get_enemy_coordinates(screenshot))
    bot.update_hp(utils.player_health(screenshot), utils.enemy_health(screenshot))
    enemies = vis.get_enemy_coordinates(screenshot)
    enemies_img = vis.draw_circles(screenshot, enemies)

    #Enemy Health bar possition
    line_color = (0, 255, 0)
    line_type = cv.LINE_4
    top_left = (utils.enemy_hp_x_pos, utils.enemy_hp_y_pos)
    bottom_right = (utils.enemy_hp_x_pos + utils.enemy_hp_bar_width, utils.enemy_hp_y_pos + utils.enemy_hp_bar_height)
    health = cv.rectangle(screenshot, top_left, bottom_right, line_color, lineType=line_type)
    #Enemy Health bar possition
    line_color = (0, 255, 0)
    line_type = cv.LINE_4
    top_left = (utils.player_hp_x_pos, utils.player_hp_y_pos)
    bottom_right = (utils.player_hp_x_pos + utils.player_hp_bar_width, utils.player_hp_y_pos + utils.player_hp_bar_height)
    health = cv.rectangle(screenshot, top_left, bottom_right, line_color, lineType=line_type)

    #refresh health percentage
    utils.current_enemy_health = utils.enemy_health(screenshot)
    utils.current_player_health = utils.player_health(screenshot)

    scale_percent = 60
    width = int(enemies_img.shape[1] * scale_percent / 100)
    height = int(enemies_img.shape[0] * scale_percent / 100)
    dim = (width, height)
    font = cv.FONT_HERSHEY_SIMPLEX
    resized = cv.resize(screenshot, dim, interpolation=cv.INTER_LINEAR)
    resized = cv.putText(resized, f"player health: {utils.current_player_health}%",
                          (210, height - 85), font, 1, (0, 255, 0), 2, cv.LINE_AA)
    resized = cv.putText(resized, f"enemy health: {utils.current_enemy_health}%",
                          (210, height - 55), font, 1, (0, 255, 0), 2, cv.LINE_AA)

    cv.imshow('Computer Vision', resized)

    #print('prvni loop' + str(loop_time))
    # debug the loop rate
    #print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    #print('druhy loop' + str(loop_time))

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')