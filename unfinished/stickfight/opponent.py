import pygame
from math import floor
class Opponent():
    def __init__(self):
        self.gravity = 0.1
        self.images = []
        self.anim = 7
        for i in range(7):
            self.images.append(pygame.image.load("Images/opponent/Idle" + str(i+1) + ".svg"))
        for i in range(7):
            self.images.append(pygame.image.load("Images/opponent/Run" + str(i+1) + ".svg"))
        self.x_velocity = 0
        self.max_velocity = 4
        self.y_velocity = 0
        self.direction = 0
        self.rect = pygame.image.load("Images/Hitbox.svg").get_rect()
        self.rect.x = 800
        self.rect.y = 400
        self.gravity_time = 0.5
        self.coyote_time = 0
        self.moved = False
    def move(self, area):
        self.coyote_time += 1
        """Move the opponent around."""
        # Move on the x axis.
        self.x_velocity += self.direction/40
        if self.direction == 0 and self.x_velocity != 0:
            if self.x_velocity < 0:
                self.x_velocity += 0.4
            else:
                self.x_velocity -= 0.4
            if self.x_velocity < 1 and self.x_velocity > -1: self.x_velocity = 0
        self.rect.x += floor(self.x_velocity)
        for i in area:
            if self.rect.colliderect(i):
                        self.rect.x -= floor(self.x_velocity)
        if self.x_velocity > self.max_velocity: self.x_velocity = self.max_velocity
        if self.x_velocity < 0 - self.max_velocity: self.x_velocity = 0 - self.max_velocity
        # Move on the y axis.
        if self.y_velocity >= self.max_velocity * 2: self.y_velocity = self.max_velocity * 2 - self.gravity
        if self.y_velocity <= 0 - self.max_velocity * 2: self.y_velocity = 0 - self.max_velocity * 2 - self.gravity
        self.y_velocity += self.gravity * self.gravity_time
        self.rect.y += floor(self.y_velocity)
        self.gravity_time += 0.1
        if self.gravity_time > 4: self.gravity_time = 4
        for i in area:
            if self.rect.colliderect(i):
                self.gravity_time = 0.5
                self.rect.y -= floor(self.y_velocity)
                if self.y_velocity < 1 and self.x_velocity > -1: self.y_velocity = 0
                self.y_velocity = 0
                self.coyote_time = 0
                break
        if self.rect.y > 1000:
            self.rect.y = 400
            self.rect.x = 600

    def blitme(self, screen, area):
        """Draw the opponent on the screen."""
        # Increase the animation variable.
        self.anim += 0.1
        if self.anim >= 13.5:
            self.anim = 7
        self.move(area) # Move the opponent.
        # Draw the opponent.
        if self.direction == -1: screen.blit(pygame.transform.flip(self.images[floor(self.anim)], True, False),(self.rect.x, self.rect.y))
        elif self.direction == 1: screen.blit(self.images[floor(self.anim)],(self.rect.x, self.rect.y))
        else: screen.blit(self.images[floor(self.anim) - 7], (self.rect.x, self.rect.y))