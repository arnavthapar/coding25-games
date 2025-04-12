import pygame
from random import randrange
from math import floor
from settings import Settings
class Enemy():
    def __init__(self, screen):
        self.screen = screen
        self.hp = []
        self.location = []
        self.image = pygame.image.load('images/enemy.svg')
        self.settings = Settings()
        self.cooldown = self.settings.enemy_cooldown
        self.enemy_c=[]
    def randomize(self, wait, endless=False, create = False, ):
        """ Create enemies """
        self.cooldown -= 1
        if self.cooldown < 1 or create:
            if (self.settings.time - wait.check() < 20) and not endless:
                self.cooldown = 10
            elif (self.settings.time - wait.check() < 40) and not endless:
                self.cooldown = 20
            else:
                self.cooldown = self.settings.enemy_cooldown - (floor(wait.check()/30))
            self.enemy_c.append([50, randrange(0, 1000), randrange(0, 800)])
    def create_enemy(self, x, y, wait):
            rect = self.image.get_rect()
            rect.x = x
            rect.y = y
            self.hp.append(self.settings.enemy_health+(floor(wait.check()/45)))
            self.location.append(rect)
    def frame(self, px:int, py:int, player, wait):
        """ Move enemies """
        destroy = []
        for i in range(len(self.enemy_c)):
            self.enemy_c[i][0] -= 1
            x = self.enemy_c[i][1]
            y = self.enemy_c[i][2]
            if self.enemy_c[i][0] in (10, 20, 30):
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('sound/Retro2.mp3'))
                self.screen.blit(self.image, (x, y))
            if self.enemy_c[i][0] < 1:
                self.create_enemy(x, y, wait)
                destroy.append(i)
        for i in destroy:
            self.enemy_c.pop(i)
        for i in range(len(self.location)):
            p = 0
            if px > self.location[i].x:
                self.location[i].x += 1.9 + (floor(wait.check()/30)/10)
                p = 1
            elif px < self.location[i].x:
                self.location[i].x -= 1.9 + (floor(wait.check()/30)/10)
                p = 2
            if py > self.location[i].y:
                self.location[i].y += 1.9 + (floor(wait.check()/30)/10)
                p = 3
            elif py < self.location[i].y:
                self.location[i].y -= 1.9 + (floor(wait.check()/30)/10)
            if self.location[i].colliderect(player):
                # Go back if hitting player
                match p:
                    case 1:
                        self.location[i].x -= 1.8
                    case 2:
                        self.location[i].x += 1.8
                    case 3:
                        self.location[i].y -= 1.8
                    case _:
                        self.location[i].y += 1.8
    def blitme(self):
        """ Draw enemies """
        for i in self.location:
            self.screen.blit(self.image, (round(i.x), round(i.y)))