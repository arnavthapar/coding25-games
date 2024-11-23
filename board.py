from keyboard import on_press, wait, KEY_DOWN
from random import randrange
from os import system
from time import sleep
def wins():
    global players
    if players[4] == int(player_count) - 2:
        if players[4] == 0: players[player_num-1]["w"] = "Won 1st Place"
        elif players[4] == 1: players[player_num-1]["w"] = "Won 2nd Place"
        elif players[4] == 2: players[player_num-1]["w"] = "Won 3rd Place"
        area = find_area()
        system('clear')
        print(area)
        area = 0
        for i in players:
            if i["w"] == "":
                players[5] += str(area+1)
                break
            area += 1
        global game_running
        game_running = False
    if players[4] == 0: players[player_num-1]["w"] = "Won 1st Place"
    if players[4] == 1: players[player_num-1]["w"] = "Won 2nd Place"
    elif players[4] == 2: players[player_num-1]["w"] = "Won 3rd Place"
    players[4] += 1
    players[5] += str(player_num)
def find_area():
    area = "Cool Game Name v1\n"
    for i in range(int(player_count)): area += "Player " + str(i+1) + " =-= Coins: "+str(players[i]["c"])+"|Square Points: "+str(players[i]["p"])+" " + players[i]["w"] + "\n"
    area += "Current Player: " + str(player_num) + "\n\n"
    for i in board:
        if i == -1: area += "  "
        elif players[0]['loc'] == i and players[0]["w"] == "": area += (colors[colormap[i]+5] + "1\033[0m"+ " ")
        elif players[1]['loc'] == i and players[1]["w"] == "": area += (colors[colormap[i]+5] + "2\033[0m"+ " ")
        elif players[2]['loc'] == i and players[2]["w"] == "" and (player_count == "3" or player_count == "4"): area += (colors[colormap[i]+5] + "3\033[0m"+ " ")
        elif players[3]['loc'] == i and players[3]["w"] == "" and player_count == "4": area += (colors[colormap[i]+5] + "4\033[0m"+ " ")
        elif i >= 0: area += (colors[colormap[i]] + "▣ " + "\033[0m")
        elif i == -2: area += "\n"
    return area
def game(): # Starts the dice rolling.
    global rolling, roll, current_roll
    rolling = True
    system('clear')
    area = find_area()
    print(area)
    roll = randrange(1, dice+1)
    current_roll = True
    print("Press r to roll the dice.")
def on_key_press(event): # Check for the s press to start the dice rolling and continue turn.
    global rolling, player_num, players, objective, current_roll
    if ((event.event_type == KEY_DOWN) and ((rolling and event.name == "r") and (current_roll))):
        current_roll = False
        print("Roll:",str(roll))
        for i in range(roll):
            sleep(0.3)
            if players[player_num-1]['loc'] + 1 == 68 and objective == 0: break
            elif players[player_num-1]['loc'] + 1 == 68:
                players[player_num-1]['loc'] = 0
                print("\nYou were teleported to the first square!")
            if players[player_num-1]['loc'] - 1 < 0 and objective == 3: break
            if objective != 3: players[player_num-1]['loc'] += 1
            else: players[player_num-1]['loc'] -= 1
            area = find_area()
            system('clear')
            print(area,"\nRoll:",str(roll))
        sleep(1)
        if players[player_num-1]['loc'] == 67:
            if objective == 1:
                players[player_num-1]['loc'] = 67
                print("Wow! Player "+str(player_num)+" just won by reaching the end!")
                wins()
        elif players[player_num-1]['loc'] <= 0:
            players[player_num-1]['loc'] = 0
            if objective == 3: wins()
        if colormap[players[player_num-1]['loc']] == 1:
            coins = randrange(1, 11)
            print("You landed on a red square.\nYou gain 1 square point but lost " + str(coins) + " coin(s).")
            players[player_num-1]['c'] -= coins
            if players[player_num-1]['c'] < 1: players[player_num-1]['c'] = 0
            players[player_num-1]['p'] += 1
            if objective == 2 and players[player_num-1]['p'] >= 20: wins()
            if objective == 5 and players[player_num-1]['p'] >= 25: wins()
            if objective == 6 and players[player_num-1]['p'] >= 15 and players[player_num-1]['c'] < 40: wins()
        elif colormap[players[player_num-1]['loc']] == 3:
            coins = randrange(1, 11)
            print("You landed on a green square.\nYou gain 1 square point and " + str(coins) + " coin(s).")
            players[player_num-1]['c'] += coins
            players[player_num-1]['p'] += 1
            if objective == 2 and players[player_num-1]['p'] >= 20: wins()
            if objective == 5 and players[player_num-1]['p'] >= 25: wins()
            if objective == 4 and players[player_num-1]['c'] >= 100: wins()
            if objective == 6 and players[player_num-1]['p'] >= 15 and players[player_num-1]['c'] < 40: wins()
        elif colormap[players[player_num-1]['loc']] == 2:
            choosing = True
            prev_objective = objective
            while choosing:
                objective = randrange(1, 7)
                if objective != prev_objective: choosing = False
            print("You landed on a yellow square. The objective has changed!")
            if objective == 1: print("Now, the objective is to get to the last square!")
            elif objective == 2: print("Now, the objective is to have at least 20 square points!")
            elif objective == 3: print("Now, the objective is to get to the first square!\nYou now move backwards.")
            elif objective == 4: print("Now, the objective is to have at least 100 coins!")
            elif objective == 5: print("Now, the objective is to have at least 25 square points!")
            elif objective == 6: print("Now, the objective is to have at least 15 square points, but have less than 40 coins!")
        elif colormap[players[player_num-1]['loc']] == 4:
            print("You landed on a blue space.\nYou can sabotage another player with coins!")
            if players[player_num-1]["c"] < 5: print("\nYou don't have enough coins to sabotage...")
            else:
                sabotaging = True
                while sabotaging:
                    print("a = 5 coins to remove 15 coins from someone\nb = 40 coins to remove 5 square points from someone\nc = 30 coins to remove 60 coins from someone\ne = don't sabotage")
                    sabotage = input("Which sabotage would you like to do?\n")
                    if sabotage == "a":
                        sabotage = "c1505"
                        sabotaging = False
                    elif sabotage == "b":
                        if players[player_num-1]["c"] >= 30:
                            sabotage = "p0540"
                            sabotaging = False
                        else:
                            area = find_area()
                            system('clear')
                            print(area, "\nYou don't have enough coins for that.")
                    elif sabotage == "c":
                        if players[player_num-1]["c"] >= 45:
                            sabotage = "c6030"
                            sabotaging = False
                        else:
                            area = find_area()
                            system('clear')
                            print(area, "\nYou don't have enough coins for that.")
                    elif sabotage == "d":
                        
                        
                        sabotaging = False
                    else:
                        area = find_area()
                        system('clear')
                        print(area, "\nYou can choose a, b, c, or d.")
                if sabotage != "d":
                    sabotaging = True
                    while sabotaging:
                        player = input("Which player do you want to sabotage?\n")
                        if not player.isnumeric():
                            area = find_area()
                            system('clear')
                            print(area, "\nChoose a player number.")
                        elif int(player) <= int(player_count):
                            player = int(player)
                            players[player-1][sabotage[0]] -= int(sabotage[1:3])
                            players[player_num-1][sabotage[0]] -= int(sabotage[3:5])
                            if players[player-1][sabotage[0]] < 0: players[player-1][sabotage[0]] = 0
                            if players[player_num-1][sabotage[0]] < 0: players[player_num-1][sabotage[0]] = 0
                            sabotaging = False
                            print("Sabotaging complete.")
                        else:
                            area = find_area()
                            system('clear')
                            print(area, "\nChoose a player number.")
        sleep(5)
        if player_num < int(player_count): player_num += 1
        else: player_num = 1
        checking = True
        while checking:
            if players[player_num-1]["w"] != "": player_num += 1
            else: checking = False
            if player_num > int(player_count): player_num = 1
        rolling = False

