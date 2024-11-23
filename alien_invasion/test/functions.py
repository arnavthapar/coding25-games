import pygame
from sys import exit

class Functions():
    def check_events(player):
        """Respond to keypresses."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT: exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.player_right = True
                    if player.player_left and player.player_right:
                        player.player_left = False
                elif event.key == pygame.K_LEFT:
                    player.player_left = True
                    if player.player_left and player.player_right:
                        player.player_right = False
                if event.key == pygame.K_UP:
                    if player.player_up != True and player.up_velocity == 0: player.up_velocity = 40
                    player.player_up = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT: player.player_right = False
                elif event.key == pygame.K_LEFT: player.player_left = False
                if event.key == pygame.K_UP:
                    if player.up_velocity > 10: player.up_velocity = 10
        return player