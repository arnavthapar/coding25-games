from os import system
from keyboard import on_press, wait, KEY_DOWN
import level_data as ld
from random import randrange
from secrets import token_bytes
from enemy import Enemies
from mysql.connector import connect, Error
def databaseRead(query):
    system('clear')
    try:
        # Opens cursor, runs the query, and fetches the results.
        cnx = connect(user='root', database='CoolHack')
        cursor = cnx.cursor(buffered=True)
        cursor.execute(query)
        cnx.commit()
        try: result = cursor.fetchall()
        except: result = None
        cursor.close()
        cnx.close()
        return result
    # Catches exceptions and prints an error message.
    except Error as err:
        print('Error: ' + err.msg + "\nPlease contact Arnav for help, or try restarting the program.")
        quit()

def enemyLightArea(location): # Handles enemy lighting.
    global enemyVisibleLevel
    def enemy_search_horizontal(location_y, room_l, room_r):
        global enemyVisibleLevel
        count = 0
        for i in range(room_r):
            enemyVisibleLevel[location_y+count] = True
            count += 1
        count = 0
        for i in range(room_l):
            enemyVisibleLevel[location_y+count] = True
            count -= 1
    enemyVisibleLevel = []
    for i in level:
        enemyVisibleLevel.append(False)
    i = True
    if ld.levelFloor["level" + str(levelNumber)][location] == ".":
        y = location
        length_r, length_l = findLength(location)
        while i :
            if (ld.levels["level" + str(levelNumber)][y] != "-" and
                ld.levels["level" + str(levelNumber)][y] != "#"
                and ld.levels["level" + str(levelNumber)][y] != "=" and
                ld.levels["level" + str(levelNumber)][y] != "~"):
                enemy_search_horizontal(y, length_l, length_r)
                y += ld.levelLength[levelNumber]
            else:
                enemy_search_horizontal(y, length_l, length_r)
                i = False
        i = True
        y = location
        while i :
            if (ld.levelFloor["level" + str(levelNumber)][y] != "-" and
                ld.levelFloor["level" + str(levelNumber)][y] != "#"
                and ld.levelFloor["level" + str(levelNumber)][y] != "="):
                enemy_search_horizontal(y, length_l, length_r)
                y -= ld.levelLength[levelNumber]
            else:
                enemy_search_horizontal(y, length_l, length_r)
                i = False
    enemyVisibleLevel[location] = True
    enemyVisibleLevel[location+ld.levelLength[levelNumber]] = True
    enemyVisibleLevel[location-ld.levelLength[levelNumber]] = True
    enemyVisibleLevel[location-1] = True
    enemyVisibleLevel[location+1] = True

def enemyPhase(player):
    index = 0
    for m in enemyData["level" + str(levelNumber)]:
        if len(enemyData["level" + str(levelNumber)][index]) > 0:
            for m in enemyData["level" + str(levelNumber)][index]:
                i = m
            if level[index+1] == "@" or level[index-1] == "@" or level[index+ld.levelLength[levelNumber]] == "@" or level[index-ld.levelLength[levelNumber]] == "@":
                randomize = randrange(1, 2)
                if randomize == 1:
                    print("The " + i + " attacks!")
                    player_data['hp'] -= Enemies.enemies[i]['atk']
            else:
                enemyLightArea(index)
                if enemyVisibleLevel[player]:
                    if debug == 1: print("Enemy at ", index, " sees the player.")
                    randomize = 1 # randrange(0, 2)
                    if randomize >= 1:
                        difference = index - player
                        if difference >= ld.levelLength[levelNumber]:
                            if (len(enemyData["level" + str(levelNumber)][index - ld.levelLength[levelNumber]]) == 0
                            and ld.levelFloor["level" + str(levelNumber)][index - ld.levelLength[levelNumber]] == "."):
                                enemyData["level" + str(levelNumber)][index - ld.levelLength[levelNumber]][i] = enemyData["level" + str(levelNumber)][index][i]
                                enemyData["level" + str(levelNumber)][index].pop(i)
                        elif (difference <= 0 - ld.levelLength[levelNumber] and
                        len(enemyData["level" + str(levelNumber)][index + ld.levelLength[levelNumber]]) == 0
                        and ld.levelFloor["level" + str(levelNumber)][index + ld.levelLength[levelNumber]] == "."):
                            enemyData["level" + str(levelNumber)][index + ld.levelLength[levelNumber]][i] = enemyData["level" + str(levelNumber)][index][i]
                            enemyData["level" + str(levelNumber)][index].pop(i)
                        elif difference < 0:
                            if len(enemyData["level" + str(levelNumber)][index + 1]) == 0:
                                enemyData["level" + str(levelNumber)][index + 1][i] = enemyData["level" + str(levelNumber)][index][i]
                                enemyData["level" + str(levelNumber)][index].pop(i)
                        elif difference > 0:
                            if len(enemyData["level" + str(levelNumber)][index - 1]) == 0:
                                enemyData["level" + str(levelNumber)][index - 1][i] = enemyData["level" + str(levelNumber)][index][i]
                                enemyData["level" + str(levelNumber)][index].pop(i)
        index += 1