query = True
while query == True:
    player_count = input("Choose a number of players from 2 to 4. ")
    if player_count == "2" or player_count == "3" or player_count == "4": query = False
    else:
        system('clear')
        print("Type 2, 3, or 4.")
rolling = False
board =[-1,0,-1,-1,15,16,17,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-2,-1,1,-1,-1,14,-1,18,-1,-1,-1,-1,-1,-1,62,61,60,59,58,57,56,55,54,53,52,-1,-1, -2,-1,2,-1,-1,13,-1,19,-1,-1,-1,-1,-1,-1,63,-1,-1,-1,-1,-1,-1,-1,-1,-1,51,-1,-1, -2,-1,3,-1,-1,12,-1,20,-1,-1,-1,-1,-1,-1,64,-1,-1,-1,-1,-1,-1,-1,-1,-1,50,-1,-1, -2,-1,4,5,-1,11,-1,21,-1,25,26,27,28,-1,65,-1,-1,-1,-1,-1,-1,-1,-1,-1,49,-1,-1, -2,-1,-1,6,-1,10,-1,22,23,24,-1,-1,29,-1,66,-1,-1,-1,-1,-1,-1,-1,46,47,48,-1,-1, -2,-1,-1,7,8,9,-1,-1,-1,-1,-1,-1,30,-1,67,-1,-1,-1,-1,42,43,44,45,-1,-1,-1,-1, -2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,31,-1,-1,-1,-1,-1,-1,41,-1,-1,-1,-1,-1,-1,-1, -2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,32,33,34,35,36,38,39,40,-1,-1,-1,-1,-1,-1,-1]
colors = {0:"\033[95m", 1:"\033[31m", 2:"\033[93m",3:"\033[92m", 4:"\033[34m", 5:"\033[105m", 6:"\033[41m", 7:"\033[103m",8:"\033[102m", 9:"\033[44m"}
# 1 Red, 0 Magenta, 2 Yellow, 3 Green, 4 Blue,
colormap = [0, 1, 1, 3, 4, 1, 2, 3, 1, 3, 1, 3, 2, 3, 1, 2, 3, 1, 3, 3, 1, 1, 1, 4, 2, 1, 1, 2, 2, 3, 1, 4, 1, 3, 4, 1, 1, 4, 4, 2, 3, 4, 2, 4, 1, 4, 3, 3, 2, 4, 2, 1, 3, 3, 4, 1, 4, 3, 1, 3, 3, 3, 1, 1, 3, 2, 2, 0]
# ▣ (for copy paste)
game_running = True
players = [{"loc":0, "c":0, "p":0, "w":""}, {"loc":0, "c":0, "p":0, "w":""}, {"loc":0, "c":0, "p":0, "w":""}, {"loc":0, "c":0, "p":0, "w":""}, 0, ""]
player_num = 1
objective = 0
""" Settings """
dice = 6 # The type of dice.
on_press(on_key_press)
while game_running:
    if not rolling: game()
print("\nThe game has finished!")
for i in range(int(player_count)):
    if i == 0: place = "st"
    elif i == 1: place = "nd"
    elif i == 2: place = "rd"
    else: place = "th"
    print(str((i+1)) + place + " Place: Player " + str(players[5][i]))
print("\nPlayer " + players[5][0] + " has won the game. Congratulations!")