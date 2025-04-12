from os import system
from random import randrange, sample
from time import sleep
from settings import Settings
from pynput import keyboard as kb
from lighting import Lighting
from json import loads
from ast import literal_eval
from math import ceil
from mysql.connector import connect, Error
from effects import *
from continued import Continued as continued
class Functions:
    def __init__(self, username:str, args:list):
        """Initialize everything."""
        self.printed = []
        self.light_debug = [0, 0] #     down:  weight, floor color,
        self.potion_names = ['Bright Potion', "Dark Potion", "Swirly Potion", "Murky Potion", "Misty Potion", "Luminous Potion", "Faint Potion", "Shimmering Potion", "Lustrous Potion", "Dazzling Potion", "Opaque Potion"]
        self.items_info =  {"consumables": {"Chicken Nugget":[2, 'y'],"Apple":[2, 'r'], "Carrot":[2, 'o']},
                            "potions": {"Nausea Potion":[10,'m'], "Water Bottle":[10,'b'], "Fruit Juice": [10,'o']},
                            "scrolls": {"Scroll of Identify":[10,'w']},
                            'statues':{"Golden Blåhaj Statue":[80, 'y'],"Arnav Statue":[30, 'w']},
                            'equippable':{"Water Walking Boots":[10, 'b'], "Blue Boots":[10, 'b'], "Cloak":[5, 'w']},
                            'other':{"Lantern":[15, 'y']},
                            'amulet':{"Fire Resistance Amulet":[20, 'r'], "Red Amulet":[20, 'r']}}
        self.items_list_info = {}
        for key in self.items_info:
            for item in self.items_info[key]:
                self.items_list_info[item] = self.items_info[key][item]
        self.categories = {"consumables":"%", "potions":"!","statues":"&","equippable":"[","other":"(", 'amulet':'"'}
        self.items_hunger = {"Chicken Nugget":60,"Apple":100, "Carrot":50}
        self.items_list = {}
        self.debug = True if args[-1] == "debug" else False
        for key in self.items_info:
            self.items_list[key] = []
            for item in self.items_info[key]:
                self.items_list[key].append(item)
        self.ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.input = 0
        self.username = "Guest" if username == "guest" else username
        self.COLORS = {"r":"\33[31m", "m":"\33[95m", "y":"\33[93m","g":"\33[32m", "l":"\33[92m", "d":"\33[34m", "b":"\x1b[38;5;26m", "w":"\33[0m", "o":"\x1b[38;5;215m", "c":"\x1b[38;5;14m"}
        self.settings = Settings() # Settings
        self.inventory_open = False
        self.status = 1 # 1 = Alive, 2 = Dead
        self.reset_game()
        try:
        #if 1==1:
                system('clear')
                # user varchar(40), area MEDIUMTEXT, player TINYTEXT, data MEDIUMTEXT, light MEDIUMTEXT, inventory MEDIUMTEXT, location varchar(10), other MEDIUMTEXT
                # Open connection and cursor, run the query, and fetch the results.
                cnx = connect(user='root', database='blahajhack')
                cursor = cnx.cursor(buffered=True)
                cursor.execute(f'SELECT * FROM saves WHERE user="{self.username}";')
                if len(cursor.fetchall()) != 0:
                    loading = input("Do you want to use your most recent save?\nWARNING: Not using it will delete it permanently! (y/n)=> ")
                    if loading == "y": self.load()
                cursor.close()
                cnx.close()
                self.delete_save()
        except Error as err:
            print(f"There was an error with checking your save file. {err}\nCreating new game...")
            sleep(2)
            self.reset_game()
        except Exception:
            print("There was an unknown error with checking your save file.\nCreating new game...")
            sleep(2)
            self.reset_game()
    def reset_game(self):
        self.exercise = {"strength": 0,"dexterity": 0,"constitution": 0, "wisdom":0, "intelligence":0, "max_hp": 0}
        self.turn = 1 # The current turn the player is on.
        self.dungeon_level = 1 # The dungeon level. (y)
        self.location = [0, 0] # Location of player. (x, z) When using this, the area's 3x2 matrix is (y, z, x) so use [1] then [0].
        self.levelData = []
        self.inventory = [] #[name(str), amount(int), status(int), status known(bool), extra status([color(str), timer(int), [special name discovered, special name], equipped, defense extra])]
        self.inventory.append(["Apple", 3, 0, True, ['w', 0, [True], 0, 0]])
        self.inventory.append(["Cloak", 1, 1, True, ['w', 0, [True], 1, 1]])
        self.hunger_points = self.settings.starting_hunger
        self.equipped = []
        self.effects = []
        self.player_att = {
            "strength": randrange(7, 9),
            "dexterity": randrange(8, 9),
            "constitution": randrange(7, 9),
            "max_hp": 20,
            "hp":20,
            "intelligence":randrange(7, 9),
            "wisdom":randrange(7, 9)
        }
        self.area = ([
            [], # Level 0 for indexing purposes.
            [["-","-","-","-","-","-","-","-","-"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","-","-","-","-"],
             ["|",".",".",".",".",".",".",".","|"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","|",".",".","|"],
             ["|",".",".",".",".",".",".",".","|"," "," "," "," "," "," "," "," "," "," "," ","-","-","-","-","-","-","-"," "," "," "," ","|",".",".","|"],
             ["|",".",".","<",".",".",".",".","+","#","#","#","#","#","#","#","#"," "," "," ","|",".",".",".",".",".","+","#","#","#","#","+",".",">","|"],
             ["|",".",".",".",".",".",".",".","|"," "," ","#"," "," "," "," ","#"," ","#","#","+",".",".",".",".",".","|"," ","#"," "," ","|",".",".","|"],
             ["|",".",".",".",".",".",".",".","|"," "," ","#"," "," "," "," ","#","#","#"," ","|",".",".",".",".",".","|"," ","#"," "," ","|",".",".","|"],
             ["-","-","+","-","-","-","-","-","-"," "," ","#"," "," "," "," ","#"," "," "," ","|",".",".",".",".",".","|"," ","#"," "," ","-","-","-","-"],
             ["|",".",".",".",".",".","|"," "," "," "," ","#"," "," "," "," ","#"," "," "," ","|",".",".",".",".",".","|"," ","#"," "," "," "," "," "," "],
             ["|",".",".",".",".",".","+","#","#","#","#","#","#"," "," ","#","#","#"," "," ","-","-","-","-","-","-","-","-","+","-","-","-"," "," "," "],
             ["|",".",".",".",".",".","|"," ","#"," "," "," ","#"," "," ","#"," ","#","#"," "," "," "," "," "," ","|",".",".",".",".",".","|"," "," "," "],
             ["|",".",".",".",".",".","|","-","+","-","-","#","#","#","#","#"," "," "," "," "," "," "," "," "," ","|",".",".",".",".",".","|"," "," "," "],
             ["-","-","-","-","-","-","-","|",".",".","+","#"," "," "," "," "," "," "," "," "," "," "," "," "," ","|",".",".",".",".",".","|"," "," "," "],
             [" "," "," "," "," "," "," ","-","-","-","-"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","-","-","-","-","-","-","-"," "," "," "]],
            [["-","-","-","-","-","-","-"," "," "," "," "," ","-","-","-","-","-"," "," "," "],["|",".",".",".",".",".","+","#","#","#","#","#","+",".",".",".","#",">"," "," "],["|",".","<",".",".",".","|"," "," "," "," "," ","|",".",".",".","|"," "," "," "],["-","-","-","-","-","-","-"," "," "," "," "," ","|",".",".",".","|"," "," "," "],[" "," "," "," "," ",' ',' ',' ',' ',' ',' ',' ','-','-','-','-','-',' ',' ',' ']],
            [["-","-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["|",".",".","+",".",".",".",".",".",".","|",".","<",".","|"],["|",">",".","|",".",".",".",".",".",".","|",".",".",".","|"],["|",".",".","|",".",".",".",".",".",".","|",".",".",".","|"],["|",".",".","|",".",".",".",".",".",".","+",".",".",".","|"],["|","-","-","-","-","+","-","-","-","-","-","-","-","-","|"],["|",".",".","+",".",".",".",".","+",".",".",".",".",".","|"],["|",".",".","|",".",".",".",".","|",".",".",".",".",".","|"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-","-"]],
            [["-","-","-",'-','-','-',' ',' ',' ',' ','-','-','-','-','-','-','-','-',' ',' ',' ',' ',' ',' ','-','-','-','-','-','-','-','-'],["|",'<','.','.','.','|',' ',' ','#','#','+','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ','|','.','.','.','.','.','.','|'],["|",'.','.','.','.','+','#','#','#',' ','|','.','.','.','.','.','.','|',' ',' ',' ','#','#','#','#','.','.','.','.','.','.','|'],["|",'.','.','.','.','|',' ',' ','#',' ','|','.','.','.','.','.','.','|',' ',' ',' ','#',' ',' ','|','.','.','.','.','>','.','|'],["-",'-','-','-','-','-',' ','#','#',' ','|','.','.','.','.','.','.','+','#','#','#','#',' ',' ','|','.','.','.','.','.','.','|'],["|",'.','.','.','.','|',' ','#',' ',' ','|','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ','|','.','.','.','.','.','.','|'],["|",'.','.','.','.','|',' ','#',' ',' ','|','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ','|','.','.','.','.','.','.','|'],["|",'.','.','.','.','|',' ','#',' ',' ','-','-','-','-','-','+','-','-',' ',' ',' ',' ',' ',' ','|','.','.','.','.','.','.','|'],["|",'.','.','.','.','+','#','#','#','#','#','#','#','#','#','#','#','#',' ',' ',' ',' ',' ',' ','-','-','-','-','-','-','-','-'],["-",'-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']],
            [["-","-","-",'-','-','-',' ',' ',' ','-','-','-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ','-','-','-','-',' ',' ',' ',' ',' ',' ',' '],["|",".",".",'.','.','|',' ',' ',' ','|','<','.','.','.','.','|',' ',' ',' ','#',' ',' ',' ',' ','|','.','.','+','#','#',' ',' ',' ',' ',' '],["|",".",".",'.','.','|',' ',' ',' ','|','.','.','.','.','.','|',' ',' ',' ','#','#','#','#','#','+','.','.','|',' ','#','#',' ','-','-','-'],["|",".",".",'.','.','|',' ',' ',' ','|','.','.','.','.','.','+','#','#','#','#',' ',' ',' ',' ','|','.','.','|',' ',' ','#','#','+','.','|'],["|",".",".",'.','.','+','#','#','#','+','.','.','.','.','.','|',' ',' ','#',' ',' ',' ',' ',' ','-','-','-','-',' ',' ',' ',' ','-','+','-'],["|",".",".",'.','.','|',' ',' ',' ','|','.','.','.','.','.','|',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#',' '],["-","-","-",'#','-','-','-','-','-','-','-','-','-','-','-','-',' ',' ','#','#','#','#',' ','-','-','-','-','-','|',' ',' ',' ',' ','#',' '],[" ",' ',' ','#',' ','|','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ','#',' ',' ','#',' ','|','.','.','.','.','|',' ',' ',' ',' ','#',' '],[" ",' ',' ','#',' ','|','.','.','.','.','|',' ',' ','#',' ',' ',' ','#','#',' ',' ','#','#','+','.','>','.','.','|',' ',' ','#','#','#',' '],[" ",'#',' ','#','#','+','.','.','.','.','+','#','#','#',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','.','.','.','.','|',' ',' ',' ',' ',' ',' '],[" ",'#','#','#',' ','-','-','-','-','-','-',' ',' ','#','#','#','#',' ',' ',' ',' ',' ',' ','|','.','.','.','.','|',' ',' ',' ',' ',' ',' '],[" ",' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','-','-','-','-','-','-',' ',' ',' ',' ',' ',' '],[" ",' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']],
            [], # level 6
            [], # level 7
            [], # level 8
            [], # level 9
            [], # level 10
            [], # level 11
            [], # level 12
            [], # level 13
            [], # level 14
            [], # level 15
            [], # level 16
            [], # level 17
            [], # level 18
            [], # level 19
            [], # level 20
            [], # level 21
            [], # level 22
            [], # level 23
            [], # level 24
            [], # level 25
            [], # level 26
            [], # level 27
            [], [], [], [], [], [], [], [], [],[],[],[],[],[],[],[],[],[],[],[],[],[],
            [["-","-","-","-","-","-","-","-","-"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
             ["|",".",".",".",".",".",".",".","|"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
             ["|",".",".",".",".",".",".",".","|"," "," "," "," "," "," "," "," "," "," "," ","-","-","-","-","-","-","-"," "," ","}","}","|","-","|"," "],
             ["|",".",".","<",".",".",".",".","+","#","#","#","#","#","#","#","#"," "," "," ","|",".",".",".",".",".","+","#","#","}","}","+",".","|"," "],
             ["|",".",".",".",".",".",".",".","|"," "," ","#"," "," "," "," ","#"," ","#","#","+",".",".",".",".",".","|"," ","#","}","}","|","-","|"," "],
             ["|",".",".",".",".",".",".",".","|"," "," ","#"," "," "," "," ","#","#","#"," ","|",".",".",".",".",".","|"," ","#"," "," "," "," "," "," "],
             ["-","-","+","-","-","-","-","-","-"," "," ","#"," "," "," "," ","#"," "," "," ","|",".",".",".",".",".","|"," ","#"," "," "," "," "," "," "],
             ["|",".",".",".",".",".","|"," "," "," "," ","#"," "," "," "," ","#"," "," "," ","|",".",".",".",".",".","|"," ","#"," "," "," "," "," "," "],
             ["|",".",".",".",".",".","#","#","#","#","#","#","#"," "," ","#","#","#"," "," ","-","-","-","-","-","-","-","-","+","-","-","-"," "," "," "],
             ["|",".",".",".",".",".","|"," ","#"," "," "," ","#"," "," ","#"," ","#","#"," "," "," "," "," "," ","|",".",".",".",".",".","|"," "," "," "],
             ["|",".",".",".",".",".","|","-","+","-","-","#","#","#","#","#"," "," "," "," "," "," "," "," "," ","|",".",".",".",".",".","|"," "," "," "],
             ["-","-","-","-","-","-","-","|",".",".","+","#"," "," "," "," "," "," "," "," "," "," "," "," "," ","|",".",".",".",".",".","|"," "," "," "],
             [" "," "," "," "," "," "," ","-","-","-","-"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","-","-","-","-","-","-","-"," "," "," "]] # level 50
            # more later
            # This can be removed later, as it will be automated with randomly generating rooms.
        ])
        lists = 0
        prev = []
        for floor in self.area:
            current = self.area[randrange(1, 6)].copy()
            while current == prev:
                current = self.area[randrange(1, 6)].copy()
            prev = current
            if floor == []:
                self.area[lists] = current.copy()
            lists += 1
        data_location = [0, 0, 0]
        for floor in self.area:
            self.levelData.append([])
            for data in floor:
                self.levelData[data_location[0]].append([])
                for _ in data:
                    self.levelData[data_location[0]][data_location[1]].append([])
                data_location[1] += 1
            data_location[0] += 1
            data_location[1] = 0
        # Add consumables to the list.
        data_location[1] = 0
        data_location[0] = 0
        self.levelData[50][3][32].append([1, 'y', "Golden Blåhaj Statue", 1, 1, False, ["y", -1, [True], 0, 0]])
        self.levelData[50][5][25].append([1, 'r', "Fire Resistance Amulet", 1, 1, False, ["w", -1, [False, "Red Amulet"], 0, 0]])
        self.levelData[50][5][24].append([1, 'b', "Water Walking Boots", 1, 1, False, ["w", -1, [False, "Blue Boots"], 0, 0]])
        for row in self.levelData:
            for tile in row:
                for _ in tile:
                    if self.area[data_location[2]][data_location[0]][data_location[1]] == ".":
                        if randrange(0, 100) == 20:
                            x = sample(self.items_list["consumables"], k=1)[0]
                            self.levelData[data_location[2]][data_location[0]][data_location[1]].append(
                                [1, self.items_list_info[x][1], x, randrange(-1, 2), 1, False, ['w', -1, [True], 0, 0]])
                        if randrange(0, 600) == 20:
                            x = sample(self.items_list["potions"], k=1)[0]
                            y = [True] if x in ["Water Bottle", "Fruit Juice"] else [False, sample(self.potion_names, k=1)[0]]
                            self.levelData[data_location[2]][data_location[0]][data_location[1]].append(
                                [1, self.items_list_info[x][1], x, randrange(-1, 2), 1, False, ['w', -1, y, 0, 0]])
                        if randrange(0, 2000) == 20:
                            self.levelData[data_location[2]][data_location[0]][data_location[1]].append(
                                [1, 'y', "Lantern", randrange(-1, 2), 1, False, ['w', randrange(20, 56), [True], 0, 0]])
                    data_location[1] += 1
                data_location[0] += 1
                data_location[1] = 0
            data_location[0] = 0
            data_location[1] = 0
            data_location[2] += 1
            x = -1
        y = 0
        for row in self.area[self.dungeon_level]:
                for tile in row:
                    x += 1
                    if tile == "<":
                        self.location[0] = x
                        self.location[1] = y
                        break
                y += 1
                x = -1
        self.lighting = Lighting(self.area) # Lighting
    def inventory_append(self, zone, inventory_index, inventory_choose, inventory_show, extras=False):
        if inventory_index == -1:
            zone += "              \33[7mInventory\33[0m"
        else:
                        x = self.inventory[inventory_index][2] if self.inventory[inventory_index][3] else ""
                        match x:
                            case -1:
                                curse = "\33[31mcursed "
                            case 0:
                                curse = "\33[0muncursed "
                            case 1:
                                curse = "\33[92mblessed "
                            case _:
                                curse = "\33[35modd-looking "
                        equipped = "" if self.inventory[inventory_index][4][3] != 1 else " (Equipped)"
                        name = self.inventory[inventory_index][0] if self.inventory[inventory_index][4][2][0] == True else self.inventory[inventory_index][4][2][1]
                        if not self.inventory[inventory_index][3]: curse = ""
                        defense = "" if self.inventory[inventory_index][4][4] == 0 else str(self.inventory[inventory_index][4][4]) + " "
                        if len(defense) != 0:
                            if defense[0] != "-":
                                defense = " +" + defense
                            else: defense = " " + defense
                        if extras:
                            for _ in self.area[self.dungeon_level][0]:
                                zone += " "
                        if self.inventory_open:
                            zone += f"              {self.COLORS[self.inventory[inventory_index][4][0]]}{curse}{defense}{name}\33[0m{equipped} ({self.inventory[inventory_index][1]})\33[0m"
                        elif inventory_choose:
                            zone += f"              {self.COLORS[self.inventory[inventory_index][4][0]]}{self.ALPHABET[inventory_index]}\33[0m) {curse}{defense}{name}\33[0m{equipped} ({self.inventory[inventory_index][1]})\33[0m"
        inventory_index += 1
        if inventory_index >= len(self.inventory):
            inventory_show = False
        return zone, inventory_index, inventory_choose, inventory_show
    def printArea(self, inventory_choose=False):
        self.hunger_points -= 1
        """Print out area onto screen."""
        inventory = self.showitems_list()
        radius = self.settings.light_radius + 2 if "Lantern" in inventory else self.settings.light_radius # Lanterns increase light amount
        levelLight = self.lighting.lightUp(self.area, self.location[0], self.location[1], self.dungeon_level, radius, self.light_debug[0])
        inventory_index = -1
        zone = ""
        loc = [0, 0]
        inventory_show = True
        idx = 0
        for row in self.area[self.dungeon_level]:
            for tile in row:
                light_level = levelLight[self.dungeon_level][loc[1]][loc[0]]
                if light_level in [2, 1]:
                    if light_level == 1:
                        zone += "\33[2m"  # Dimmed text for previously seen squares.
                    if tile == "}" and loc != self.location:
                        zone += "\33[31m"
                    if loc == self.location:
                        zone += "@"
                    elif len(self.levelData[self.dungeon_level][loc[1]][loc[0]]) > 0:
                        item = self.levelData[self.dungeon_level][loc[1]][loc[0]][0]
                        for i in self.items_list:
                            if item[2] in self.items_list[i]:
                                category = i
                                break
                        amount = ""
                        if len(self.levelData[self.dungeon_level][loc[1]][loc[0]]) > 1:
                            amount = '\33[41m'
                        zone += f"{amount}{self.COLORS[self.levelData[self.dungeon_level][loc[1]][loc[0]][0][1]]}{amount}{self.categories[category]}\33[0m"
                    else:
                        zone += tile
                    zone += "\33[0m"  # Reset text formatting
                else:
                    zone += " "
                loc[0] += 1
            if self.inventory_open or inventory_choose:
                if inventory_show:
                    zone, inventory_index, inventory_choose, inventory_show = self.inventory_append(zone, inventory_index, inventory_choose, inventory_show)
            idx += 1
            zone += "\n"
            loc[0] = 0
            loc[1] += 1

        # Print stored messages and the current zone
        list_name = list(self.username)
        divisor = (len(list_name)/self.player_att['max_hp'])
        left = divisor * self.player_att['hp']
        hp_name_list = self.health(ceil(left), list_name, self.player_att['max_hp'], self.player_att['hp'])
        hp_name = ""
        for i in hp_name_list:
            hp_name += i
        printing = "\n".join(self.printed) + "\n" + zone + "\n"
        printing += f"[{hp_name}] St:{self.player_att['strength']} Dx:{self.player_att['dexterity']} Co:{self.player_att['constitution']} Wi:{self.player_att['wisdom']} In:{self.player_att['intelligence']}"
        printing += "\n" + f"HP:{self.player_att['hp']}({self.player_att['max_hp']}) Dlvl: {self.dungeon_level} T: {self.turn} | {self.get_weight()[0]} {self.get_food()}"
        if self.turn % 50 == 0:
            self.save()
        for _ in range(len(self.inventory) - idx):
            if self.inventory_open or inventory_choose:
                if inventory_show:
                    printing += '\n'
                    printing, inventory_index, inventory_choose, inventory_show = self.inventory_append(printing, inventory_index, inventory_choose, inventory_show, True)
        system('clear')
        print(printing)
        self.printed = []
    def health(self, left=2, length=5, max=20, hp=20):
        length2 = []
        m = 0
        for i in range(len(length)):
            if left > i: m += 1
        if hp == max:
            x = "\33[7m"
        elif m >= 4/5 * len(length):
            x = '\33[102m'
        elif m >= 3/5 * len(length):
            x = '\33[43m'
        elif m >= 2/5 * len(length):
            x = '\x1b[48;5;215m'
        elif m <= 2/5 * len(length):
            x = '\33[41m'
        for i in range(len(length)):
            if left > i:
                y = x + length[i] + "\33[0m"
                length2.append(y)
            else:
                length2.append(length[i])
        return length2
    def get_weight(self) -> str:
        max_weight = self.player_att['strength'] * 3 + round(self.player_att['max_hp'] / 4)
        weight = 0
        printing = ""
        for item in self.inventory:
            for key in self.items_list:
                if item[0] in self.items_list[key]:
                    weight += self.items_info[key][item[0]][0] * item[1]
                    break
        if weight > max_weight:
            printing = "Burdened"
            if weight > round(max_weight * (1.25)):
                printing = "Strained"
                if weight > max_weight * 2:
                    printing = "Stressed"
                    if weight > round(max_weight * (2.4)):
                        printing = "\33[33mOvertaxed\33[0m"
                        if weight > max_weight * 3:
                            printing = "\33[31mOverloaded\33[0m"
        return printing, max_weight, weight
    def get_food(self) -> str:
        printing = ""
        if self.hunger_points < 150:
            printing = "Hungry"
            if self.hunger_points < 50:
                printing = "\33[33mWeak\33[0m"
                if self.hunger_points < 0:
                    printing = "\33[31mStarving\33[0m"
                    if self.hunger_points < -30:
                        printing = "\33[41mStarving\33[0m"
                        self.player_att['hp'] -= ceil(self.player_att['hp'] / 5)
        elif self.hunger_points > 800:
            printing = "Satiated"
        return printing

    def inventoryList(self) -> dict:
        """List the items in the inventory with the alphabet as keys in a dictionary."""
        idx = 0
        items_list = {}
        for item in self.inventory:
            items_list[self.ALPHABET[idx]] = item[0]
            idx += 1
        return items_list

    def showitems_list(self) -> list:
        """Gives back a list of every item in a players inventory."""
        items_list = []
        for item in self.inventory: items_list.append(item[0])
        return items_list
    def exer(self):
        x = round(self.exercise['strength'])
        if x < 0:
            m = -1
        else:
            m = 1
        if (x <= -1 or x >= 1) and (self.turn % 5 == 0) and (randrange(0, 51) == 20) and (self.player_att['strength'] > 4) and (self.player_att['strength'] < 19): #! Strength
            self.player_att['strength'] += m
            if x < 0: self.printed.append("You feel weak. Your strength decreases.")
            else: self.printed.append("You must have been exercising! Your strength increases.")
            self.exercise['strength'] -= m

        x = round(self.exercise['constitution'])
        if x < 0:
            m = -1
        else:
            m = 1
        if (x <= -1 or x >= 1) and (self.turn % 5 == 0) and (randrange(0, 51) == 20) and (self.player_att['constitution'] > 4) and (self.player_att['constitution'] < 19): #! Constitution
            self.player_att['constitution'] += x % m
            if x < 0: self.printed.append("You feel weak. Your constitution decreases.")
            else: self.printed.append("You feel powerful! Your constitution increases!")
            self.exercise['constitution'] -= x % 2

        x = round(self.exercise['wisdom'])
        if x < 0:
            m = -1
        else:
            m = 1
        if (x <= -1 or x >= 1) and (self.turn % 5 == 0) and (randrange(0, 51) == 20) and (self.player_att['wisdom'] > 4) and (self.player_att['wisdom']< 19): #! Wisdom
            self.player_att['wisdom'] += x % m
            if x < 0: self.printed.append("You feel foolish. Your wisdom decreases.")
            else: self.printed.append("You feel understanding. Your wisdom increases.")
            self.exercise['wisdom'] -= x % 2

        x = round(self.exercise['intelligence'])
        if x < 0:
            m = -1
        else:
            m = 1
        if (x <= -1 or x >= 1) and (self.turn % 5 == 0) and (randrange(0, 51) == 20) and (self.player_att['intelligence'] > 4) and (self.player_att['intelligence']< 19): #! Intelligence
            self.player_att['intelligence'] += x % m
            if x < 0: self.printed.append("You feel stupid. Your intelligence decreases.")
            else: self.printed.append("You feel smart. Your intelligence increases!")
            self.exercise['intelligence'] -= x % 2

        x = round(self.exercise['dexterity'])
        if x < 0:
            m = -1
        else:
            m = 1
        if (x <= -1 or x >= 1) and (self.turn % 5 == 0) and (randrange(0, 51) == 20) and (self.player_att['dexterity'] > 4) and (x < 19): #! DEXTERITY
            self.player_att['dexterity'] += x % m
            if x < 0: self.printed.append("You feel sluggish. Your dexterity decreases.")
            else: self.printed.append("You must have been working on your reflexes! Your dexterity increases.")
            self.exercise['dexterity'] -= x % 2

            if self.player_att['strength'] <= 4:
                print("You are too weak to even hold yourself up anymore. You collapse.")
                self.player_att['hp'] = 0
                self.death()
                return False
            if self.player_att['intelligence'] <= 4:
                print("You are too stupid to even walk. You collapse.")
                self.player_att['hp'] = 0
                self.death()
                return False
            if self.player_att['dexterity'] <= 4:
                self.player_att['hp'] = 0
                print("You have such bad reactions that it takes seconds to realize you moved your hand. You collapse.")
                self.death()
                return False
    def discover(self, prev, item):
        for i in range(len(self.inventory)):
            if self.inventory[i][0] == item[0]:
                idx = i
        article1 = "a"
        article2 = "this"
        if item[0] in ['A', 'E', "I", "O", "U"]:
            article1 = "an"
        if prev[-1] == "s":
            article2 = "these"
        self.inventory[idx][4][2][1] == True
        final = f"You discover {article2} {prev} is {article1} {item[0]}!"
        return final

    def checkKeydownEvents(self, key=None):
     if self.status != 2 and self.input == 0:
      """Run appropriate code for keydown events."""
      try:
        if key.char == 'i':
            self.inventory_open = 1 - self.inventory_open
            self.turn -= 1
            self.hunger_points += 1
        elif self.inventory_open == False:
                match key.char:
                    case "m": # Use staircases
                        if self.area[self.dungeon_level][self.location[1]][self.location[0]] == ">":
                            self.dungeon_level += 1
                            x = -1
                            y = 0
                            for i in self.area[self.dungeon_level]:
                                for tile in i:
                                    x += 1
                                    if tile == "<":
                                        self.location[0] = x
                                        self.location[1] = y
                                        break
                                y += 1
                                x = -1
                        elif self.area[self.dungeon_level][self.location[1]][self.location[0]] == "<":
                            if "Golden Blåhaj Statue" in self.showitems_list() and self.dungeon_level == 1:
                                self.location[0] = 10000
                                self.printArea()
                                print("You win! You go up the staircase and ascend.")
                                self.death(True)
                                if self.username != "Guest" and self.debug == False:
                                    try:
                                    #if 1==1:
                                        # Open connection and cursor, run the query, and fetch the results.
                                        cnx = connect(user='root', database='blahajhack')
                                        cursor = cnx.cursor(buffered=True)
                                        cursor.execute(f'SELECT wins FROM users WHERE name="{self.username}";')
                                        wins = cursor.fetchall()[0][0]
                                        cursor.execute(f'UPDATE users SET wins="{str(wins+1)}" WHERE name="{self.username}";')
                                        cnx.commit()
                                    except Error as err:
                                        print("There was an error with increasing your win count.", err)
                                    except Exception as err:
                                        print("There was an unkown error with increasing your win count.", err)
                                    self.delete_save()
                                return False
                            elif self.dungeon_level == 1:
                                self.input = 2
                                sleep(0.1)
                                print(f"\bYou hear the voice of {self.COLORS['c']}\33[0mBlåhaj, Thou must have the statue, or thy will regret this. Do you still want to go up? (y/n)=> ")
                            else:
                                self.dungeon_level -= 1
                                x = -1
                                y = 0
                                for i in self.area[self.dungeon_level]:
                                    for tile in i:
                                        x += 1
                                        if tile == ">":
                                            self.location[0] = x
                                            self.location[1] = y
                                            break
                                    y += 1
                                    x = -1
                        else:
                            self.printed.append("There is no staircase here.")
                            self.turn -= 1
                            self.hunger_points += 1
                    case 'w': # Wearing
                        self.printArea(True)
                        print("Which item? =>")
                        self.input = 4
                        self.turn += 5
                    case 'e': # Eating
                        self.printArea(True)
                        print("Which item? =>")
                        self.input = 5
                        self.turn += 1
                    case 'd': # Drinking
                        self.printArea(True)
                        print("Which item? =>")
                        self.input = 6
                        self.turn += 1
                    case ",": # Picking up
                        if len(self.levelData[self.dungeon_level][self.location[1]][self.location[0]]) == 0:
                            self.printed.append("There is no item to pick up here.")
                            self.turn -= 1
                            self.hunger_points += 1
                        elif len(self.inventory) < 53:
                            for info in self.levelData[self.dungeon_level][self.location[1]][self.location[0]]:
                                if info[0] == 1:
                                    article = "a"
                                    name = info[2] if info[6][2][0] else info[6][2][1]
                                    if name[0] in ["A", "E", "I", "O", "U"]:
                                        article = "an"
                                    if name[-1] == "s":
                                        article = "the"
                                    _, max_weight, weight, = self.get_weight()
                                    for i in self.items_info:
                                        #self.printed.append(i, info[2], i[info[2]], weight+i[info[2]], max_weight*4)
                                        if info[2] in self.items_info[i]:
                                            if weight + self.items_info[i][info[2]][0] > max_weight * 4:
                                                self.printed.append("You are not strong enough to hold all these items.")
                                                break
                                    else:
                                        self.printed.append(f"You pick up {article} {name.lower()}.")
                                        self.levelData[self.dungeon_level][self.location[1]][self.location[0]].pop(0)
                                        idx = 0
                                        show = False
                                        for item in self.inventory:
                                            if item[0] == info[2] and item[3] != False and (item[2] == info[3]) and item[4] != False:
                                                self.inventory[idx][1] += 1
                                                show = True
                                                break
                                            idx += 1
                                        if not show:
                                            self.inventory.append([info[2], 1, info[3], info[5], info[6]]) #[name(str), amount(int), status(int), status known(bool), extra status(list of ints)]
                                            break
                        else:
                            self.printed.append("Your backpack is too full to hold anymore items.")
                            self.turn -= 1
                            self.hunger_points += 1
                    case "n":
                        self.printArea(True)
                        print("Which item? => ")
                        self.input = 1
                    case 'Q':
                        print("Are you sure you want to quit? (y/n)=>")
                        self.input = 3
                    case "'":
                        if self.debug: self.light_debug[0] = 1-self.light_debug[0]
                        else:self.printed.append("' is not a valid key.")
                    case '"':
                        if self.debug: self.light_debug[1] = 1-self.light_debug[1]
                        else:self.printed.append("\" is not a valid key.")
                    case "-":
                        if self.debug: self.dungeon_level -= 1
                        else:self.printed.append("- is not a valid key.")
                        self.hunger_points -= 1
                        self.turn -= 1
                    case "[":
                        if self.debug: self.player_att['hp'] -= 1
                        else:self.printed.append("[ is not a valid key.")
                        self.hunger_points -= 1
                        self.turn -= 1
                    case "=":
                        if self.debug: self.dungeon_level += 1
                        else:self.printed.append("= is not a valid key.")
                        self.hunger_points -= 1
                        self.turn -= 1
                    case "}":
                        if self.debug: self.player_att['strength'] += 1
                        else:self.printed.append("} is not a valid key.")
                        self.hunger_points -= 1
                        self.turn -= 1
                    case "{":
                        if self.debug: self.player_att['strength'] -= 1
                        else:self.printed.append("{ is not a valid key.")
                        self.hunger_points -= 1
                        self.turn -= 1
                    case "]":
                        if self.debug: self.player_att['hp'] += 1
                        else:self.printed.append("] is not a valid key.")
                        self.hunger_points -= 1
                        self.turn -= 1
                    case "_":
                        if self.debug: self.dungeon_level = 1
                        else:self.printed.append("_ is not a valid key.")
                        self.hunger_points -= 1
                        self.turn -= 1
                    case "+":
                        if self.debug: self.dungeon_level = 50
                        else:self.printed.append("+ is not a valid key.")
                        self.hunger_points -= 1
                        self.turn -= 1
                    case '\\':
                        if self.debug:
                            x = literal_eval(input("[name(str), amount(int), status(int), status known(bool), extra status([color(str), timer(int), [special name discovered, special name], equipped, defense extra])]\n=>"))
                            self.inventory.append(x)
                        else:self.printed.append("\\ is not a valid key.")
                        self.hunger_points -= 1
                        self.turn -= 1
                    case _:
                            self.printed.append(f"{key} is not a valid key.")
                            self.turn -= 1
                            self.hunger_points += 1
      except AttributeError:
        if not self.inventory_open:
            if key in [kb.Key.right, kb.Key.left,  kb.Key.up, kb.Key.down]:
                    """Move player in any direction."""
                    self.exercise['strength'] += 0.003
                    if self.get_weight()[0] not in ["", "Burdened"]:
                        if randrange(0, 5) == 2:
                            self.exercise['strength'] += 0.001
                            self.exercise['dexterity'] -= randrange(0, 3)/100
                    match key:
                        case kb.Key.up:
                            self.location[1] -= 1
                        case kb.Key.left:
                            self.location[0] -= 1
                        case kb.Key.down:
                            self.location[1] += 1
                        case _:
                            self.location[0] += 1
                    try:
                    #if 1==1:
                        if (self.area[self.dungeon_level][self.location[1]][self.location[0]] in ["-", "|", " ", "}"]) and self.light_debug[1] != 1:
                            if (self.area[self.dungeon_level][self.location[1]][self.location[0]] in ["}"]):
                                if "Fire Resistance Amulet" not in self.equipped and "Water Walking Boots" not in self.equipped:
                                    self.exercise['strength'] -= 0.03
                                    self.player_att["hp"] -= 150
                                    if self.player_att["hp"] < 1:
                                        self.status = 2
                                        print("You walk into the lava, and immediately melt.")
                                        self.death()
                                        return False
                                    else:
                                        item_holding = " and some of your items were dropped or destroyed." if (len(self.inventory) > 0 and not (len(self.inventory) == 1 and self.inventory[0][0] == "Golden Blåhaj Statue")) else "."
                                        text = f"You are able to get out of the lava, but it severly damages you{item_holding}"
                                        self.printed.append(text)
                                        for i in range(len(self.inventory)):
                                            if self.inventory[i-1][0] != "Golden Blåhaj Statue" and self.inventory[i-1][0] != "Fire Resistance Amulet" and randrange(0, 3) == 2:
                                                self.inventory.pop(i)
                                elif "Water Walking Boots" not in self.equipped:
                                    for i in range(len(self.inventory)):
                                        if self.inventory[i][0] == "Fire Resistance Amulet":
                                            if not self.inventory[i][4][2][0]:
                                                self.inventory[i][4][2][0] = True
                                                self.printed.append(f"{self.discover(self.inventory[i][4][2][1], self.inventory[i])} You almost sink though, and you still can't pass this lava.")
                                            else:
                                                self.printed.append("You almost sink. You can't pass this lava.")
                                            break
                                elif "Fire Resistance Amulet" not in self.equipped:
                                    for i in range(len(self.inventory)):
                                        if self.inventory[i][0] == "Water Walking Boots":
                                            if not self.inventory[i][4][2][0]:
                                                self.inventory[i][4][2][0] = True
                                                self.printed.append(f"{self.discover(self.inventory[i][4][2][1], self.inventory[i])} Unfortunately, you are not fire resistant, and start to burn.")
                                                self.player_att['hp'] -= 100
                                            else:
                                                self.printed.append("You are standing on the lava, but also burning.")
                                                self.player_att['hp'] -= 100
                                elif ("Fire Resistance Amulet" in self.equipped) and ("Water Walking Boots" in self.equipped):
                                    for i in range(len(self.inventory)):
                                        if self.inventory[i][0] == "Water Walking Boots":
                                            if not self.inventory[i][4][2][0]:
                                                self.printed.append(self.discover(self.inventory[i][4][2][1], self.inventory[i]))
                                        elif self.inventory[i][0] == "Fire Resistance Amulet":
                                            if not self.inventory[i][4][2][0]:
                                                self.printed.append(self.discover(self.inventory[i][4][2][1], self.inventory[i]))
                                        self.inventory[i][4][2][0] = True
                            if (self.area[self.dungeon_level][self.location[1]][self.location[0]] not in ["}"]) or ("Water Walking Boots" not in self.equipped and "Fire Resistance Amulet" in self.equipped):
                                            match key:
                                                case kb.Key.up:
                                                    self.location[1] += 1
                                                case kb.Key.left:
                                                    self.location[0] += 1
                                                case kb.Key.down:
                                                    self.location[1] -= 1
                                                case _:
                                                    self.location[0] -= 1
                                            self.turn -= 1
                                            self.hunger_points += 1
                                            self.exercise['strength'] -= 0.003
                        else:
                            if self.exer() == False:
                                return False
                    except Exception as err:
                        print(err)
                        if key == kb.Key.up:
                            self.location[1] += 1
                        elif key == kb.Key.left:
                            self.location[0] += 1
                        elif key == kb.Key.down:
                            self.location[1] -= 1
                        else:
                            self.location[0] -= 1
                        self.turn -= 1
                        self.hunger_points += 1
                    if self.area[self.dungeon_level][self.location[1]][self.location[0]] == "+":
                        self.area[self.dungeon_level][self.location[1]][self.location[0]] = "~"
                    data = self.levelData[self.dungeon_level][self.location[1]][self.location[0]]
                    if len(data) > 0:
                        info = ""
                        curse = ""
                        amount = 0
                        for item in data:
                            if amount == 1 and item[0] == 1:
                                amount += 1
                            elif item[0] == 1:
                                info = item
                                amount += 1
                        extras = "" if amount == 1 else f"There are {amount} items here. "
                        if info[5]:
                            match info[3]:
                                case -1:
                                    curse = "\33[31mcursed "
                                case 0:
                                    curse = "\33[0muncursed "
                                case 1:
                                    curse = "\33[92mblessed "
                                case _:
                                    curse = "\33[35modd-looking "
                        name = info[2] if info[6][2][0] else info[6][2][1]
                        article = "is a"
                        if name[0] in ["A", "E", "I", "O", "U"]:
                            article = "is an"
                        if name[-1] == "s":
                            article = "are some"
                        self.printed.append(f"{extras}There {article} {curse}\33[0m{name.lower()} on the floor here.")
            else:
                match key:
                    # Some random messages for obscure buttons.
                    case kb.Key.delete:
                        self.printed.append("Why does that button even exist?")
                        self.turn -= 1
                        self.hunger_points += 1
                    case kb.Key.f19:
                        self.printed.append("When will anyone even use a F19?")
                        self.turn -= 1
                        self.hunger_points += 1
                    case kb.Key.f20:
                        self.printed.append("What kind of keyboard even has an F20!?")
                        self.turn -= 1
                        self.hunger_points += 1
                    case _:
                        if key not in [kb.Key.enter, kb.Key.backspace, kb.Key.space, kb.Key.shift, kb.Key.shift_r, kb.Key.alt_r, kb.Key.alt, kb.Key.cmd, kb.Key.cmd_r, kb.Key.ctrl,kb.Key.tab]:
                            full = f"{str(key)[4:]} is not a valid key."
                            self.printed.append(full)
                            self.turn -= 1
                            self.hunger_points += 1
      if key not in [kb.Key.enter, kb.Key.backspace, kb.Key.space, kb.Key.shift, kb.Key.shift_r, kb.Key.alt_r, kb.Key.alt, kb.Key.cmd, kb.Key.cmd_r, kb.Key.ctrl,kb.Key.tab] and (self.input == 0) and (key != None):
        self.printArea()
        self.turn += 1
      else:
          self.hunger_points += 1
     elif self.input != 0:
        if key not in [kb.Key.enter, kb.Key.shift, kb.Key.shift_r]:
            try:
                key_new = key.char
            except AttributeError:
                key_new = key
            match self.input:
                case 1: self.printed = continued.investigate(self.inventoryList(), self.printed, key_new)
                case 2:
                    x, self.printed, self.location = continued.floor_one(self.printed, self.location, kb, key_new)
                    if not x:
                        print("You reach the surface, and your blood turns to vinegar. (It's a very weird feeling)")
                        self.death()
                        return False
                case 3:
                    if key_new == "y":
                        self.save()
                        return False # Returning false ends pynput, ending the program
                case 4: self.inventory, self.printed, self.equipped, self.turn = continued.wear(self.inventoryList(), self.inventory, self.printed, self.equipped, self.items_list, self.turn, key_new)
                case 5: self.inventory, self.hunger_points, self.turn =  continued.eat(self.inventory, self.ALPHABET, self.items_hunger, self.hunger_points, self.printed, self.turn, key_new)
                case 6: self.inventory, self.printed, self.hunger_points, self.turn = continued.drink(self.inventory, self.ALPHABET, self.printed, self.hunger_points, self.turn, self.items_info, key_new)
            self.input = 0
            self.printArea()
     if self.status == 2 or self.player_att['hp'] <= 0:
        self.printArea()
        self.death()
        return False
    def death(self, win = False):
        """Deal with people with skill issues, and also winning."""
        sleep(0.5)
        if not win: print("\bYou die...")
        option = ""
        #if win == False and len(self.inventory) != 0: option = input("Do you want your possesions identified? (y/n)=> ")
        #if win == True or option.lower() == "y":
        if 1 == 1:
            inventory_index = -1
            option = ""
            if option.lower().strip() == "y" or option == "":
                if len(self.inventory) != 0:
                    for _ in range(len(self.inventory) + 1):
                        if inventory_index == -1:
                            print("\n\33[7mItems Held\33[0m")
                        else:
                            match self.inventory[inventory_index][2]:
                                case -1:
                                    x = "\33[31mcursed"
                                case 0:
                                    x = "\33[0muncursed"
                                case 1:
                                    x = "\33[92mblessed"
                                case _:
                                    x = "\33[35modd-looking"
                            equipped = "" if self.inventory[inventory_index][4][3] != 1 else " (Equipped)"
                            name = self.inventory[inventory_index][0] if self.inventory[inventory_index][4][2][0] == True else self.inventory[inventory_index][4][2][1]
                            defense = "" if self.inventory[inventory_index][4][4] == 0 else str(self.inventory[inventory_index][4][4]) + " "
                            if len(defense) != 0:
                                if defense[0] != "-":
                                    defense = " +" + defense
                                else: defense = " " + defense
                            print(f"{self.COLORS[self.inventory[inventory_index][4][0]]}{x} {defense}{name}\33[0m{equipped} ({self.inventory[inventory_index][1]})")
                        inventory_index += 1
                    print()
                else:
                    print("You held nothing.")
        print("\33[0mAttributes:")
        if "Fire Resistance Amulet" in self.equipped:
            print("You were fire resistant.")
        else: print("You had no resistances.")
        if self.get_weight()[0] != "":
            print(f"You were {self.get_weight()[0].lower()}.")
        else:
            print("You were not over-encumbered.")
        if not win: print("You were dead at the time of your death.")
        else: print("You ascended.")
        self.delete_save()
    def delete_save(self):
        if self.debug == False:
            cnx = connect(user='root', database='blahajhack')
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f'SELECT * FROM saves WHERE user="{self.username}";')
            if len(cursor.fetchall()) != 0:
                cursor.execute(f'DELETE FROM saves WHERE user="{self.username}";')
                cnx.commit()

    def save(self):
        if self.username != "Guest":
            """Save the game."""
            try:
                system('clear')
                # user varchar(40), area MEDIUMTEXT, player TINYTEXT, data MEDIUMTEXT, light MEDIUMTEXT, inventory MEDIUMTEXT, location varchar(10), dungeon varchar(3), other MEDIUMTEXT
                # Open connection and cursor, run the query, and fetch the results.
                cnx = connect(user='root', database='blahajhack')
                cursor = cnx.cursor(buffered=True)
                location = str(self.location[0]) + "," + str(self.location[1])
                #cursor.execute("DROP TABLE saves;")
                #cursor.execute("CREATE TABLE saves(user varchar(40), area MEDIUMTEXT, player TINYTEXT, data MEDIUMTEXT, light MEDIUMTEXT, inventory MEDIUMTEXT, location varchar(10), dungeon varchar(3), other MEDIUMTEXT, exercise MEDIUMTEXT)")
                cursor.execute(f'SELECT * FROM saves WHERE user="{self.username}";')
                saves = cursor.fetchall()
                if saves != []: cursor.execute(f'UPDATE saves SET area="{self.area}", player="{self.player_att}", data="{self.levelData}", light="{self.lighting.levelLight}", inventory="{self.inventory}", location="{location}", dungeon="{self.dungeon_level}",other="[{self.hunger_points}, {self.turn}, {self.equipped}]", exercise="{self.exercise}";')
                cursor.execute(f'INSERT INTO saves(user, area, player, data, light, inventory, location, dungeon, other, exercise) VALUES("{self.username}", "{self.area}", "{self.player_att}", "{self.levelData}", "{self.lighting.levelLight}", "{self.inventory}", "{location}", "{self.dungeon_level}", "[{self.hunger_points}, {self.turn}, {self.equipped}]", "{self.exercise}");')
                cnx.commit()
            except Error as err:
                print("There was an error with saving.", err)
            except Exception as err:
                print("There was an unkown error with saving.", err)

    def load(self) -> None:
        """Load the game."""
        try:
        #if 1 == 1:
                system('clear')
                # user varchar(40), area MEDIUMTEXT, player TINYTEXT, data MEDIUMTEXT, light MEDIUMTEXT, inventory MEDIUMTEXT, location varchar(10), other MEDIUMTEXT
                # Open connection and cursor, run the query, and fetch the results.
                cnx = connect(user='root', database='blahajhack')
                cursor = cnx.cursor(buffered=True)
                cursor.execute(f'SELECT * FROM saves WHERE user="{self.username}";')
                if 1 == 1:
                    a = cursor.fetchall()
                    x_pos = ""
                    y_pos = ""
                    y_adding = False
                    for i in a[0][6]:
                        if i == ",":
                            y_adding = True
                        elif not y_adding:
                            x_pos += i
                        else:
                            y_pos += i
                    player = a[0][2].replace("'", '"')
                    self.area = literal_eval(a[0][1])
                    self.player_att = loads(player)
                    self.levelData = literal_eval(a[0][3])
                    self.lighting.levelLight = loads(a[0][4])
                    self.inventory = literal_eval(a[0][5])
                    self.location = [int(x_pos), int(y_pos)]
                    self.dungeon_level = int(a[0][7])
                    self.turn = int(literal_eval(a[0][8])[1])
                    self.hunger_points = int(literal_eval(a[0][8])[0])
                    self.equipped = literal_eval(a[0][8])[2]
                    new = a[0][9].replace("'", '"')
                    self.exercise = loads(new)
        except Error as err:
            print(f"There was an error with loading your save file. {err} \nCreating new game...")
            sleep(2)
            self.reset_game()
        except Exception as err:
            if self.debug:
                print(f"There was an error with loading your save file. The error \"{err}\" occurred.\nCreating new game...")
            else:
                print("There was an unknown error with loading your save file.\nCreating new game...")
            sleep(2)
            self.reset_game()
if __name__ == "__main__":
    from sys import argv
    functions = Functions("guest", argv)
    functions.printArea()
    with kb.Listener(on_press=functions.checkKeydownEvents) as listener:
        listener.join()