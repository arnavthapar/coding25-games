import matplotlib.pyplot as plt
import numpy as np
from dictlist import di

l = {
    2:3,
    3:6,
    4:7,
    5:7,
    6:7,
    7:7,
    8:4,
    9:7,
    10:4,
    11:0,
    12:0,
    13:0,
    14:1,
    15:5,
}
w = {
    2:6,
    3:3,
    4:2,
    5:2,
    6:2,
    7:2,
    8:5,
    9:2,
    10:5,
    11:9,
    12:9,
    13:9,
    14:9,
    15:4,
    }

y = []
x = []
for i in tuple(l.keys()):
    y.append(i)
    x.append(l[i])
plt.subplot(2, 2, 1)
xLpoints = np.array(y)
yLpoints = np.array(x)
plt.title("Wins and losses by character count") # Loc moves the title.
plt.suptitle("Hangman")
plt.grid(ls = '--', lw = 2)
plt.xlabel("Letters")
plt.ylabel("Wins and Losses")
plt.plot(xLpoints, yLpoints, 'o-r', lw=1.5,)
y = []
x = []
for i in tuple(w.keys()):
    y.append(i)
    x.append(w[i])
xWpoints = np.array(y)
yWpoints = np.array(x)
plt.plot(xWpoints, yWpoints, 'o-g', lw=1.5,)
#plt.legend(title = "Legend") # Adds a legend.
lengths = {}
for i in di:
    if i[0] not in tuple(lengths.keys()):
        lengths[i[0]] = 1
    else:
        lengths[i[0]] += 1
plt.subplot(1, 2, 2)
values = []
names = []
plt.title("First Letters")
for i in sorted(tuple(lengths.keys())):
    names.append(i)
    values.append(lengths[i])
plt.pie(values, labels=names)


lengths = {}
for i in di:
    if len(i) not in tuple(lengths.keys()):
        lengths[len(i)] = 1
    else:
        lengths[len(i)] += 1
plt.subplot(2, 2, 3)
values = []
names = []
plt.title("Length of words")
for i in sorted(tuple(lengths.keys())):
    names.append(i)
    values.append(lengths[i])
plt.bar(height=values, x=names)
plt.show()