from random import randrange, shuffle, choice
from os import system
class Cards():
    def __init__(self):
        self.PREFIXES = ("Ace", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Jack", "Queen", "King")
        self.SUITS = ("Hearts", "Clubs", "Diamonds", "Spades")
        self.deck = []
        self.hands = []
        self.splitHands = {}
    def newDeck(self):
        self.deck = []
        for suit in self.SUITS:
            for prefix in self.PREFIXES:
                self.deck.append(f"{prefix} of {suit}")
    def shuffle(self): shuffle(self.deck)
    def giveHands(self, people:int, amount:int):
        self.hands = []
        for listIndex in range(people):
            self.hands.append([])
            for _ in range(amount):
                index = randrange(0, len(self.deck))
                self.hands[listIndex].append(self.deck[index])
                self.deck.pop(index)
    def pullCard(self, player:int):
        if self.hasSplit(player):
            selection = choice(self.deck)
            self.deck.remove(selection)
            self.splitHands[player].append(selection)
        if self.findValue(player) > 21: return
        if (player == 0) and (self.findValue(player) > 16): return
        selection = choice(self.deck)
        self.deck.remove(selection)
        self.hands[player].append(selection)
    def findValue(self, player:int, split:bool=False) -> int:
        value = 0
        aces = 0
        for i in self.hands[player]:
            value += min(self.PREFIXES.index(i.split(" ")[0]), 10)
            if i.split(" ")[0] == "Ace":
                value += 11
                aces += 1
        if value > 21:
            while (aces != 0) and (value > 21):
                aces -= 1
                value -= 10
        if split and self.hasSplit(players):
            splitValue = self.splitHandValue(player)
            if (splitValue < value > 21) or (22 > splitValue > value):
                return splitValue
        return value
    def getSplittable(self, player:int) -> bool:
        prefixes = []
        for i in self.hands[player]:
            prefixes.append(i.split(" ")[0])
        if (len(prefixes) != len(set(prefixes))) and (player not in self.splitHands):
            return True
        return False
    def dealerStatus(self) -> str: return "(Stood) " if self.findValue(0) >= 17 else ""
    def split(self, player:int):
        self.splitHands[player] = [self.hands[player][0]]
        self.hands[player].pop(0)
    def hasSplit(self, player:int) -> bool: return True if player in self.splitHands else False
    def splitHandValue(self, player:int) -> int:
        value = 0
        aces = 0
        if not self.hasSplit(player):
            return 0
        for i in self.splitHands[player]:
            value += min(self.PREFIXES.index(i.split(" ")[0]), 10)
            if i.split(" ")[0] == "Ace":
                value += 11
                aces += 1
        if value > 21:
            while (aces != 0) and (value > 21):
                aces -= 1
                value -= 10
        return value
if __name__ == "__main__":
    cards = Cards()
    cards.newDeck()
    cards.shuffle()
    #players = int(input("Players => "))
    players = 1
    cards.giveHands(players+1, 2)
    below = True
    turn = 0
    while below:
        system('clear')
        turn += 1
        print("Current Hand", cards.hands[players])
        if cards.hasSplit(players):
            print("Split Hand", cards.splitHands[players])
        print(f"Your total is {cards.findValue(players)}.")
        if cards.hasSplit(players):
            print(f"Your split hand total is {cards.splitHandValue(players)}.")
        print("Dealer Hand (Stands on 17)", cards.hands[0])
        print(f"{cards.dealerStatus()}The dealer's total is {cards.findValue(0)}.")
        print("\nh) Hit\ns) Stand")
        if turn == 1:
            if cards.getSplittable(players):
                print("p) Split")
            #print("d) Double")
        action = input("\n=> ")
        match action:
            case 'p':
                if (turn == 1) and cards.getSplittable(players): cards.split(players)
            case 'd':
                if turn == 1:
                    cards.pullCard(0)
                    cards.pullCard(players)
                    print("Current Hand", cards.hands[players])
                    if cards.hasSplit(players):
                        print("Split Hand", cards.splitHands[players])
                    print(f"Your best total is {cards.findValue(players, True)}.")
                    while cards.findValue(0) < 17:
                        cards.pullCard(0)
                    if (cards.findValue(0) > cards.findValue(players)) and (cards.findValue(0) < 22):
                        print(f"The dealer ended with {cards.findValue(0)}. You lost...")
                    elif cards.findValue(0) == cards.findValue(players):
                        print(f"The dealer ended with {cards.findValue(0)}. You tied.")
                    else:
                        print(f"The dealer ended with {cards.findValue(0)}. You won!")
                    below = False
            case 'h':
                cards.pullCard(players)
                cards.pullCard(0)
            case 's':
                while cards.findValue(0) < 17:
                    cards.pullCard(0)
                if (cards.findValue(0) > cards.findValue(players, True)) and (cards.findValue(0) < 22):
                    print(f"The dealer ended with {cards.findValue(0)}. You lost...")
                elif cards.findValue(0) == cards.findValue(players, True):
                    print(f"The dealer ended with {cards.findValue(0)}. You tied.")
                else:
                    print(f"The dealer ended with {cards.findValue(0)}. You won!")
                below = False
        # Check for below 21
        if (cards.findValue(players) > 21) or (cards.splitHandValue(players) > 21):
            print("You're over 21!")
            below = False
            print("Current Hand", cards.hands[players])
            if cards.hasSplit(players):
                print("Split Hand", cards.splitHands[players])
            print(f"Your best total is {cards.findValue(players, True)}.")
            while cards.findValue(0) < 17:
                cards.pullCard(0)
            if cards.findValue(players, True) > 21:
                if (cards.findValue(0) > cards.findValue(players, True)) and (cards.findValue(0) < 22):
                    print(f"The dealer ended with {cards.findValue(0)}. You lost...")
                elif cards.findValue(0) <= 21:
                    print(f"The dealer ended with {cards.findValue(0)}. You lost...")
                else:
                    print(f"The dealer ended with {cards.findValue(0)}. You tied.")
            else:
                if (cards.findValue(0) > cards.findValue(players, True)) and (cards.findValue(0) < 22):
                    print(f"The dealer ended with {cards.findValue(0)}. You lost...")
                elif cards.findValue(0) == cards.findValue(players, True):
                    print(f"The dealer ended with {cards.findValue(0)}. You tied.")
                else:
                    print(f"The dealer ended with {cards.findValue(0)}. You won!")