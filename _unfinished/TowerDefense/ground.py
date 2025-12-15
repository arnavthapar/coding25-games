import pygame

class Ground():
    def load(self, path:str) -> pygame.surface.Surface:
        return pygame.image.load(f'images/{path}.png')
    def __init__(self, grid:list) -> None:
        self.grid = grid
        self.path1 = self.load('path1')
        self.path2 = self.load('path2')
        self.path3 = self.load('path3')
        self.back = self.load('back')
        self.sidebarImages = (self.load("entersidebar"), self.load("exitsidebar"), self.load("sidebar"), self.load("insidebar"), self.load("sideback"))
        self.buttonImages = (self.load("nextwave"),)
        self.turretImages = (self.load("towers/turret"),)
    def draw(self, screen:pygame.surface.Surface, area:list, towers:dict[tuple[int, int]:tuple[int, classmethod]], setup:int=0):
        location = [0, 0]
        array_y = 0
        array_x = 0
        for x in range(self.grid[1]):
            for y in range(self.grid[0]):
                if y == 15 and setup == 1:
                    screen.blit(self.sidebarImages[2], location)
                elif y in (16, 17, 18) and setup == 1:
                    match (x, y):
                        case (1, 16):
                            screen.blit(self.sidebarImages[4], location)
                            screen.blit(self.turretImages[0], location)
                        case (10, 16):
                            screen.blit(self.buttonImages[0], location)
                        case (10, 17):
                            pass
                        case _:
                            screen.blit(self.sidebarImages[3], location)
                else:
                    match area[array_y][array_x]:
                        case 0: screen.blit(self.back, location)
                        case 1: screen.blit(self.path1, location)
                        case 2: screen.blit(self.path2, location)
                        case 3: screen.blit(self.path3, location)
                        case 4: screen.blit(pygame.transform.rotate(self.path3, 90), location)
                        case 5: screen.blit(pygame.transform.rotate(self.path3, 180), location)
                        case 6: screen.blit(pygame.transform.rotate(self.path3, 270), location)
                    if ((x, y) == (1, 14)) and setup == 1:
                        screen.blit(self.sidebarImages[1], location)
                    if ((x, y) == (1, 18)) and setup == 2:
                        screen.blit(self.sidebarImages[1], location)
                if (x, y) in towers:
                    screen.blit(self.turretImages[towers[(x, y)][0]], location)
                location[0] += 64
                array_x += 1
            array_y += 1
            array_x = 0
            location[1] += 64
            location[0] = 0