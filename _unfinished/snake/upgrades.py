import pygame

class Upgrades:
    def __init__(self, screen: pygame.surface.Surface, images: tuple):
        self.screen = screen
        self.upgrades = [0] * 10
        self.upgrades[0] = 1
        self.images = images
        self.Uimages = (0, 1, 2, 3,)
        self.layer = {1: 0, 2: 1, 3: 1, 4: 2, 5: 2}
        self.x = {1: 0, 2: 1, 3: -1, 4: 1, 5: -1}
        self.connections = {1: [2, 3], 2: [4], 3: [5], 4:[]}
        self.points = {0:4, 1:15, 2: 40, 3: 50}
        self.shade = pygame.image.load('images/upgrades/shade.png')
        self.upgraded = pygame.image.load('images/upgrades/done.png')

        self.flash_timer = [0.0] * 10
        self.pop_timer = [0.0] * 10
        self.upgrade_sound = pygame.mixer.Sound("sound/click.mp3")

    def drawAll(self, CY: int, center: tuple, dt: float):
        positions = {}

        for idx, img in enumerate(self.Uimages):
            uid = idx + 1
            if uid not in self.layer or uid not in self.x:
                continue

            x = center[0] - 64 - self.x[uid] * 100
            y = center[1] - 64 + CY * 2 - self.layer[uid] * 256
            center_pos = (x + self.images[img].get_width() // 2, y + self.images[img].get_height() // 2)
            positions[uid] = (x, y, center_pos)

        for src, targets in self.connections.items():
            for dst in targets:
                if src in positions and dst in positions:
                    pygame.draw.line(
                        self.screen, (255, 255, 255),
                        positions[src][2], positions[dst][2], 4
                    )

        for idx, (uid, (x, y, _)) in enumerate(positions.items()):
            img = self.images[uid - 1]
            scale = 1.0

            if self.pop_timer[idx] > 0:
                scale = 1.2 - (self.pop_timer[idx] / 0.2) * 0.2
                self.pop_timer[idx] -= dt

            scaled_img = pygame.transform.scale(
                img,
                (int(img.get_width() * scale), int(img.get_height() * scale))
            )
            self.screen.blit(
                scaled_img,
                (x + (img.get_width() - scaled_img.get_width()) // 2,
                 y + (img.get_height() - scaled_img.get_height()) // 2)
            )

            if self.flash_timer[idx] > 0:
                glow = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                alpha = int(255 * (self.flash_timer[idx] / 0.3))
                pygame.draw.ellipse(glow, (0, 255, 0, alpha), glow.get_rect())
                self.screen.blit(glow, (x, y))
                self.flash_timer[idx] -= dt

            if self.upgrades[idx] == 0:
                self.screen.blit(self.shade, (x, y))
            elif self.upgrades[idx] == 2:
                self.screen.blit(self.upgraded, (x, y))

    def get_rects(self, CY: int, center: tuple) -> dict:
        rects = []

        for idx, img in enumerate(self.images):
            uid = idx + 1
            if uid not in self.layer or uid not in self.x:
                continue

            x = center[0] - 64 - self.x[uid] * 100
            y = center[1] - 64 + CY * 2 - self.layer[uid] * 256
            rects.append(pygame.Rect(x, y, img.get_width(), img.get_height()))

        return rects

    def click(self, index):
        self.upgrades[index] = 2
        self.flash_timer[index] = 0.3
        self.pop_timer[index] = 0.2
        self.upgrade_sound.play()
        for i in self.connections[index+1]:
            self.upgrades[i-1] = 1