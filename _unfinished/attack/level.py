from random import randrange
from pygame import image
class Level():
    def __init__(self, text):
        #       Level 1  2  3  4  5
        self.speed = (5, 5, 5, 5, 10)
        self.attack= (1, 1, 1, 1, 2)
        self.h_timer=(12, 10, 8, 6, 4)
        self.p_speed=(0.05, 0.05, 0.1, 0.1, 0.2)
        self.levels = [0, 0, 0, 0, 0]
        self.choices = []
        self.text = text
        self.overlay = image.load('images/overlay.svg').convert_alpha()
    def level(self, screen):
        """ Level up player """
        screen.blit(self.overlay, (0, 540))
        screen.blit(self.overlay, (716, 0))
        screen.blit(self.overlay, (716, 540))
        screen.blit(self.overlay, (0, 0))
        self.text.write("LEVEL UP: SELECT ONE", 300, 200)
        for i in ('a','b'):
            x = randrange(1, 5)
            idx = 0
            while x in self.choices:
                x = randrange(1, 5)
                if idx > 50:
                    break
                idx += 1
            loc = 400 if i == 'a' else 500
            if self.levels[x-1] != 5:
                writing = ""
                match x:
                    case 1:writing = "Upgrade attack speed to level"
                    case 2:writing = "Upgrade attack damage to level"
                    case 3:writing = "Upgrade player speed to level"
                    case 4:writing = "Upgrade homing bullet frequency to level"
                self.text.write(f"{i}) {writing} {self.levels[x-1] + 1}", 200, loc)
                self.choices.append(x)
            else:
                self.text.write(f"{i}) Gain 1 Health", 400, loc)
                self.choices.append(0)
    def answer(self, x, player, bullet):
        """ Increase stats and do other upgrades gotten from leveling up """
        i = self.choices[x]
        match i:
            case 0:player.hp += 1
            case 1:bullet.timer_reset -= self.speed[self.levels[0]]
            case 2:bullet.attack += self.attack[self.levels[1]]
            case 3:player.speed += self.attack[self.levels[2]]
            case 4:
                bullet.h_timer_reset = bullet.timer_reset * self.h_timer[self.levels[3]]
                bullet.h_timer = bullet.h_timer_reset
                bullet.timer = bullet.timer_reset
        self.levels[i-1] += 1
        bullet.level = False
        self.choices = []
        return player, bullet