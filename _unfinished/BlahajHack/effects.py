from random import randrange
from enum import Enum
class Effects(Enum):
    HALLU = 1
    CONFUSE = 2
    FROZEN = 3
    SLEEP = 4
    STONING = 5
    #HALLU = 6
    POISON = 7
class Affected():
    def __init__(self):
        pass
    def subtract(self, effects:list=[], status=1, exercise=[]):
        for i in range(len(effects)):
            if randrange(0, 3) == 2:
                effects[i][1] -= 1
                if effects[i][1] == 0:
                    effects.remove(i)
            if effects[i][0] == Effects.POISON and effects[i][0] == 0:
                status = 2
            match effects[i][0]:
                case Effects.POISON:
                    exercise['constitution'] -= randrange(0, 2)/10
                    exercise['wisdom'] -= randrange(3, 6)/100
                case Effects.HALLU:
                    exercise['intelligence'] -= randrange(0, 2)/100
                    exercise['wisdom'] -= randrange(0, 2)/100
                case Effects.CONFUSE:
                    exercise['wisdom'] -= randrange(0, 2)/100
                case Effects.FROZEN:
                    exercise['dexterity'] -= randrange(0, 2)/10
                case Effects.STONING:
                    exercise['dexterity'] -= randrange(0, 2)/10
            return effects, status, exercise
        