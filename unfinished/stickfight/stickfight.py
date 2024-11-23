import pygame
from player import Player
from levels import Levels
from opponent import Opponent
from keys import Keys

def check_events(player, opponent):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.moved = True
                player.direction = 1
            if event.key == pygame.K_LEFT:
                player.moved = True
                player.direction = -1
            if event.key == pygame.K_UP:
                player.moved = True
                if player.y_velocity == 0 or player.coyote_time < 8: player.y_velocity = -8
            if event.key == pygame.K_d:
                opponent.moved = True
                opponent.direction = 1
            elif event.key == pygame.K_a:
                opponent.moved = True
                opponent.direction = -1
            if event.key == pygame.K_w:
                opponent.moved = True
                if opponent.y_velocity == 0 or opponent.coyote_time < 8: opponent.y_velocity = -8
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                #if (event.key == pygame.K_RIGHT and not event.key == pygame.K_LEFT
                    #or not event.key == pygame.K_RIGHT and event.key == pygame.K_LEFT):
                    player.direction = 0
            if event.key == pygame.K_UP:
                    if player.y_velocity < -1: player.y_velocity = -1
            if event.key == pygame.K_d or event.key == pygame.K_a: opponent.direction = 0
            if event.key == pygame.K_w:
                    if opponent.y_velocity < -1: opponent.y_velocity = -1
    return player, opponent
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("QEYDWIUYHI")
player = Player()
levels = Levels()
opponent = Opponent()
# TODO https://itch.io/profile/shikashipx OTHER
# TODO https://greenpixels.itch.io KEYS CREATOR
# TODO link to the creator of the images of the keyboard keys.
# TODO and https://nathangibson.myportfolio.com nathan gibson for sound
# TODO if used, put link to shikashipx for the rpg images.
# TODO put link and name in credits.
keys = Keys()
while True:
    player, opponent = check_events(player, opponent)
    screen.fill([0, 150, 255])
    player.blitme(screen, levels.area)
    opponent.blitme(screen, levels.area)
    levels.blitme(screen)
    keys.blitme(screen, player, opponent)
    pygame.display.flip()