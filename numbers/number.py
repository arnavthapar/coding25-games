from random import randrange
from os import system

correctAnswer = True
while correctAnswer:
    digits = input("Choose an amount of numbers from 1 - 15 => ")
    if digits.isnumeric():
        if int(digits) < 16:
            correctAnswer = False
    system('clear')
    print("That is not a valid number.")
system('clear')
digits = int(digits)
num1 = '1'
num2 = '9'
for i in range(digits - 1):
    num1 += '0'
    num2 += '9'
num1 = int(num1)
num2 = int(num2)
number = randrange(num1, num2 + 1)
num = True
guesses = 0
while num:
    print("Guesses:", guesses)
    action = input("a) More Than\nb) Less Than\nc) ? Digit\ng) Guess\n\n=> ")
    match action:
        case "a":
            x = int(input("Greater than what? => "))
            if x > number:
                system('clear')
                print(x, "is greater than the number.")
            else:
                system('clear')
                print(x, "is not greater than the number.")
        case "b":
            x = int(input("Less than what? => "))
            if x < number:
                system('clear')
                print(x, "is less than the number.")
            else:
                system('clear')
                print(x, "is not less than the number.")
        case "c":
            x = int(input("Which digit? => "))
            system('clear')
            if x <= len(str(number)):
                print("Digit", x, "is", str(number)[x - 1] + ".")
            else:
                print("That is not a valid place value.")
                guesses -= 1
        case "g":
            x = int(input("Equal to what? => "))
            if x == number:
                system('clear')
                print(x, "is the number.")
                print("You took", guesses + 1, "guesses.")
                num = False
            else:
                system('clear')
                print(x, "is not the number.")
    guesses += 1
