import pygame
from area import Area
from upgrades import Upgrades
from random import randrange
import numpy as np
import math
from text import Text
def check_events(snakeDir:list, scroll_velocity:float, points):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP, pygame.CONTROLLER_BUTTON_DPAD_UP):
                if len(snakeDir) > 0:
                    if snakeDir[0] != 180:
                        snakeDir.append(0)
                elif prevDir != 180: snakeDir.append(0)
            if event.key in (pygame.K_s, pygame.K_DOWN, pygame.CONTROLLER_BUTTON_DPAD_DOWN):
                if len(snakeDir) > 0:
                    if snakeDir[0] != 0:
                        snakeDir.append(180)
                elif prevDir != 0: snakeDir.append(180)
            if event.key in (pygame.K_a, pygame.K_LEFT, pygame.CONTROLLER_BUTTON_DPAD_LEFT):
                if len(snakeDir) > 0:
                    if snakeDir[0] != 90:
                        snakeDir.append(270)
                elif prevDir != 90: snakeDir.append(270)
            if event.key in (pygame.K_d, pygame.K_RIGHT, pygame.CONTROLLER_BUTTON_DPAD_RIGHT):
                if len(snakeDir) > 0:
                    if snakeDir[0] != 270:
                        snakeDir.append(90)
                elif prevDir != 270: snakeDir.append(90)
            if len(snakeDir) > 5:
                    if len(snakeDir) > 1: snakeDir.pop(0)
        elif event.type in (pygame.MOUSEWHEEL, pygame.JOYBALLMOTION):
           scroll_velocity += event.y * 100
        elif event.type in (pygame.MOUSEBUTTONDOWN,):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for idx, i in enumerate(upgrades.get_rects(CAMERA_Y, SCREEN_CENTER)):
                    if i.collidepoint(mouse_x, mouse_y) and points > upgrades.points[idx]:
                        points -= upgrades.points[idx]
                        upgrades.click(idx)
    return snakeDir, scroll_velocity, points


def apply_wave_distortion(surface, time):
    original = pygame.surfarray.array3d(surface)
    distorted = np.zeros_like(original)

    for y in range(704):
        offset_x = int(20 * math.sin(y * 0.05 + time * 0.05))
        if offset_x > 0:
            distorted[offset_x:, y] = original[:-offset_x, y]
        elif offset_x < 0:
            distorted[:offset_x, y] = original[-offset_x:, y]
        else:
            distorted[:, y] = original[:, y]

    return pygame.surfarray.make_surface(distorted)

def load(name:str) -> pygame.surface.Surface:
    return pygame.image.load(f"images/{name}.png")
def loadU(name:str) -> pygame.surface.Surface:
    return pygame.image.load(f"images/upgrades/{name}.png")
snakeArea = []
for idx in range(7):
    snakeArea.append([])
    for _ in range(13):
        snakeArea[idx].append(0)
snakeLocs = [(3, 0), (3, 1), (3, 2)]
snakeImgs = [6, 7, 13]
snakeDir = [90]
# Load pygame
pygame.init()
pygame.mixer.init()
# Start up sounds and images
screen = pygame.display.set_mode((1024, 704))
text = Text(screen)
upgradesImgs = (loadU("redPlus"), loadU('moreRed'), loadU('blue'), loadU('bluePlus'))
images = {1:load("snakeM"), 2:load('snakeDL'), 3:load('snakeDR'), 4:load('snakeUL'), 5:load('snakeUR'), 6:load('snakeR'), 7:load("snakeS"), 8:load('snakeL'), 9:load('snakeU'), 10:load('snakeD'),
          11: load("snakeDE"), 12:load("snakeUE"), 13:load('snakeLE'), 14:load('snakeRE')}
