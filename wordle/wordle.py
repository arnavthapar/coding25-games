from dictlist import di as dictionary
from os import system
from random import choice

def clear(): system('clear')
selection = ""

while selection not in ("c", "r"):
    selection = input(""
                    "c) Choose word\n"
                    "r) Random word\n"
                    "=> ")
clear()
word = ""
if selection == "c":
    while len(word) != 5:
        word = input("Pick a word => ")
        clear()
        if len(word) != 5:
            print("The word must be five letters.")
elif selection == "r": word = choice(dictionary)
clear()
win = 0
attempts = 0
all = []
while win == 0 and attempts < 6:
    guess = ""
    attempts += 1
    while 1:
        for i in all:
            print(i)
        guess = input("Pick a word => ")
        clear()
        if len(guess) != 5:
            print("The word must be five letters.")
        elif guess not in dictionary:
            print("That is not an allowed word.")
        else:
            break
    shown = ""
    for idx, i in enumerate(guess):
        if word[idx] == i:
            shown += f"\x1b[38;5;34m{i}\033[0m"
        elif i in word:
            shown += f"\x1b[38;5;228m{i}\033[0m"
        else: shown += i
    all.append(shown)
    if guess == word:
        win == 1
for i in all:
    print(i)
if win == 1:
    print("You won!")
else:
    print(f"You lost. The word was {word}.")