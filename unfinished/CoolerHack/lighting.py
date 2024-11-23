class Lighting():
    def __init__(self, area = []):
        # example of lighting
        #      #####
        #     #######
        #    ####@####
        #     #######
        #      #####
        #
        #
        # 1 = Have seen, 2 = Can see, 0 = Never saw
        self.levelLight = []
        x = -1
        z = 0
        for i in area:
            self.levelLight.append([])
            for m in i:
                self.levelLight[z].append([])
                x += 1
                for _ in m:
                    self.levelLight[z][x].append(0)
            z += 1
            x = -1
    def reset(self, area):
        x = -1
        y = 0
        z = 0
        for i in area:
            for m in i:
                x += 1
                for _ in m:
                    if self.levelLight[z][x][y] == 2: self.levelLight[z][x][y] = 1
                    y += 1
                y = 0
            z += 1
            x = -1
    def bresenham_line(self, x0, y0, x1, y1):
        """Bresenham's Line Algorithm to get points on a line from (x0, y0) to (x1, y1)."""
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        return points

    def lightUp(self, area, location_x, location_y, level, radius=4):
        """Light up squares."""
        self.reset(area)
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance <= radius:
                    line_points = self.bresenham_line(location_x, location_y, location_x + dx, location_y + dy)
                    for lx, ly in line_points:
                        if lx < 0 or ly < 0 or lx >= len(area[level][0]) or ly >= len(area[level]):
                            break
                        if area[level][ly][lx] in ["|", "-", " ", "="]:
                            self.levelLight[level][ly][lx] = 2 # Mark lit walls
                            break  # Stop the light at the wall
                        self.levelLight[level][ly][lx] = 2  # Mark lit squares
        return self.levelLight