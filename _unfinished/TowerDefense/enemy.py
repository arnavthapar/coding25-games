import pygame

TILE_SIZE = 64  # size of each tile (normally 64)
ENEMY_SPEED = 2  # pixels per frame (must be 1, 2, 4, 8, 16, 32, or 64)
BASE_HEALTH = 20

class Enemy:
    def __init__(self, e_area:list[list[int]], start_tiles:list[int, int], rect):
        """
        e_area: 2D list representing the map directions (1=down,2=left,3=right,4=up)
        start_tiles: list of starting tile positions [[x, y], [x, y], ...]
        """
        self.enemy_area = e_area
        self.enemies = []
        self.image = pygame.image.load('images/enemy.png')
        self.rect = self.image.get_rect()
        # Initialize enemies at center of tiles
        if ENEMY_SPEED not in (1, 2, 4, 16, 32, 64):
            raise ArithmeticError("TILE_SIZE must be 1, 2, 4, 16, 32, or 64 to prevent errors")
        for tile in start_tiles:
            x, y = tile
            px = x * TILE_SIZE + TILE_SIZE // 2
            py = y * TILE_SIZE + TILE_SIZE // 2
            self.enemies.append({
                "tile": [x, y],
                "pos": [px, py],
                "direction": 0,
                "timer": 0, # Timer until direction is checked
                "health": BASE_HEALTH,
                "type": 1, # Type of enemy
                "rect": rect
            })

    def move(self):
        new_enemies = []
        for e in self.enemies:
            # Update current tile
            e["tile"][0] = e["pos"][0] // TILE_SIZE
            e["tile"][1] = e["pos"][1] // TILE_SIZE

            # Decide direction if timer expired
            if e["timer"] <= 0:
                area_pos = self.enemy_area[e["tile"][1]][e["tile"][0]]
                e["timer"] = TILE_SIZE  # move for one tile

                if area_pos == 1:  # down
                    e["direction"] = (0, ENEMY_SPEED)
                elif area_pos == 2:  # left
                    e["direction"] = (-ENEMY_SPEED, 0)
                elif area_pos == 3:  # right
                    e["direction"] = (ENEMY_SPEED, 0)
                elif area_pos == 4:  # up
                    e["direction"] = (0, -ENEMY_SPEED)
            if e["pos"][0] > 1216:
                continue
            if e["pos"][0] < 0:
                continue
            if e["pos"][1] > 768:
                continue
            if e["pos"][1] < 0:
                continue
            # Move enemy
            e["pos"][0] += e["direction"][0]
            e["pos"][1] += e["direction"][1]
            e["timer"] -= ENEMY_SPEED
            new_enemies.append(e)

        self.enemies = new_enemies

    def draw(self, screen):
        for e in self.enemies:
            x = e["pos"][0] - self.rect.width // 2
            y = e["pos"][1] - self.rect.height // 2
            screen.blit(self.image, (x, y))
