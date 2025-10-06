import pygame
from pytweening import easeInOutSine
from random import choice
from enums import BACK, valueTable
class Opponent():
    def __init__(self, screen:pygame.surface.Surface, images:dict, load):
        self.screen = screen
        self.images = images
        self.screenRect = screen.get_rect()
        self.y = self.screenRect.top + 15
        self.x = self.screenRect.right - 276
        self.clock = pygame.time.Clock()
        self.tween = easeInOutSine
        self.chosen = None
        self.movable = True
        self.top = self.screenRect.top
        self.standing = False
        self.chips = (load("chip0", "chip"), load('chip1', 'chip'))
        # Flight
        self.flight_states = {}
        self.flight_duration = 0.5  # seconds
        self.card_states = []
        self.target_pos = (self.screenRect.left + 20, self.screenRect.centery-128)  # where to fly the card to
        pygame.mixer.init()
        self.move = pygame.mixer.Sound('sounds/cardMove.mp3')
        self.previous = []
        self.moving = False
    def blitme(self, opponent:list, time:bool=False, turn:int=0, maxCount:int=9):
        remove = []
        dt = self.clock.tick(60) / 1000  # frame time in seconds

        # Init card states if needed
        if len(self.card_states) != len(opponent):
            self.card_states = [{
                "hover": False,
                "progress": 0.0,
                "flying": False,
                "time_elapsed": 0.0,
                "start_pos": (0, 0)
            } for _ in opponent]

        back_x, back_y = self.x, self.y
        
        # Step 3: Handle flight
        if turn == 1 and time:
            if self.movable and len(opponent) > 0:
                self.movable = False
                self.chosen = choice(range(len(opponent))) # Select card
                state = self.card_states[self.chosen] # Get card state
                if not state["flying"]:
                    state["flying"] = True
                    state["time_elapsed"] = 0.0
                    offset = -100 * self.tween(state["progress"])
                    state["start_pos"] = (back_x, back_y + offset)
                    pygame.mixer.Channel(1).play(self.move) # Play card moving sound
                    self.moving = True


        # Step 4: Update states
        for idx, state in enumerate(self.card_states):
            if state["flying"]:
                state["time_elapsed"] += dt
                if state["time_elapsed"] > 1:
                    remove.append(idx)

        # Step 5: Draw normal card
        if len(opponent) != 0 and not ((len(opponent) == 1) and self.moving):
            self.screen.blit(self.images[BACK], (back_x, back_y))

        # Step 6: Draw flying cards
        for idx, state in enumerate(self.card_states):
            if not state["flying"]: continue
            t = min(state["time_elapsed"] / self.flight_duration, 1.0)
            eased = self.tween(t)
            start_x, start_y = state["start_pos"]
            target_x, target_y = self.target_pos
            x = start_x + (target_x + ((len(self.previous) * 50) % 150) - start_x) * eased
            y = start_y + (target_y - start_y) * eased
            self.screen.blit(self.images[opponent[idx]], (x, y))

        # Step 7: Remove the hovered card if it exists
        for i in remove:
            self.previous.append(opponent[i])
            opponent.pop(i)
            self.moving = False
            turn = 0
        count = 0

        for i in self.previous:
            count += valueTable[i]
        if count > maxCount - 2:
            self.standing = True
        #if self.standing:
        self.drawChip()
        return opponent, turn
    def flyPrevious(self, init=False, bottom=0):
        # Init card states if needed
        if init:
            self.flight_states = [{
                "progress": 0.0,
                "time_elapsed": 0.0,
                "start_pos": (0, self.target_pos[1])
            } for _ in self.previous]
        ####
        dt = self.clock.tick(60) / 1000  # frame time in seconds
        for idx, state in enumerate(self.flight_states):
            state["time_elapsed"] += dt
        ###
            t = min(state["time_elapsed"] / self.flight_duration, 1.0)
            eased = self.tween(t)
            _, start_y = state["start_pos"]

            y = start_y + (bottom + 356 - start_y) * eased
            self.screen.blit(self.images[self.previous[idx]], (self.target_pos[0] + ((idx * 50) % 150), y))
            if state["time_elapsed"] > 1:
                self.cardTurnFinishFlight = False

    def drawPrevious(self):
        for idx, i in enumerate(self.previous):
            self.screen.blit(self.images[i], (self.target_pos[0] + ((idx*50)%150), self.target_pos[1]))
    def drawChip(self):
        if self.standing:
            self.screen.blit(self.chips[1], (self.x - 120, self.y))
        else:
            self.screen.blit(self.chips[0], (self.x - 120, self.y))
    #def updateScreen(self, screen): self.screen = screen