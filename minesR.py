import random
def checkSurroundings(array, x, y): # Determine how many mines are around a given square
		answer = 0
		if x > 0 and array[x - 1][y] == "m":
				answer += 1
		if x < 8 and array[x + 1][y] == "m":
				answer += 1
		if y > 0 and array[x][y - 1] == "m":
				answer += 1
		if y < 8 and array[x][y + 1] == "m":
				answer += 1
		if x > 0 and y > 0 and array[x - 1][y - 1] == "m":
				answer += 1
		if x < 8 and y < 8 and array[x + 1][y + 1] == "m":
				answer += 1
		if x < 8 and y > 0 and array[x + 1][y - 1] == "m":
				answer += 1
		if x > 0 and y < 8 and array[x - 1][y + 1] == "m":
				answer += 1
		return answer

def output(array): # Outputs board
		print("  A B C D E F G H I")
		letters = ["J ", "K ", "L ", "M ", "N ",  "O ", "P ", "Q ", "R "]
		for i in range(9):
			line = letters[i]
			for j in array[i]: line += str(j) + " "
			print(line)
def revealCoords(external, internal, x, y): # Check coordinates
		if internal[x][y] == "m": # Player clicked on mine, game over
			external[x][y] = internal[x][y]
			return True
		elif internal[x][y] > 0: external[x][y] = internal[x][y] # Normal square
		else: # 0 square, requires recursion
			external[x][y] = internal[x][y]
			if x > 0 and (external[x - 1][y] == "#" or external[x - 1][y] == "f"): revealCoords(external, internal, x - 1, y)
			if x < 8 and (external[x + 1][y] == "#" or external[x + 1][y] == "f"): revealCoords(external, internal, x + 1, y)
			if y > 0 and (external[x][y - 1] == "#" or external[x][y - 1] == "f"): revealCoords(external, internal, x, y - 1)
			if y < 8 and (external[x][y + 1] == "#" or external[x][y + 1] == "f"): revealCoords(external, internal, x, y + 1)
			if (x > 0 and y > 0) and (external[x - 1][y - 1] == "#" or external[x - 1][y - 1] == "f"): revealCoords(external, internal, x - 1, y - 1)
			if (x < 8 and y < 8) and(external[x + 1][y + 1] == "#" or external[x + 1][y + 1] == "f"): revealCoords(external, internal, x + 1, y + 1)
			if (x < 8 and y > 0) and (external[x + 1][y - 1] == "#" or external[x + 1][y - 1] == "f"): revealCoords(external, internal, x + 1, y - 1)
			if (x > 0 and y < 8) and (external[x - 1][y + 1] == "#" or external[x - 1][y + 1] == "f"): revealCoords(external, internal, x - 1, y + 1)
		return False

def checkWin(external, internal): #check if won
		for i in range(9):
			for j in range(9):
				if external[i][j] == "#" or external[i][j] == "f":
					if internal[i][j] != "m": return False
		return True

# Minefield for internal reference
internal = [["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"]]
# Minefield shown to player
external = [["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"], ["#", "#", "#", "#", "#", "#", "#", "#", "#"]]

# Generate mines
counter = 10
while counter > 0:
	x = random.randint(0, 8)
	y = random.randint(0, 8)
	if internal[x][y] != "m":
		internal[x][y] = "m"
		counter -= 1

# Finish generating internal
checked = 0
for i in range(9):
	for j in range(9):
		if internal[i][j] != "m":
			checked = checkSurroundings(internal, i, j)
			internal[i][j] = checked
lose = False #game over, loss
win = False #game over, win
action = "" #cfr
coords = "" #coordinates
cx = {"j":0, "k":1, "l":2, "m":3, "n":4, "o":5, "p":6, "q":7, "r":8} #dictionary for x coordinates
cy = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8} #dictionary for y coordinates

# Game play
while not lose and not win:
	output(internal)
	print()
	action = input("Would you like to reveal a square (C), place a flag (F), or remove a flag (R)? ")
	action = action.lower()
	if action == "c": #reveal a square
		coords = input('Input coordinates with no punctuation or spaces (ex. "aj"). ')
		print()
		coords = coords.lower()
		if len(coords) > 1 and (coords[0] in cy and coords[1] in cx):
				y = cy[coords[0]]
				x = cx[coords[1]]
				if external[x][y] == "#": lose = revealCoords(external, internal, x, y) # Empty square, call function
				elif external[x][y] == "f": # Flagged square, ask for permission
					confirm = input('You have already placed a flag in that spot. Are you sure you want to reveal it? Type "yes" to confirm, anything else to go back. ')
					print()
					if confirm == "yes": lose = revealCoords(external, internal, x, y)
				else: print("That square has already been revealed.\n") # This square has already been revealed
		else: print("Sorry, those coordinates don't make sense.\n")
		win = checkWin(external, internal)

	elif action == "f": #place flag
		coords = input('Input coordinates with no punctuation or spaces (ex. "aj"). ')
		print()
		coords = coords.lower()
		if len(coords) > 1:
			if coords[0] in cy and coords[1] in cx:
				y = cy[coords[0]]
				x = cx[coords[1]]
				if external[x][y] == "#": external[x][y] = "f"  # Empty square, place flag
				elif external[x][y] == "f": print("That square already has a flag on it\n") # Flagged square
				else: print("That square has already been revealed\n") # This square has already been revealed
			else: print("Sorry, those coordinates don't make sense\n")
		else: print("Sorry, those coordinates don't make sense\n")
	elif action == "r": # Remove flag
		coords = input('Input coordinates with no punctuation or spaces (ex. "aj"). \n')
		coords = coords.lower()
		if len(coords) > 1:
			if coords[0] in cy and coords[1] in cx:
				y = cy[coords[0]]
				x = cx[coords[1]]
				if external[x][y] == "f": external[x][y] = "#" # Flagged square, remove flags
				else: print("That square already doesn't have a flag\n") # This square already doesn't have a flag
			else: print("Sorry, those coordinates don't make sense\n")
		else: print("Sorry, those coordinates don't make sense\n")
	else: print("That doesn't make sense. Your options are C, F, or R")
if win: # Win
	output(internal)
	print("\nCongratulations! You won!")
else: # Lose
	output(external)
	print("\nSorry, you lost.")