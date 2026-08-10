import pygame
from sprites import Spritesheet
from boards import BOARDS
from random import randrange, random, choice
from text import Text
from collections import defaultdict
import math
from ui import PlayerUI
CELL_SIZE = 64
SPRITESHEET_ROW_SIZE = 8
SCREEN_W = 768
SCREEN_H = 640
def easeInOut(t: float) -> float:
    return t * t * (3 - 2 * t)
def easeOut(t:float) -> float:
    return 1 - (1 - t) ** 3
def makeGlow(surface:pygame.surface.SurfaceType, color:tuple[int], radius=8, strength=80):
    glow = pygame.Surface(
        (surface.get_width() + radius*2, surface.get_height() + radius*2),
        pygame.SRCALPHA
    )

    # Tint copy
    tinted = surface.copy()
    tinted.fill(color)

    for i in range(radius, 0, -2):
        alpha = strength * (i / radius)
        tinted.set_alpha(int(alpha))
        glow.blit(
            pygame.transform.smoothscale(
                tinted,
                (surface.get_width() + i,
                surface.get_height() + i)
            ),
            (radius - i//2, radius - i//2)
        )

    return glow
def draw_board(screen:pygame.surface.SurfaceType, board:list[int]):
    #for i, row in enumerate(board):
    #    for j, _ in enumerate(row):
    #        screen.blit(backgroundImage, (j*CELL_SIZE, i*CELL_SIZE))
    for i, row in enumerate(board[0]):
        for j, cell in enumerate(row):
            if cell != -1:
                if cell == 1:
                    screen.blit(
                        glow, (j*CELL_SIZE - 8, i*CELL_SIZE - 8))
                screen.blit(shadowImage, (j*CELL_SIZE, (i+1)*CELL_SIZE))
                x = (cell % SPRITESHEET_ROW_SIZE) * CELL_SIZE
                y = (cell // SPRITESHEET_ROW_SIZE) * CELL_SIZE
                screen.blit(sprites.image_at((x, y, CELL_SIZE, CELL_SIZE)), (j*CELL_SIZE, i*CELL_SIZE))
def updatePlayerMap():
    player_by_loc = defaultdict(list)
    for p in (player1, player2, player3, player4):
        player_by_loc[p["loc"]].append(p)
    return player_by_loc
def lerp(a, b, t):
    return a + (b - a) * t
def drawPlayers(screen:pygame.surface.SurfaceType, board:list[int], player_by_loc:defaultdict):
    shadows = []
    players = []
    for i, row in enumerate(board[0]):
        for j in range(len(row)):
            players_here = player_by_loc.get(board[1][i][j], [])
            for player in players_here:
                eased = easeInOut(player["offset"])
                offset = eased * CELL_SIZE
                player_loc = (j*CELL_SIZE+(player["offsetdir"][1]*offset), i*CELL_SIZE+(player["offsetdir"][0]*offset))
                shadows.append((player_loc[0], player_loc[1] + 16))
                players.append((player["image"], player_loc))
    for shadow in shadows:
        screen.blit(playerShadowImage, shadow)
    for player in players:
        screen.blit(*player)

player1 = {
    "image":pygame.image.load("assets/players/blue.png"),
    "loc":1, "offsetdir": (0, 0), "offset": 0, "idx":1, "coins":0
}
player2 = {
    "image":pygame.image.load("assets/players/green.png"),
    "loc":2, "offsetdir": (0, 0), "offset": 0, "idx":2, "coins":0
    }
player3 = {
    "image":pygame.image.load("assets/players/purple.png"),
    "loc":3, "offsetdir": (0, 0), "offset": 0, "idx":3, "coins":0
    }
player4 = {
    "image":pygame.image.load("assets/players/red.png"),
    "loc":4, "offsetdir": (0, 0), "offset": 0, "idx":4, "coins":0
    }

pygame.mixer.init()
clickSound = pygame.mixer.Sound('audio/Retro2.mp3')
coinSound = pygame.mixer.Sound('audio/coin.mp3')
coinSoundGain = pygame.mixer.Sound('audio/gainCoins.mp3')
clickSound.set_volume(0.5)

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), vsync=1)
pygame.display.set_caption("Board Game")

