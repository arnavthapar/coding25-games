import pygame
pygame.init() # Initialize Pygame
def events(selected, movements): # Check keyboard events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            selected, movements = check_clicks(movements, mouse_x, mouse_y)
    return selected, movements
def check_clicks(movements, x, y): # Check if the clicked square is a square with a piece.
    selected = -1
    list_x = 0
    list_y = 0
    for i in collisions:
        for m in i:
            if m.collidepoint(x, y):
                if selected != -1 and movable[list_x][list_y]:
                    board[list_x][list_y] = selected
                selected = board[list_x][list_y]
                movements = check_movements(selected, list_x, list_y)
                break
            list_x += 1
        list_y += 1
        list_x = 0
    return selected, movements
def load_other(screen):
    screen.blit(white_background, (0, 490))
    screen.blit(selected_text, (10, 500))
    if selected_piece != -1: screen.blit(pieces[selected_piece], (100, 560))
def load_pieces(screen) -> None: # Load the pieces.
    x = 10
    y = 10
    x2 = 0
    y2 = 0
    for i in board:
        for m in i:
            if m != -1: # Check if the square is not empty
                if movable[x2][y2]:
                    screen.blit(pieces[0], (x, y))
                else:
                    screen.blit(pieces[m], (x, y))
            x += 62
            x2 += 1
        x = 10
        x2 = 0
        y2 += 1
        y += 62
def check_movements(piece, position_y, position_x) -> list:
    movable = [[], [], [], [], [], [], [], []]
    for i in range(8):
        movable[0].append(False)
        movable[1].append(False)
        movable[2].append(False)
        movable[3].append(False)
        movable[4].append(False)
        movable[5].append(False)
        movable[6].append(False)
        movable[7].append(False)
    match piece:
        case -1:
            pass
        case 0: # Queen W
            pass
        case 1: # King W
            pass
        case 2: # Knight W
            pass
        case 3: # Pawn W
            if board[position_x][position_y + 1] == -1:
                movable[position_x + 1][position_y] = True
            if board[position_x + 1][position_y - 1] > 5:
                movable[position_x + 1][position_y - 1] = True
            if board[position_x + 1][position_y + 1] > 5:
                movable[position_x + 1][position_y + 1] = True
            print(movable)
    return movable
background = pygame.image.load('board.png') # Background
# Load starting position
white_background = pygame.image.load('white_back.svg')
selected_text = pygame.image.load('text/SELECTED.png')
pieces = []
pieces.append(pygame.image.load('pieces/queen.png'))
pieces.append(pygame.image.load('pieces/king.png'))
pieces.append(pygame.image.load('pieces/knight.png'))
pieces.append(pygame.image.load('pieces/pawn.png'))
pieces.append(pygame.image.load('pieces/rook.png'))
pieces.append(pygame.image.load('pieces/bishop.png'))
pieces.append(pygame.image.load('pieces/queen1.png'))
pieces.append(pygame.image.load('pieces/king1.png'))
pieces.append(pygame.image.load('pieces/knight1.png'))
pieces.append(pygame.image.load('pieces/pawn1.png'))
pieces.append(pygame.image.load('pieces/rook1.png'))
pieces.append(pygame.image.load('pieces/bishop1.png'))
startup_position_white = [4, 2, 5, 1, 0, 5, 2, 4]
startup_position_black = [10, 8, 11, 6, 7, 11, 8, 10]
# 496 ÷ 8 = 62
board = [[], [], [], [], [], [], [], []]
for i in startup_position_white:
    board[0].append(i)
    board[1].append(3)
    board[2].append(-1)
    board[3].append(-1)
    board[4].append(-1)
    board[5].append(-1)
    board[6].append(9)
for i in startup_position_black:
    board[7].append(i)
# Deal with the mouse collision list.
collisions = [[],[],[],[],[],[],[],[]]
square_rect = pieces[0].get_rect()
y = 10
x = 10
for i in range(8):
    for m in range(8):
        square_rect.x = x
        square_rect.y = y
        collisions[i].append(square_rect.copy())
        y += 62
    y = 10
    x += 62
# Start screen.
screen = pygame.display.set_mode((720, 680))
pygame.mouse.set_visible(True)
pygame.display.set_caption("Chess But Weird")
selected_piece = -1
font = pygame.font.SysFont(None, 48)
movable = [[], [], [], [], [], [], [], []]
for i in range(8):
        movable[0].append(False)
        movable[1].append(False)
        movable[2].append(False)
        movable[3].append(False)
        movable[4].append(False)
        movable[5].append(False)
        movable[6].append(False)
        movable[7].append(False)
while True: # Game loop.
    selected_piece, movable = events(selected_piece, movable)
    screen.fill((70, 70, 70))
    load_other(screen)
    screen.blit(background, (0, 0))
    load_pieces(screen)
    pygame.display.flip()