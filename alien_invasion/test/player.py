import pygame

class Player():
    def __init__(self, center, grid):
		# Load the player hitbox and get its rect.
        self.hitbox = pygame.image.load('images/Hitbox.png')
        self.rect = self.hitbox.get_rect()
        # Set up movment variables.
        self.walk = 1
        self.up_velocity = 0
        self.player_y = center[1] * 2 - 53
        self.player_x = 0
        self.player_up = False
        self.player_left = False
        self.player_right = False

        self.grid = grid
    def update_player(self, level):
        """Move player."""
        if self.player_left: self.player_x -= 3
        elif self.player_right: self.player_x += 3
        if self.up_velocity > 0:
            self.player_y -= self.up_velocity / 6
            self.up_velocity -= 0.5
        else:
            if self.player_y < self.grid[str(level)+"f"]:
                self.up_velocity -= 0.5
                if self.player_y > 5: self.player_y -= self.up_velocity / 2.5
                else: self.player_y -= self.up_velocity
            else:
                self.player_y = self.grid[str(level)+"f"]
                self.player_up = False
                self.up_velocity = 0
    def blitme(self, screen):
        """Draw player and create walking animation."""
        if self.player_up:
            if self.player_left and not self.player_right: screen.blit(pygame.transform.flip(pygame.image.load('images/Walk1.png'), True, False), (self.player_x, self.player_y))
            else: screen.blit(pygame.image.load('images/Walk1.png'), (self.player_x, self.player_y))
        elif self.player_left and not self.player_right:
            screen.blit(pygame.transform.flip(pygame.image.load('images/Walk'+str(round(self.walk))+'.png'), True, False), (self.player_x, self.player_y))
            if self.walk < 6: self.walk += 0.05
            else: self.walk = 1
        elif self.player_right and not self.player_left:
            screen.blit(pygame.image.load('images/Walk'+str(round(self.walk))+'.png'), (self.player_x, self.player_y))
            if self.walk < 6: self.walk += 0.05
            else: self.walk = 1
        else: screen.blit(pygame.image.load('images/Idle.png'), (self.player_x, self.player_y))
        return screen