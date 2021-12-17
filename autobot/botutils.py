import cv2 as cv

class Utils:

    max_player_health = 30.0  # px
    max_enemy_health = 30.0  # px
    current_player_health = 100  # %
    current_enemy_health = 100  # %

    player_hp_x_pos = 0
    player_hp_y_pos = 0
    player_hp_bar_width = 0
    player_hp_bar_height = 0
    enemy_hp_x_pos = 0
    enemy_hp_y_pos = 0
    enemy_hp_bar_width = 0
    enemy_hp_bar_height = 0

    def __init__(self, offset_x, offset_y, w, h, UI_info):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.w = w
        self.h = h
        self.get_UI_positions(UI_info, offset_x, offset_y)

    def get_UI_positions(self, UI_info, offset_x, offset_y):
        lines = []
        with open(UI_info, 'r') as file:
            for line in file:
                if "=" in line:
                    variable, value = line.split('=')
                    lines.append(value)

        player_status = lines[2:4]
        print(player_status)
        self.player_hp_x_pos = int(player_status[0]) + 22
        self.player_hp_y_pos = int(player_status[1]) + 41
        self.player_hp_bar_width = 150
        self.player_hp_bar_height = 4

        enemy_status = lines[6:8]
        print(enemy_status)
        self.enemy_hp_x_pos = int(enemy_status[0]) + 22
        self.enemy_hp_y_pos = int(enemy_status[1]) + 28
        self.enemy_hp_bar_width = 150
        self.enemy_hp_bar_height = 4
    
    def player_health(self, screenshot):
        y = self.player_hp_y_pos
        h = self.player_hp_bar_height + y
        x = self.player_hp_x_pos
        w = self.player_hp_bar_width + x
        im = screenshot[y:h, x:w]
        rgb = im[1]
        #print(rgb)
        current_player_health = 0
        for r in range(0, len(rgb), 5):
            r = rgb[r][2]
            if r >= 100:
                current_player_health += 1.0
        percent_health = current_player_health * 100.0 / self.max_player_health
        percent_health = round(percent_health, 1)
        return percent_health

    def enemy_health(self, screenshot):
        
        y = self.enemy_hp_y_pos
        h = self.enemy_hp_bar_height + y
        x = self.enemy_hp_x_pos
        w = self.enemy_hp_bar_width + x
        im = screenshot[y:h, x:w]
        rgb = im[2]
        #print(rgb)
        current_enemy_health = 0
        for r in range(0, len(rgb), 5):
            r = rgb[r][2]
            if r == 135:
                current_enemy_health += 1.0
        enemy_percent_health = current_enemy_health * 100.0 / self.max_enemy_health
        enemy_percent_health = round(enemy_percent_health, 1)
        #print('Enemy Health ' + str(enemy_percent_health))
        return enemy_percent_health