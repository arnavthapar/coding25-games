import pygame
from random import choice
from pytweening import easeInOutSine
from time import time

class NumbersBox():
    def __init__(self, screen:pygame.surface.Surface):
        self.screen = screen
        self.screenRect = screen.get_rect()

        self.numbers = (self.load("number9"),self.load("number10"), self.load("number11"), self.load("number12"), self.load("number13"),
            self.load("number14"), self.load("number15"), self.load("number16"), self.load("number17"), 
            self.load("number18"),
            self.load("number19"), )#self.load("number20"))
        self.maxBox = self.load('maxFrame', '')
        self.fontNumbers = {"0": self.load('zero', 'numbers/font'), "1": self.load('one', 'numbers/font'), "2": self.load('two', 'numbers/font'), "3": self.load('three', 'numbers/font'), "4": self.load('four', 'numbers/font'),
                            "5": self.load('five', 'numbers/font'), "6": self.load('six', 'numbers/font'), "7": self.load('seven', 'numbers/font'), "8": self.load('eight', 'numbers/font'), "9": self.load('nine', 'numbers/font')}
        self.count = 0
        self.numberSelection = None
        self.max = 19
        self.counting = False
        self.draw_box = False
        pygame.mixer.init()
        self.click = pygame.mixer.Sound('sounds/click.mp3')
        # Flight
        self.flying = False
        self.fly_start_time = 0
        self.fly_start_y = 0
        self.fly_target_y = 0
        # Box flight
        self.fly_start_y_box = 0
        self.fly_target_y_box = 0

        self.ease = easeInOutSine
        self.draw = True
        
        # Counting
        
        self.start_time = 0
        self.duration = 6.0  # total duration in seconds
        self.last_change_time = 0
        self.change_interval = 0.05
        self.progress = 0.0

    def load(self, image:str, location:str="numbers"):
        return pygame.image.load(f"images/{location}/{image}.png")

    def startCount(self):
        if not self.count:
            self.start_time = time()
        self.draw = True
        self.counting = True
        self.count += 1
        current_time = time()
        elapsed = current_time - self.start_time
        self.progress = min(elapsed / self.duration, 1.0)

        # Calculate how fast to change numbers based on tweened time
        # (starts fast, ends slow)
        interval = 0.05 + (0.9 * self.ease(self.progress))  # grows from ~0.05 → 1

        if current_time - self.last_change_time >= interval:
            self.last_change_time = current_time
            self.numberSelection = choice(self.numbers)
            pygame.mixer.Channel(1).play(self.click)

        # Done counting
        if self.progress >= 1.0:
            self.counting = False
            self.progress = 0.0
            self.max = self.numbers.index(self.numberSelection) + 9

    def fly(self, bottom:int=0, top:int=0):
        self.draw_box = False
        if not self.flying:
            self.flying = True
            self.fly_start_time = time()
            self.fly_start_y = self.screenRect.centery - 128
            self.fly_target_y = bottom
            self.fly_start_y_box = top - 50
            self.fly_target_y_box = self.screenRect.centery - 128

        t = (time() - self.fly_start_time) / 2
        if t >= 1.0:
            self.flying = False
            self.draw = False
            self.draw_box = True
            self.screen.blit(self.maxBox, (self.screenRect.centerx - 128, self.screenRect.centery - 128))
            strIdx = str(self.max)
            if strIdx == "9": strIdx = "8"
            self.screen.blit(self.fontNumbers[strIdx[0]], ((self.screenRect.centerx + 20, self.screenRect.centery - 108)))
            if len(str(self.max)) == 2:
                self.screen.blit(self.fontNumbers[strIdx[1]], ((self.screenRect.centerx + 50, self.screenRect.centery - 108)))
            return
        # Draw big grey number box
        tweened_t = self.ease(min(t, 1.0))
        current_y = self.fly_start_y + (self.fly_target_y - self.fly_start_y) * tweened_t
        self.screen.blit(self.numberSelection, (self.screenRect.centerx - 128, current_y))
        # Draw new box
        current_y = self.fly_start_y_box + (self.fly_target_y_box - self.fly_start_y_box) * tweened_t
        self.screen.blit(self.maxBox, (self.screenRect.centerx - 128, current_y))
        # Draw numbers in the new box
        strIdx = str(self.max)
        self.screen.blit(self.fontNumbers[strIdx[0]], ((self.screenRect.centerx + 20, current_y + 20)))
        if len(strIdx) == 2:
            self.screen.blit(self.fontNumbers[strIdx[1]], ((self.screenRect.centerx + 50, current_y + 20)))



    def blitme(self):
        if self.numberSelection != None and self.draw:
            self.screen.blit(self.numberSelection, (self.screenRect.centerx-128, self.screenRect.centery-128))
            if self.count != 0:
                self.startCount()
        if self.draw_box:
            self.screen.blit(self.maxBox, (self.screenRect.centerx - 128, self.screenRect.centery - 128))
            strIdx = str(self.max)
            self.screen.blit(self.fontNumbers[strIdx[0]], ((self.screenRect.centerx + 20, self.screenRect.centery - 108)))
            if len(strIdx) == 2:
                self.screen.blit(self.fontNumbers[strIdx[1]], ((self.screenRect.centerx + 50, self.screenRect.centery - 108)))

    #def updateScreen(self, screen): self.screen = screen