def createEnemy() -> None:
    exit = False
    while not exit:
        if len(enemyData["level" + str(levelNumber)][levelNumber-10]) == 0:
            randomEnemy = True
            counter = 0
            while randomEnemy:
                randomize = randrange(0, len(ld.levels["level" + str(levelNumber)]))
                if (ld.levelFloor["level" + str(levelNumber)][randomize] == "." or ld.levelFloor["level" + str(levelNumber)][randomize] == "#") and not level[randomize] == "@" and not visibleLevel["level" + str(levelNumber)][randomize] and len(levelData["level"+str(levelNumber)][randomize]) == 0:
                    randomEnemy = False
                elif counter > 100:
                    exit = True
                    randomEnemy = False
                    break
                counter += 1
            if not exit:
                if levelNumber <= 5:
                        randomEnemy = randrange(1, 5)
                        index = 0
                        for i in Enemies.enemies:
                            if index == randomEnemy:
                                break
                            index += 1
                        enemyData["level" + str(levelNumber)][randomize][i] = Enemies.enemies[i]['health']
        exit = True

def initializeData() -> None: # Creates the level data and level light dictionaries.
    global levelLight, levelData, p_area, enemyData
    levelLight = {}
    p_area = {}
    levelData = {}
    enemyData = {}
    for i in ld.levels:
        levelData[i] = []
        levelLight[i] = []
        p_area[i] = []
        enemyData[i] = []
        for m in ld.levels[i]:
            levelData[i].append([])
            levelLight[i].append(False)
            p_area[i].append("")
            enemyData[i].append({})

def visible():
    global visibleLevel
    visibleLevel = {}
    for i in ld.levels:
        visibleLevel[i] = []
        for m in ld.levels[i]:
            visibleLevel[i].append(False)

def findLength(place):
    count_r = 0
    count_l = 0
    u = False
    while not u:
        if ld.levelFloor["level" + str(levelNumber)][place+count_r] == "-" or ld.levelFloor["level" + str(levelNumber)][place+count_r] == "|" or ld.levelFloor["level" + str(levelNumber)][place+count_r] == "#"  or ld.levelFloor["level" + str(levelNumber)][place+count_r] == " " or ld.levelFloor["level" + str(levelNumber)][place+count_r] == "=" or ld.levelFloor["level" + str(levelNumber)][place+count_r] == "~": u = True
        count_r += 1
    u = False
    count = 0
    while not u:
        if ld.levelFloor["level" + str(levelNumber)][place+count] == "-" or ld.levelFloor["level" + str(levelNumber)][place+count] == "|" or ld.levelFloor["level" + str(levelNumber)][place+count] == "#" or ld.levelFloor["level" + str(levelNumber)][place+count] == " " or ld.levelFloor["level" + str(levelNumber)][place+count] == "=" or ld.levelFloor["level" + str(levelNumber)][place+count] == "~": u = True
        count -= 1
        count_l += 1
    return count_r, count_l

