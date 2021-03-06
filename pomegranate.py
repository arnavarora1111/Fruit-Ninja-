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
from fruit import Fruit

#Pomegranate class for creating pink pomegranates
#subclass of Fruit
class Pomegranate(Fruit):
    def __init__(self,cx,cy):
        super().__init__(cx,cy)
        self.r = 30 
        self.fill = "pink"
    
    def __eq__(self,other):
        return (isinstance(other,Pomegranate) and ((self.cx == other.cx) and
                            self.cy == other.cy))

    def draw(self,canvas):
        canvas.create_oval(self.cx -  self.r, self.cy - self.r,  
                            self.cx + self.r, self.cy + self.r,
                            fill=self.fill)