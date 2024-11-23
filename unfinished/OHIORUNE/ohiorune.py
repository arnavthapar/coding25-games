import pygame
from background import Background
from player import Player
from area import Area
def check_events(player):
    """Respond to keypresses."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.player_right = True
                player.direction = 90
                if player.player_left and player.player_right:
                    player.player_left = False
            elif event.key == pygame.K_LEFT:
                player.player_left = True
                player.direction = -90
                if player.player_left and player.player_right:
                        player.player_right = False
            elif event.key == pygame.K_UP:
                player.player_up = True
                player.direction = 0
                if player.player_up and player.player_down:
                        player.player_down = False
            elif event.key == pygame.K_DOWN:
                player.player_down = True
                player.direction = 180
                if player.player_up and player.player_down:
                        player.player_up = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT: player.player_right = False
            elif event.key == pygame.K_LEFT: player.player_left = False
            elif event.key == pygame.K_UP: player.player_up = False
            elif event.key == pygame.K_DOWN: player.player_down = False
    return player

pygame.init()
screen = pygame.display.set_mode((556, 448))
pygame.display.set_caption("QEYDWIUYHI")
player = Player()
area = Area()
level = 0
background = Background()
area.blit_area2(level)
area.blit_area3(level)
area.blit_area1(level)
while True:
    player = check_events(player)
    screen.fill([255, 255, 255])
    background.blitme(level, area.areas, screen)
    area.load1(screen)
    player.update_player(area)
    player.blit(screen)
    area.load2(screen)
    pygame.display.flip()