def lightArea(loc, mov, movement): # Handles lighting.
    def search_horizontal(location_y, room_l, room_r):
        count = 0
        for m in range(room_r):
            levelLight["level" + str(levelNumber)][location_y+count] = True
            visibleLevel["level" + str(levelNumber)][location_y+count] = True
            count += 1
        count = 0
        for m in range(room_l):
            levelLight["level" + str(levelNumber)][location_y+count] = True
            visibleLevel["level" + str(levelNumber)][location_y+count] = True
            count -= 1

    visible()
    if not movement:
        mov = 0
    location = loc + mov
    i = True
    if ld.levelFloor["level" + str(levelNumber)][location] == ".":
        y = location
        length_r, length_l = findLength(location)
        while i :
            if ld.levels["level" + str(levelNumber)][y] != "-" and ld.levels["level" + str(levelNumber)][y] != "#" and ld.levels["level" + str(levelNumber)][y] != "=" and ld.levels["level" + str(levelNumber)][y] != "~":
                search_horizontal(y, length_l, length_r)
                y += ld.levelLength[levelNumber]
            else:
                search_horizontal(y, length_l, length_r)
                i = False
        i = True
        y = location
        while i :
            if ld.levels["level" + str(levelNumber)][y] != "-" and ld.levels["level" + str(levelNumber)][y] != "#":
                search_horizontal(y, length_l, length_r)
                y -= ld.levelLength[levelNumber]
            else:
                search_horizontal(y, length_l, length_r)
                i = False
    levelLight["level" + str(levelNumber)][(loc+mov + ld.levelLength[levelNumber] + 1)] = True
    visibleLevel["level" + str(levelNumber)][(loc+mov + ld.levelLength[levelNumber] + 1)] = True
    levelLight["level" + str(levelNumber)][(loc+mov - ld.levelLength[levelNumber] - 1)] = True
    visibleLevel["level" + str(levelNumber)][(loc+mov - ld.levelLength[levelNumber] - 1)] = True
    levelLight["level" + str(levelNumber)][(loc+mov + ld.levelLength[levelNumber] - 1)] = True
    visibleLevel["level" + str(levelNumber)][(loc+mov + ld.levelLength[levelNumber] - 1)] = True
    levelLight["level" + str(levelNumber)][(loc+mov - ld.levelLength[levelNumber] + 1)] = True
    visibleLevel["level" + str(levelNumber)][(loc+mov - ld.levelLength[levelNumber] + 1)] = True
    levelLight["level" + str(levelNumber)][(loc+mov)] = True
    visibleLevel["level" + str(levelNumber)][(loc+mov)] = True
    levelLight["level" + str(levelNumber)][loc+mov-ld.levelLength[levelNumber]] = True
    visibleLevel["level" + str(levelNumber)][loc+mov+ld.levelLength[levelNumber]] = True
    levelLight["level" + str(levelNumber)][loc+mov+ld.levelLength[levelNumber]] = True
    visibleLevel["level" + str(levelNumber)][loc+mov-ld.levelLength[levelNumber]] = True
    levelLight["level" + str(levelNumber)][loc+mov+1] = True
    visibleLevel["level" + str(levelNumber)][loc+mov-1] = True
    levelLight["level" + str(levelNumber)][loc+mov-1] = True
    visibleLevel["level" + str(levelNumber)][loc+mov+1] = True

