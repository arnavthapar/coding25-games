from os import system
from random import randrange, sample
from time import sleep
from lighting import Lighting
from settings import Settings
from pynput import keyboard
from json import loads
from mysql.connector import connect, Error
class Functions:
    def __init__(self, username):
        """Initialize everything."""
        self.printed = []
        self.items_weight= {"consumables": {"Chicken Nugget":2,"Apple":2, "Carrot":2},
                            "potions": {"Nausea Potion":7},
                            'statues':{"Golden Blåhaj Statue":100,"Arnav Statue":60},
                            'other':{"Mysterious Tablet":20, "Lantern":15}}
        self.items_list = {}
        for key in self.items_weight:
            self.items_list[key] = []
            for item in self.items_weight[key]:
                self.items_list[key].append(item)
        self.alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.input = 0
        self.username = "Guest" if username == "guest" else username
        self.player_att = {
            "strength": 7,
            "attack": 9,
            "defense": 0,
            "max_hp": 20,
            "hp":20
        }
        self.colors = {"r":"\033[31m", "m":"\033[95m", "y":"\033[93m","g":"\033[92m", "b":"\033[34m", "w":""}
        # The blue looks purple on some systems/terminals.
        self.area = ([
            [[]], # Level 0 for indexing purposes.
            [["-","-","-","-","-","-","-","-","-"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","-","-","-","-"],
             ["|",".",".",".",".",".",".",".","|"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","|",".",".","|"],
             ["|",".",".",".",".",".",".",".","|"," "," "," "," "," "," "," "," "," "," "," ","-","-","-","-","-","-","-"," "," "," "," ","|",".",".","|"],
             ["|",".",".","<",".",".",".",".","=","#","#","#","#","#","#","#","#"," "," "," ","|",".",".",".",".",".","=","#","#","#","#","=",".",">","|"],
             ["|",".",".",".",".",".",".",".","|"," "," ","#"," "," "," "," ","#"," ","#","#","=",".",".",".",".",".","|"," ","#"," "," ","|",".",".","|"],
             ["|",".",".",".",".",".",".",".","|"," "," ","#"," "," "," "," ","#","#","#"," ","|",".",".",".",".",".","|"," ","#"," "," ","|",".",".","|"],
             ["-","-","=","-","-","-","-","-","-"," "," ","#"," "," "," "," ","#"," "," "," ","|",".",".",".",".",".","|"," ","#"," "," ","-","-","-","-"],
             ["|",".",".",".",".",".","|"," "," "," "," ","#"," "," "," "," ","#"," "," "," ","|",".",".",".",".",".","|"," ","#"," "," "," "," "," "," "],
             ["|",".",".",".",".",".","#","#","#","#","#","#","#"," "," ","#","#","#"," "," ","-","-","-","-","-","-","-","-","=","-","-","-"," "," "," "],
             ["|",".",".",".",".",".","|"," ","#"," "," "," ","#"," "," ","#"," ","#","#"," "," "," "," "," "," ","|",".",".",".",".",".","|"," "," "," "],
             ["|",".",".",".",".",".","|","-","=","-","-","#","#","#","#","#"," "," "," "," "," "," "," "," "," ","|",".",".",".",".",".","|"," "," "," "],
             ["-","-","-","-","-","-","-","|",".",".","=","#"," "," "," "," "," "," "," "," "," "," "," "," "," ","|",".",".",".",".",".","|"," "," "," "],
             [" "," "," "," "," "," "," ","-","-","-","-"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","-","-","-","-","-","-","-"," "," "," "],],
            [["-","-","-","-","-","-","-"," "," "," "," "," ","-","-","-","-","-"," "," "," "],["|",".",".",".",".",".","=","#","#","#","#","#","=",".",".",".","#",">"," "," "],["|",".","<",".",".",".","|"," "," "," "," "," ","|",".",".",".","|"," "," "," "],["-","-","-","-","-","-","-"," "," "," "," "," ","|",".",".",".","|"," "," "," "],[" "," "," "," "," ",' ',' ',' ',' ',' ',' ',' ','-','-','-','-','-',' ',' ',' ']],
            [["-","-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["|",".",".","=",".",".",".",".",".",".","|",".","<",".","|"],["|",">",".","|",".",".",".",".",".",".","|",".",".",".","|"],["|",".",".","|",".",".",".",".",".",".","|",".",".",".","|"],["|",".",".","|",".",".",".",".",".",".","=",".",".",".","|"],["|","-","-","-","-","=","-","-","-","-","-","-","-","-","|"],["|",".",".","=",".",".",".",".","=",".",".",".",".",".","|"],["|",".",".","|",".",".",".",".","|",".",".",".",".",".","|"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-","-"]],
            [["-","-","-",'-','-','-',' ',' ',' ',' ','-','-','-','-','-','-','-','-',' ',' ',' ',' ',' ',' ','-','-','-','-','-','-','-','-'],["|",'<','.','.','.','|',' ',' ','#','#','=','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ','|','.','.','.','.','.','.','|'],["|",'.','.','.','.','=','#','#','#',' ','|','.','.','.','.','.','.','|',' ',' ',' ','#','#','#','#','.','.','.','.','.','.','|'],["|",'.','.','.','.','|',' ',' ','#',' ','|','.','.','.','.','.','.','|',' ',' ',' ','#',' ',' ','|','.','.','.','.','>','.','|'],["-",'-','-','-','-','-',' ','#','#',' ','|','.','.','.','.','.','.','=','#','#','#','#',' ',' ','|','.','.','.','.','.','.','|'],["|",'.','.','.','.','|',' ','#',' ',' ','|','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ','|','.','.','.','.','.','.','|'],["|",'.','.','.','.','|',' ','#',' ',' ','|','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ','|','.','.','.','.','.','.','|'],["|",'.','.','.','.','|',' ','#',' ',' ','-','-','-','-','-','=','-','-',' ',' ',' ',' ',' ',' ','|','.','.','.','.','.','.','|'],["|",'.','.','.','.','=','#','#','#','#','#','#','#','#','#','#','#','#',' ',' ',' ',' ',' ',' ','-','-','-','-','-','-','-','-'],["-",'-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']],
            [["-","-","-",'-','-','-',' ',' ',' ','-','-','-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ','-','-','-','-',' ',' ',' ',' ',' ',' ',' '],["|",".",".",'.','.','|',' ',' ',' ','|','<','.','.','.','.','|',' ',' ',' ','#',' ',' ',' ',' ','|','.','.','=','#','#',' ',' ',' ',' ',' '],["|",".",".",'.','.','|',' ',' ',' ','|','.','.','.','.','.','|',' ',' ',' ','#','#','#','#','#','=','.','.','|',' ','#','#',' ','-','-','-'],["|",".",".",'.','.','|',' ',' ',' ','|','.','.','.','.','.','=','#','#','#','#',' ',' ',' ',' ','|','.','.','|',' ',' ','#','#','=','.','|'],["|",".",".",'.','.','=','#','#','#','=','.','.','.','.','.','|',' ',' ','#',' ',' ',' ',' ',' ','-','-','-','-',' ',' ',' ',' ','-','=','-'],["|",".",".",'.','.','|',' ',' ',' ','|','.','.','.','.','.','|',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#',' '],["-","-","-",'#','-','-','-','-','-','-','-','-','-','-','-','-',' ',' ','#','#','#','#',' ','-','-','-','-','-','|',' ',' ',' ',' ','#',' '],[" ",' ',' ','#',' ','|','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ','#',' ',' ','#',' ','|','.','.','.','.','|',' ',' ',' ',' ','#',' '],[" ",' ',' ','#',' ','|','.','.','.','.','|',' ',' ','#',' ',' ',' ','#','#',' ',' ','#','#','=','.','>','.','.','|',' ',' ','#','#','#',' '],[" ",'#',' ','#','#','=','.','.','.','.','=','#','#','#',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','.','.','.','.','|',' ',' ',' ',' ',' ',' '],[" ",'#','#','#',' ','-','-','-','-','-','-',' ',' ','#','#','#','#',' ',' ',' ',' ',' ',' ','|','.','.','.','.','|',' ',' ',' ',' ',' ',' '],[" ",' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','-','-','-','-','-','-',' ',' ',' ',' ',' ',' '],[" ",' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']],
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
            # more later
            # This can be removed later, as it will be automated with randomly generating rooms.
        ])
        self.turn = 1 # The current turn the player is on.
        self.dungeon_level = 1 # The dungeon level. (z)
        self.location = [0, 0] # Location of player. (x, y) When using this, the area's 3x2 matrix is (z, y, x) so use [1] then [0].
        self.levelData = []
        self.settings = Settings() # Settings
        self.lighting = Lighting(self.area) # Lighting
        # Sets up the levelData list, which is used for enemies, items and more.
        data_location = [0, 0]
        self.inventory_open = False
        self.status = 1 # 1 = Alive, 2 = Dead
        self.inventory = [] #[name(str), amount(int), status(int), status known(bool), extra status(list of ints)]\
            # In the extra status, 0 = No extra status. 1 = countdown (candles, time related items_list), 2 = other
        for i in self.area:
            self.levelData.append([])
            for data in i:
                self.levelData[data_location[0]].append([])
                for _ in data:
                    self.levelData[data_location[0]][data_location[1]].append([])
                data_location[1] += 1
            data_location[0] += 1
            data_location[1] = 0
        self.hunger_points = self.settings.starting_hunger
        # Add consumables to the list.
        data_location[1] = 0
        data_location[0] = 0
        data_location.append(0)
        for i in self.levelData:
            for tile in i:
                for _ in tile:
                    if self.area[data_location[2]][data_location[0]][data_location[1]] == ".":
                        if randrange(0, 80) == 20:
                            self.levelData[data_location[2]][data_location[0]][data_location[1]].append([1, None, sample(self.items_list["consumables"], k=1)[0], randrange(-1, 2), 1, False, [0]])
                        if randrange(0, 80) == 20:
                            self.levelData[data_location[2]][data_location[0]][data_location[1]].append([1, None, "Lantern", randrange(-1, 2), 1, False, [1, randrange(15, 24)]])
                    data_location[1] += 1
                data_location[0] += 1
                data_location[1] = 0
            data_location[0] = 0
            data_location[1] = 0
            data_location[2] += 1

    def printArea(self, inventory_choose=False):
        self.hunger_points -= 1
        """Print out area onto screen."""
        inventory = self.showitems_list()
        radius = self.settings.light_radius + 2 if "Lantern" in inventory else self.settings.light_radius # Lanterns increase light amount
        levelLight = self.lighting.lightUp(self.area, self.location[0], self.location[1], self.dungeon_level, radius)
        inventory_index = -1
        zone = ""
        loc = [0, 0]
        inventory_show = True
        for row in self.area[self.dungeon_level]:
            for tile in row:
                light_level = levelLight[self.dungeon_level][loc[1]][loc[0]]
                if light_level in [2, 1]:
                    if light_level == 1:
                        zone += "\033[2m"  # Dimmed text for previously seen squares.
                    if loc == self.location:
                        zone += "@"
                    elif len(self.levelData[self.dungeon_level][loc[1]][loc[0]]) > 0:
                        zone += "%"
                    else:
                        zone += tile
                    if light_level == 1:
                        zone += "\033[0m"  # Reset text formatting
                else:
                    zone += " "
                loc[0] += 1
            if self.inventory_open or inventory_choose:
                if inventory_show:
                    if inventory_index == -1:
                        zone += "              \033[7mInventory\033[0m"
                    else:
                        if self.inventory_open:
                            zone += f"              {self.inventory[inventory_index][0]} ({self.inventory[inventory_index][1]})"
                        elif inventory_choose:
                            zone += f"              {self.alphabet[inventory_index]}) {self.inventory[inventory_index][0]} ({self.inventory[inventory_index][1]})"
                    inventory_index += 1
                    if inventory_index >= len(self.inventory):
                        inventory_show = False
            zone += "\n"
            loc[0] = 0
            loc[1] += 1

        # Print stored messages and the current zone
        printing = "\n".join(self.printed) + "\n" + zone + "\n"
        printing += f"{self.username} ST:{self.player_att['strength']} AT:{self.player_att['attack']} DE:{self.player_att['defense']} HP:{self.player_att['max_hp']}/{self.player_att['hp']}"
        printing += "\n" + f"{self.get_weight()} {self.get_food()}"
        system('clear')
        print(printing)
        self.printed = []

    def get_weight(self) -> str:
        max_weight = self.player_att['strength'] * 3 + (self.player_att['hp'] - (round(self.player_att['max_hp'] / 4)))
        weight = 0
        printing = ""
        for item in self.inventory:
            for key in self.items_list:
                if item[0] in self.items_list[key]:
                    weight += self.items_weight[key][item[0]] * item[1]
                    break
        if weight > max_weight:
            printing = "Burdened"
            if weight > round(max_weight * (3/2)):
                printing = "Strained"
                if weight > max_weight * 2:
                    printing = "Stressed"
                    if weight > round(max_weight * (12/5)):
                        printing = "\033[33mOvertaxed\033[0m"
                        if weight > max_weight * 3:
                            printing = "\033[31mOverloaded\033[0m"
        return printing
    def get_food(self) -> str:
        printing = ""
        if self.hunger_points < 150:
            printing = "Hungry"
            if self.hunger_points < 50:
                printing = "\033[33mWeak\033[0m"
                if self.hunger_points < 0:
                    printing = "\033[31mStarving\033[0m"
                    if self.hunger_points < -30:
                        print("You die of starvation.")
                        self.status = 2
        elif self.hunger_points > 800:
            printing = "Satiated"
        return printing

    def continue_investigate(self, key=""):
                    self.printed = []
                    if key in self.inventoryList():
                        match self.inventoryList()[key]:
                            case 'Apple':
                                self.printed.append("It appears to be a red, spherical object.")
                            case 'Chicken Nugget':
                                self.printed.append("It is a yellow food made from chicken. You wonder who put it here.")
                            case 'Golden Blåhaj Statue':
                                self.printed.append("It is a golden statue representing Blåhaj.")
                            case 'Mysterious Tablet':
                                self.printed.append("It appears to have many symbols engraved onto it, and is made out of stone.")
                            case 'Carrot':
                                self.printed.append("It is orange and cylindrical.")
                            case 'Nausea Potion':
                                self.printed.append("This does not seem like something good to drink.")
                            case 'Unknown Potion':
                                self.printed.append("It looks like some sort of liquid, but you do not know what it is.")
                            case 'Lantern':
                                self.printed.append("It appears to be a battery powered lantern. You wonder how they got the batteries.")
                            case 'Arnav Statue':
                                self.printed.append("It is a statue of a familiar figure.")
    def continue_floor_one(self, x=""):
                            if x.strip().lower() == "y":
                                self.printed.append("You reach the surface, and your blood turns to vinegar. (It's a very weird feeling)")
                                self.location = [99999, 99999]
                                self.status = 2
                            else:
                                self.printed.append("You decide that would be a bad idea.")

    def inventoryList(self) -> dict:
        """List the items in the inventory."""
        idx = 0
        items_list = {}
        for i in self.inventory:
            items_list[self.alphabet[idx]] = i[0]
            idx += 1
        return items_list

    def showitems_list(self) -> list:
        """Gives back a list of every item in a players inventory."""
        items_list = []
        for i in self.inventory:
            items_list.append(i[0])
        return items_list

    def checkKeydownEvents(self, key = None):
     if self.status != 2 and self.input == 0:
      """Run appropriate code for keydown events."""
      try:
        if key.char == 'i':
            self.inventory_open = 1 - self.inventory_open
        elif (key == "space") and (self.inventory_open):
            self.inventory_open = 0
        elif self.inventory_open == False:
                match key.char:
                    case "m":
                        """Use staircases."""
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
                            if self.dungeon_level == 1:
                                self.input = 2
                                sleep(0.1)
                                print("You hear the voice of Blåhaj, Thou must have the statue, or thy will regret this. Do you still want to go up? (y/n)=> ")
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
                    case ",":
                        if len(self.levelData[self.dungeon_level][self.location[1]][self.location[0]]) == 0:
                            self.printed.append("There is no item to pick up here.")
                        for info in self.levelData[self.dungeon_level][self.location[1]][self.location[0]]:
                            if info[0] == 1:
                                article = "a"
                                if info[2][0] in ["A", "E", "I", "O", "U"]:
                                    article = "an"
                                self.printed.append(f"You pick up {article} {info[2]}.")
                                self.levelData[self.dungeon_level][self.location[1]][self.location[0]].pop(0)
                                idx = 0
                                show = False
                                for item in self.inventory:
                                    if item[0] == info[2]:
                                        self.inventory[idx][1] += 1
                                        show = True
                                        break
                                    idx += 1
                                if not show:
                                    self.inventory.append([info[2], 1, info[3], info[5], info[6]]) #[name(str), amount(int), status(int), status known(bool), extra status(list of ints)]
                                    break
                    case "n":
                        self.printArea(True)
                        print("Which item? => ")
                        self.input = 1
                    case 'Q':
                        print("Are you sure you want to quit? (y/n)=>")
                        self.input = 3
                    case _:
                            self.printed.append(f"{key} is not a valid key.")
      except AttributeError:
        if not self.inventory_open:
            if key in [keyboard.Key.right, keyboard.Key.left,  keyboard.Key.up, keyboard.Key.down]:
                    """Move player in any direction."""
                    match key:
                        case keyboard.Key.up:
                            self.location[1] -= 1
                        case keyboard.Key.left:
                            self.location[0] -= 1
                        case keyboard.Key.down:
                            self.location[1] += 1
                        case _:
                            self.location[0] += 1
                    try:
                        if (self.area[self.dungeon_level][self.location[1]][self.location[0]] in ["-", "|", " "]):
                            match key:
                                case keyboard.Key.up:
                                    self.location[1] += 1
                                case keyboard.Key.left:
                                    self.location[0] += 1
                                case keyboard.Key.down:
                                    self.location[1] -= 1
                                case _:
                                    self.location[0] -= 1
                    except:
                        if key == keyboard.Key.up:
                            self.location[1] += 1
                        elif key == keyboard.Key.left:
                            self.location[0] += 1
                        elif key == keyboard.Key.down:
                            self.location[1] -= 1
                        else:
                            self.location[0] -= 1
                    if self.area[self.dungeon_level][self.location[1]][self.location[0]] == "=":
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
                            match i[3]:
                                case -1:
                                    curse = "\033[31mcursed "
                                case 0:
                                    curse = "\033[0muncursed "
                                case 1:
                                    curse = "\033[92mblessed "
                                case _:
                                    curse = "\033[35modd-looking "
                        article = "a"
                        if info[2][0] in ["A", "E", "I", "O", "U"]:
                            article = "an"
                        self.printed.append(f"{extras}There is {article} {curse}\033[0m{info[2]} on the floor here.")
            else:
                match key:
                    # Some random messages for obscure buttons.
                    case keyboard.Key.delete: self.printed.append("Why does that button even exist?")
                    case keyboard.Key.f19: self.printed.append("When will anyone even use a F19?")
                    case keyboard.Key.f20: self.printed.append("What kind of keyboard even has an F20!?")
                    case _:
                        if key == None:
                            self.printed.append("That is not a valid key.")
                        else:
                            if key not in [keyboard.Key.enter, keyboard.Key.backspace, keyboard.Key.space, keyboard.Key.shift, keyboard.Key.shift_r]:
                                self.printed.append(str(key)[4:-1] + str(key)[-1] + " is not a valid key.")
      if self.status == 2:
        self.death()
        return False
      if key not in [keyboard.Key.enter, keyboard.Key.delete, keyboard.Key.space, keyboard.Key.shift, keyboard.Key.shift_r] and self.input == 0:
        self.printArea()
     elif self.input != 0:
        if key not in [keyboard.Key.enter, keyboard.Key.shift, keyboard.Key.shift_r]:
            try:
                key_new = key.char
            except AttributeError:
                key_new = key
            match self.input:
                case 1:
                    self.continue_investigate(key_new)
                case 2:
                    self.continue_floor_one(key_new)
                case 3:
                    if key_new == "y":
                        self.save()
                        return False # Returning false ends pynput, ending the program
            self.input = 0
            self.printArea()
     if self.status == 2:
        self.death()
        return False
    def death(self):
        """Deal with people with skill issues."""
        print("You die...")
        sleep(0.1)
        #option = input("Do you want your possesions identified? (y/n)=> ")
        inventory_index = -1
        option = ""
        if option.lower().strip() == "y" or option == "":
            if len(self.inventory) != 0:
                for _ in range(len(self.inventory) + 1):
                    if inventory_index == -1:
                        print("\n\033[7mItems Held\033[0m")
                    else:
                        match self.inventory[inventory_index][2]:
                            case -1:
                                x = "\033[31mcursed"
                            case 0:
                                x = "\033[0muncursed"
                            case 1:
                                x = "\033[92mblessed"
                            case _:
                                x = "\033[35modd-looking"
                        print(x, self.inventory[inventory_index][0])
                    inventory_index += 1
                print()
            else:
                print("You held nothing.")
            print("\033[0mAttributes:")
            print("You had no resistances.")
            if self.get_weight() != "":
                print(f"You were {self.get_weight().lower()}.")
            else:
                print("You were not over-encumbered.")
            print("You were dead at the time of your death.")
    def save(self):
        """Run database queries and get results."""
        try:
            system('clear')
            #user varchar(40), area MEDIUMTEXT, player TINYTEXT, data MEDIUMTEXT, light MEDIUMTEXT, inventory MEDIUMTEXT, location varchar(10), other MEDIUMTEXT
            # Open connection and cursor, run the query, and fetch the results.
            cnx = connect(user='root', database='CoolHack')
            cursor = cnx.cursor(buffered=True)
            location = str(self.location.append(self.dungeon_level))
            cursor.execute(f'INSERT INTO saves(user, area, player, data, light, inventory, location, other) VALUES("
                           {self.username}", "{str(self.area)}", "{str(self.player_att)}", "
                           {str(self.levelData)}", "{str(self.lighting.levelLight)}", "{str(self.inventory)}", "{location}", "{str(self.hunger_points)}");')
            cnx.commit()
        except Error as err:
            print("There was an error with saving.", err)
        except Exception:
            print("There was an unkown error with saving.")