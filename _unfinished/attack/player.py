import pygame
from random import randrange
class Player():
    def __init__(self, screen):
        self.screen = screen
        self.x_move = 0
        self.y_move = 0
        self.iframes = 0
        self.image = pygame.image.load('images/bishop.png').convert_alpha()
        self.explosion = pygame.image.load('images/explosion.svg').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.hp = 5
        self.xp = 0
        self.lv = 1
        self.speed = 1.7
    def explode(self):
        self.explosion = pygame.transform.rotate(self.explosion, randrange(-360, 360))
        self.explosion_rect = self.explosion.get_rect()
        self.explosion_rect.center = self.rect.center
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sound/Explosion18.wav'))
        self.screen.blit(self.explosion, self.explosion_rect) #self.explosion)
    def frame(self, enemy):
        """ Move Player """
        self.iframes -= 1
        self.rect.x += self.x_move
        self.rect.y += self.y_move
        # Keep player in the screen boundaries
        if self.rect.x <= 0:
            self.rect.x = 1
        if self.rect.y <= 0:
            self.rect.y = 1
        if self.rect.x >= 950:
            self.rect.x = 949
        if self.rect.y >= 750:
            self.rect.y = 749
        # Damage player
        idx = 0
        for i in enemy.location:
            if self.rect.colliderect(i):
                if not self.iframes > 0:
                    self.hp -= 1
                    self.iframes = 50
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound('sound/Explosion18.wav'))
            idx += 1
    def blitme(self):
        """ Draw player """
        self.screen.blit(self.image, (round(self.rect.x), round(self.rect.y)))