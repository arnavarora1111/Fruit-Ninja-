#Arnav Arora
#arnavaro
#December 5,2020
#Section: D0

import pygame
from pygame import mixer
from cmu_112_graphics import *
from dataclasses import make_dataclass
from tkinter import *
import math
import random
import time

#Bomb class for creating bombs
#score either decreases if user hits the bomb or the game is over
#(depends on game mode)
class Bomb(object):
    def __init__(self,cx,cy):
        self.cx = cx
        self.cy = cy
        self.r = 40
        self.fill = "black"
        self.targetY = random.randint(0,100)
        self.speedX = random.choice([-2,-1,1,2])
        self.speedY = 70
        self.direction = 1
    
    def __eq__(self,other):
        return (isinstance(other,Bomb) and ((self.cx == other.cx) and
                            self.cy == other.cy))
    
    def draw(self,canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r,  
                            self.cx + self.r, self.cy + self.r,
                            fill=self.fill)