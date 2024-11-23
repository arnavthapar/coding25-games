import dictlist
import random
import os

def randomize():
    wordtype = input("Do you want to input a word? If no, type length to choose the length of the word, or type no for a random word. ").lower()
    if wordtype == "length":
        while True:
            length_2 = input("What length do you want? ")
            if length_2.isnumeric():
                length_2 = int(length_2)
                if length_2 == 189819:
                    return dictlist.cheese
                elif 1 < length_2 < 15 or length_2 == 45:
                    while True:
                        word_str = random.choice(dictlist.di)
                        if len(word_str) == length_2:
                            return word_str
                else:
                    print("There is no word of that length.")
            else:
                print("Please type a positive number.")
    elif wordtype == "yes":
        return input("Input the word. ")
    elif wordtype == "no":
        return random.choice(dictlist.di)
    else:
        print("Please type: No, Yes, or Length.")
        return randomize()

word_str = randomize()
word = list(word_str)
shown_list = ["_" for _ in word]
guessed_letters = []
pics = [
    "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\  |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\  |\n /    |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\  |\n / \  |\n      |\n========="
]

print("""
 _                                           
| |                                          
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __ 
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \\
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |                      
                   |___/                       
""")

complete = False
lives = 6

while lives > 0 and not complete:
    guess = input("Guess a letter: ").lower()
    os.system('clear')
    if len(guess) == 1 and guess.isalpha():
        if guess in word and guess not in guessed_letters:
            for i, letter in enumerate(word):
                if letter == guess:
                    shown_list[i] = guess
            guessed_letters.append(guess)
        elif guess in guessed_letters:
            print("You already guessed that letter.")
        else:
            lives -= 1
            guessed_letters.append(guess)
        if "_" not in shown_list:
            complete = True
    else:
        print("Please input one letter at a time. It must be a letter of the standard English alphabet.")
    
    print(pics[6 - lives])
    print(' '.join(shown_list))

if complete:
    print("Great job! You won.")
else:
    print("You lost. The word was", word_str + ".")