colors = (load('red'), load('yellow'), load('blue'), load('green'))
transitionImgs = (load('transition'), load('black'))
appleLoc = {"r":(3, 6), "y":(999, 999), "b":(999, 999), "g":(999, 999)}
sounds = (pygame.mixer.Sound('sound/beep.mp3'), pygame.mixer.Sound('sound/slide.mp3'))
bg = pygame.transform.scale(pygame.image.load("images/swirl.jpg").convert(), (1024, 704))
area = Area(load, screen)
upgrades = Upgrades(screen, upgradesImgs)
# Set game variables
points = 0
turns = 15
# Set any other variables
pygame.display.set_caption("Snake but no")
clock = pygame.time.Clock()
time = 0
snakePDir = [90, 90, 90]
kept = True
prevDir = 90
playing = True
transition = 0
skill = False
screenRect = screen.get_rect()
SCREEN_CENTER = (screenRect.centerx, screenRect.centery)
screenRect = None
t = 0
CAMERA_Y = 0
CAMERA_Y_TARGET = 0
scroll_velocity = 0.0
while True:
    dt = clock.tick(60) / 1000
    if playing:
        screen.fill((200, 200, 200))
        previous = snakeLocs[-1]
        time += dt
        if time > 0.1:
            time = 0
            if len(snakeDir) == 0: snakeDir.append(prevDir)
            match snakeDir[0]:
                case 0:
                    prevDir = 0
                    snakeDir.pop(0)
                    snakeImgs.pop(0)
                    snakeLocs.pop(0)
                    snakePDir.pop(0)
                    snakePDir.append(0)
                    if (previous[0] - 1, previous[1]) in snakeLocs: transition += dt
                    snakeLocs.append((previous[0] - 1, previous[1]))
                    match snakeImgs[-1]:
                        case 14: # Right
                            snakeImgs[-1] = 3
                        case 13: # Left
                            snakeImgs[-1] = 2
                        case 11: # Up
                            snakeImgs[-1] = 1
                    snakeImgs.append(11)
                    turns += 1
                case 90:
                    prevDir = 90
                    snakeDir.pop(0)
                    snakeImgs.pop(0)
                    snakeLocs.pop(0)
                    snakePDir.pop(0)
                    snakePDir.append(90)
                    if (previous[0], previous[1] + 1) in snakeLocs: transition += dt
                    snakeLocs.append((previous[0], previous[1] + 1))
                    match snakeImgs[-1]:
                        case 13: # Right
                            snakeImgs[-1] = 7
                        case 12: # Down
                            snakeImgs[-1] = 3
                        case 11: # Up
                            snakeImgs[-1] = 5
                    snakeImgs.append(13)
                    turns += 1
                case 180:
                    prevDir = 180
                    snakeDir.pop(0)
                    snakeImgs.pop(0)
                    snakeLocs.pop(0)
                    snakePDir.pop(0)
                    snakePDir.append(180)
                    if (previous[0] + 1, previous[1]) in snakeLocs: transition += dt
                    snakeLocs.append((previous[0] + 1, previous[1]))
                    match snakeImgs[-1]:
                        case 14: # Right
                            snakeImgs[-1] = 5
                        case 13: # Left
                            snakeImgs[-1] = 4
                        case 12: # Down
                            snakeImgs[-1] = 1
                    snakeImgs.append(12)
                    turns += 1
                case 270:
                    prevDir = 270
                    snakeDir.pop(0)
                    snakeImgs.pop(0)
                    snakeLocs.pop(0)
                    snakePDir.pop(0)
                    snakePDir.append(270)
                    if (previous[0], previous[1] - 1) in snakeLocs: transition += dt
                    snakeLocs.append((previous[0], previous[1] - 1))
                    match snakeImgs[-1]:
                        case 12: # Down
                            snakeImgs[-1] = 2
                        case 14: # Left
                            snakeImgs[-1] = 7
                        case 11: # Up
                            snakeImgs[-1] = 4
                    snakeImgs.append(14)
                    turns += 1

        match snakeImgs[0]:
            case 1:
                if (snakeImgs[1] in (1, 2, 3)) and not ((snakeImgs[1] == 1) and (snakePDir[1] == 0)):
                    snakeImgs[0] = 10
                else:
                    snakeImgs[0] = 9
            case 2: # UL
                if snakePDir[1] == 0:
                    snakeImgs[0] = 9
                else:
                    snakeImgs[0] = 8
            case 3: # UR
                if snakePDir[1] == 0:
                    snakeImgs[0] = 9
                else:
                    snakeImgs[0] = 6
            case 4: # DL
                if snakePDir[1] == 180:
                    snakeImgs[0] = 10
                else:
                    snakeImgs[0] = 8
            case 5: # DR
                if snakePDir[1] == 180:
                    snakeImgs[0] = 10
                else:
                    snakeImgs[0] = 6
            case 7:
                if (snakeImgs[1] in (7, 3, 5)) and not ((snakeImgs[1] == 7) and (snakePDir[1] == 90)):
                    snakeImgs[0] = 8
                else:
                    snakeImgs[0] = 6
        for i in appleLoc:
            if appleLoc[i] in snakeLocs:
                snakeLocs.insert(0, snakeLocs[0])
                snakeImgs.insert(0, snakeImgs[0])
                pygame.mixer.Channel(1).play(sounds[0])
                snakePDir.insert(0, snakePDir[0])
                points += 2
                while appleLoc[i] in snakeLocs:
                    appleLoc[i] = (randrange(0, 6), randrange(0, 11))
        area.draw(snakeArea, snakeLocs, snakeImgs, images, appleLoc, colors)
        snakeDir, _, points = check_events(snakeDir, scroll_velocity, points)
        text.write(f"{points} POINTS", 800, 20)
        if len(snakeLocs) == 60:
            transition += dt
            pygame.mixer.Channel(2).play(sounds[1])
        for i in snakeLocs:
            if ((i[0] < 0) or i[0] > 6) or ((i[1] < 0) or i[1] > 11):
                transition += dt
                pygame.mixer.Channel(2).play(sounds[1])
    if transition > 0:
        check_events(snakeDir, scroll_velocity, points)
        playing = False
        transition += dt
        screen.blit(transitionImgs[0], (1024 - (transition * 1024), 0))
        screen.blit(transitionImgs[0], (2048 - (transition * 1024), 0))
        if transition > 3:
            skill = True
            transition = 0
            CAMERA_Y = 0
    elif skill:
        _, scroll_velocity, points = check_events(snakeDir, scroll_velocity, points)
        t += 1

        # Update target position with current velocity
        CAMERA_Y_TARGET += scroll_velocity * dt
        # Friction: slow the scroll_velocity over time
        scroll_velocity *= 0.9 ** (dt * 60)  # smooth exponential decay
        CAMERA_Y += (CAMERA_Y_TARGET - CAMERA_Y) * 10.0 * dt
        distorted = apply_wave_distortion(bg, t)
        CAMERA_Y_TARGET = max(min(CAMERA_Y_TARGET, 400), -100)
        screen.blit(distorted, (0, 0))
        text.write(f"{points} POINTS", 800, 20)
        upgrades.drawAll(CAMERA_Y, SCREEN_CENTER, clock.tick(60)/1000)
        #screen.blit(upgrades[0], (SCREEN_CENTER[0] - 64, SCREEN_CENTER[1] - 64 + CAMERA_Y * 2))
    pygame.display.flip()