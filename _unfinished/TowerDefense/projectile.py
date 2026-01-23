import pygame
from settings import Settings
class Bullets():
    def __init__(self, towerType:int):
        self.color = (255, 255, 255)
        self.settings = Settings()
        self.speed_factor = self.settings.BASE_BULLET_SPEED
        self.bullets = []
        self.towerType = towerType
        self.angle = 0
        self.towerTypesList = {
            0:{"NAME":"Basic Turret", "RANGE":130, "COOLDOWN":40, "DAMAGE":3, "SPEED":1,"EXTRA":{}},
            1:{"NAME":"Full Turret", "RANGE":200, "COOLDOWN":4, "DAMAGE":1, "SPEED":1,"EXTRA":{}},
            2:{"NAME":"Dual Turret", "RANGE":200, "COOLDOWN":4, "DAMAGE":1, "SPEED":1, "EXTRA":{"DUAL":True}},
            3:{"NAME":"Sniper", "RANGE":1000, "COOLDOWN":80, "DAMAGE":15, "SPEED":4, "EXTRA":{}},
            4:{"NAME":"Quick Turret", "RANGE":130, "COOLDOWN":2, "DAMAGE":0.05, "SPEED":2, "EXTRA":{}},
        }
        self.towerInfo = self.towerTypesList[self.towerType]
        self.timer_reset = self.towerInfo["COOLDOWN"]
        self.timer = self.timer_reset
        self._last_angle = None
        self._rotated = None

    def get_rotated_image(self, turretImages:list[pygame.surface.SurfaceType]) -> pygame.surface.SurfaceType:
        angle = -self.angle - 180
        if angle != self._last_angle:
            self._rotated = pygame.transform.rotate(
                turretImages[self.towerType], angle
            )
            self._last_angle = angle
        return self._rotated
    def calc_nearest_enemy(self, e_rect:list[dict], rect:pygame.rect.RectType
                            ) -> tuple[pygame.math.Vector2, pygame.math.Vector2]:
        """ Find nearest enemy and calculate angle to it """
        center = pygame.Vector2(rect.center)
        vector = pygame.Vector2()
        if len(e_rect) > 0:
            # Find closest enemy
            rx, ry = rect.center
            en = min(
                e_rect,
                key=lambda e: (e["rect"].centerx - rx) ** 2 + (e["rect"].centery - ry) ** 2
            )
            # Find angle
            ex, ey = en["rect"].center
            x_a = ex - rect.centerx
            y_a = ey - rect.centery
            c = (x_a**2 + y_a**2) # Pythagorean Theorem
            if c > self.towerInfo["RANGE"] ** 2: return False, False # sqrt of 16900 is 130
            angle = -pygame.math.Vector2(x_a, y_a).angle_to((1, 0))
            self.angle = angle
        else:
            return False, False # 100 if no enemy on the screen
        vector.from_polar((self.speed_factor * 4 * self.towerInfo["SPEED"], angle))
        return center, vector,
    def shoot(self, screen, e_rect:list, player:list[int, int], screen_rect:pygame.rect.RectType) -> float | int:
        """ Fire new bullets and move other bullets """
        # Check for new bullets
        self.timer -= 1
        #rect = pygame.Rect(0, 0, 20, 20)
        #rect.center = [player[1] + 40, player[0] + 40]
        #pygame.draw.circle(screen, self.color, rect.center, self.towerInfo["RANGE"])
        if self.timer == 0:
            self.timer = self.timer_reset
            # Create rect for new bullet and store it
            rect = pygame.Rect(0, 0, 20, 20)
            rect.center = (player[1], player[0]) # Intended swap
            #rect.centery = player.rect.centery
            center, vector = self.calc_nearest_enemy(e_rect, rect)
            if center == False:
                return 0
            self.bullets.append([rect, vector, center])
            if "DUAL" in self.towerInfo["EXTRA"]:
                self.bullets.append([rect.copy(), -vector, center.copy()])
        for i in range(len(self.bullets) - 1, -1, -1):
            # Draw bullets
            pygame.draw.circle(screen, self.color, self.bullets[i][0].center, 14)
            self.bullets[i][2] += self.bullets[i][1]
            self.bullets[i][0].center = self.bullets[i][2]
            if not screen_rect.colliderect(self.bullets[i][0]):
                self.bullets.pop(i)
                continue
            for idx in range(len(e_rect) - 1, -1, -1):
                m = e_rect[idx]
                # Check if any bullet has hit an enemy
                if self.bullets[i][0].colliderect(m["rect"]):
                    self.bullets.pop(i)
                    # Reduce enemy health
                    e_rect[idx]["health"] -= self.towerInfo["DAMAGE"]
                    if e_rect[idx]["health"] < 1:
                            e_rect.pop(idx)
                    break
        return self.angle