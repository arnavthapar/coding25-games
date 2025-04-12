import pygame

class Background():
    def __init__(self):
        self.grass_image = pygame.image.load("images/Grass.png")
        self.room_image = pygame.image.load("images/Room.png")
    def blitme(self, level, area, screen):
        if area[level][0]: screen.blit(self.grass_image, (0, 0))
        if not area[level][0]: screen.blit(self.room_image, (0, 0))