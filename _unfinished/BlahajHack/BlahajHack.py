from pynput import keyboard
from game_functions import Functions
from os import system
from mysql.connector import connect, Error
from sys import argv
# Last Update: March 29 2025
def databaseRun(query=""):
    """Run database queries and get results."""
    try:
        system('clear')
        # Open connection and cursor, run the query, and fetch the results.
        cnx = connect(user='root', database='blahajhack')
        cursor = cnx.cursor(buffered=True)
        cursor.execute(query)
        cnx.commit()
        try:
            return cursor.fetchall()
        except:
            return None
    except Error as err:
        return [("There was an error with connecting to the database.\n" + err.msg, None, None, None, 'w')]
    except Exception as err:
        if argv[-1] == "debug":
            return [(f"There was an error with connecting to the database. The error {err} occurred.", None, None, None, 'w')]
        else:
            return [("There was an error with connecting to the database. An unknown error occurred.", None, None, None, 'w')]
ascii = "░▒▓███████▓▒░░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░       ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░\n░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ \n░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░\n░▒▓███████▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░▒▓████████▓▒░▒▓████████▓▒░      ░▒▓█▓▒░      ░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓██████▓▒░\n░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░ \n░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ \n░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░       ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░"
#ascii = "                                                                                 ,--,\n    ,---,.   ,--,                 ,---,                                        ,--.'|                           ,-.\n  ,'  .'  \\,--.'|               ,--.' |                                     ,--,  | :                       ,--/ /|\n,---.' .' ||  | :               |  |  :                      .--.        ,---.'|  : '                     ,--. :/ |\n|   |  |: |:  : '               :  :  :                    .--,`|        |   | : _' |                     :  : ' /\n:   :  :  /|  ' |     ,--.--.   :  |  |,--.  ,--.--.       |  |.         :   : |.'  |  ,--.--.     ,---.  |  '  /\n:   |    ; '  | |    /       \\  |  :  '   | /       \\      '--`_         |   ' '  ; : /       \\   /     \\ '  |  :\n|   :     \\|  | :   .--.  .-. | |  |   /' :.--.  .-. |     ,--,'|        '   |  .'. |.--.  .-. | /    / ' |  |   \\\n|   |   . |'  : |__  \\__\\/: . . '  :  | | | \\__\\/: . .     |  | '        |   | :  | ' \\__\\/: . ..    ' /  '  : |. \\\n'   :  '; ||  | '.'| ,\" .--.; | |  |  ' | : ,\" .--.; |     :  | |        '   : |  : ; ,\" .--.; |'   ; :__ |  | ' \\ \\\n|   |  | ; ;  :    ;/  /  ,.  | |  :  :_:,'/  /  ,.  |   __|  : '        |   | '  ,/ /  /  ,.  |'   | '.'|'  : |--'\n|   :   /  |  ,   /;  :   .'   \\|  | ,'   ;  :   .'   \\.'__/\\_: |        ;   : ;--' ;  :   .'   \\   :    :;  |,'\n|   | ,'    ---`-' |  ,     .-./`--''     |  ,     .-./|   :    :        |   ,/     |  ,     .-./\\   \\  / '--'\n`----'              `--`---'               `--`---'     \\   \\  /         '---'       `--`---'     `----'\n                                                         `--`-'"
colors = {"r":"\33[31m", "m":"\33[95m", "y":"\33[93m","g":"\33[32m", "l":"\33[92m", "d":"\33[34m", "b":"\x1b[38;5;26m", "w":"\33[0m", "o":"\x1b[38;5;215m", "c":"\x1b[38;5;14m"}
menu = True
userList = {}
result = databaseRun('SELECT * FROM users;')
for i in result:
    userList[i[0]] = i[1]
status = databaseRun("SELECT name, status FROM users WHERE status>0;")
status2 = []
user_status = 0
username = "guest"
for m in status:
    status2.append(m[0])
if username in status2:
    for i in status:
        if username == i[0]:
            print(status)
            user_status = i[1]
            break
