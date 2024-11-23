import dictlist
import random
import os
def randomize(): # Randomizes the word.
    wordtype = input("Do you want to input a word? If no, type length to choose the length of the word, or type no for a random word. ").lower()
    if wordtype == "length":
        length = True
        while length == True:
            length_2 = input("What length do you want? ")
            if length_2.isnumeric(): # Checks if length is a number.
                if int(length_2) == 189819:
                    word_str = dictlist.cheese
                    length = False
                elif (int(length_2) > 1 and int(length_2) < 15) or int(length_2) == 45: # Checks if the length is possible.
                    length = False
                else: print("There is no word of that length.") # Prints when there is no word of the length inputted.
            else: print("Please type a positive number.") # Prints when the length is not a positive number.
        while length == False:
            if int(length_2) != 189819:
                word_str = random.choice(dictlist.di)
                if len(word_str) == int(length_2): length = True
            else: length = True
    elif wordtype == "yes": word_str = input("Input the word. ")
    elif wordtype == "no": word_str = random.choice(dictlist.di)
    else:
        print("Please type: No, Yes, or Length.")
        word_str = randomize()
    return(word_str)
word_str = randomize()
word = []
shown_list = []
loop = 0
for _ in range(len(word_str)): # Creates the shown_list and word lists.
    shown_list.append("_")
    word.append(word_str[loop])
    loop += 1
index_list = word
guessed_letters = []
pics = ["  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========", "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========", "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========", "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========", "  +---+\n  |   |\n  O   |\n /|\  |\n      |\n      |\n=========", "  +---+\n  |   |\n  O   |\n /|\  |\n /    |\n      |\n=========", "  +---+\n  |   |\n  O   |\n /|\  |\n / \  |\n      |\n========="]
print (" _\n| |\n| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __ \n| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ \n| | | | (_| | | | | (_| | | | | | | (_| | | | |\n|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|\n                    __/ |\n                   |___/")
complete = False # The game is not won already.
lives = 6 # 6 mistakes and you are out.
"""Start the main game loop."""
while lives > 0 and complete == False:
    guess = input("Guess a letter: ")
    os.system('clear') # Clears the screen,
    if len(guess) == 1 and guess.isalpha(): # Checks if the guess is 1 character long and in the alphabet.
        if guess in word and guess not in guessed_letters:
            while guess in index_list:
                num = index_list.index(guess)
                shown_list[num] = word[num]
                index_list[num] = "~"
            guessed_letters.append(guess)
        elif guess in guessed_letters: print("You already guessed that letter.")
        else:
            lives -= 1
            guessed_letters.append(guess)
        if "_" not in shown_list: complete = True
    else: print("Please input one a time. It must be a letter of the alphabet.")
    print(pics[(6 - lives)])
    print(' '.join(shown_list))
if complete == True: print("Great job! You won.")
else:
    print("You lost.")
    print("The word was", word_str + ".")