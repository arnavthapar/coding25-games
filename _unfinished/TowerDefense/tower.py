import pygame
from ground import Ground
from enemy import Enemy
from levels import levels
from projectile import Bullets
def check_events(setup:int):
    """Respond to keypresses."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if setup == 1:
                rect64x64.center = (940, 96)
                if rect64x64.collidepoint(event.pos):
                    setup = 2
                    continue
                rect128x64.topleft = (1024, 640)
                if rect128x64.collidepoint(event.pos):
                    setup = 0
                    continue
            if setup == 2:
                rect64x64.center = (1184, 96)
                if rect64x64.collidepoint(event.pos):
                    setup = 1
    return setup
pygame.init()
screen = pygame.display.set_mode((1216, 768))
pygame.display.set_caption("Tower Defense")
ground = Ground((19, 12))
area = levels[1][0]
rect64x64 = pygame.image.load("images/back.png").get_rect()
rect128x64 = pygame.image.load("images/nextwave.png").get_rect()
enemies = Enemy(levels[1][1], [[5, 0], [5, 1]], pygame.image.load("images/enemy.png").get_rect())
clock = pygame.time.Clock()
towers = {(2, 4):(0, Bullets())}
setup = 1
while 1:
    while setup in (1, 2):
        setup = check_events(setup)
        screen.fill((5, 255, 68))
        ground.draw(screen, area, towers, setup)
        pygame.display.flip()
        clock.tick(60)
    while setup == 0:
        setup = check_events(setup)
        screen.fill((5, 255, 68))
        enemies.move()
        ground.draw(screen, area, towers)
        for i in tuple(towers.items()):
            i[1][1].shoot(screen, enemies.enemies, (i[0][0] * 64, i[0][1] * 64))
        enemies.draw(screen)
        pygame.display.flip()
        clock.tick(60)