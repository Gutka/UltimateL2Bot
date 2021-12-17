import keyboard
import pyautogui

from threading import Lock, Thread
from pynput.mouse import Button, Controller
from time import time, sleep
from math import sqrt
import numpy as np

class BotState:
    INITIALIZING = 0
    SEARCHING = 1
    ATTACKING = 2
    PICKING = 3
    REBUFFING = 4

class BotActions:

    init_seconds = 4

    # threading
    stopped = True
    lock = None

    # properties
    state = None
    targets = []
    offset_x = 0
    offset_y = 0
    window_w = 0
    window_h = 0
    player_health = 100
    enemy_health = 0
    buffed = True
    mouse = Controller()

    def __init__(self, offset_x, offset_y, w, h, init_seconds, abilities):
        self.lock = Lock()

        self.offset_x = offset_x
        self.offset_y = offset_y
        self.window_w = w
        self.window_h = h

        self.init_seconds = init_seconds
        self.state = BotState.INITIALIZING

        self.DEBUFF = abilities[0]
        self.DAMAGE = abilities[1]
        self.PICK = abilities[2]
        self.NEXTTARGET = abilities[-1]
    
    def update_hp(self, player, enemy):
        with self.lock:
            self.enemy_health = enemy
            self.player_health = player

    def update_targets(self, targets):
        with self.lock:
            self.targets = targets

    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)

    def target(self):
        target_i = 0
        targets = self.target_sorting(self.targets)
        #keyboard.press('SHIFT')
        if len(targets) > 0:
            x, y = self.get_screen_position(targets[0])
            pyautogui.moveTo(x, y + 30, 0.1)
            #pyautogui.click(x, y + 30, 2, 0.25)
            self.mouse.click(Button.left)
            sleep(0.1)
            return True
        return False
    
    def turn_camera(self, distance):
        x = (self.offset_x + self.window_w / 2)
        y = (self.offset_y + self.window_h / 2)
        #pyautogui.moveTo(x, y, 0.2)
        #self.mouse.press(Button.right)
        #pyautogui.moveTo(distance, 0, 1)
        #self.mouse.release(Button.right)
        sleep(0.2)
    
    def target_sorting(self, targets):
        x = self.window_w / 2
        y = self.window_h / 2
        #targets.sort(key = lambda p: (p[0] - x)**2 + (p[1] - y)**2)
        targets.sort( key = lambda p: p[1], reverse = True)
        return targets

    def attack(self):
        print('utok')
        timestamp = time()
        keyboard.send('F2')
        sleep(0.1)
        while not self.stopped:
            # if (time() - timestamp) > 15:
            #     keyboard.send('ESC')
            #     self.turn_camera(500)
            #     break
            if self.enemy_health == 0:
                keyboard.send('F3')
                sleep(1)
                keyboard.send('F3')
                sleep(1)
                keyboard.send('F3')
                sleep(1)
                keyboard.send('F4')
                sleep(1)
                
                break
            elif self.player_health <= 50 and self.enemy_health > 0:
                print('Healing potion used')
                keyboard.send('F8')
            elif self.player_health > 10 and self.enemy_health > 0:
                ability = self.DAMAGE
                keyboard.send('F7')
                keyboard.send('F2')#keyboard.send(ability)                         
                print('znovu utoci')
                sleep(3)



    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        print('startuje')
        t.start()

    def stop(self):
        self.stopped = True
        sleep(0.25)
        keyboard.send('F12')

        # this is the main logic controller
    def run(self):
        while not self.stopped:
            if self.state == BotState.INITIALIZING:
                sleep(self.init_seconds)
                keyboard.send('F12')
                with self.lock:
                    self.state = BotState.SEARCHING

            elif self.state == BotState.SEARCHING:
                self.message = "Looking for enemies"
                if self.player_health == 0:
                    self.buffed = False
                    with self.lock:
                        self.state = BotState.REBUFFING
                elif self.target():
                    with self.lock:
                        self.state = BotState.ATTACKING
                else:
                   self.turn_camera(200)

            elif self.state == BotState.ATTACKING:
                self.attack()
                with self.lock:
                    self.state = BotState.SEARCHING

            elif self.state == BotState.REBUFFING:
                if self.buffed:
                    with self.lock:
                        self.state = BotState.SEARCHING
                else:
                    pass
