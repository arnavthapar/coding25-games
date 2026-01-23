import pygame
from ground import Ground
from enemy import Enemy
from levels import levels
from projectile import Bullets
from settings import Settings
def check_events(setup:int, selectedTower:int | None, towers:dict) -> tuple[int, int | None, dict]:
    """Respond to keypresses."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                selectedTower = None
            if event.key == pygame.K_f:
                print("FPS:", clock.get_fps())
        if event.type == pygame.MOUSEBUTTONDOWN:
            if setup in (1, 2) and selectedTower is not None:
                tx = (event.pos[1] + 32) // 64
                ty = (event.pos[0] + 32) // 64
                rect64x64.center = (1184, 96)
                if not (setup == 1 and (ty > 14)):
                    if not (setup == 2 and rect64x64.collidepoint(event.pos)):
                        rect64x64.center = (940, 96)
                        if not (setup == 1 and rect64x64.collidepoint(event.pos)):
                            if area[tx][ty] == 0:
                                if not (tx, ty) in towers:
                                    towers[(tx, ty)] = Bullets(selectedTower)
                                    selectedTower = None
            if setup == 1:
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
                    rect64x64.topleft = (1024+64*((i)%2), 64*(int(i/2)+1))
                    if rect64x64.collidepoint(event.pos):
                        selectedTower = i
                        continue
            if setup == 2:
                rect64x64.center = (1184, 96)
                if rect64x64.collidepoint(event.pos):
                    setup = 1
    return setup, selectedTower, towers
pygame.init()
screen = pygame.display.set_mode((1216, 768))
pygame.display.set_caption("Tower Defense")
ground = Ground((19, 12))
TOWER_COUNT = len(Bullets(0).towerTypesList)
settings = Settings()

#! Settings
levelCurrent = settings.startingLevel

selectedTower = None
area = levels[levelCurrent][0]
rect64x64 = pygame.Rect(0, 0, 64, 64)
rect128x64 = pygame.Rect(0, 0, 128, 64)
clock = pygame.time.Clock()
towers = {(7, 4):(Bullets(4)), (5, 13):(Bullets(4)), (11, 9):(Bullets(2))}
setup = 1
screenRect = screen.get_rect()
enemyRect = pygame.image.load("images/enemy.png").get_rect()
while 1:
    setup, selectedTower, towers = check_events(setup, selectedTower, towers)
    ground.draw(screen, area, setup)
    if setup in (1, 2):
        changeSetup = False
        #print(selectedTower, towers)
        ground.drawTowers(screen, towers, setup)
        if selectedTower is not None:
            mx, my = pygame.mouse.get_pos()
            screen.blit(ground.turretImages[selectedTower], (((mx - 32)//64)*64+64, ((my-32)//64)*64+64))

    elif setup == 0:
        if not changeSetup:
            changeSetup = True
            enemies = Enemy(levels[levelCurrent][1], [[5, 0] for _ in range(40)], enemyRect, 15)
        enemies.move(screenRect)
        for (tx, ty), tower in towers.items():
            tower.shoot(screen, enemies.enemies, (tx * 64 + 32, ty * 64 + 32), screenRect)
        ground.drawTowers(screen, towers, setup)
        enemies.draw(screen)
    pygame.display.flip()
    clock.tick(60)