def loadArea(): # Prints the level.
    if not inventory: # Prints when inventory is closed.
        if not info:
            area = ""
            global p_area
            index = 0
            for i in level:
                if levelLight["level" + str(levelNumber)][index] or i == "\n":
                    if visibleLevel["level" + str(levelNumber)][index] or i == "\n": # Checks if you can see a square currently.
                        if len(enemyData["level" + str(levelNumber)][index]) > 0 and not i == "@":
                            for m in enemyData["level" + str(levelNumber)][index]:
                                    i = m
                            if not hallu:
                                area += Enemies.enemies[i]['color'] + Enemies.enemies[i]['symbol'] + "\033[0m"
                                p_area["level"+str(levelNumber)][index] = Enemies.enemies[i]['color'] + Enemies.enemies[i]['symbol'] + "\033[0m"
                            else:
                                randomize = randrange(1, 2)
                                area += Enemies.enemies[randomize]['color'] + Enemies.enemies[randomize]['symbol'] + "\033[0m"
                                p_area["level"+str(levelNumber)][randomize] = Enemies.enemies[i]['color'] + Enemies.enemies[str(enemyData[i])]
                        elif i == "&":
                            if levelNumber == 50:
                                if not hallu:
                                    area += "\033[33m&\033[0m"
                                    p_area["level"+str(levelNumber)][index] = "\033[33m&\033[0m"
                                else:
                                    area += "\033[33m&\033[0m\033[7m\033[32m\033[3m"
                                    p_area["level"+str(levelNumber)][index] = "\033[33m&\033[0m\033[7m\033[32m\033[3m"
                            else:
                                if hallu != True:
                                    area += "\033[97m&\033[0m"
                                    p_area["level"+str(levelNumber)][index] = "\033[97m&\033[0m"
                                else:
                                    area += "\033[97m&\033[0m\033[7m\033[32m\033[3m"
                                    p_area["level"+str(levelNumber)][index] = "\033[97m&\033[0m\033[7m\033[32m\033[3m"
                        elif hallu and not super_hallu:
                            randomize = randrange(1, 10)
                            if randomize == 2 and i != "\n": area += str(token_bytes(6))[4]
                            else:
                                area += i
                                p_area["level"+str(levelNumber)] += i
                        elif super_hallu:
                            randomize = randrange(2, 4)
                            if i != "\n" and randomize == 3:  area += str(token_bytes(6))[4]
                            else:
                                area += i
                                p_area["level"+str(levelNumber)][index] = i
                        else:
                            area += i
                            p_area["level"+str(levelNumber)][index] = i
                    else:
                        if not hallu:
                            area += ("\033[2m" + p_area["level"+str(levelNumber)][index] + "\033[0m") # Prints the previous area's square if you can't see the square.
                        else:
                            area += ("\033[2m" + p_area["level"+str(levelNumber)][index] + "\033[0m\033[7m\033[32m\033[3m") # Prints the previous area's square if you can't see the square.
                else:
                    if not hallu: area += " "
                    else: area += "\033[0m \033[7m\033[32m\033[3m"
                    p_area["level"+str(levelNumber)][index] = "\033[0m \033[7m\033[32m\033[3m"
                index += 1
            print(area + "\n")
            print(name.title() + " the Blåhaj Enthusiast | HP " + str(player_data['hp']) + "/" + str(player_data['max_hp']) + " ATK: " + str(player_data['atk']) +  " DEF: " + str(player_data['defense']), "Turn: ", turnNumber)
        else:
            print("Help\nEscape = End Game\nArrows = Move Around\n, = Pick Up Items\ni = Exit/Enter Inventory\nm = Use Stairs\nd = Drink\n")
    else: # Prints when inventory is open.
        print("Inventory\nHP: " + str(player_data['hp']) + "/" + str(player_data['max_hp']))
        if debug == 1: print(inventoryItems)
        for i in inventoryItems:
            if inventoryItems[i] == 1:
                print(i)
            else: print(str(inventoryItems[i]) + " " + i + "s")

def createLevel(level): # Creates the list needed to track the level.
    level = []
    for i in ld.levels["level"+str(levelNumber)]:
        level.append(i)
    return level

