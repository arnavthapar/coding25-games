import pygame
TILE_SIZE = 64  # size of each tile (normally 64)
ENEMY_SPEED = 2  # pixels per frame (must be 1, 2, 4, 8, 16, 32, or 64)
BASE_HEALTH = 2

class Enemy:
    def __init__(self, e_area:list[list[int]], start_tiles:list[int, int], rect:pygame.rect.Rect, seconds:int):
        """
        e_area: 2D list representing the map directions (1=down,2=left,3=right,4=up)
        start_tiles: list of starting tile positions [[x, y], [x, y], ...]
        """
        self.enemy_area = e_area
        self.enemies = []
        self.image = pygame.image.load('images/enemy.png')
        self.rect = self.image.get_rect()
        # Initialize enemies at center of tiles
        if ENEMY_SPEED not in (1, 2, 4, 8, 16, 32, 64):
            raise ArithmeticError("TILE_SIZE must be 1, 2, 4, 8, 16, 32, or 64 to prevent errors")
        self.enemyTimer = []
        for idx, tile in enumerate(start_tiles):
            x, y = tile
            px = x * TILE_SIZE + TILE_SIZE // 2
            py = y * TILE_SIZE + TILE_SIZE // 2
            self.enemyTimer.append({
                "tile": [x, y],
                "pos": [px, py],
                "direction": (0, 0),
                "timer": 0, # Timer until direction is checked
                "health": BASE_HEALTH,
                "type": 1, # Type of enemy
                "rect": rect.copy(),
                "time": seconds * (idx + 1)
            })
            self.timer = 0
        self.DIR_LOOKUP = {
            1: (0, ENEMY_SPEED),
            2: (-ENEMY_SPEED, 0),
            3: (ENEMY_SPEED, 0),
            4: (0, -ENEMY_SPEED),
        }


    def move(self, screen_rect):
        self.timer += 1
        for idx in range(len(self.enemyTimer) -1, -1, -1):
            enemy = self.enemyTimer[idx]
            if enemy["time"] == self.timer:
                self.enemies.append(enemy)
                self.enemyTimer.pop(idx)
        #new_enemies = []
        for idx, e in enumerate(self.enemies):
            # Update current tile
            pos = e["pos"]
            dir = e["direction"]
            e["tile"][0] = pos[0] // TILE_SIZE
            e["tile"][1] = pos[1] // TILE_SIZE

            # Decide direction if timer expired
            if e["timer"] <= 0:
                area_pos = self.enemy_area[e["tile"][1]][e["tile"][0]]
                e["timer"] = TILE_SIZE  # move for one tile

                dir = self.DIR_LOOKUP.get(area_pos, (0, 0))
            if not screen_rect.colliderect(e["rect"]):
                self.enemies.pop(idx)
            # Move enemy
            pos[0] += dir[0]
            pos[1] += dir[1]
            e["direction"] = dir
            e["pos"] = pos
            e["timer"] -= ENEMY_SPEED
            e["rect"].center = e["pos"]

        #self.enemies = new_enemies

    def draw(self, screen):
        for e in self.enemies:
            screen.blit(self.image, (e["rect"]))
