import pygame
from math import ceil

class Player():
    def __init__(self):
        self.hitbox = pygame.image.load("images/player/hitbox.png")
        self.rect = self.hitbox.get_rect()
        # Set up movment variables.
        self.direction = 90
        self.animation = 0
        self.player_up = False
        self.player_left = False
        self.player_right = False
        self.player_down = False
        self.rect.x = 35
        self.rect.y = 40

    def update_player(self, area):
        """Move player."""
        self.animation += 1
        change_x = 0
        change_y = 0
        if self.animation > 100: self.animation = 1
        prev_location = (self.rect.x, self.rect.y)
        if int(self.player_left) + int(self.player_right) + int(self.player_up) + int(self.player_down) > 1:
            if self.player_left: change_x -= 1
            elif self.player_right: change_x += 1
            if self.player_up: change_y -= 1
            elif self.player_down: change_y += 1
        else:
            if self.player_left: change_x -= 2
            elif self.player_right: change_x += 2
            if self.player_up: change_y -= 2
            elif self.player_down: change_y += 2
        self.rect.x += change_x
        self.rect.y += change_y
        for i in area.rects:
            if self.rect.colliderect(i):
                self.rect.y = prev_location[1]
                self.rect.x = prev_location[0]

    def blit(self, screen):
        if not(self.player_left or self.player_up or self.player_down or self.player_right): screen.blit(pygame.image.load("images/player/idle"+str(self.direction)+".png"), (self.rect.x, self.rect.y))
        else: screen.blit(pygame.image.load("images/player/walk"+str(self.direction)+"."+str(ceil(self.animation/20))+".png"), (self.rect.x, self.rect.y))
        return screen