def on_key_press(event): # Check for key presses and act accordingly.
    global dead, win
    if not dead and not win:
        if event.event_type == KEY_DOWN:
            global levelData, inventory, levelNumber, level, death_query, potion_query, hallu, super_hallu, info, player_data, enemyVisibleLevel, turnNumber
            moved = False
            movement = False
            add = 0
            key = event.name
            turn = False
            system('clear')
            if debug == 1: print(key)
            length = len(level)
            i = 0
            levelNum = "level" + str(levelNumber)
            while i < length:
                if "@" == level[i]:
                    break
                i += 1
            if key != "y":
                death_query = False
                potion_query = False
            if not inventory:
                if key == "left" or key == "up" or key == "down" or key == "right":
                    if hallu != True:
                        if key == "left": add = -1
                        elif key == "right": add = 1
                        elif key == "up": add = 0 - ld.levelLength[levelNumber]
                        elif key == "down": add = ld.levelLength[levelNumber]
                    else:
                        randomize = randrange(1,3)
                        if randomize != 1:
                            if key == "left": add = -1
                            elif key == "right": add = 1
                            elif key == "up": add = 0 - ld.levelLength[levelNumber]
                            elif key == "down": add = ld.levelLength[levelNumber]
                        else:
                            randomize = randrange(0, 4)
                            if randomize <= 1: add = -1
                            elif randomize == 2: add = 1
                            elif randomize == 3: add = 0 - ld.levelLength[levelNumber]
                            elif randomize >= 4: add = ld.levelLength[levelNumber]
                    if debug == 1: print(str(level[i+add]), str(i), str(add), str(enemyData[levelNum][i+add]))
                    if level[i+add] != "-" and level[i+add] != "|" and level[i+add] != "\n" and level[i+add] != " ":
                        level[i+add] = "@"
                        level[i] = ld.levels[levelNum][i]
                        moved=True
                        turn = True
                    else:
                        movement = True
                    #if len(enemyData[i + add]) > 1:
                        
                    if ld.levels[levelNum][i+add] == "=":
                        ld.levels[levelNum][i+add] = "~"
                    if ld.levels[levelNum][i+add] == "%" or ld.levels[levelNum][i+add] == "[" or ld.levels[levelNum][i+add] == "&":
                        if len(levelData[levelNum][i+add]) == 0 and ld.levels[levelNum][i+add] == "%":
                            levelData[levelNum][i+add].append(ld.items["consumables"][randrange(0, 3, 1)])
                        elif len(levelData[levelNum][i+add]) == 0 and ld.levels[levelNum][i+add] == "[":
                            levelData[levelNum][i+add].append(ld.items["potions"][0])
                        elif len(levelData[levelNum][i+add]) == 0 and ld.levels[levelNum][i+add] == "&":
                            if levelNumber == 50:
                                levelData[levelNum][i+add].append(ld.items["statues"][0])
                            elif levelNumber == 4:
                                levelData[levelNum][i+add].append(ld.items["statues"][1])
                                print("There is something engraved on the statue here. It says, \"Ishil was here.\"")
                            elif levelNumber == 5:
                                print("There is something engraved on the statue here. It says, \"Ajan was here.\"")
                                levelData[levelNum][i+add].append(ld.items["statues"][2])
                        if not hallu and not super_hallu:
                            if len(levelData[levelNum][i+add]) == 1:
                                if levelData[levelNum][i+add][0].lower()[0] == "a" or levelData[levelNum][i+add][0].lower()[0] == "e" or levelData[levelNum][i+add][0].lower()[0] == "i" or levelData[levelNum][i+add][0].lower()[0] == "o" or levelData[levelNum][i+add][0].lower()[0] == "u":
                                    print("Here is an "+ levelData[levelNum][i+add][0].lower() + ".")
                                else: print("Here is a "+ levelData[levelNum][i+add][0].lower() + ".")
                            elif len(levelData[levelNum][i+add]) > 1:
                                if levelData[levelNum][i+add][0].lower()[0] == "a" or levelData[levelNum][i+add][0].lower()[0] == "e" or levelData[levelNum][i+add][0].lower()[0] == "i" or levelData[levelNum][i+add][0].lower()[0] == "o" or levelData[levelNum][i+add][0].lower()[0] == "u":
                                    print("Here is an " + levelData[levelNum][i+add][0].lower() + ", along with other items.")
                                else: print("Here is a " + levelData[levelNum][i+add][0].lower() + ", along with other items.")
                        else: print("There is something here.")
                    if hallu and not super_hallu:
                        randomize = randrange(0, 500)
                        if debug == 1: print(randomize)
                        if randomize == 4:
                            print("\033[0mYou feel better.")
                            hallu = False
                    elif super_hallu:
                        randomize = randrange(0,1000)
                        if debug == 1: print(randomize)
                        if randomize == 283: super_hallu = hallu = False
                elif key == "m":
                    if ld.levels[levelNum][i] == "<":
                        if levelNumber == 1:
                            if "Golden Blåhaj Statue" in inventoryItems:
                                print("You head up, and Blåhaj is now pleased. You win!\nPress Escape and start the program again to restart.")
                                win = True
                            elif not hallu and not super_hallu: print("You hear the voice of Blåhaj, \"Thy must collect the stolen treasure.\" \nDo you really want to go up?(y/n)")
                            elif hallu and not super_hallu: print("You hear something like \"Thee must call the stalactite treason.\" \nbut you can't make out the sounds very well.\nDo you still want to go up?(y/n)")
                            else:
                                print("You go up, and then you get hit by a disintigration laser.")
                                player_data['hp'] = 0
                            death_query = True
                        else:
                            levelNumber -= 1
                            if debug == 1:print(levelNumber)
                            level = createLevel(level)
                            length = len(level)
                            i = 0
                            while i < length:
                                if ">" == level[i]: break
                                i += 1
                            level[i] = "@"
                            lightArea(i, 0, True)
                            levelLight["level" + str(levelNumber)][i] = True
                    elif ld.levels[levelNum][i] == ">":
                            levelNumber += 1
                            if debug == 1:print(levelNumber)
                            level = createLevel(level)
                            length = len(level)
                            i = 0
                            while i < length:
                                if "<" == level[i]:
                                    break
                                i += 1
                            level[i] = "@"
                            lightArea(i, 0, True)
                            levelLight["level" + str(levelNumber)][i] = True
                    elif not hallu:
                        print("There is no staircase here.")
                        movement = True
                    else:
                        print("You trip, and hit the floor. There is probably no staircase here.")
                        movement = True
                    turn = True
                elif key == "y":
                    if death_query :
                        print("You go up, and then Blåhaj fires a disintegration laser at you.")
                        player_data['hp'] = 0
                        death_query = False
                    elif potion_query :
                        if not hallu: print("\033[7m\033[32m\033[3mYou drink the potion, and you start to feel weird...")
                        if hallu:
                            print("You feel extremely terrible...")
                            super_hallu = True
                        if inventoryItems['Nausea Potion'] == 1: inventoryItems.pop('Nausea Potion')
                        else: inventoryItems['Nausea Potion'] -= 1
                        hallu = True
                        turn = True
                elif key == "d":
                    if "Nausea Potion" in inventoryItems:
                        print("Do you want to drink your Potion of Nausea? (y/n)")
                        potion_query = True
                elif key == "0":
                    if not info: info = True
                    else: info = False
                # Messages for obscure buttons.
                elif key == "page down": print("Why did you even click that?")
                elif key == "page up": print("Page up? Did you really think that would do something?")
                elif key == "end": print("It's Escape to end the game, not the actual end button.")
                elif key == "f3": print("What are you doing?")
                elif key == "f8": print("So many buttons. YOU DON'T NEED TO CLICK 'EM ALL! This isn't Pokemon!")
                elif key == "+": print("CHEESE")
                elif key == "caps lock": print("Capitals are stupid. use lowercase.")
                elif key == "right option": print("Who even uses the right option button?")
                elif key == "forward delete": print("Why does that button even exist?")
                elif key == "home": print("...")
                elif key == "*": print("bruh")
                elif key == "tab": print("Im going to tab you out of existence.")
                elif key == "f16": print("Why do you have an F16, and why are you pressing it?")
                elif key == "f19": print("When will anyone even use a F19?")
                elif key == "f2": print("﷽𒈙꧅ဪ")
                elif key == "f1": print("ƒ1 ≠ çhéêsè")
                elif key == ",":
                    if len(levelData[levelNum][i]) > 0:
                        if levelData[levelNum][i][0] != "":
                            if debug == 1: print(levelData[levelNum][i][0])
                            if len(levelData[levelNum][i]) == 1: ld.levels[levelNum][i] = "."
                            if not(levelData[levelNum][i][0] in inventoryItems.keys()): inventoryItems[levelData[levelNum][i][0]] = 1
                            else:
                                for m in inventoryItems.keys():
                                    if m == levelData[levelNum][i][0]: break
                                inventoryItems[m] += 1
                            levelData[levelNum][i].remove(levelData[levelNum][i][0])
                            level[i] = "@"
                    elif not hallu:
                        print("There is nothing here to pick up.")
                        movement = True
                    else:
                        print("You swipe your hand at the floor, but you don't feel anything.")
                        movement = True
                    turn = True
            if key == "i":
                if inventory : inventory = False
                else: inventory = True
            if not potion_query and not death_query:
                if turn:
                    if not movement: randomize = randrange(0, 101)
                    else:
                        randomize = randrange(0, 5)
                        if randomize != 3: randomize = randrange(0, 51)
                        else: randomize = randrange(0, 101)
                    if debug == 1: print(randomize)
                    if randomize != 5: createEnemy()
                    enemyPhase(i+add)
            if player_data['hp'] <= 0:
                player_data['hp'] = 0
                dead = True
                print("\nYou die...\nPress Escape and start the program again to restart.")
            lightArea(i, add, moved)
            if turn: turnNumber += 1
            loadArea()

