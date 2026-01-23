#import pygame
class Area():
    def __init__(self, load, screen):
        self.images = ()
        self.screen = screen
        self.border = load('border')
    def draw(self, area:list, snake:list, snakeImgs:list, images:tuple, apple:dict, colorsImgs:tuple):
        locs = []
        for i in apple:
            locs.append(apple[i])
        for idxY, y in enumerate(area):
            for idxX, _ in enumerate(y):
                if (idxY, idxX) in snake:
                    self.screen.blit(images[snakeImgs[snake.index((idxY, idxX))]], ((idxX + 2) * 64, (idxY + 2) * 64))
                elif (idxY, idxX) in locs:
                    self.screen.blit(colorsImgs[ locs.index((idxY, idxX)) ], ((idxX+2) * 64, (idxY+2) * 64))
        for i in range(9):
            self.screen.blit(self.border, (64, ((i+1) * 64)))
        for i in range(12):
            self.screen.blit(self.border, (((i+2) * 64), 64))
        for i in range(9):
            self.screen.blit(self.border, (896, ((i+1) * 64)))
        for i in range(12):
            self.screen.blit(self.border, (((i+2) * 64), 576))