"""Starts the menu."""
dev_text = ""
while menu:
    system('clear')
    print('Stretch the terminal so you can see the word "BlahajHack" for the best experience while playing.')
    print(ascii)
    debug = "Debug" if argv[-1] == "debug" else ""
    print(f"{debug} Beta 1.13")
    print("\nPlaying as", username,"\n\np) Play BlåhajHack\nl) Check leaderboard")
    if username != "guest":
        print("\ns) Change settings for account\no) Log out")
    else:
        print("\na) Log in to account\nc) Create account")
    print("\nq) Quit game\n"+dev_text)
    if int(user_status) > 0:
        print("u) Change status of users.")
    mode = input("=> ")
    if mode == "q":
        system('clear')
        quit()
    elif mode == "o":
        username = "guest"
        user_status = 0
    elif mode == "p":
        menu = False
    elif mode == "a" and username == "guest":
        system('clear')
        newUser = input("Type your username. Typing nothing or a nonexistent username aborts.\n\n=> ")
        if not newUser == "guest":
            if newUser in userList:
                system('clear')
                password = input("Type your password. Typing an incorrect password aborts.\n\n=> ")
                if password == userList[newUser]:
                    username = newUser
                    if username in status2:
                        for i in status:
                            if username == i[0]:
                                user_status = i[1]
                                break
    elif mode == "c" and username == "guest":
        createUser = True
        cancel = False
        system('clear')
        while createUser:
            taken = False
            username = input("Type a username. Type nothing to abort.\n\n=> ")
            system('clear')
            if username == "":
                cancel = True
                createUser = False
                username = "guest"
            else:
                for i in userList:
                    if i.lower() == username.lower():
                        print("That username is already taken.")
                        taken = True
                if not taken:
                    if not username.isalnum():
                        print("Your password can only be made out of letters and numbers.")
                    elif username == "guest":
                        print("Your username cannot be guest:")
                    elif len(username) > 25:
                        print("Your name cannot be more than 25 characters.")
                    else:
                        createUser = False
                else: taken = False
        if not cancel: createUser = True
        while createUser:
            password = input("Type a password.\n\n=> ")
            if not password.isalnum():
                system('clear')
                print("Your password can only be made out of letters and numbers.")
            elif len(password) > 40:
                system('clear')
                print("Your password cannot be more than 40 characters.")
            else: createUser = False
        try:
            databaseRun(f'INSERT INTO users(name, password, wins, losses, color, status) VALUES("{username}","{password}", 0, 0, "w", 0);')
        except: pass
        result = databaseRun("SELECT * FROM users")
        for i in result: userList[i[0]] = i[1]
    elif mode == "l":
        result = databaseRun('SELECT * FROM users ORDER BY wins DESC, losses ASC, status DESC;')
        index = 1
        status3 = databaseRun("SELECT name FROM users WHERE status>0;")
        status4 = []
        for m in status3: status4.append(m[0])
        print("---TOP 5---")
        for i in result:
            if i[0] == username:
                userData = []
                userData.append(index)
                userData.append(i[2])
                userData.append(i[3])
            if index < 6:
                if i[0] in status2:
                    print("#"+str(index)+".\33[3m "+ colors[i[4]] + i[0] +"\33[0m has " + str(i[2]) + " win(s) and " + str(i[3]) + " loss(es).")
                elif not i[0] == "guest":
                    print("#"+str(index)+". "+ colors[i[4]] + i[0] +"\33[0m has " + str(i[2]) + " win(s) and " + str(i[3]) + " loss(es).")
            else: break
            if i[0] != "guest":
                index += 1
        if username != "guest":
            # The guest user should not recieve their own stats.
            print(f"\nYou are placed #{userData[0]} and have " + str(userData[1]) + " wins and " + str(userData[2]) + " losses.")
        mode = input("\n\nPress enter to exit the leaderboard.")
    elif mode == "s" and username != "guest":
        system('clear')
        mode = input("DELETE) Delete ALL user data(All uppercase)\nc) Change the color of your name on the leaderboard\nn) Change your name.\np) to change your password.\n\n=> ")
        if mode == "DELETE":
            databaseRun(f'DELETE FROM users WHERE name="{username}";')
            print("User successfully deleted.")
            quit()
        if mode == "c":
            colorSelection = True
            system('clear')
            while colorSelection:
                color = input(f"What color do you want your name to be?\n{colors['r']}r) red{colors['o']}\no) orange{colors['y']}\ny) yellow\n{colors['g']}g) green\n{colors['b']}b) blue\n{colors['c']}c) cyan\n{colors['m']}m) magenta\n\33[0mw) white\n\n=> ")
                system('clear')
                if color in colors:
                    databaseRun(f'UPDATE users SET color="{color}" WHERE name="{username}";')
                    colorSelection = False
                else: print("That is not a valid color.")
        if mode == "n":
            createUser = True
            system('clear')
            change = True
            while createUser:
                taken = False
                previous = username
                username = input("Type a username.\nType nothing to abort.\n\n=> ")
                system('clear')
                if username != "":
                    for i in userList:
                        if i.lower() == username.lower():
                            print("That username is already taken.")
                            taken = True
                    if not taken:
                        if not username.isalnum():
                            print("Your username must made of only letters and numbers.")
                        elif username == "guest":
                            print("Your username cannot be guest.")
                        elif len(username) > 25:
                            print("Your name cannot be more than 25 characters.")
                        else:
                            createUser = False
                    else: taken = False
                else:
                    createUser = False
                    username = previous
                    change = False
            if change:
                databaseRun('UPDATE users SET name="' + username + '"WHERE name="' + previous + '";')
                result = databaseRun('SELECT * FROM users;')
                for i in result: userList[i[0]] = i[1]
        if mode == "p":
            createUser = True
            system('clear')
            while createUser:
                password = input("Type a password.\nType nothing to cancel.\n\n=> ")
                system('clear')
                if password != "":
                    if not password.isalnum():
                        print("Your password must be alphanumeric.")
                    elif len(password) > 40:
                        print("Your password cannot be more than 40 characters.")
                    else: createUser = False
                else: createUser = False
            if password != "":
                databaseRun(f'UPDATE users SET password="{password}"WHERE name="{username}";')
                result = databaseRun('SELECT * FROM users;')
                for i in result: userList[i[0]] = i[1]
    elif mode == "u":
            if int(user_status) > 0:
                statusUser = input("Which user do you want to change the status of?")
                stats = input("To which level?")
                if int(stats) > int(user_status):
                    dev_text = "You cannot promote someone to a level higher than yourself."
                elif statusUser == "MrChickenNugget" or statusUser == username:
                    dev_text = "You cannot change the status level of someone with an already higher or same status level than you."
                elif str(statusUser) not in userList:
                    dev_text = "That user does not exist."
                else:
                    databaseRun(f'UPDATE users SET status="{stats}"WHERE name="{statusUser}";')
                status = databaseRun("SELECT name, status FROM users WHERE status>0;")
                status2 = []
                for m in status: status2.append(m[0])
                if username in status2:
                    for i in status:
                        if username == i[0]:
                            print(status)
                            user_status = i[1]
                            break
    else:
        system('clear')
"""Start up BlåhajHack."""
functions = Functions(username, argv)
functions.printArea()
with keyboard.Listener(on_press=functions.checkKeydownEvents) as listener:
    listener.join()