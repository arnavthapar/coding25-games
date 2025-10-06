import pygame
from enums import *
from random import choice

def check_events():#screenRect):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not hold.clicking:# and (hold.turn == 0):
            hold.clicked = True
        '''elif event.type == pygame.VIDEORESIZE:
            width, height = event.size
            if width < 1024:
                width = 1024
            if height < 800:
                height = 800
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            screenRect = screen.get_rect()
            hold.updateScreen(screen)
            opponent.updateScreen(screen)
            numbers.updateScreen(screen)
    return screenRect'''

def startGame(screenRect:pygame.rect.Rect):
    numbers.startCount()
    while numbers.counting: # Decide top
        check_events()
         
        screen.fill((80, 180, 80))
        #screen.blit(background, (0, 0))
        hold.blitme(screenRect.bottom,cards, False)
        numbers.blitme()
        opponent.blitme(opCards)
        pygame.display.flip()

    numbers.fly(screenRect.bottom, screenRect.top)
    while numbers.flying: # Fly number away
        check_events()
        screen.fill((80, 180, 80))
        #screen.blit(background, (0, 0))
        hold.blitme(screenRect.bottom,cards, False)
        numbers.fly()
        opponent.blitme(opCards)
        pygame.display.flip()

def load(image:str, location:str="cards"):
    return pygame.image.load(f"images/{location}/{image}.png")

def opponentTurn(opCount, cards, opCards, max):
    # Opponent turn
    if opCount <= numbers.max:
        opponent.movable = True
        opCount = 0
        hold.turn = 1
        while hold.turn == 1:
            check_events()
            screen.fill((80, 180, 80))
            hold.drawPrevious()
            cards = hold.blitme(screenRect.bottom,cards, False)
            numbers.blitme()
            opponent.drawPrevious()
            opCards, hold.turn = opponent.blitme(opCards, True, hold.turn, max)
            pygame.display.flip()
        for i in opponent.previous:
            opCount += valueTable[i]
    opponent.movable = False
    return opCount
#background = load("background", "")
images={SPADES_ACE:load("spadesace"), SPADES_ONE:load("spadesone"), SPADES_TWO:load("spadestwo"), SPADES_THREE:load("spadesthree"), SPADES_FOUR:load("spadesfour"), SPADES_FIVE:load("spadesfive"),
        SPADES_SIX:load("spadessix"), SPADES_SEVEN:load("spadesseven"), SPADES_EIGHT:load("spadeseight"), SPADES_NINE:load("spadesnine"), SPADES_TEN:load("spadesten"),
        SPADES_KING:load("spadesking"), SPADES_QUEEN:load("spadesqueen"), SPADES_JESTER:load("spadesjester"),
        
        HEARTS_ACE:load("heartsace"), HEARTS_ONE:load("heartsone"), HEARTS_TWO:load("heartstwo"), HEARTS_THREE:load("heartsthree"), HEARTS_FOUR:load("heartsfour"),  HEARTS_FIVE:load("heartsfive"),
        HEARTS_SIX:load("heartssix"), HEARTS_SEVEN:load("heartsseven"), HEARTS_EIGHT:load("heartseight"), HEARTS_NINE:load("heartsnine"), HEARTS_TEN:load("heartsten"),
        HEARTS_JESTER:load("heartsjester"), HEARTS_QUEEN:load("heartsqueen"), HEARTS_KING:load("heartsking"),
        
        SPADES_ZERO:load("spadeszero"),
        HEARTS_ZERO:load("heartszero"),
        DIAMONDS_ZERO:load("diamondszero"),
        RIPPED:load("ripped"),
        JOKER:load("joker"), ROUND:load('round'), BACK:load('back')}

screen = pygame.display.set_mode((1500, 800))#, pygame.RESIZABLE)
pygame.display.set_caption("[insert cool game name here]")
from hold import Hold
hold = Hold(screen, images, load)
from opponent import Opponent
opponent = Opponent(screen, images, load)
from numbersBox import NumbersBox
numbers = NumbersBox(screen)

all_choices = list(images.keys())
cards = [choice(all_choices) for _ in range(13)]
opCards = [choice(all_choices) for _ in range(13)]
screenRect = screen.get_rect()
previousCards = []

startGame(screenRect) # Start the turn
reset = []
resetOp = []
opCount = 0
count = 0
while True:
    count = 0
    hold.clicking = False
    opponent.standing = False
    hold.standing = False
    # Player turn
    while (count <= numbers.max) and not hold.standing:
        hold.turn = 0
        count = 0
        while (hold.turn == 0) and not hold.standing:
            check_events()
            screen.fill((80, 180, 80))
            hold.drawPrevious()
            cards = hold.blitme(screenRect.bottom,cards)
            numbers.blitme()
            opponent.drawPrevious()
            opCards, hold.turn = opponent.blitme(opCards, False, hold.turn, numbers.max)
            pygame.display.flip()
        for i in hold.previous:
            count += valueTable[i]

        if not opponent.standing:
            opCount = opponentTurn(opCount, cards, opCards, numbers.max)
    while (opCount <= numbers.max) and not opponent.standing:
        opCount = opponentTurn(opCount, cards, opCards, numbers.max)
    opCount = 0

    # Fly down cards
    hold.cardTurnFinishFlight = True
    hold.flyPrevious(True, screenRect.bottom)
    opponent.flyPrevious(True, screenRect.bottom)
    while hold.cardTurnFinishFlight:
        check_events()
        screen.fill((80, 180, 80))
        hold.blitme(screenRect.bottom, cards, False)
        opponent.blitme(opCards, False, 0, numbers.max)
        hold.flyPrevious(False, screenRect.bottom)
        numbers.blitme()
        opponent.flyPrevious(False, screenRect.bottom)
        pygame.display.flip()
    reset = hold.previous
    hold.previous = [] # Reset
    resetOp = opponent.previous
    opponent.previous = []