# Set noise
noise = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
for _ in range(2000):
    x = randrange(0, SCREEN_W)
    y = randrange(0, SCREEN_H)
    noise.set_at((x, y), (255, 255, 255, 30))


playerShadowImage = pygame.image.load("assets/players/shadow.png")
#backgroundImage = pygame.image.load("assets/sky.png")
shadowImage = pygame.image.load("assets/shadow.png")
coinImage = pygame.image.load("assets/coin.png")
sprites = Spritesheet("assets/spaces.png")
diceImages = (
    pygame.image.load("assets/dice/dice1.png"),
    pygame.image.load("assets/dice/dice2.png"),
    pygame.image.load("assets/dice/dice3.png"),
    pygame.image.load("assets/dice/dice4.png"),
    pygame.image.load("assets/dice/dice5.png"),
    pygame.image.load("assets/dice/dice6.png"))
sprites = Spritesheet("assets/spaces.png")
glow = makeGlow(sprites.image_at((64, 0, CELL_SIZE, CELL_SIZE)), (0, 0, 0))
glow.set_alpha(40)
board_surface = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
draw_board(board_surface, BOARDS[1])

clock = pygame.time.Clock()
running = True

text = Text(screen)

turn = 1

# Dice Rolling
roll_timer = 0.0
roll_progress = 0.0
total_roll_time = 4
dice_roll = 1
wait = 0
added = 0
rolling = True
rolled = False
done = False
roll_text_offset = 0.0
rolling_offset_going = 0
roll_prg_offset = 0.0
chosen = False

# Spaces
coinsGained = False
flash = pygame.Surface((SCREEN_W, SCREEN_H))
flash.set_alpha(80)
flash.fill((255, 240, 200))

