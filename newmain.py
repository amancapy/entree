import random
import numpy as np
from time import perf_counter as ptime
# import pygame as pg


# mutate val by up to rate%, as long as it's between down and up
def mutate(val, down, up, rate=0.03):
    change_pcnt = val * rate * random.randint(1, 101) / 100
    val += random.choice([0.983, -0.953]) * change_pcnt

    while not down < val:
        change_pcnt = val * rate * random.randint(1, 101) / 100
        val = val + 0.983 * change_pcnt  # print("down", val, down)
    while not val < up:
        change_pcnt = val * rate * random.randint(1, 101) / 100
        val = val - 0.953 * change_pcnt  # print("up", val, up)
    return val


def sapling(p1, p2):
    """
    birth is a complicated process 🤓

    at face value the (somewhat impressive) list comprehensions look incomprehensible, but here's a very simple
    explanation:
    the sapling's stem is initialized with min() of the number of brances
    """

    def nearavg(val1, val2):
        splitratio = random.randint(450, 550) / 1000
        return val1 * splitratio + val2 * (1 - splitratio)

    sap = Tree(p1.stem.box_w, p1.stem.o, nearavg(p1.b_n_l, p2.b_n_l), nearavg(p1.b_n_r, p2.b_n_r))
    sap.color = (nearavg(p1.stem.color[0], p2.stem.color[0]),
                 nearavg(p1.stem.color[1], p2.stem.color[1]),
                 nearavg(p1.stem.color[2], p2.stem.color[2]))
    sap.mutrate = nearavg(p1.mutrate, p2.mutrate)

    sap.stem.width = nearavg(p1.stem.width, p2.stem.width)
    sap.stem.height = nearavg(p1.stem.height, p2.stem.height)
    sap.stem.color = sap.color

    sap.stem.b_l = [sap.stem.Branch(sap.stem, sap.stem.box_w, sap.stem.o,
                                    nearavg(p1.stem.b_l[i].angle, p2.stem.b_l[i].angle))
                    for i in range(int(min((len(p1.stem.b_l), len(p2.stem.b_l)))))]
    if int(sap.b_n_l - len(sap.stem.b_l)) != 0:
        sap.stem.b_l.extend([sap.stem.Branch(sap.stem, sap.stem.box_w, sap.stem.o,
                                             np.mean([sap.stem.b_l[i].angle
                                                      for _ in range(int(sap.b_n_l - len(sap.stem.b_l)))]))
                             for i in range(min(len(p1.stem.b_l), len(p2.stem.b_l)))])

    sap.mut()
    return sap


class Tree:
    class Stem:
        def __init__(self, parent, box_w, o, b_n_l, b_n_r):
            self.box_w = box_w
            self.o = o
            self.parent = parent

            self.width = box_w / o / 20
            self.height = box_w / o / 1.75
            self.color = parent.color
            self.mutrate = parent.mutrate

            self.b_l = [self.Branch(self, box_w, o, 60) for _ in range(int(b_n_l))]
            self.b_r = [self.Branch(self, box_w, o, 60) for _ in range(int(b_n_r))]

        def mut(self):
            self.width = mutate(self.width, 7, self.box_w / self.o / 10, self.mutrate)
            self.height = mutate(self.height, 10, self.box_w / self.o / 1.4, self.mutrate / 20)
            self.color = (mutate(self.color[0], 1, 250, self.mutrate),
                          mutate(self.color[1], 1, 255, self.mutrate),
                          mutate(self.color[2], 1, 255, self.mutrate))

            self.b_l = [l_branch.mut() for l_branch in self.b_l]
            self.b_r = [r_branch.mut() for r_branch in self.b_r]


        class Branch:
            def __init__(self, parent, box_w, o, angle):
                self.box_w = box_w
                self.o = o
                self.parent = parent

                self.base_h = box_w / o / 12
                self.width = box_w / o / 50
                self.length = box_w / o / 6
                self.angle = angle
                self.color = parent.color
                self.mutrate = parent.mutrate

            def mut(self):
                self.base_h = mutate(self.base_h, 10, self.parent.height / 2)
                self.width = mutate(self.width, 1, self.parent.width * 0.75, self.mutrate)
                self.length = mutate(self.length, 4, self.box_w / self.o / 3, self.mutrate)
                self.angle = mutate(self.angle, 45, 75, self.mutrate)
                self.color = (mutate(self.color[0], 1, 250, self.mutrate),
                              mutate(self.color[1], 1, 255, self.mutrate),
                              mutate(self.color[2], 1, 255, self.mutrate))
                return self

            def get(self):
                return self

    def __init__(self, box_w, o, b_n_l, b_n_r):
        self.b_n_l = b_n_l
        self.b_n_r = b_n_r
        self.color = (100, 100, 100)
        self.mutrate = 0.03

        self.stem = self.Stem(self, box_w, o, b_n_l, b_n_r)

    def mut(self):
        self.b_n_l = mutate(self.b_n_l, 1, 7, self.mutrate)
        self.b_n_r = mutate(self.b_n_r, 1, 7, self.mutrate)
        self.mutrate = mutate(self.mutrate, 0.01, 0.1, self.mutrate)

        self.stem.mut()


stime = ptime()
o = 5  # population size will be o * o
for _ in range(100):
    pool = [Tree(30, o, random.randint(30, 60) / 10, random.randint(30, 60) / 60) for _ in range(o * o)]
    pool = [sapling(random.choice(pool), random.choice(pool)) for _ in range(o * o)]


print((ptime() - stime) / 100)
