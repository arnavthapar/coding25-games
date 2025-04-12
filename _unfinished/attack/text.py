import pygame.font
class Text():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 48)
    def write(self, message:str="No Message Given", x:int=0, y:int=0, color:tuple=(255, 255, 255)):
        """ Write text """
        image = self.font.render(message, True, color)
        self.screen.blit(image, (x, y))