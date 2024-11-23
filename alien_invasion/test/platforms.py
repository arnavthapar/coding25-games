import pygame

class Platforms():
    def __init__(self, platform, grid):
        self.grid = grid
        self.platform_list = platform
        self.basic = pygame.image.load('images/platforms/Tile_02.png')
        self.rect = self.basic.get_rect()
    def generate_platform_constants(self, platform, screen, loc, extra):
        if platform == ")row":
            x_location = 0
            for i in range(self.grid):
                screen.blit(pygame.image.load('images/platforms/'+extra+'.png'), (x_location, loc))
                x_location += 64
        return screen
    def load(self, screen, level):
        for i in self.platform_list[level]:
            if ")" in i[0]: screen = self.generate_platform_constants(i[0], screen, i[1], i[2])
            else: screen.blit(pygame.image.load('images/platforms/'+i[0]), i[1:3])
        return screen