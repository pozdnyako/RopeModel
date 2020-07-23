import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.animation as animation

import time

dt = 0.3

class Element:
    def __init__(self, pos = np.array([[0.0],[0.0]])):
        self.pos = pos
        self.vel = np.array([[0.0], [0.0]])

    def __repr__(self):
        return '%s %s, %s %s' % (self.pos[0,0], self.pos[1,0], self.vel[0,0], self.vel[1,0])

   
def dist(self, other):
    return ((self[0,0] - other[0,0]) ** 2 + (self[1,0] - other[1,0]) **2 ) ** 0.5
    
def force(self, other, length, rigidity):
    _dist = dist(self.pos, other.pos)

    if _dist > length:
        return (_dist - length) * rigidity / _dist * (other.pos - self.pos)
    else:
        return np.array([[0.0], [0.0]])
    
class Rope:
    def __init__(self, ammount, length, weight, rigidity, viscosity, pos0):
        self.elements = [Element(pos0[i]) for i in range(ammount)]
        self.ammount = ammount
        self.length = length
        self.weight = weight
        self.rigidity = rigidity
        self.viscosity = viscosity

    def update(self):
        for i in range(self.ammount):
            l = Element()
            r = Element()

            if i == 0:
                l = self.elements[self.ammount - 1]
            else:
                l = self.elements[i - 1]

            if i == self.ammount - 1:
                r = self.elements[0]
            else:
                r = self.elements[i + 1]

            cur = self.elements[i]

            F = np.add(force(cur, l, self.length, self.rigidity),
                       force(cur, r, self.length, self.rigidity))

            F = np.add(F, -self.viscosity * cur.vel)

            F = np.add(F, np.array([[0.0], [-5.0]]))

            cur.vel += F / self.weight * dt
            
            if i == 0 or i == self.ammount - 1:
                cur.vel = np.array([[0.0],[0.0]])

        for cur in self.elements:
            cur.pos += cur.vel * dt

def main():
    ammount = 20
    t = 0.0
    
    pos0 = []
    for i in range(ammount):
        pos0.append(np.array([[i * 10.0 / ammount],[0.0]]))

    rope = Rope(ammount,
                length=0.5,
                weight=1.0,
                rigidity=1.0,
                viscosity=1.0,
                pos0=pos0)
    
    ells = [Ellipse(xy = rope.elements[i].pos,
                   width = 0.1, height = 0.1,
                   angle = 0)
            for i in range(ammount)]
    
    fig, ax = plt.subplots()

    ax.set_xlim(0, 10)
    ax.set_ylim(-300, 5)

    for e in ells:
        ax.add_artist(e)

    plots = []
    for idx, el in enumerate(rope.elements):
        nextelem = rope.elements[(idx + 1) % len(rope.elements)]
        plots.append(plt.plot([el.pos[0,0], nextelem.pos[0,0]], [el.pos[1,0], nextelem.pos[1,0]]))

    def update(*args):
        nonlocal t
        nonlocal rope
        nonlocal plots

        for idx, curplot in enumerate(plots):
            el = rope.elements[idx]
            nextelem = rope.elements[(idx + 1) % len(rope.elements)]

            curplot[0].set_data([el.pos[0,0], nextelem.pos[0,0]], [el.pos[1,0], nextelem.pos[1,0]])

        rope.update()

        t += dt

    ani = animation.FuncAnimation(fig, update, interval=1)
    plt.show()

main()