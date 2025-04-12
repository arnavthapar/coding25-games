# ([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
# ((True), ['095^2a'], ['095^2a'], ['095^2a'], ['095^2a'], ['095^2a'],['095^2a'],['095^2a'],['095^2a'],['095^2a'],['095^2a'],['095^2a'],['095^2a'],['095^2a'],['095^2a'])
"""
17 length
14 height

"""
from random import randrange
p = input("preset: ")
b = input("back: ")
if p == "0":
    x = [(b)]
    for i in range(17):
        x.append([])
        for l in range(14):
            r = randrange(0, 10)
            if r == 0: x[i+1].append('056^2')
            if r == 1: x[i+1].append('057^2')
            if r == 2: x[i+1].append('058^2a')
            if r == 3: x[i+1].append('059^2a')
            else: x[i+1].append(2)
print(x)