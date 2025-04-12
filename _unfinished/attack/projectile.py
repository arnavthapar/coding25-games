import pygame
from random import randrange
from numpy import arctan2, degrees
from settings import Settings
from wait import Wait
from datetime import datetime
class Bullets():
    def __init__(self):
        self.wait = Wait()
        self.settings = Settings()
        self.color = self.settings.bullet_color
        self.h_color = self.settings.homing_bullet_color
        self.speed_factor = 1
        self.bullets = []
        self.timer_reset = self.settings.bullet_time
        self.timer = self.timer_reset
        self.h_timer_reset = self.timer_reset * 14 #! 14
        self.h_timer = self.h_timer_reset
        self.attack = 1 #! 1
        self.level = False
    def calc_nearest_enemy(self, e_rect, rect):
        """ Find nearest enemy and calculate angle to it """
        center = pygame.Vector2(rect.center)
        vector = pygame.Vector2()
        if len(e_rect) > 0:
            # Find closest enemy
            en = min([e for e in e_rect], key=lambda e: pow(e.x-rect.x, 2) + pow(e.y-rect.y, 2))
            # Find angle
            x_a = en.x - rect.x
            y_a = en.y - rect.y
            theta_r = arctan2(y_a, x_a)
            angle = degrees(theta_r)
        else:
            angle = 100 # 100 if no enemy on the screen
        vector.from_polar((1, angle))
        return center, vector
    def shoot(self, screen, e_rect:list, player, enemy, level):
        """ Fire new bullets and move other bullets """
        # Check for new bullets
        leveled = 0
        self.timer -= 1
        self.h_timer -= 1
        if self.timer < 1:
            self.timer = self.timer_reset
            if self.h_timer < 1:
                self.h_timer = self.h_timer_reset
                h = True
            else: h = False
            # Create rect for new bullet and store it
            rect = pygame.Rect(0, 0, 20, 20)
            rect.center = player.rect.center
            rect.top = player.rect.top
            #rect.centery = player.rect.centery
            center, vector = self.calc_nearest_enemy(e_rect, rect)
            self.bullets.append([rect, vector, center, h])
        for i in range(len(self.bullets)):
            if i > len(self.bullets) - 1:
                break
            # Draw bullets
            if self.bullets[i][3]:
                pygame.draw.rect(screen, self.h_color, self.bullets[i][0])
            else:
                pygame.draw.rect(screen, self.color, self.bullets[i][0])
            if self.bullets[i][3]:
                # Move homing bullets toward nearest enemy
                center, vector = self.calc_nearest_enemy(e_rect, self.bullets[i][0])
                self.bullets[i][1] = vector
                self.bullets[i][2] = center
            self.bullets[i][2] += self.bullets[i][1] * 4
            self.bullets[i][0].center = self.bullets[i][2]
            idx = 0
            for m in e_rect:
                # Check if any bullet has hit an enemy
                if self.bullets[i][0].colliderect(m):
                    self.bullets.pop(i)
                    # Reduce enemy health
                    enemy.hp[idx] -= self.attack
                    if enemy.hp[idx] < 1:
                            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sound/explosion.mp3'))
                            enemy.hp.pop(idx)
                            enemy.location.pop(idx)
                            # Level up player
                            player.xp += randrange(1, 3)
                            if player.xp > 15:
                                player.lv += 1
                                player.xp -= 15
                                leveled = datetime.now()
                                level.level(screen)
                                # Reset bullet timers
                                self.level = True
                                if self.timer < 10:
                                    self.timer = 10
                                if self.h_timer < 40:
                                    self.h_timer = 40
                    break
                else:
                    # Destroy bullets if they go off the edge of screen
                    if self.bullets[i][0].x <= 0:
                        self.bullets.pop(i)
                        break
                    elif self.bullets[i][0].y <= 0:
                        self.bullets.pop(i)
                        break
                    elif self.bullets[i][0].x >= 1141:
                        self.bullets.pop(i)
                        break
                    elif self.bullets[i][0].y >= 750:
                        self.bullets.pop(i)
                        break
                idx += 1
        return leveled