import pygame
from ground import Ground
from enemy import Enemy
from levels import levels
def check_events():
    """Respond to keypresses."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
pygame.init
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Tower Defense")
ground = Ground((19, 12))
area = levels[1][0]
enemies = Enemy(area, levels[1][1], 19)
while True:
    check_events()
    screen.fill((5, 255, 68))
    enemies.move()
    screen = ground.load(screen, area)
    screen = enemies.load(screen)
    pygame.display.flip()