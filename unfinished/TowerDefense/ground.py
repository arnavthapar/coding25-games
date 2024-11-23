import pygame

class Ground():
    def __init__(self, grid) -> None:
        self.grid = grid
        self.path1 = pygame.image.load('images/path1.svg')
        self.path2 = pygame.image.load('images/path2.svg')
        self.path3 = pygame.image.load('images/path3.svg')
    def load(self, screen, area):
        location = [0, 0]
        array_y = 0
        array_x = 0
        for i in range(self.grid[1]):
            for i in range(self.grid[0]):
                if area[array_y][array_x] == 1: screen.blit(self.path1, location)
                if area[array_y][array_x] == 2: screen.blit(self.path2, location)
                if area[array_y][array_x] == 3: screen.blit(self.path3, location)
                if area[array_y][array_x] == 4: screen.blit(pygame.transform.rotate(self.path3, 90), location)
                if area[array_y][array_x] == 5: screen.blit(pygame.transform.rotate(self.path3, 180), location)
                if area[array_y][array_x] == 6: screen.blit(pygame.transform.rotate(self.path3, 270), location)
                location[0] += 63
                array_x += 1
            array_y += 1
            array_x = 0
            location[1] += 63
            location[0] = 0
        return screen