# FPS
dt = 0
time = 0
fps_timer = 0
fps_write = False
writing = ""
animations = [
    [0, 0.0, []],   # 0 gain coins
    [0, 0.0, 0.0],  # 1 text animation
    [0, 0.0, []],   # 2 lose coins
]
# Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if rolling and not rolled and not chosen and rolling_offset_going == 0:
                    chosen = True
                    roll_progress = 0
                    roll_timer = 0

                    prev_roll = None

                    added = 0
                    final_roll = 2 #randrange(1, 7)
                    path = {}
                    for r, i in enumerate(BOARDS[1][1]):
                        for c, tile in enumerate(i):
                            if tile != -1:
                                path[tile] = (r, c)
            elif event.key == pygame.K_c:
                if done:
                    done = False
                    rolled = False
                    writing = ""
                    rolling = True
                    coinsGained = False
                    turn = max((turn + 1) % 5, 1)
                    rolling_offset_going = -1
    screen.fill((32, 58, 42))
    screen.blit(noise, (0, 0))
    screen.blit(board_surface, (0, 0))
    player_map = updatePlayerMap()
    drawPlayers(screen, BOARDS[1], player_map)
    if rolling:
        if not rolled and not chosen:
            roll_timer += dt
            if roll_timer >= 0.05:
                dice_roll = randrange(1, 7)
                roll_timer = 0
                pygame.mixer.Channel(1).play(clickSound)

            text.write("Press R to stop rolling.", SCREEN_W / 2 - 174, SCREEN_H / 2 + 46)
        elif not rolled and chosen:
            roll_progress += dt / total_roll_time

            stickiness = easeInOut(roll_progress)
            if roll_progress > 1:
                delay = 0.8
            else:
                delay = lerp(0.05, 0.5, easeOut(roll_progress))
            roll_timer += dt

            if roll_timer >= delay:
                roll_timer = 0
                if 0.8 > roll_progress or (1 > roll_progress > 0.85):
                    if random() < stickiness:
                        if random() < 0.2:
                            dice_roll = max(1, min(6, final_roll + choice((-1, 1))))
                        else:
                            dice_roll = final_roll
                    else:
                        dice_roll = randrange(1, 7)
                    if dice_roll == prev_roll:
                        dice_roll = max(1, min(6, dice_roll + choice((-1, 1))))
                    prev_roll = dice_roll

                    pygame.mixer.Channel(1).play(clickSound)
            if roll_progress >= 1.4:
                dice_roll = final_roll
                pygame.mixer.Channel(1).play(clickSound)
                rolled = True
                roll_progress = 0
                chosen = False
                wait = 33 + time
                rolling_offset_going = 1

        else:
            if time >= wait:
                wait += 33
                match turn:
                    case 1:
                        player1["loc"] += 1
                        player1["offset"] = 0
                    case 2:
                        player2["loc"] += 1
                        player2["offset"] = 0
                    case 3:
                        player3["loc"] += 1
                        player3["offset"] = 0
                    case 4:
                        player4["loc"] += 1
                        player4["offset"] = 0
                added += 1
            else:
                match turn:
                    case 1:
                        if player1["loc"] < len(path):
                            (x1, y1), (x2, y2) = path[player1["loc"]], path[player1["loc"] + 1]
                            player1["offsetdir"] = (x2 - x1, y2 - y1)
                            player1["offset"] += 1 / 32
                            player1["offset"] = min(player1["offset"], 1.0)
                    case 2:
                        if player2["loc"] < len(path):
                            (x1, y1), (x2, y2) = path[player2["loc"]], path[player2["loc"] + 1]
                            player2["offsetdir"] = (x2 - x1, y2 - y1)
                            player2["offset"] += 1 / 32
                            player2["offset"] = min(player2["offset"], 1.0)
                    case 3:
                        if player3["loc"] < len(path):
                            (x1, y1), (x2, y2) = path[player3["loc"]], path[player3["loc"] + 1]
                            player3["offsetdir"] = (x2 - x1, y2 - y1)
                            player3["offset"] += 1 / 32
                            player3["offset"] = min(player3["offset"], 1.0)
                    case 4:
                        if player4["loc"] < len(path):
                            (x1, y1), (x2, y2) = path[player4["loc"]], path[player4["loc"] + 1]
                            player4["offsetdir"] = (x2 - x1, y2 - y1)
                            player4["offset"] += 1 / 33
                            player4["offset"] = min(player4["offset"], 1.0)
            if added == dice_roll:
                player_by_loc = updatePlayerMap()
                cell = None
                done = True
                for idx, i in enumerate(BOARDS[1][0]):
                    for idx2, j in enumerate(i):
                        for i in player_by_loc.get(BOARDS[1][1][idx][idx2], []):
                            if i["idx"] == turn:
                                cell = j
                                break
                        if cell != None: break
                    if cell != None: break
                if cell == 2:
                    coinSoundGain.play()
                    animations[0] = [1, 0.0, []]
                    done = False
                elif cell == 0:
                    coinSound.play()
                    animations[2] = [1, 0.0, []]
                    done = False
                rolling = False
                time = 0
    if done:
        text.write("Press C to end turn ", SCREEN_W / 2 - 174, SCREEN_H / 2 + 46)
    # Go up and down when rolled and starting roll
    if rolling_offset_going != 0:
        roll_prg_offset += dt
        roll_prg_offset = min(roll_prg_offset, 1.0)
        if rolling_offset_going == 1:
            roll_text_offset = easeOut(roll_prg_offset)
        else:
            roll_text_offset = 1 - easeOut(roll_prg_offset)
        if roll_prg_offset >= 1.0:
            rolling_offset_going = 0
            roll_prg_offset = 0
    # Animations
    for idx, i in enumerate(animations):
        if len(i) < 1:
            continue
        if i[0] == 0:
            continue
        match idx:
            case 0:
                i[1] += dt * 2
                if i[1] < 3:
                    if int(i[1] * 10) % 2 == 0:
                        for _ in range(15):
                            angle = random() * 6.28
                            speed = randrange(200, 350)
                            i[2].append([
                                randrange(0, SCREEN_W),
                                0,
                                math.cos(angle) * speed,
                                math.sin(angle) * speed
                            ])
                if i[1] > 2.2:
                    if not coinsGained:
                        if len(animations[1]) == 0:
                            animations[1] = [0, 0.0, 0]
                        if animations[1][0] == 0:
                            animations[1] = [1, 0.0, 0]
                            coinsGain = randrange(1, 11)
                            match turn:
                                case 1: player1["coins"] += coinsGain
                                case 2: player2["coins"] += coinsGain
                                case 3: player3["coins"] += coinsGain
                                case 4: player4["coins"] += coinsGain
                        animations[1][1] += dt
                        animations[1][2] = 1 - easeOut(animations[1][1])
                        if animations[1][1] > 1.0:
                            coinsGained = True
                            animations[1][0] = 0
                        writing = f"Player {turn} collected {coinsGain} coins!"
                re = []
                for idx, c in enumerate(i[2]):
                    c[3] += 900 * dt # Gravity
                    c[0] += c[2] * dt
                    c[1] += c[3] * dt
                    screen.blit(coinImage, (c[0], c[1]))
                    if c[1] > SCREEN_H: re.append(idx)
                for l in reversed(re): i[2].pop(l)
                if i[1] > 6:
                    i[0] = 0
                    i[1] = 0
                    i[2] = []
                    done = True
            case 2:
                i[1] += dt * 2
                if i[1] < 3:
                    if int(i[1] * 10) % 2 == 0:
                        for idx, row in enumerate(BOARDS[1][1]):
                            for idx2, space in enumerate(row):
                                for playerL in player_by_loc.get(BOARDS[1][1][idx][idx2], []):
                                    if playerL["idx"] == turn:
                                        loc = (idx2*64+16, idx*64+16)
                                        break
                        angle = random() * 6.28
                        speed = randrange(200, 350)
                        i[2].append([
                            *loc,
                            math.cos(angle) * speed,
                            math.sin(angle) * speed
                            ])
                if i[1] > 2.2:
                    if not coinsGained:
                        if len(animations[1]) == 0:
                            animations[1] = [0, 0.0, 0]
                        if animations[1][0] == 0:
                            animations[1] = [1, 0.0, 0]
                            coinsGain = randrange(1, 11)
                            match turn:
                                case 1: player1["coins"] -= coinsGain
                                case 2: player2["coins"] -= coinsGain
                                case 3: player3["coins"] -= coinsGain
                                case 4: player4["coins"] -= coinsGain
                        animations[1][1] += dt
                        animations[1][2] = 1 - easeOut(animations[1][1])
                        if animations[1][1] > 1.0:
                            coinsGained = True
                            animations[1][0] = 0
                        writing = f"Player {turn} lost {coinsGain} coins!"
                re = []
                for idx, c in enumerate(i[2]):
                    c[3] -= 900 * dt # Gravity
                    c[0] += c[2] * dt
                    c[1] += c[3] * dt
                    screen.blit(coinImage, (c[0], c[1]))
                    if c[1] > SCREEN_H: re.append(idx)
                for l in reversed(re): i[2].pop(l)
                if i[1] > 6:
                    i[0] = 0
                    i[1] = 0
                    i[2] = []
                    done = True
    if writing != "":
        text.write(writing, -1, SCREEN_H / 2 - 17 + 300 * animations[1][2])
    text.write(f"Roll for Player {turn}: ", SCREEN_W / 2 - 146, SCREEN_H / 2 - 17 - 280 * roll_text_offset)
    screen.blit(diceImages[dice_roll - 1], (SCREEN_W / 2 + 146, SCREEN_H / 2 - 32 - 280 * roll_text_offset))
    time += 1 + dt
    # Draw Player UI
    PlayerUI.draw((player1, player2, player3, player4), screen, text.write, coinImage)
    # FPS check
    fps_timer += dt
    if fps_timer >= 5:
        fps = clock.get_fps()
        fps_timer = 0
        if 0 < fps < 30:
            fps_write = True
        else:
            fps_write = False
    if fps_write:
        text.write(f"LOW FPS: {round(fps)} ", 5, SCREEN_H - 32)
    pygame.display.flip()
    dt = clock.tick(60) / 1000
pygame.quit()