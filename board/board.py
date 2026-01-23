import pygame
from sprites import Spritesheet
from boards import BOARDS
from random import randrange
from text import Text
from collections import defaultdict
CELL_SIZE = 64
SPRITESHEET_ROW_SIZE = 8
SCREEN_W = 768
SCREEN_H = 640
def ease_in_out(t: float) -> float:
    # Smoothstep (ease-in-ease-out)
    return t * t * (3 - 2 * t)
def make_glow(surface:pygame.surface.SurfaceType, color:tuple[int], radius=8, strength=80):
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
def update_player_map():
    player_by_loc = defaultdict(list)
    for p in (player1, player2, player3, player4):
        player_by_loc[p["loc"]].append(p)
    return player_by_loc
def draw_players(screen:pygame.surface.SurfaceType, board:list[int], player_by_loc:defaultdict):
    shadows = []
    players = []
    for i, row in enumerate(board[0]):
        for j in range(len(row)):
            players_here = player_by_loc.get(board[1][i][j], [])
            for player in players_here:
                eased = ease_in_out(player["offset"])
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
    "loc":1, "offsetdir": (0, 0), "offset": 0, "idx":1
}
player2 = {
    "image":pygame.image.load("assets/players/green.png"),
    "loc":2, "offsetdir": (0, 0), "offset": 0, "idx":2
    }
player3 = {
    "image":pygame.image.load("assets/players/purple.png"),
    "loc":3, "offsetdir": (0, 0), "offset": 0, "idx":3
    }
player4 = {
    "image":pygame.image.load("assets/players/red.png"),
    "loc":4, "offsetdir": (0, 0), "offset": 0, "idx":4
    }
diceImages = (
    pygame.image.load("assets/dice/dice1.png"),
    pygame.image.load("assets/dice/dice2.png"),
    pygame.image.load("assets/dice/dice3.png"),
    pygame.image.load("assets/dice/dice4.png"),
    pygame.image.load("assets/dice/dice5.png"),
    pygame.image.load("assets/dice/dice6.png"))
sprites = Spritesheet("assets/spaces.png")
pygame.mixer.init()
clickSound = pygame.mixer.Sound('audio/Retro2.mp3')
clickSound.set_volume(0.2)
glow = make_glow(sprites.image_at((64, 0, CELL_SIZE, CELL_SIZE)), (0, 0, 0))
glow.set_alpha(40)
playerShadowImage = pygame.image.load("assets/players/shadow.png")
#backgroundImage = pygame.image.load("assets/sky.png")
shadowImage = pygame.image.load("assets/shadow.png")
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
text = Text(screen)
pygame.display.set_caption("Board Game")
sprites = Spritesheet("assets/spaces.png")
noise = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
for _ in range(2000):
    x = randrange(0, SCREEN_W)
    y = randrange(0, SCREEN_H)
    noise.set_at((x, y), (255, 255, 255, 30))
turn = 0
rolled = False
time = 0
board_surface = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
draw_board(board_surface, BOARDS[1])
running = True
clock = pygame.time.Clock()
turn = 1
rolling = True
wait = 0
added = 0
rolls = 0
done = False
roll_timer = 0
dice_roll = 1
dt = 0
fps_timer = 0
fps_write = False

chosen = False
animations = [0, 0, 0, 0, 0, 0]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if rolling and not rolled and not chosen:
                    chosen = True
                    added = 0
                    path = {}
                    for r, i in enumerate(BOARDS[1][1]):
                        for c, tile in enumerate(i):
                            if tile != -1:
                                path[tile] = (r, c)
            elif event.key == pygame.K_c:
                if done:
                    done = False
                    rolled = False
                    rolling = True
                    turn = max((turn + 1) % 5, 1)
    screen.fill((32, 58, 42))
    screen.blit(noise, (0, 0))
    screen.blit(board_surface, (0, 0))
    player_map = update_player_map()
    draw_players(screen, BOARDS[1], player_map)
    if rolling:
        if not rolled and not chosen:
            roll_timer += dt
            if roll_timer >= 0.05:
                dice_roll = randrange(1, 7)
                roll_timer = 0
                pygame.mixer.Channel(1).play(clickSound)

            text.write("Press R to stop rolling.", SCREEN_W / 2 - 174, SCREEN_H / 2 + 46)
        elif not rolled and chosen:
            roll_timer += dt
            if roll_timer >= 0.1 * max(rolls / 2, 1):
                dice_roll = randrange(1, 7)
                roll_timer = 0
                rolls += 1
                pygame.mixer.Channel(1).play(clickSound)
            if rolls >= 10:
                rolled = True
                rolls = 0
                chosen = False
                wait = 33 + time
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
                player_by_loc = update_player_map()
                '''cell = None
                for idx, i in enumerate(BOARDS[1][1]):
                    for idx2, j in enumerate(i):
                        for i in player_by_loc.get(BOARDS[1][1][i][j], []):
                            if i["idx"] == turn:
                                cell = j
                                break
                        if cell != None: break
                    if cell != None: break
                if cell == 0:
                    animations[0] = {1:0.0}
                elif cell == 2:
                    animations[1] = {-1:0.0}'''
                rolling = False
                done = True
                time = 0
    if done:
        text.write("Press C to end turn ", SCREEN_W / 2 - 174, SCREEN_H / 2 + 46)

    text.write(f"Roll for Player {turn}: ", SCREEN_W / 2 - 146, SCREEN_H / 2 - 17)
    screen.blit(diceImages[dice_roll - 1], (SCREEN_W / 2 + 146, SCREEN_H / 2 - 32))
    time += 1 + dt
    fps_timer += dt
    if fps_timer >= 5:
        fps = clock.get_fps()
        fps_timer = 0
        #print(fps)
        if 0 < fps < 30:
            fps_write = True
        else:
            fps_write = False
    if fps_write:
        text.write(f"LOW FPS: {round(fps)} ", 5, SCREEN_H - 32)
    pygame.display.flip()
    dt = clock.tick(60) / 1000
pygame.quit()