import pygame

class Levels():
    def __init__(self) -> None:
        self.area = []
        self.image = pygame.image.load("images/_Land1.svg")
        rect = pygame.image.load("images/_HitLand1.svg").get_rect()
        x = [(600, 500), (0, 600), (20, 300), (300, 400)]
        for i in x:
            rect.x = i[0]
            rect.y = i[1]
            self.area.append(rect.copy())
    def blitme(self, screen) -> None:
        for i in self.area:
            screen.blit(self.image, (i.x, i.y))