import pygame

class Keys():
    def __init__(self):
        self.images = []
        self.images.append(pygame.transform.scale(pygame.image.load("images/keys/W.png"), (32, 32)))
        self.images.append(pygame.transform.scale(pygame.image.load("images/keys/A.png"), (32, 32)))
        self.images.append(pygame.transform.scale(pygame.image.load("images/keys/S.png"), (32, 32)))
        self.images.append(pygame.transform.scale(pygame.image.load("images/keys/D.png"), (32, 32)))
        self.images.append(pygame.transform.scale(pygame.image.load("images/keys/ARROWUP.png"), (32, 32)))
        self.images.append(pygame.transform.scale(pygame.image.load("images/keys/ARROWLEFT.png"), (32, 32)))
        self.images.append(pygame.transform.scale(pygame.image.load("images/keys/ARROWRIGHT.png"), (32, 32)))
        self.images.append(pygame.transform.scale(pygame.image.load("images/keys/ARROWDOWN.png"), (32, 32)))
    def blitme(self, screen, player, opponent):
        if not player.moved:
            x = player.rect.x
            y = player.rect.y
            y -= 20
            x += 36
            screen.blit(self.images[6], (x, y))
            x -= 30
            #screen.blit(self.images[7], (x, y)) # down arrow
            x -= 30
            screen.blit(self.images[5], (x, y))
            x += 30
            #y -= 30
            screen.blit(self.images[4], (x, y))
        if not opponent.moved:
            x = opponent.rect.x
            y = opponent.rect.y
            y -= 20
            x += 36
            screen.blit(self.images[3], (x, y))
            x -= 30
            #screen.blit(self.images[2], (x, y)) # s
            x -= 30
            screen.blit(self.images[1], (x, y))
            x += 30
            #y -= 30
            screen.blit(self.images[0], (x, y))