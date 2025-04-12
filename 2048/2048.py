from random import randrange, sample
from sys import argv
import pygame
class num_game:
    def __init__(self):
        self.area = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.screen = pygame.display.set_mode((500, 500))
        self.screen.fill([255, 255, 255])
        self.grid = pygame.image.load("images/grid.png")
        self.prev_area = ''
        self.large = True if argv[-1] == "large" else False
        self.one = True if argv[-1] == "one" else False
        self.lose = False
        self.win = False
        self.msg_image = ""
        self.msg_image_rect = ""
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, 500, 500)
        self.rect.center = self.screen.get_rect().center
        pygame.display.set_caption("2048")
    def print_area(self, area) -> str:
        x2 = 15
        y2 = 15
        self.screen.blit(self.grid,(0, 0))
        for y in area:
            for x in y:
                if x != 0:
                    try:
                        img = pygame.transform.scale(pygame.image.load(f"images/{x}.svg"), (105, 105))
                    except:
                        img = pygame.transform.scale(pygame.image.load(f"images/{x}.webp"), (105, 105))
                    self.screen.blit(img,(x2, y2))
                x2 += 121
            y2 += 121
            x2 = 15
        if self.lose:
            self.msg_image = self.font.render("You lost...", True, (255, 255, 255), (0, 0, 0))
            self.msg_image_rect = self.msg_image.get_rect()
            self.msg_image_rect.center = self.rect.center
            self.screen.blit(self.msg_image, self.msg_image_rect)
        if self.win and not self.large:
            self.msg_image = self.font.render("You win!", True, (255, 255, 255), (0, 0, 0))
            self.msg_image_rect = self.msg_image.get_rect()
            self.msg_image_rect.center = self.rect.center
            self.screen.blit(self.msg_image, self.msg_image_rect)
    def random(self) -> int:
        return randrange(0, 4)
    def num(self) -> int:
        if not self.one:
            return sample([2, 4], k=1)[0]
        return 1
    def move(self, dir, test=False, area=""):
        row_num = 0
        match dir:
            case "left":
                if not test:
                    for row in self.area:
                        filtered = self.shift_and_merge(row)
                        self.area[row_num] = filtered
                        row_num += 1
                else:
                    for row in area:
                        filtered = self.shift_and_merge(row)
                        area[row_num] = filtered
                        row_num += 1
                    return area

            case "right":
                if not test:
                    for row in self.area:
                        filtered = self.shift_and_merge(row[::-1])
                        self.area[row_num][::-1] = filtered
                        row_num += 1
                else:
                    for row in area:
                        filtered = self.shift_and_merge(row[::-1])
                        area[row_num][::-1] = filtered
                        row_num += 1
                    return area

            case "up":
                if not test:
                    self.area = list(map(list, zip(*self.area)))
                    for row in self.area:
                        filtered = self.shift_and_merge(row)
                        self.area[row_num] = filtered
                        row_num += 1
                    self.area = list(map(list, zip(*self.area)))
                else:
                    area = list(map(list, zip(*area)))
                    for row in area:
                        filtered = self.shift_and_merge(row)
                        area[row_num] = filtered
                        row_num += 1
                    area = list(map(list, zip(*area)))
                    return area

            case "down":
                if not test:
                    self.area = list(map(list, zip(*self.area)))
                    for row in self.area:
                        filtered = self.shift_and_merge(row[::-1])
                        self.area[row_num][::-1] = filtered
                        row_num += 1
                    self.area = list(map(list, zip(*self.area)))
                else:
                    area = list(map(list, zip(*area)))
                    for row in area:
                        filtered = self.shift_and_merge(row[::-1])
                        area[row_num][::-1] = filtered
                        row_num += 1
                    area = list(map(list, zip(*area)))
                    return area
    def shift_and_merge(self, row):
        """Moves numbers left, merges them, then fills with zeros."""
        filtered = [num for num in row if num != 0]
        i = 0
        while i < len(filtered) - 1:
            if filtered[i] == filtered[i + 1]:
                filtered[i] += filtered[i]
                filtered.pop(i + 1)
            i += 1
        while len(filtered) < 4: filtered.append(0)
        return filtered

    def check_events(self):
        self.create = True
        moved = False
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    self.prev_area = [row[:] for row in self.area]
                    if not self.lose and not self.win:
                        match event.key:
                            case pygame.K_LEFT:
                                self.move("left")
                            case pygame.K_RIGHT:
                                self.move("right")
                            case pygame.K_UP:
                                self.move("up")
                            case pygame.K_DOWN:
                                self.move("down")
                        if self.prev_area != self.area:
                            moved = True
        
        found = False
        while found == False and moved == True:
            x = self.random()
            y = self.random()
            if self.area[x][y] == 0:
                self.area[x][y] += self.num()
                found = True
        self.print_area(self.area)
        pygame.display.flip()
        zeros = False
        for i in self.area:
            for m in i:
                if m == 2048:
                    self.win = True
                elif m == 0:
                    zeros = True
                    break
        if not zeros:
            if self.move('left', True, self.area) == self.area:
                if self.move('right', True, self.area) == self.area:
                    if self.move('up', True, self.area) == self.area:
                        if self.move('down', True, self.area) == self.area:
                            self.lose = True
num = num_game()
pygame.init()

num.area[num.random()][num.random()] += num.num()
num.print_area(num.area)
while True:
    num.check_events()
    pygame.display.flip()