colors = {"r":"\033[31m", "m":"\033[95m", "y":"\033[93m","g":"\033[92m", "b":"\033[34m", "w":""}
loginUser = True
loginPass = True
userList = {}
system('clear')
result = databaseRead('SELECT * FROM users;')
for i in result: userList[i[0]] = i[1]
while loginUser:
    user = input("Type your username, or type c to create a new user. Type e to end the program.\n")
    if user == "c":
        loginPass = False
        createUser = True
        system('clear')
        while createUser :
            taken = False
            user = input("Type a username: ")
            for i in userList:
                if i.lower() == user.lower():
                    system('clear')
                    print("That username is already taken.")
                    taken = True
            if not taken:
                if not user.isalnum():
                    system('clear')
                    print("Your username must be alphanumeric.")
                elif user == "c" or user == "e":
                    system('clear')
                    print("Your username cannot be c or e.")
                elif len(user) > 25:
                    system('clear')
                    print("Your name cannot be more than 25 characters.")
                else: createUser = False
            else: taken = False
        createUser = True
        while createUser :
            password = input("Type a password: ")
            if not password.isalnum():
                system('clear')
                print("Your password must be alphanumeric.")
            elif len(password) > 40:
                system('clear')
                print("Your password cannot be more than 40 characters.")
            else: createUser = False
            databaseRead('INSERT INTO users(name, password, wins, losses, color) VALUES("'+user+'","'+password+'", 0, 0, "w");')
            loginUser = False
            result = databaseRead("SELECT * FROM users")
            for i in result: userList[i[0]] = i[1]
    else:
        if user == "e": quit()
        if user in userList: loginUser = False
        else:
            system('clear')
            print("Try again, that is not a user which exists.")
