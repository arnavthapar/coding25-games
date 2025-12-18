import pygame
from ground import Ground
from enemy import Enemy
from levels import levels
from projectile import Bullets
from math import floor
def check_events(setup:int, selectedTower:int, towers:dict):
    """Respond to keypresses."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if setup in (1, 2) and selectedTower is not None:
                tx = (event.pos[1] + 32) // 64
                ty = (event.pos[0] + 32) // 64
                towers[(tx, ty)] = Bullets(selectedTower)
                selectedTower = None
            elif setup == 1:
                # Check for round start and set aside setup
                rect64x64.center = (940, 96)
                if rect64x64.collidepoint(event.pos):
                    setup = 2
                    continue
                rect128x64.topleft = (1024, 640)
                if rect128x64.collidepoint(event.pos):
                    setup = 0
                    continue
                # Placing towers
                for i in range(TOWER_COUNT):
                    rect64x64.topleft = (1024+64*((i)%2), 64*(floor(i/2)+1))
                    if rect64x64.collidepoint(event.pos):
                        selectedTower = i
                        continue
            elif setup == 2:
                rect64x64.center = (1184, 96)
                if rect64x64.collidepoint(event.pos):
                    setup = 1
    return setup, selectedTower, towers
pygame.init()
screen = pygame.display.set_mode((1216, 768))
pygame.display.set_caption("Tower Defense")
ground = Ground((19, 12))

TOWER_COUNT = len(Bullets(0).towerTypesList)

levelCurrent = 1
selectedTower = None
area = levels[levelCurrent][0]
rect64x64 = pygame.image.load("images/back.png").get_rect()
rect128x64 = pygame.image.load("images/nextwave.png").get_rect()
clock = pygame.time.Clock()
towers = {(7, 4):(Bullets(0)), (5, 13):(Bullets(1)), (11, 9):(Bullets(2))}
setup = 1
screenRect = screen.get_rect()
enemyRect = pygame.image.load("images/enemy.png").get_rect()
while 1:
    setup, selectedTower, towers = check_events(setup, selectedTower, towers)
    ground.draw(screen, area, setup)
    if setup in (1, 2):
        changeSetup = False
        #print(selectedTower, towers)
        ground.drawTowers(screen, towers)
        if selectedTower is not None:
            mx, my = pygame.mouse.get_pos()
            screen.blit(ground.turretImages[selectedTower], (((mx - 32)//64)*64+32, ((my-32)//64)*64+32))

    elif setup == 0:
        if not changeSetup:
            changeSetup = True
            enemies = Enemy(levels[levelCurrent][1], [[5, 0] for _ in range(300)], enemyRect, 5)
        enemies.move(screenRect)
        for (tx, ty), tower in towers.items():
            tower.shoot(screen, enemies.enemies, (tx * 64, ty * 64), screenRect)
        ground.drawTowers(screen, towers)
        enemies.draw(screen)
    pygame.display.flip()
    clock.tick(60)
        #print(clock.get_fps())