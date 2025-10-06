import pygame
def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
screen = pygame.display.set_mode((485, 360))
pygame.display.set_caption("idk bro")
bg = pygame.image.load('bg.svg')
player_img = pygame.transform.smoothscale(pygame.image.load('player.svg'), (31, 24))
level = pygame.image.load('map.svg')
pygame.init()
tick30 = 0
delta = 1
res = 4
fov = 60
py, px = 0, 0
while True:
    screen.blit(bg, (0, 0))
    screen.blit(level, (0, 0))
    screen.blit(player_img, (px, py))
    pygame.display.flip()