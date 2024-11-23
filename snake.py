from os import system
from time import sleep
from keyboard import on_press, KEY_DOWN
from random import randrange
def key(event) -> None:
    if event.event_type == KEY_DOWN:
        global direction
        key = event.name
        if key == "left": direction = 1
        elif key == "right": direction = 2
        elif key == "up": direction = 3
        elif key == "down": direction = 4
def move(grid, body, length, alive, win):
    grid[body[0][0]][body[0][1]] = '#'
    body.pop(0)
    try:
        if direction == 1:
            body.append([body[-1][0], body[-1][1] - 1])
        elif direction == 2:
            body.append([body[-1][0], body[-1][1] + 1])
        elif direction == 3:
            body.append([body[-1][0] - 1, body[-1][1]])
        elif direction == 4:
            body.append([body[-1][0] + 1, body[-1][1]])
        prev = grid[body[-1][0]][body[-1][1]]
        if prev == "@":
            length += 1
            body.insert(0, body[0])
            if len(body) == 77:
                alive = False
                win = True
            else: grid = place(grid, body)
        if "▣" in prev: alive = False
    except: alive = False
    return body, grid, length, alive, win
def place(grid, body) -> list:
    placing = True
    while placing:
        place = [0, 0]
        place[0] = randrange(0, 7)
        place[1] = randrange(0, 11)
        no = False
        for i in body:
            if i == place: no = True
        if not no:
            grid[place[0]][place[1]] = "@"
            placing = False
    return grid
speed = 4

length = 3
direction = 2
body = [[5, 0], [5, 1], [5, 2]]
alive = True
grid = [['#','#','#','#','#','#','#','#','#','#','#'],['#','#','#','#','#','#','#','#','#','#','#'],['#','#','#','#','#','#','#','#','#','#','#'],['#','#','#','#','#','#','#','#','#','#','#'],['#','#','#','#','#','#','#','#','#','#','#'],['#','#','#','#','#','#','#','#','#','#','#'],['#','#','#','#','#','#','#','#','#','#','#']]
grid = place(grid, body)
system('clear')
on_press(key)
win = False
while alive:
    body, grid, length, alive, win = move(grid, body, length, alive, win)
    if not alive: break
    area = ""
    for i in body: grid[i[0]][i[1]] = "\033[34m▣\033[0m"
    for i in grid:
        for m in i:
            if m == "@": m = "\033[31m@\033[0m"
            area += m + " "
        area += "\n"
    system('clear')
    print(area)
    sleep(1 - speed/5)
if win:print("You won!")
else:print("You lost.")