system('clear')
while loginPass :
    x = input("Type your password. Type e to end the program.\033[30m\n")
    if x == "e": quit()
    if x == userList[user]: loginPass = False
    else:
        system('clear')
        print("\033[0mThat password is incorrect.")
modeSelection = True
system('clear')
while modeSelection :
    mode = input("\033[0mDo you want to view the leaderboard, or start a game? \n(l = leaderboard, g = game, s = user settings, e = end session)\n")
    if mode == "l":
        result = databaseRead('SELECT * FROM users ORDER BY wins DESC, losses ASC;')
        index = 1
        for i in result:
            if i[0] == user:
                userData = []
                userData.append(index)
                userData.append(i[2])
                userData.append(i[3])
            if index < 6:
                if i[0] == "MrChickenNugget":
                    print("#"+str(index)+".\033[3m "+colors[i[4]] + "MrChickenNugget" +"\033[0m has " + str(i[2]) + " wins and " + str(i[3]) + " losses.")
                else: print("#"+str(index)+". "+colors[i[4]] + i[0] +"\033[0m has " + str(i[2]) + " wins and " + str(i[3]) + " losses.")
            index += 1
        print("\nYou are placed #" + str(userData[0]) + " and have " + str(userData[1]) + " wins and " + str(userData[2]) + " losses.")
    elif mode == "g":
        system('clear')
        modeSelection = False
        # Initializes the variables.
        player_data = {
            'max_hp':12,
            'hp':1299999,
            'atk':5,
            'defense':2
        }
        debug = 0 # Debug mode. 1 = On, 0 = Off.
        levelNumber = 4 # Starting level.
        """Programs:CoolHack.py, enemy.py, level_data.py"""
        print("Expand your terminal until you can see the word \"CoolHack\" for the best experience when playing.")
        print(ld.ascii)
        name = input("What will your name be?")
        level = ld.levels # Creates the list to track the level.
        dead = death_query = hallu = inventory = info = super_hallu = win = False
        inventoryItems = {} # Makes your inventory empty when game is started.
        initializeData() # Creates the levelData, p_area, and levelLight dictionaries.
        level = createLevel(level)
        key = 'None' # Initializes the key variable.
        # Creates player.
        length = len(level)
        enemies_killed = 0
        i = 0
        turnNumber = 0
        enemyVisibleLevel = {}
        while i < length:
            if "<" == level[i]: break
            i += 1
        level[i] = "@"
        system('clear')
        lightArea(i, 0, False)
        loadArea() # Loads the area for the first time.
        print("Press 0 for help with controls.\nPress Escape to exit the game.")
        on_press(on_key_press)
        wait('esc') # When Escape is pressed, the game ends.
    elif mode == "s":
        system('clear')
        mode = input("Type DELETE (all uppercase) to delete the user. This will delete ALL user data!\nType c to change the color of your name on the leaderboard.\nType n to change your name.\nType p to change your password.\n")
        if mode == "DELETE":
                databaseRead('DELETE FROM users WHERE name="'+user+'";')
                print("User successfully deleted.")
                quit()
        if mode == "c":
            colorSelection = True
            while colorSelection :
                system('clear')
                color = input("Type the color you want your name to be.\nred = r\nyellow = y\ngreen = g\nblue = b\nmagenta = m\nwhite = w\n")
                if color in colors:
                    databaseRead('UPDATE users SET color="'+color+'"WHERE name="'+user+'";')
                    colorSelection = False
                else: print("Please type r, y, g, b, m, or w.")
        if mode == "n":
            createUser = True
            system('clear')
            change = True
            while createUser :
                taken = False
                previous = user
                user = input("Type a username.\nType c to cancel.\n")
                if user != "c":
                    for i in userList:
                        if i.lower() == user.lower():
                            system('clear')
                            print("That username is already taken.")
                            taken = True
                    if not taken:
                        if not user.isalnum():
                            system('clear')
                            print("Your username must be alphanumeric.")
                        elif user == "c" or user == "e":
                            system('clear')
                            print("Your username cannot be c or e.")
                        elif len(user) > 25:
                            system('clear')
                            print("Your name cannot be more than 25 characters.")
                        else: createUser = False
                    else: taken = False
                else:
                    createUser = False
                    user = previous
                if change:
                    databaseRead('UPDATE users SET name="'+user+'"WHERE name="'+previous+'";')
                    result = databaseRead('SELECT * FROM users;')
                    for i in result: userList[i[0]] = i[1]
        if mode == "p":
            createUser = True
            system('clear')
            while createUser:
                taken = False
                previous = userList[user]
                password = input("Type a password.\nType c to cancel.\n")
                if not password.isalnum():
                    system('clear')
                    print("Your password must be alphanumeric.")
                elif len(password) > 40:
                    system('clear')
                    print("Your password cannot be more than 40 characters.")
                else: createUser = False
                databaseRead('UPDATE users SET password="'+password+'"WHERE name="'+previous+'";')
                result = databaseRead('SELECT * FROM users;')
                for i in result: userList[i[0]] = i[1]
    elif mode == "e": quit()
    else:
        system('clear')
        print("Type l, g, e, or s.")