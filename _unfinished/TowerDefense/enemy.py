import pygame

class Enemy():
    def __init__(self, area, e_area, len) -> None:
        self.area = area
        self.loc = [[337, 77], [337, 140]]
        self.pos = [[5, 0], [5, 0]]
        self.len = len
        self.timer = [63, 63]
        self.direction = [0, 0]
        self.enemy_area = e_area
        self.image = pygame.image.load('images/enemy.svg')
    # def generate_enemies():
    def move(self):
        for e in range(len(self.loc)):
            self.pos[e][0] = int(self.loc[e][0]/63)
            self.pos[e][1] = int(self.loc[e][1]/63)
            if self.timer[e] <= 0:
                area_pos = self.enemy_area[self.pos[e][1]][self.pos[e][0]]
                self.timer[e] = 61
                if area_pos == 1: self.loc[e][1] += 2
                elif area_pos == 2: self.loc[e][0] -= 2
                elif area_pos == 3: self.loc[e][0] += 2
                elif area_pos == 4: self.loc[e][1] -= 2
                elif area_pos == 5: self.loc.pop(e)
                self.direction[e] = area_pos
            else:
                if self.direction[e] == 1: self.loc[e][1] += 2
                elif self.direction[e] == 2: self.loc[e][0] -= 2
                elif self.direction[e] == 3: self.loc[e][0] += 2
                elif self.direction[e] == 4: self.loc[e][1] -= 2
                self.timer[e] -= 2
    def load(self, screen):
        for e in range(len(self.loc)): screen.blit(self.image, self.loc[e])
        return screen