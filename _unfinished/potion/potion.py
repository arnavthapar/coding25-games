from constant import Constants as _c
from constant import Combinations as _m
from os import system as sys
from math import floor
from random import randrange
def printBottle(liquid:_c):
    if liquid.value["color"] in COLORS:
        color = COLORS[liquid.value["color"]]
    else: color = COLORS["gargreen"]
    print(f"\x1b[38;5;94m _____  \n |___|\n\33[0m /{color}###\33[0m\\\n|{color}#####\33[0m|\n|{color}#####\33[0m|\n|{color}#####\33[0m|\n|{color}#####\33[0m|\n \u203E\u203E\u203E\u203E\u203E")

def printCabinet(l:list[_c]):
    print("Current Cabinet")
    for i in l:
        print(f"{COLORS[i.value["color"]]}{i.name.replace("_", " ")}\33[0m")
def addEffect(effect:_c):
    effects[effect] = effect.value["length"]

def addPotion(*potions:_c):
    for i in potions:
        potionCabinet.setdefault(i, {"amount": 0})["amount"] += 1

def removePotion(*potions:_c):
    for i in potions:
        if i in potionCabinet:
            potionCabinet[i]["amount"] -= 1
            if potionCabinet[i]["amount"] <= 0:
                del potionCabinet[i]

def removeIngredient(*ingredients:_c):
    for i in ingredients:
        if i in cabinet:
            cabinet[i]["amount"] -= 1
            if cabinet[i]["amount"] <= 0:
                del cabinet[i]

def listCabinet(l:list[_c], removed:_c | None = None) -> dict[str, _c]:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    a = {}
    offset = 0
    for idx, val in enumerate(l):
        if val != removed:
            print(f"{alphabet[idx-offset]}) {val.name.replace('_', ' ')} ({l[val]["amount"]})")
            a[alphabet[idx-offset]] = val
        else:
            offset = 1
    return a

cabinet = {_c.Nightrose:{"amount":2}, _c.Frostblossom:{"amount":2}, _c.Whispleaf:{"amount":1}}
potionCabinet = {_c.Speed:{"amount":1}, _c.Sleep:{"amount":17}}
effects = {}
COLORS={"dred":"\x1b[38;5;1m", "red":"\x1b[38;5;9m", "orange":"\x1b[38;5;214m", "yellow":"\x1b[38;5;227m", "gargreen":"\x1b[38;5;2m", "lgreen":"\x1b[38;5;46m",
        "dgreen":"\x1b[38;5;106m", "dblue":"\x1b[38;5;19m", "blue":"\x1b[38;5;27m", "lblue":"\x1b[38;5;39m", "purple":"\x1b[38;5;99m", "dpurple":"\x1b[38;5;97m",
        "violet":"\x1b[38;5;135m", "pink":"\x1b[38;5;219m", "white":"\33[0m", "backwhite":"\x1b[48;5;255m", "grey":"\x1b[38;5;248m", "black":"\x1b[38;5;0m",
        "ice":"\x1b[38;5;153m"}
