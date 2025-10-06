import pygame
def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1024, 704))
pygame.display.set_caption("idk")

while True:
    check_events()
    screen.fill((255, 255, 255))
    pygame.display.flip()