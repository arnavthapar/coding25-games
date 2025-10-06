from random import randrange
from enum import Enum
class Effects(Enum):
    HALLU = 1
    CONFUSED = 2
    FROZEN = 3
    SLEEP = 4
    STONING = 5
    DECEIT = 6
    POISON = 7
class Affected():
    def subtract(effects:list, status, exercise):
        for i in range(len(effects)):
            if randrange(0, 3) == 2:
                effects[i][1] -= 1
                if effects[i][1] == 0:
                    effects.pop(effects.index([effects[i][0], 0]))
                    break
            if effects[i][0] == Effects.POISON and effects[i][1] == 0:
                status = 2
            match effects[i][0]:
                case Effects.POISON:
                    exercise['constitution'] -= randrange(0, 2)/10
                    exercise['wisdom'] -= randrange(3, 6)/100
                case Effects.HALLU:
                    exercise['intelligence'] -= randrange(0, 2)/100
                    exercise['wisdom'] -= randrange(0, 2)/100
                case Effects.CONFUSED:
                    exercise['wisdom'] -= randrange(0, 2)/100
                case Effects.FROZEN:
                    exercise['dexterity'] -= randrange(0, 2)/10
                case Effects.DECEIT:
                    exercise['dexterity'] -= randrange(0, 2)/10
                    exercise['constitution'] -= randrange(0, 2)/10
                    exercise['wisdom'] -= randrange(3, 6)/100
                    exercise['intelligence'] -= randrange(2, 6)/100
                case Effects.STONING:
                    exercise['dexterity'] -= randrange(0, 2)/10
                    exercise['constitution'] -= randrange(1, 2)/10
        return effects, status, exercise
    def addEffect(effects:list, effect, turns, printed:list):
        match effect:
            case Effects.HALLU:
                printed.append('You feel weird.')
            case Effects.CONFUSED:
                printed.append('You can\'t think straight.')
            case Effects.FROZEN:
                printed.append('You feel extremely cold, and you can\'t move your body.')
            case Effects.SLEEP:
                printed.append('You fell asleep!')
            case Effects.STONING:
                printed.append('You are turning to stone!')
            case Effects.DECEIT:
                printed.append('You feel doubtful, or so you think.')
            case Effects.POISON:
                printed.append('You feel sick...')
            case _:
                printed.append('You feel extremely confused.')
        effects.append([effect, turns])
        return effects, printed