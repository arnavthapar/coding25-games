from os import system
t = '-123456789'
game = 1
f = [1, 2, 3, 4, 5, 6, 7, 8, 9]
def check(t: str) -> int:
    game = 1
    if t[1:4] == "xxx":
        game = 2
    elif t[4:7] == "xxx":
        game = 2
    elif t[7:10] == "xxx":
        game = 2
    elif (t[1] == "x" and t[4] == "x" and t[7] == "x"):
        game = 2
    elif (t[2] == "x" and t[5] == "x" and t[8] == "x"):
        game = 2
    elif (t[3] == "x" and t[6] == "x" and t[9] == "x"):
        game = 2
    elif (t[1] == "x" and t[5] == "x" and t[9]== "x"):
        game = 2
    elif (t[3] == "x" and t[7] == "x" and t[5] == "x"):
        game = 2
    elif t[1:4] == "ooo":
        game = 3
    elif t[4:7] == "ooo":
        game = 3
    elif t[7:10] == "ooo":
        game = 3
    elif (t[1] == "o" and t[4] == "o" and t[7] == "o"):
        game = 3
    elif (t[2] == "o" and t[5] == "o" and t[8] == "o"):
        game = 3
    elif (t[3] == "o" and t[6] == "o" and t[9] == "o"):
        game = 3
    elif (t[1] == "o" and t[5] == "o" and t[9]== "o"):
        game = 3
    elif (t[3] == "o" and t[7] == "o" and t[5] == "o"):
        game = 3
    no_draw = False
    if game == 1:
        for i in f:
            if str(i) in t:
                no_draw = True
                break
        if not no_draw:
            game = 0
    return game
def print_area(t) -> None:
    print(t[1] + "|" + t[2] + "|" + t[3])
    print("-----")
    print(t[4] + "|" + t[5] + "|" + t[6])
    print("-----")
    print(t[7] + "|" + t[8] + "|" + t[9])
while game == 1:
    system('clear')
    print_area(t)
    game = check(t)
    loc_set = True
    if game != 1:
        loc_set = False
    while loc_set:
        loc = input("Player 1: Input the location of the x => ")
        if loc.isnumeric():
            loc = int(loc)
            if loc > 0 and loc < 10:
                if t[loc] != "o" and t[loc] != "x":
                    t = t.replace(str(loc), "x")
                    loc_set = False
                else:
                    print("Please enter a valid value.")
            else:
                print("Please enter a valid value.")
        else:
            print("Please enter a valid value.")
    loc_set = True
    system('clear')
    print_area(t)
    game = check(t)
    if game != 1:
        loc_set = False
    while loc_set:
        loc = input("Player 2: Input the location of the x => ")
        if loc.isnumeric():
            loc = int(loc)
            if loc > 0 and loc < 10:
                if t[loc] != "o" and t[loc] != "x":
                    t = t.replace(str(loc), "o")
                    loc_set = False
                else:
                    print("Please enter a valid value.")
            else:
                print("Please enter a valid value.")
        else:
            print("Please enter a valid value.")
match game:
    case 0:
        print("The game ended in a tie.")
    case 2:
        print("Player 1 has won.")
    case 3:
        print("Player 2 has won.")