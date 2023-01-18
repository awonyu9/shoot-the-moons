# projectile.py
#   Defining a new Projectile class
#   by Alexandra Wonyu

from math import *

class Projectile:
    """Insert a description of what the
    class Projectile does."""
    def __init__(self, angle, velocity, height):
        self.xpos = 0.0
        self.ypos = height
        theta = radians(angle)
        self.xvel = velocity * cos(theta)
        self.yvel = velocity * sin(theta)

    def update(self, time):
        "Here's another docstring for you."
        self.xpos = self.xpos + time * self.xvel
        yvel1 = self.yvel - time * 9.8
        self.ypos = self.ypos + time * (self.yvel + yvel1) / 2.0
        self.yvel = yvel1

    def getX(self):
        return self.xpos

    def getY(self):
        return self.ypos
