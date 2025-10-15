from constant import Constants as _c
from constant import Combinations as _m
from os import system as sys
def printBottle(liquid:int):
    color = COLORS[liquid.value["color"]]
    print(f"\x1b[38;5;94m _____  \n |___|\n\33[0m /{color}###\33[0m\\\n|{color}#####\33[0m|\n|{color}#####\33[0m|\n|{color}#####\33[0m|\n|{color}#####\33[0m|\n \u203E\u203E\u203E\u203E\u203E")
def printCabinet(l:list):
    print("Current Cabinet")
    for i in l:
        print(i.name.replace("_", ""))
def listCabinet():
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    a = {}
    for i in enumerate(potionCabinet):
        print(f"{alphabet[i[0]]}) {i[1].name.replace('_', ' ')}")
        a[alphabet[i[0]]] = i[1]
    return a
cabinet = {_c.Nightrose:{"amount":1}, _c.Frostblossom:{"amount":1}}
potionCabinet = {_c.Instant_Freezing:{"amount":1}, _c.Create_Flowers:{"amount":1}, _c.Echoing:{"amount":1},_c.Enlargement:{"amount":1}}
effects = {}
shownEffects = {}
COLORS={"dred":"\x1b[38;5;1m", "reld":"\x1b[38;5;9m", "orange":"\x1b[38;5;214m", "yellow":"\x1b[38;5;227m", "gargreen":"\x1b[38;5;2m", "lgreen":"\x1b[38;5;46m",
        "dgreen":"\x1b[38;5;106m", "dblue":"\x1b[38;5;19m", "blue":"\x1b[38;5;27m", "lblue":"\x1b[38;5;39m", "purple":"\x1b[38;5;99m", "dpurple":"\x1b[38;5;97m",
        "violet":"\x1b[38;5;135m", "pink":"\x1b[38;5;219m", "white":"\33[0m", "backwhite":"\x1b[48;5;255m", "grey":"\x1b[38;5;248m", "black":"\x1b[38;5;0m",
        "ice":"\x1b[38;5;153m"}
alive = True
while alive:
    sys('clear')
    print("c) Check Cabinet")
    print("q) Check Potion Cabinet")
    #print("e) Combine Liquids")
    print("d) Drink Liquid")
    print("a) Create Potion")
    print("s) Investigate Liquid")
    #print("p) Pour Liquid")
    print("r) Throw Away")
    choice = input("\n=> ")
    sys('clear')
    match choice:
        case "q":
            printCabinet(potionCabinet)
            input(f"{COLORS["backwhite"]}continue\33[0m")
        case "c":
            printCabinet(cabinet)
            input(f"{COLORS["backwhite"]}continue\33[0m")
        case "e":
            pass
        case "d":
            a = listCabinet()
            x = input("=> ")
            if x in a:
                match a[x]:
                    case _c.Instant_Freezing:
                        print("You instantly freeze, and soon die.")
                        alive = False
                    case _c.Water:
                        print("It's water.")
                    case _c.Garbage:
                        print("This tastes really bad... You throw up.")
                    case _c.Remove_Rust:
                        print("It tastes like soda.")
                    case _c.Create_Flowers | _c.Indigestion:
                        print("You don't feel very good, but nothing too bad happens.")
                    case _c.Heating:
                        print("You are warm.")
                    case _c.Cooling:
                        print("You are cold.")
                    case _c.Levitation:
                        print("You are in the air, but not very much.")
                    case _c.Light_Poison:
                        print("You don't feel very good... You are going to die soon.")
                    case _c.Heavy_Poison:
                        print("You die after around 5 minutes.")
                        alive = False
                    case _c.Spicy:
                        print("You definitely don't want to drink that again. It's so spicy you feel like your mouth is actually burning.")
                    case _c.Sleep:
                        print("You fall asleep, and wake up later.")
                        print("") #! Time loss
                    case _c.Acid, _c.Shadow:
                        print("Your insides burn up. You die.")
                        alive = False
                    case _c.Digestion:
                        print("You seem to have a faster metabolism.")
                        #lose
                    case _c.Energy:
                        print("You feel energetic!")
                    case _c.Teleportation:
                        print("You are suddenly outside of your store. You walk back inside.")
                    case _c.Electricity:
                        print("Your insides feel like static electricity.")
                    case _c.Enlargement:
                        print("You become far larger than you usually are for some time, but it goes away soon.")
                    case _c.Shrinking:
                        print("You become far smaller than you usually are for some time, but it goes away soon.")
                    case _c.Mold_Removal | _c.Rusting | _c.Insect_Fighting_Bravery | _c.Memory_Enhancement | _c.Fire_Resistance | _c.Regeneration:
                        print("Nothing seems to happen.")
                    case _c.Stickiness:
                        print("You start sticking to every surface. This is definitely annoying.")
                    case _c.Slight_Invisibility:
                        print("You seem to disappear, but you can see yourself if you squint and look hard enough.")
                    case _c.Invisibility:
                        print("You disappear. You cannot see yourself.")
                    case _c.Second_Thoughts:
                        print("It tastes sort of soury, but you're not sure. Did you actully drink it? Maybe. You start to put the glass down, but you think about it first.")
                    case _c.Speed:
                        print("You are faster than before.")
                    case _c.Slowness:
                        print("You can't move very fast.")
                    case _c.Hearing:
                        print("You hear tiny noises. Anything moving is far louder than before.")
                    case _c.Fire:
                        print("You start burning, and die.")
                    case _c.Power_Amplification:
                        print("You feel strong.")
                    case _c.Silencing:
                        print("You can't talk.")
                    case _c.Echoing:
                        print("Your voice echos.")
                    case _c.Whispering:
                        print("You can't speak louder than a whisper.")
                    case _c.Frostburn:
                        print("The drink is insanely spicy yet incredibly cold.")
                    case _c.Glowing:
                        print("You start to glow.")
                potionCabinet[a[x]]["amount"] -= 1
                if potionCabinet[a[x]]["amount"] < 1:
                    del potionCabinet[a[x]]
                input(f"{COLORS["backwhite"]}continue\33[0m")
            else:
                input(f"{x} is not a valid input.\n{COLORS["backwhite"]}continue\33[0m")
        case "r":
            a = listCabinet()
            x = input("=> ")
            if x in a:
                potionCabinet[a[x]]["amount"] -= 1
                if potionCabinet[a[x]]["amount"] == 0:
                    del potionCabinet[a[x]]
                input(f"{COLORS["backwhite"]}continue\33[0m")
            else:
                input(f"{x} is not a valid input.\n{COLORS["backwhite"]}continue\33[0m")
        case "a":
            pass
        case "s":
            printBottle(_c.Instant_Freezing)
            input(f"{COLORS["backwhite"]}continue\33[0m")
        case "z":
            sys('clear')
            quit()