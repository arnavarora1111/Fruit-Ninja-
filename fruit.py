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

#Fruit Class which inititalizes the fruits used in the game
#Superclass
class Fruit(object):
    def __init__(self,cx,cy):
        self.cx = cx
        self.cy = cy
        self.r = 20
        #target Y values for when the fruit should begin coming down
        self.targetY = random.randint(0,100)
        #x and y speeds of the fruit when thrown 
        self.speedX = random.choice([-2,-1,1,2,3,-3])
        self.speedY = 75
        #direction of the fruit when it is randomly thrown up on the screen
        self.direction = 1