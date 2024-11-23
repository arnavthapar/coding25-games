from pynput import keyboard
from game_functions import Functions
from os import system
from mysql.connector import connect, Error

# Last Update: Nov 11 2024
def databaseRun(query=""):
    """Run database queries and get results."""
    try:
        system('clear')
        # Open connection and cursor, run the query, and fetch the results.
        cnx = connect(user='root', database='CoolHack')
        cursor = cnx.cursor(buffered=True)
        cursor.execute(query)
        cnx.commit()
        try:
            return cursor.fetchall()
        except:
            return None
    except Error as err:
        return [("There was an error with the query.\n" + err.msg, None, None, None, 'w')]
    except Exception:
        return [("There was an error with connecting to the database. An unknown error occurred", None, None, None, 'w')]

ascii = " _______  _______  _______  _        _______  _______           _______  _______  _       \n(  ____ \\(  ___  )(  ___  )( \\      (  ____ \\(  ____ )|\\     /|(  ___  )(  ____ \\| \\    /\\\n| (    \\/| (   ) || (   ) || (      | (    \\/| (    )|| )   ( || (   ) || (    \\/|  \\  / /\n| |      | |   | || |   | || |      | (__    | (____)|| (___) || (___) || |      |  (_/ / \n| |      | |   | || |   | || |      |  __)   |     __)|  ___  ||  ___  || |      |   _ (  \n| |      | |   | || |   | || |      | (      | (\\ (   | (   ) || (   ) || |      |  ( \\ \\ \n| (____/\\| (___) || (___) || (____/\\| (____/\\| ) \\ \\__| )   ( || )   ( || (____/\\|  /  \\ \\\n(_______/(_______)(_______)(_______/(_______/|/   \\__/|/     \\||/     \\|(_______/|_/    \\/"
colors = {"r":"\033[31m", "m":"\033[95m", "y":"\033[93m","g":"\033[92m", "b":"\033[34m", "w":""}
game_running = True
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
    print('Stretch the terminal so you can see the word "CoolerHack" for the best experience while playing.')
    print(ascii)
    print("\nPlaying as", username,"\n\np) Play CoolerHack 0.0\nl) Check leaderboard")
    if username != "guest":
        print("\ns) Change settings for account\no) Log out")
    else:
        print("\na) Log in to account\nc) Create account")
    print("\nq) Quit game\n\n"+dev_text)
    if int(user_status) > 0:
        print("u) Change status of users.")
    dev_text = ""
    mode = input("=> ")
    if mode == "q":
        system('clear')
        quit()
    elif mode == "o":
        username = "guest"
        user_status = 0
    elif mode == "p":
        if int(user_status) >= 0:
            menu = False
        else:
            dev_text = "Sorry, the game hasn't been finished yet, so only developers can access it."
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
        databaseRun(f'INSERT INTO users(name, password, wins, losses, color) VALUES("{username}","{password}", 0, 0, "w");')
        result = databaseRun("SELECT * FROM users")
        for i in result: userList[i[0]] = i[1]
    elif mode == "l":
        result = databaseRun('SELECT * FROM users ORDER BY wins DESC, losses ASC;')
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
                    print("#"+str(index)+".\033[3m "+ colors[i[4]] + i[0] +"\033[0m has " + str(i[2]) + " wins and " + str(i[3]) + " losses.")
                elif not i[0] == "guest":
                    print("#"+str(index)+". "+ colors[i[4]] + i[0] +"\033[0m has " + str(i[2]) + " wins and " + str(i[3]) + " losses.")
            if i[0] != "guest":
                index += 1
        if username != "guest":
            # The guest user should not recieve their own stats.
            print("\nYou are placed #" + str(userData[0]) + " and have " + str(userData[1]) + " wins and " + str(userData[2]) + " losses.")
        mode = input("\n\nPress enter to exit the leaderboard.")
    elif mode == "s" and username != "guest":
        system('clear')
        mode = input("DELETE) Delete ALL user data(All uppercase)\nc) Change the color of your name on the leaderboard\nn) Change your name.\np) to change your password.\n\n=> ")
        if mode == "DELETE":
            databaseRun('DELETE FROM users WHERE name="'+username+'";')
            print("User successfully deleted.")
            quit()
        if mode == "c":
            colorSelection = True
            system('clear')
            while colorSelection:
                color = input("What color do you want your name to be?\nr) red\ny) yellow\ng) green\nb) blue\nm) magenta\nw) white\n\n=> ")
                system('clear')
                if color in colors:
                    databaseRun('UPDATE users SET color="'+color+'" WHERE name="'+username+'";')
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
                elif statusUser not in userList:
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
"""Start up Coolerhack."""
functions = Functions(username)
x = -1
y = 0
for i in functions.area[functions.dungeon_level]:
        for m in i:
            x += 1
            if m == "<":
                functions.location[0] = x
                functions.location[1] = y
                break
        y += 1
        x = -1
functions.printArea()
with keyboard.Listener(
        on_press=functions.checkKeydownEvents) as listener:
    listener.join()