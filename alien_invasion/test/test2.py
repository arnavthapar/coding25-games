import pygame
from player import Player
from functions import Functions as functions
from platforms import Platforms
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Platformer")
center = []
center.append(screen.get_rect().centerx)
center.append(screen.get_rect().centery)
grid = {"1f":618, 1:[[')row', 736, "Tile_15"], [')row', 672, "Tile_02"]]}
# Y levels for the grid are 736, 672, 608
# One block is 32 x 32. Half a block is 16.
platforms = Platforms(grid, 19)
walk = level = 1
player = Player(center, grid)

while True: # Game loop.
    player = functions.check_events(player)
    player.update_player(level)
    screen.fill((176, 224, 230))
    screen = player.blitme(screen)
    screen = platforms.load(screen, level)
    pygame.display.flip()