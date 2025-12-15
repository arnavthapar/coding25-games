import pygame
from numpy import arctan2, degrees
class Bullets():
    def __init__(self):
        self.color = (255, 255, 255)
        self.h_color = (255, 255, 0)
        self.speed_factor = 1
        self.bullets = []
        self.timer_reset = (20)
        self.timer = self.timer_reset
        self.attack = 1 #! 1
    def calc_nearest_enemy(self, e_rect, rect):
        """ Find nearest enemy and calculate angle to it """
        center = pygame.Vector2(rect.center)
        vector = pygame.Vector2()
        if len(e_rect) > 0:
            # Find closest enemy
            en = min([e for e in e_rect], key=lambda e: pow(e["pos"][0]-rect.x, 2) + pow(e["pos"][1]-rect.y, 2))
            # Find angle
            x_a = en["pos"][0] - rect.x
            y_a = en["pos"][1] - rect.y
            theta_r = arctan2(y_a, x_a)
            angle = degrees(theta_r)
        else:
            angle = 100 # 100 if no enemy on the screen
        vector.from_polar((1, angle))
        return center, vector
    def shoot(self, screen, e_rect:list, player:list[int, int]):
        """ Fire new bullets and move other bullets """
        # Check for new bullets
        leveled = 0
        self.timer -= 1
        if self.timer < 1:
            self.timer = self.timer_reset
            # Create rect for new bullet and store it
            rect = pygame.Rect(0, 0, 20, 20)
            rect.center = player[::-1]
            rect.top = player[1] + 32
            #rect.centery = player.rect.centery
            center, vector = self.calc_nearest_enemy(e_rect, rect)
            self.bullets.append([rect, vector, center])
        for i in range(len(self.bullets)):
            if i > len(self.bullets) - 1:
                break
            # Draw bullets
            pygame.draw.rect(screen, self.color, self.bullets[i][0])
            self.bullets[i][2] += self.bullets[i][1] * 4
            self.bullets[i][0].center = self.bullets[i][2]
            idx = 0
            for m in e_rect:
                #rect.topleft = e_rect["pos"]
                # Check if any bullet has hit an enemy
                if self.bullets[i][0].colliderect(m["rect"]):
                    self.bullets.pop(i)
                    # Reduce enemy health
                    e_rect[idx]["health"] -= self.attack
                    if e_rect[idx]["health"] < 1:
                            e_rect.pop(idx)
                    break
                else:
                    # Destroy bullets if they go off the edge of screen
                    if self.bullets[i][0].x <= 0:
                        self.bullets.pop(i)
                        break
                    elif self.bullets[i][0].y <= 0:
                        self.bullets.pop(i)
                        break
                    elif self.bullets[i][0].x >= 1184:
                        self.bullets.pop(i)
                        break
                    elif self.bullets[i][0].y >= 768:
                        self.bullets.pop(i)
                        break
                idx += 1
        return leveled