alive = True
timeRemoval = 0
time = [1, 0, 1]
while alive:
    sys('clear')
    print(f"It is {time[0]}:{time[1]:02}, on day {time[2]}.")
    print("c) Check Cabinet")
    print("q) Check Potion Cabinet")
    print("d) Drink Liquid")
    print("a) Create Potion")
    print("s) Investigate Liquid")
    print("r) Throw Away")
    print("z) Exit")
    if len(effects) != 0:
        print("Current Effects:")
        for i in effects:
            print(i.name)
    choice = input("\n=> ")
    sys('clear')
    match choice:
        case "q":
            printCabinet(potionCabinet)
            input(f"{COLORS["backwhite"]}continue\33[0m")
        case "c":
            printCabinet(cabinet)
            input(f"{COLORS["backwhite"]}continue\33[0m")
        case "d":
            a = listCabinet(potionCabinet)
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
                        effects = {}
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
                        addEffect(_c.Poisoned)
                    case _c.Heavy_Poison:
                        print("You die after around 5 minutes.")
                        alive = False
                    case _c.Spicy:
                        print("You definitely don't want to drink that again. It's so spicy you feel like your mouth is actually burning.")
                    case _c.Sleep:
                        print("You fall asleep, and wake up later.")
                        timeRemoval += randrange(2, 6)
                    case _c.Acid:
                        print("Your insides burn up. You die.")
                        alive = False
                    case _c.Shadow:
                        print("Your vision blurs significantly, and you hear a horrible ringing noise...\nYou drop to the ground, as you can't hold your weight anymore. You feel as if your bones were disintigrating. They are, and you soon die.")
                        alive = False
                    case _c.Digestion:
                        print("You seem to have a faster metabolism.")
                        for i in effects:
                            i = floor(i/2)
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
                        if a[x] == _c.Fire_Resistance:
                            addEffect(_c.Fire_Resisting)
                        elif a[x] == _c.Regeneration:
                            addEffect(_c.Regenerating)
                    case _c.Stickiness:
                        print("You start sticking to every surface. This is definitely annoying.")
                    case _c.Slight_Invisibility:
                        print("You seem to disappear, but you can see yourself if you squint and look hard enough.")
                        addEffect(_c.Invisible)
                    case _c.Invisibility:
                        print("You disappear. You cannot see yourself.")
                        addEffect(_c.Invisible)
                    case _c.Second_Thoughts:
                        print("It tastes sort of soury, but you're not sure. Did you actully even drink it?\nYou start to put the bottle down, but you have to think about it first.")
                    case _c.Speed:
                        print("You are faster than before.")
                        addEffect(_c.Quickened)
                    case _c.Slowness:
                        print("You can't move very fast.")
                        addEffect(_c.Slowed)
                    case _c.Hearing:
                        print("You hear tiny noises. Anything moving is far louder than before.")
                    case _c.Fire:
                        print("You start burning, and die.")
                    case _c.Power_Amplification:
                        print("You feel strong.")
                    case _c.Silencing:
                        print("You can't talk.")
                        addEffect(_c.Silenced)
                    case _c.Echoing:
                        print("Your voice echos.")
                    case _c.Whispering:
                        print("You can't speak louder than a whisper.")
                    case _c.Frostburn:
                        print("The drink is insanely spicy yet incredibly cold.")
                    case _c.Glowing:
                        print("You start to glow.")
                    case _:
                        print("What even is this thing???")
                removePotion(a[x])
                input(f"{COLORS["backwhite"]}continue\33[0m")
            else:
                input(f"{x} is not a valid input.\n{COLORS["backwhite"]}continue\33[0m")
        case "r":
            choice = input("Throw away an ingredient or a potion?\na) Ingredient\nb) Potion\n\n=> ")
            if choice == "b":
                a = listCabinet(potionCabinet)
            elif choice == "a":
                a = listCabinet(cabinet)
            else:
                input(f"{x} is not a valid input.\n{COLORS["backwhite"]}continue\33[0m")
                continue
            x = input("=> ")
            if x in a:
                if choice == "b":
                    removePotion(a[x])
                elif choice == "a":
                    removeIngredient(a[x])
                input(f"{COLORS["backwhite"]}continue\33[0m")
            else:
                input(f"{x} is not a valid input.\n{COLORS["backwhite"]}continue\33[0m")
        case "a":
            listed1 = listCabinet(cabinet)
            print("Pick the first ingredient. Type anything not listed above to abort.")
            choice1 = input("=> ")
            if choice1 not in listed1:
                print("That is not a valid letter.")
                input(f"{COLORS["backwhite"]}continue\33[0m")
                continue
            sys('clear')
            listed2 = listCabinet(cabinet, listed1[choice1])
            print("Pick the second ingredient. Type anything not listed above to abort.")
            choice2 = input("=> ")
            if choice2 not in listed2:
                print("That is not a valid letter.")
                input(f"{COLORS["backwhite"]}continue\33[0m")
                continue
            choice1 = listed1[choice1]
            choice2 = listed2[choice2]
            if _m.combinations[choice1.name][choice2.name] == None:
                result = _c.Garbage
            else: result = _m.combinations[choice1.name][choice2.name]
            print(f"You combined {choice1.name} and {choice2.name}, and got a Potion of {result.name}!")
            addPotion(result)
            timeRemoval += 1
            removeIngredient(choice1, choice2)
            input(f"{COLORS["backwhite"]}continue\33[0m")
        case "s":
            listed = listCabinet(potionCabinet)
            print("Pick the potion to investigate. Type anything not listed above to abort.")
            choice = input("=> ")
            if choice in listed:
                printBottle(listed[choice])
                match listed[choice]:
                    case _c.Instant_Freezing:
                        print("It is freezing cold. It's somewhat solid, but still liquid enough to drink. If you drank it though, it would probably freeze you to death because of the temperature.")
                    case _c.Water:
                        print("It's water.")
                    case _c.Garbage:
                        print("Whatever this is, it does not seem like you should drink it.")
                    case _c.Remove_Rust:
                        print("It's fizzy.")
                    case _c.Create_Flowers | _c.Indigestion:
                        print("It's very viscous.")
                    case _c.Heating | _c.Spicy:
                        print("It is warm.")
                    case _c.Cooling:
                        print("It is cold.")
                    case _c.Levitation:
                        print("Your finger flicks upward when you try to put it in the liquid.")
                    case _c.Light_Poison | _c.Heavy_Poison:
                        print("It stings to touch.")
                    case _c.Sleep | _c.Teleportation:
                        print("It's a translucent purple.")
                    case _c.Acid | _c.Shadow:
                        print("It hurts a lot when you touch the liquid, probably better not to do it again.")
                    case _c.Digestion:
                        print("It smells nice.")
                    case _c.Energy:
                        print("It smells like coffee.")
                    case _c.Electricity:
                        print("When you put your finger in it, it gains a lot of static electricity.")
                    case _c.Enlargement:
                        print("It's somewhat glossy. It's a highly saturated green.")
                    case _c.Shrinking:
                        print("It's looks solid, but acts like a liquid. It's a very saturated pink.")
                    case _c.Mold_Removal | _c.Rusting | _c.Insect_Fighting_Bravery | _c.Memory_Enhancement | _c.Fire_Resistance | _c.Regeneration | _c.Second_Thoughts | _c.Hearing | _c.Silencing | _c.Power_Amplification:
                        print("Nothing seems too special about this potion.")
                    case _c.Stickiness:
                        print("Your finger feels like you put glue on it.")
                    case _c.Slight_Invisibility | _c.Invisibility:
                        print("Your finger almost seemed to disappear.")
                    case _c.Speed:
                        print("You feel more aware when you touch it.")
                    case _c.Slowness:
                        print("It takes an unsual amount of time to get your finger out of the liquid.")
                    case _c.Fire:
                        print("Your hand lights on fire, and when you take it out, it extinguishes. It's a incredibly bright orange.")
                    case _c.Echoing:
                        print("Your hand feels larger when you put it in, but nothing visually happens.")
                    case _c.Whispering:
                        print("Your hand feels smaller when you put it in, but nothing visually happens.")
                    case _c.Frostburn:
                        print("Your hand feels cold and hot at the same time.")
                    case _c.Glowing:
                        print("It's incredibly bright. It's hard to look directly at.")
                    case _:
                        print("Where did you get this?")
            input(f"{COLORS["backwhite"]}continue\33[0m")
        case "z":
            sys('clear')
            quit()
    for i in effects.copy():
        effects[i] -= timeRemoval
        if effects[i] <= 0:
            del effects[i]
    time[0] += timeRemoval
    timeRemoval = 0
    if time[0] > 10:
        print("It's getting late. You go to sleep...")
        print("You wake up and finish the start of your day.")
        print("It is now 1 PM.")
        time[0:1] = [1, 0]
        time[2] += 1
        effects = {}
        input(f"{COLORS["backwhite"]}continue\33[0m")