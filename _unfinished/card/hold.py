import pygame
from pytweening import easeInOutSine
from enums import BACK
from random import choice
class Hold():
    def __init__(self, screen:pygame.surface.Surface, images:list, load):
        self.screen = screen
        self.images = images
        self.tween = easeInOutSine
        self.buttonImages = (load('button0', "button"), load('button1', "button"), load('button2', "button"),
                             load('stand0', "button"), load('stand1', "button"), load('stand2', "button"))
        self.screenRect = screen.get_rect()
        # Flight
        self.flight_states = {}
        self.cardTurnFinishFlight = False
        self.card_states = []
        self.flight_duration = 0.5  # seconds
        self.target_pos = (self.screenRect.right - 276, self.screenRect.centery - 128)  # where to fly the card to
        self.clock = pygame.time.Clock()
        # Button
        self.draw_standing = False
        self.time = 0
        self.clicking = False
        self.clicked = False
        self.turn = 0
        self.standing = False
        
        self.previous = [] # Holds previous card
        pygame.mixer.init()
        self.sounds = (pygame.mixer.Sound('sounds/cardMove.mp3'), pygame.mixer.Sound('sounds/buttonClick.mp3'))

    def blitme(self, bottom, cards: list, clickable: bool = True) -> list:
        remove = []
        dt = self.clock.tick(60) / 1000  # Frame time in seconds

        # Initialize card states if needed
        if len(self.card_states) != len(cards):
            self.card_states = [{
                "flying": False,
                "time_elapsed": 0.0,
                "start_pos": (0, 0)
            } for _ in cards]

        button_img = self.buttonImages[1]
        back_x, back_y = 20, bottom - 270
        button_rect = pygame.Rect(self.screenRect.centerx - 250, bottom - 230, button_img.get_width(), button_img.get_height())
        stand_rect = pygame.Rect(self.screenRect.centerx + 130, bottom - 230, button_img.get_width(), button_img.get_height())

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Handle click to fly a random card if hit button is clicked
        if self.turn == 0 and clickable and not self.clicking:
            if self.clicked:
                self.clicked = False
                if button_rect.collidepoint(mouse_x, mouse_y): # Hitting
                    # Choose random unflying card
                    valid_indices = [i for i, state in enumerate(self.card_states) if not state["flying"]]
                    if valid_indices:
                        idx = choice(valid_indices)
                        state = self.card_states[idx]
                        state["flying"] = True
                        state["time_elapsed"] = 0.0
                        state["start_pos"] = (back_x, back_y)
                        pygame.mixer.Channel(1).play(self.sounds[0]) # Card noise
                        pygame.mixer.Channel(2).play(self.sounds[1]) # Button noise
                        self.clicking = True
                elif stand_rect.collidepoint(mouse_x, mouse_y): # Standing
                    self.standing = True
                    pygame.mixer.Channel(2).play(self.sounds[1]) # Button noise
                    self.clicked = False
                    self.draw_standing = True
        else: self.clicked = False

        if self.draw_standing:
            self.time += dt
            if self.time > 1:
                self.time = 0
                self.draw_standing = False
        else: self.time = 0

        # Update flying cards
        for idx, state in enumerate(self.card_states):
            if state["flying"]:
                state["time_elapsed"] += dt
                if state["time_elapsed"] > 1:
                    remove.append(idx)

        # Draw the back card
        if len(cards) != 0 and not ((len(cards) == 1) and self.clicking):
            self.screen.blit(self.images[BACK], (back_x, back_y))
        self.drawButton(bottom)

        # Draw flying cards
        for idx, state in enumerate(self.card_states):
            if not state["flying"]:
                continue

            t = min(state["time_elapsed"] / self.flight_duration, 1.0)
            eased = self.tween(t)
            start_x, start_y = state["start_pos"]
            target_x, target_y = self.target_pos

            x = start_x + (target_x - ((len(self.previous) * 50) % 150) - start_x) * eased
            y = start_y + (target_y - start_y) * eased

            self.screen.blit(self.images[cards[idx]], (x, y))

        # Remove flown cards
        for i in remove:
            #print(i)
            self.previous.append(cards[i])
            cards.pop(i)
            self.turn = 1
            self.clicking = False
            #print(self.clicking)
        #print(self.turn, self.cardTurnFinishFlight, self.clicked, clickable, self.clicking)
        return cards

    def drawPrevious(self):
        for idx, i in enumerate(self.previous):
            self.screen.blit(self.images[i], (self.target_pos[0]-((idx*50)%150), self.target_pos[1]))

    def flyPrevious(self, init=False, bottom=0):
        # Init card states if needed
        if init:
            self.flight_states = [{
                "progress": 0.0,
                "time_elapsed": 0.0,
                "start_pos": (0, self.target_pos[1])
            } for _ in self.previous]
        ####
        if len(self.previous) != 0:
            dt = self.clock.tick(60) / 1000  # frame time in seconds
            for idx, state in enumerate(self.flight_states):
                state["time_elapsed"] += dt
            ###
                t = min(state["time_elapsed"] / self.flight_duration, 1.0)
                eased = self.tween(t)
                _, start_y = state["start_pos"]

                y = start_y + (bottom + 356 - start_y) * eased
                self.screen.blit(self.images[self.previous[idx]], (self.target_pos[0]-((idx * 50) % 150), y))
                if state["time_elapsed"] > 0.3:
                    self.cardTurnFinishFlight = False
        else:
            if init:
                self.flight_states = 0.0
            dt = self.clock.tick(60) / 1000  # frame time in seconds
            self.flight_states += dt
            if self.flight_states > 0.3:
                self.cardTurnFinishFlight = False

    def drawButton(self, bottom):
        length = len(self.card_states)
        for idx, i in enumerate(self.card_states):
            if i["time_elapsed"] > 0.3:
                self.screen.blit(self.buttonImages[1], (self.screenRect.centerx - 250, bottom - 230))
                break
            elif i["time_elapsed"] > 0.1:
                self.screen.blit(self.buttonImages[2], (self.screenRect.centerx - 250, bottom - 230))
                break
            elif idx == length - 1:
                self.screen.blit(self.buttonImages[0], (self.screenRect.centerx - 250, bottom - 230))
        if (len(self.card_states) == 0):
            self.screen.blit(self.buttonImages[0], (self.screenRect.centerx - 250, bottom - 230))
        if self.time <= 0.1:
            self.screen.blit(self.buttonImages[3], (self.screenRect.centerx + 100, bottom - 230))
        elif self.time > 0.3:
            self.screen.blit(self.buttonImages[4], (self.screenRect.centerx + 100, bottom - 230))
        elif self.time > 0.1:
            self.screen.blit(self.buttonImages[5], (self.screenRect.centerx + 100, bottom - 230))
    

    #def updateScreen(self, screen): self.screen = screen