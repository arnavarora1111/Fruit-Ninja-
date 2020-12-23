#Arnav Arora
#arnavaro
#December 9 2020
#Section: D0

from cmu_112_graphics import *
from dataclasses import make_dataclass
from tkinter import *
import math
import random
import time
from os import path

#imports for the fruit and bomb classes
from fruit import Fruit
from apple import Apple
from banana import Banana
from pomegranate import Pomegranate
from coconut import Coconut
from watermelon import Watermelon
from specialfruit1 import SpecialFruit1
from specialfruit2 import SpecialFruit2
from bomb import Bomb

#Source for all animations and graphics framework:
#cmu_112_graphics
#https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
#https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
#https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html


#Main class that runs the game
#Source for background image (self.image1): https://images.wikia.nocookie.net/__cb48/fruitninja/images/5/50/Wiki-background
class Main(App):
    def appStarted(self):
        #used for keeping track of the time left in the game
        self.timePassed = 0
        self.timePassed2 = 0

        #keeps track of the score
        self.counter = 0
        url = 'https://images.wikia.nocookie.net/__cb48/fruitninja/images/5/50/Wiki-background'
        self.image1 = self.loadImage(url)
        self.gameOver = False
        self.isPaused = False

        #initial values for changing the level of the game
        self.level = 1
        self.levelChange = True
        self.currentLevel = 0

        #used for probability of fruit occuring
        self.weight = []

        #used for start screen
        self.gameMode = None
        self.waitingForMousePress = False
        self.difficulty = None
        self.timerDelay = 50

        #avoids delay when the mouse is pressed on the screen
        #from cmu_112_graphics.py
        self.mouseMovedDelay = 1

        #initializes game mode buttons
        self.classicCx = self.width//10
        self.arcadeCx = self.width//2
        self.zenCx = self.width - 100
        self.cy = self.height - 200
        self.r = 70
        self.menuCx = self.width//14
        self.menuCy = self.height - 80
        self.saveCx = self.width//14
        self.saveCy = self.height - 240

        #initializes save and menu options
        self.save = None
        self.menu = False
        self.defaultLives = 3

        #allows an absolute path
        #used eventually for saving the current user data in a local file
        self.dir = path.dirname(__file__)

        #used for advancing to the next level
        self.nextLevelKey = False

        #used for mouse dragging/slicing
        self.prevX = None
        self.prevY = None
        self.currX = None
        self.currY = None
        self.accuracy = 0

        #keeps track of how many times user misses the target
        self.misses = 0
        #keeps track of how many times user hits the target
        self.hits = 0

        self.loadPrevData = False
        Main.reset(self)

        #loads previous data from the user
        Main.loadData(self)
        
        #keep track of user statistics
        self.totalFruitsHit = 0
        self.totalFruitsThrown = 0
        self.totalFruitsMissed = 0
        self.totalBombsHit = 0
        self.levelFruitsThrown = 0
        
        #distance between the intersections of the fruits and bombs
        self.bombIntersectionDistance = 5
        self.fruitIntersectionDistance = 20
        
    #reset function for certain values 
    #occurs when a next level is reached or user clicks on menu button
    def reset(self):
        self.time = 15
        self.timer = self.time
        self.lives = 3
        self.totalLives = 0

        #clears the screen after each level
        self.fruits = []
    
    #if user hits a bomb in zen mode the screen will clear
    def reset2(self):
        self.fruits = []

    #method picks a random fruit from all the possible options of fruits
    def randomFruit(self,x,y):
        #list for keeping track of the prbabilites of fruits and bombs
        weight = []
        banana = Banana(x,y)
        apple = Apple(x,y)
        pomegranate = Pomegranate(x,y)
        bomb = Bomb(x,y)
        coconut = Coconut(x,y)
        watermelon = Watermelon(x,y)
        specialFruit1 = SpecialFruit1(x,y)
        specialFruit2 = SpecialFruit2(x,y)
        allFruits = [banana,apple,pomegranate,coconut,watermelon,bomb]
        allFruitsZen = [banana,apple,pomegranate,coconut,watermelon,specialFruit1,specialFruit2,bomb]

        #weights add probability to a fruit or bomb
        #weight for bomb will be less than weight for fruit since we want
        #bombs to appear less often
        weight = Main.fruitAndBombProbability(self)
        num = random.randint(1,6)
        if(self.gameMode == "zen"):
            randomFruitSelection = random.choices(allFruitsZen, weights=weight,k=1)[0]
        else:
            randomFruitSelection = random.choices(allFruits, weights=weight,k=1)[0]
        return randomFruitSelection
    
    #algorithim for determining the probability of when a fruit or bomb 
    #should be thrown up
    #depends on the timer and accuracy of the user
    #if accuracy is high, make bombs appear more often
    #if accuracy is lower, make fruits appear more often
    #Changes current level difficulty based on how user is playing right now
    def fruitAndBombProbability(self):
        if(self.timer < 20 and self.accuracy > 80):
            bomb = random.randint(30,40)
            if(self.gameMode == "zen"):
                self.weight = [10,10,10,10,10,1,1,bomb]
            else:
                self.weight = [10,10,10,10,10,bomb]
        elif(self.timer < 20 and self.accuracy > 60):
            bomb = random.randint(20,30)
            if(self.gameMode == "zen"):
                self.weight = [15,10,15,10,10,3,3,bomb]
            else:
                self.weight = [15,10,15,10,10,bomb]
        elif(self.timer < 20 and self.accuracy > 40):
            bomb = random.randint(10,20)
            if(self.gameMode == "zen"):
                self.weight = [15,15,15,15,10,5,5,bomb]
            else:
                self.weight = [15,15,15,15,10,bomb]
        elif(self.timer < 20 and self.accuracy > 20):
            bomb = random.randint(5,10)
            if(self.gameMode == "zen"):
                self.weight = [20,20,10,10,20,6,6,bomb]
            else:
                self.weight = [20,20,10,10,20,bomb]
        elif(self.timer < 20 and self.accuracy >= 0):
            bomb = random.randint(1,5)
            if(self.gameMode == "zen"):
                self.weight = [10,20,30,20,10,8,8,bomb]
            else:
                self.weight = [10,20,30,20,10,bomb]
        return self.weight

    #checks to see which fruit the user clicked on
    @staticmethod
    def pointIsInFruit(x,y,fruit):
        return (((fruit.cx - x)**2 + (fruit.cy - y)**2)**0.5 <= fruit.r)
    
    #method sets prevX,prevY,currX,currY back to none after mouse is no longer 
    #dragging on the screen
    def mouseReleased(self, event):
        if(self.gameOver):
            return
        self.prevX,self.prevY = None, None
        self.currX,self.currY = None, None
    
    #used for slicing the fruit
    def mouseDragged(self, event):
        if(self.gameOver and (not self.levelChange)):
            return
        #keep track of current and previous x and y values of mouse
        if self.prevX is not None and self.prevY is not None:
            self.prevX, self.prevY = self.currX, self.currY
            self.currX, self.currY = event.x, event.y
        else:
            self.prevX, self.prevY = event.x, event.y

        #checks to see if the mouse drag was in the path of the fruit
        #increments and decrements score based on fruit or bomb
        for fruits in self.fruits:
            for i,fruit in enumerate(fruits):
                if((self.totalFruitsThrown > 0)):
                    self.accuracy = 100*(self.totalFruitsHit/self.totalFruitsThrown)

                if(Main.pointIsInFruit(event.x,event.y,fruit)):
                    #if user slashes a bomb, then the game is over for classic mode
                    if(isinstance(fruit,Bomb) and (self.gameMode == "classic")):
                        self.gameOver = True
                        self.totalBombsHit = 1

                    #for arcade and zen mode the score decreases if user hits a bomb
                    elif((isinstance(fruit,Bomb)) and (self.gameMode == "arcade")
                                and (self.counter > 10)):
                        self.counter -= 10
                        self.totalBombsHit += 1

                    elif((isinstance(fruit,Bomb)) and (self.gameMode == "zen")
                                and (self.counter > 10)):
                        self.counter -= 30
                        self.totalBombsHit += 1
                        #clears the screen of all fruits and bombs
                        Main.reset2(self)
                    #increment counter if the user hits a fruit
                    else:
                        if(isinstance(fruit,SpecialFruit1) or isinstance(fruit,SpecialFruit2)):
                            self.counter += 50
                        else:
                            self.counter += 10  
                    #pop the fruit if the user draggs the mouse through the fruit
                    fruits.pop(i)

                    #increments number of hits of fruits by 1
                    if(not isinstance(fruit,Bomb)):
                        self.totalFruitsHit += 1

    '''
    Based on the number of bombs hit and the accuracy of the user, the game
    will speed up or slow down. Takes the accumlated accuracy and bombs hit
    These functions change the other level's difficulty based on the user's 
    past performance 
    '''
    #difficulty settings of level 1 based on user performance
    def level1(self):
        self.timerDelay = 40
        if(((self.totalBombsHit < 2) and (self.timer < 20)) or (self.accuracy > 80)):
            self.timerDelay = 25

    #difficulty settings of level 2 based on user performance
    def level2(self):
        self.timerDelay = 30
        if(((self.totalBombsHit < 3) and (self.timer < 20)) or (self.accuracy > 70)):
            self.timerDelay = 20
    
    #difficulty settings of level 3 based on user performance
    def level3(self):
        self.timerDelay = 15
        if(((self.totalBombsHit < 4) and (self.timer < 20)) or (self.accuracy > 60)):
            self.timerDelay = 10
    
    #difficulty settings of level 4 based on user performance
    def level4(self):
        self.timerDelay = 7
        if(((self.totalBombsHit < 4) and (self.timer < 20)) or (self.accuracy > 50)):
            self.timerDelay = 3
    
    #function chooses fruits from the randomFruit function
    #throws more fruits depending on accuracy of user and number of bombs hit
    #and on the level the user is currently at 
    #overlap of bombs and fruit increase to make game more difficult
    def chooseFruits(self,x,y):
        newFruit = Main.randomFruit(self,x,y)
        newFruit2 = Main.randomFruit(self,x,y)
        newFruit3 = Main.randomFruit(self,x,y)
        total1 = [newFruit]
        total2 = [newFruit,newFruit2]
        total3 = [newFruit,newFruit2,newFruit3]
        random1 = (total1,total2)
        random2 = (total2,total3)
        if(self.currentLevel == 1):
            totalFruits = total1
            if((self.accuracy > 80) or (self.totalBombsHit < 2)):
                totalFruits = random.choice(random1)
                self.bombIntersectionDistance = 5
                self.fruitIntersectionDistance = 25
        elif(self.currentLevel == 2):
            totalFruits = total1
            if((self.accuracy > 70) or (self.totalBombsHit < 3)):
                totalFruits = random.choice(random1)
                self.bombIntersectionDistance = 10
                self.fruitIntersectionDistance = 20
        elif(self.currentLevel == 3):
            totalFruits = total2
            if((self.accuracy > 60) or (self.totalBombsHit < 5)):
                totalFruits = random.choice(random2)
                self.bombIntersectionDistance = 15
                self.fruitIntersectionDistance = 15
        elif(self.currentLevel == 4):
            totalFruits = random.choice(random2)
            if((self.accuracy > 50) or (self.totalBombsHit < 6)):
                totalFruits = total3
                self.bombIntersectionDistance = 20
                self.fruitIntersectionDistance = 10
        return totalFruits
    
    #used to calculate the area between the two circles that intersect
    #determines overlap between the fruits and bombs
    #source for formula used: https://diego.assencio.com/?index=8d6ca3d82151bad815f78addf9b5c1c6
    def circlesIntersectArea(self):
        for fruits in self.fruits:
            for fruit in range(len(fruits) - 1):
                r1 = (fruits[fruit].r) ** 2
                r2 = (fruits[fruit + 1].r) ** 2
                d = (fruits[fruit].r + fruits[fruit + 1].r)
                d1 = (r1 - r2 + (d**2))/(2*d)
                d2 = (r2 - r1 + (d**2))/(2*d)
                a1 = (r1 * math.acos(d1/r1)) - (d1 * ((r1-(d1**2))**0.5))
                a2 = (r2 * math.acos(d2/r2)) - (d2 * ((r2-(d2**2))**0.5))
                #total intersection area between the two fruits or bombs
                total = a1 + a2
                if(isinstance(fruits[fruit],Bomb)):
                    if(total > self.bombIntersectionDistance):
                        fruits[fruit].cx += (2 * fruits[fruit].speedX)
                        fruits[fruit].cy += (0.1 * fruits[fruit].speedY)
                else:
                    if(total > self.fruitIntersectionDistance):
                        fruits[fruit].cx += (2 * fruits[fruit].speedX)
                        fruits[fruit].cy += (0.1 * fruits[fruit].speedY)

    #main function for the classic mode and determines the path of the fruit
    #decides when game is over or when the level changes
    #includes lives instead of a timer
    def classicModeRandomFruit(self):
        #game is over if lives are 0 and when level 4 is reached
        if((self.lives <= 0) or (not self.levelChange)):
            self.gameOver = True

        if(not self.nextLevelKey):
            if(self.lives > 0):
                if(self.level == 4 or self.currentLevel == 4):
                    self.levelChange = False
                self.timePassed += 1
                if(self.timePassed % 10 == 0 and self.waitingForMousePress == True):
                    #generate random starting x coordinate on the screen
                    #keep it from the edges of the screen
                    x = random.randint(200,900)
                    #start y at the bottom so the fruits rise up
                    y = self.height - 1
                    randomFruits = Main.chooseFruits(self,x,y)
                    self.fruits.append(randomFruits)
                    
                    #each level ends after 15 fruits are thrown
                    for i in randomFruits:
                        if(not isinstance(i,Bomb)):
                            self.totalFruitsThrown += 1
                            self.levelFruitsThrown += 1
                            if(self.levelFruitsThrown > 15 and (self.currentLevel != 4)):
                                Main.reset(self)
                                self.level += 1
                                self.currentLevel += 1
                                self.nextLevelKey = True 
                                self.levelFruitsThrown = 0 
                            elif(self.levelFruitsThrown > 15 and (self.currentLevel == 4)):
                                self.gameOver == True 

                #speed of moving fruit on screen
                for fruits in self.fruits:
                    for fruit in fruits:
                        fruit.cx += fruit.speedX
                        fruit.cy -= fruit.speedY    
                        fruit.speedY -= (5 * fruit.direction)
                        
                        #fruit needs to start coming down after it reaches targetY value 
                        if fruit.cy < fruit.targetY:
                            fruit.direction = -1 * fruit.direction
                    
                        #decrement number of lives if fruit reaches the 
                        #bottom of the screen without being popped 
                        y = self.height - 1
                        if(not isinstance(fruit,Bomb)):
                            if(fruit.cy > y):
                                self.lives -= 1

                Main.circlesIntersectArea(self)

    #main function for the arcade and zen mode
    #uses a timer instead of lives
    def arcadeAndZenModeRandomFruit(self):
        if(not self.nextLevelKey):
            self.timePassed2 += 1
            normalTimeDelay = 100
            time = normalTimeDelay//self.timerDelay
            total = (10*time)/2
            if(self.timePassed2 % 20 == 0):
                self.timer -= 1

            if(self.timer != 0):
                if(self.level == 4 or self.currentLevel == 4):
                    self.levelChange = False
                self.timePassed += 1
                if(self.timePassed % 10 == 0 and self.waitingForMousePress == True):
                    #generate random starting x coordinate on the screen
                    #keep it from the edges of the screen
                    x = random.randint(200,900)
                    #start y at the bottom so the fruits rise up
                    y = self.height
                    randomFruits = Main.chooseFruits(self,x,y)
                    self.fruits.append(randomFruits)
                    #adds 1 to the counter of total fruits thrown
                    for i in randomFruits:
                        if(not isinstance(i,Bomb)):
                            self.totalFruitsThrown += 1
                #speed of moving fruit on screen
                for fruits in self.fruits:
                    for fruit in fruits:
                        fruit.cx += fruit.speedX
                        fruit.cy -= fruit.speedY    
                        fruit.speedY -= (5 * fruit.direction)
                        
                        #fruit needs to start coming down after it reaches targetY value 
                        if fruit.cy < fruit.targetY:
                            fruit.direction = -1 * fruit.direction

                Main.circlesIntersectArea(self)

            #game is over if the timer is 0 and when level 4 is reached
            elif((self.timer == 0) and (not self.levelChange)):
                        self.gameOver = True

            #goes to the next level
            else:
                Main.reset(self)
                self.level += 1
                self.currentLevel += 1
                self.nextLevelKey = True

    #appends a random fruit to the fruit list after each call to timer fired       
    def timerFired(self):
        if(self.gameOver or self.isPaused):
            return

        #sets up the gameplay for each specific level
        if(self.currentLevel == 1):
                Main.level1(self)
        if(self.currentLevel == 2):
                Main.level2(self)
        if(self.currentLevel == 3):
                Main.level3(self)
        if(self.currentLevel == 4):
                Main.level4(self)

        if(self.gameMode=="classic"):
            Main.classicModeRandomFruit(self)

        if((self.gameMode=="arcade") or (self.gameMode=="zen")):
            Main.arcadeAndZenModeRandomFruit(self)

    #user has to press a key to move on to the next level
    def keyPressed(self,event):
        if(self.nextLevelKey):
            self.nextLevelKey = not self.nextLevelKey 
        
        #asks the user to see if this is the first time playing the game
        if(event.key == "1" and self.gameMode == None):
            Main.appStarted(self)
            Main.loadStartOfGame(self)

        #pressing 2 reloads previous values from the game before
        if(event.key == "2" and self.gameMode == None):
            Main.loadData(self)
    
    #when the user first plays the game the values should be default values
    #sources used to learn how to load and save the data locally:
    #https://cmdlinetips.com/2016/01/opening-a-file-in-python-using-with-statement/
    #https://www.w3schools.com/python/ref_file_write.asp
    def loadStartOfGame(self):
        with open(path.join(self.dir, "Score.txt"), 'w') as f:
            f.write("0")
            f.write("\n")
            f.write("0")
            f.write("\n")
            f.write(str(self.time))
            f.write("\n")
            f.write("None")
            f.write("\n")
            f.write("0")
            f.write("\n")
            f.write("0")
            f.write("\n")
            f.write("0")
            f.write("\n")
            f.write(str(self.defaultLives))
            f.write("\n")
            self.gameMode = None

    #saves user data in a local file
    #sources used to learn how to load and save the data locally:
    #https://cmdlinetips.com/2016/01/opening-a-file-in-python-using-with-statement/
    #https://www.w3schools.com/python/ref_file_write.asp
    def saveData(self):
        self.save = True
        with open(path.join(self.dir, "Score.txt"), 'w') as f:
            f.write(str(self.counter))
            f.write("\n")
            f.write(str(self.currentLevel))
            f.write("\n")
            f.write(str(self.timer))
            f.write("\n")
            f.write(str(self.gameMode))
            f.write("\n")
            f.write(str(self.totalFruitsThrown))
            f.write("\n")
            f.write(str(self.totalFruitsHit))
            f.write("\n")
            f.write(str(self.totalBombsHit))
            f.write("\n")
            f.write(str(self.lives))

    #loads the data from the previous game the user was playing
    #sources used to learn how to load and save the data locally:
    #https://cmdlinetips.com/2016/01/opening-a-file-in-python-using-with-statement/
    #https://www.w3schools.com/python/ref_file_write.asp
    def loadData(self):
        currData = open("Score.txt","r")
        self.counter = int(currData.readline())
        self.currentLevel = int(currData.readline())
        self.timer = int(currData.readline())
        mode = currData.readline()
        self.totalFruitsThrown = int(currData.readline())
        self.totalFruitsHit = int(currData.readline())
        self.totalBombsHit = int(currData.readline())
        self.lives = int(currData.readline())
        self.gameMode = None

    #check to see if user clicked in classic mode circle
    def pointIsInCircle(self,x,y):
        return (((self.classicCx - x)**2 + (self.cy- y)**2)**0.5 <= self.r) 
    
    #check to see if user clicked in arcade mode circle
    def pointIsInCircle2(self,x,y):
        return (((self.arcadeCx - x)**2 + (self.cy- y)**2)**0.5 <= self.r)  
    
    #check to see if user clicked in zen mode circle
    def pointIsInCircle3(self,x,y):
        return (((self.zenCx - x)**2 + (self.cy- y)**2)**0.5 <= self.r) 

    #check to see if user clicked in menu circle
    def pointIsInCircle4(self,x,y):
        return (((self.menuCx - x)**2 + (self.menuCy- y)**2)**0.5 <= self.r) 

    #check to see if user clicked in save circle
    def pointIsInCircle5(self,x,y):
        return (((self.saveCx - x)**2 + (self.saveCy- y)**2)**0.5 <= self.r)   


    #draws the line to see where the user is slicing the fruit
    def mouseDrag(self,canvas):
        if(self.gameOver):
            return
        if (self.prevX is not None and self.prevY is not None 
                    and self.currX is not None and self.currY is not None):
            canvas.create_line(self.prevX, self.prevY, self.currX, self.currY, 
                                fill ="red",width=5)
    
    #displays user accuracy of hitting the fruits in the middle of screen
    def userAccuracy(self,canvas):
        accuracy = self.accuracy
        canvas.create_text(self.width//2-50,50,
                        text=("Accuracy: %0.1f" % accuracy),
                        font='Arial 40 bold',fill="white")
    
    #displays the probability of a bomb being thrown up 
    def displayBombProbability(self,canvas):
        #takes the last item from the weight list to compute the percentage
        if(len(self.weight) > 0):
            probability = self.weight[-1]
        else:
            probability = 0
        canvas.create_text(self.width//2-50,110,
                        text=f'Bomb Probability: {probability} %',
                        font='Arial 20 bold',fill="white")

    #displays the amount of time left on the screen
    #for arcade and zen mode only
    def timeLeft(self,canvas):
        canvas.create_text(self.width-150,50,
                        text=f'Time Left: {self.timer}',font='Arial 40 bold',
                        fill="white")

    #displays the amount of lives left on the screen
    #for classic mode only
    def livesRemaining(self,canvas):
        canvas.create_text(self.width-125,50,
                        text=f'Lives: {self.lives}',font='Arial 40 bold',
                        fill="white")

    #draws the screen given the image
    def drawScreen(self,canvas):
        canvas.create_image(600, 400, image=ImageTk.PhotoImage(self.image1))
        for fruits in self.fruits:
            for fruit in fruits:
                fruit.draw(canvas)
    
    #displays the score and updates based on the amount of fruits hit
    def drawScore(self,canvas):
        canvas.create_text(120,50,text=f'Score: {self.counter}',
                            font='Arial 40 bold',fill="white")
    
    #displays the level in the bottom right of the screen
    def drawLevel(self,canvas):
        canvas.create_text(self.width - 100,self.height - 50,
                        text=f'Level: {self.level}',font='Arial 40 bold',
                        fill="white")

    #check to see which button the user clicked in
    def mousePressed(self,event):
        if(Main.pointIsInCircle(self,event.x,event.y) and (self.gameMode==None)):
            self.gameMode = "classic"
            self.isPaused = False
            self.currentLevel = 1
            self.waitingForMousePress = not self.waitingForMousePress

        elif(Main.pointIsInCircle2(self,event.x,event.y) and (self.gameMode == None)):
            self.gameMode = "arcade"
            self.isPaused = False
            self.currentLevel = 1
            self.waitingForMousePress = not self.waitingForMousePress

        elif(Main.pointIsInCircle3(self,event.x,event.y) and (self.gameMode == None)):
            self.gameMode = "zen"
            self.isPaused = False
            self.currentLevel = 1
            self.waitingForMousePress = not self.waitingForMousePress
        
        elif(Main.pointIsInCircle4(self,event.x,event.y) and ((self.gameMode == "classic")
                or (self.gameMode=="arcade") or (self.gameMode=="zen"))):
            self.menu = not self.menu
            self.gameMode = None
            self.waitingForMousePress = not self.waitingForMousePress
            Main.loadStartOfGame(self)
            Main.appStarted(self)
        
        elif(Main.pointIsInCircle5(self,event.x,event.y) and ((self.gameMode == "classic")
                or (self.gameMode=="arcade") or (self.gameMode=="zen"))):
            Main.saveData(self)
            self.gameMode = None
            self.waitingForMousePress = not self.waitingForMousePress
            self.isPaused = not self.isPaused
    
    #menu button
    def menuButton(self,canvas):
        color = "darkblue"
        canvas.create_oval(self.menuCx-self.r,self.menuCy-self.r,
                            self.menuCx+self.r,self.menuCy+self.r,fill=color)
        canvas.create_text(self.menuCx,self.menuCy,text="Menu",
                                font = "Arial 30 bold", fill = "white")
    
    #save button
    def saveButton(self,canvas):
        color = "black"
        canvas.create_oval(self.saveCx-self.r,self.saveCy-self.r,
                            self.saveCx+self.r,self.saveCy+self.r,fill=color)
        canvas.create_text(self.saveCx,self.saveCy,text="Save",
                                font = "Arial 30 bold", fill = "white")

    #classic mode button
    def classicMode(self,canvas):
        color = "green"
        canvas.create_oval(self.classicCx-self.r,self.cy-self.r,
                            self.classicCx+self.r,self.cy+self.r,fill=color)
        canvas.create_text(self.classicCx,self.cy,text="Classic",
                                font = "Arial 30 bold", fill = "white")
    
    #arcade mode button
    def arcadeMode(self,canvas):
        color = "red"
        canvas.create_oval(self.arcadeCx-self.r,self.cy-self.r,
                            self.arcadeCx+self.r,self.cy+self.r,fill=color)
        canvas.create_text(self.arcadeCx,self.cy,text="Arcade",
                                font = "Arial 30 bold", fill = "white")
    
    #zen mode button
    def zenMode(self,canvas):
        color = "purple"
        canvas.create_oval(self.zenCx-self.r,self.cy-self.r,
                            self.zenCx+self.r,self.cy+self.r,fill=color)
        canvas.create_text(self.zenCx,self.cy,text="Zen",
                                font = "Arial 30 bold", fill = "white")

    #displays black rectange in the start screen
    #user has choice to press 1 or 2
    #either restarts the game or loads previous values
    def playedBefore(self,canvas):
        color = "black"

        canvas.create_rectangle(self.width//2 - 300,self.height//2 - 100,
                            self.width//2 + 300,self.height//2 + 100,fill=color)

        canvas.create_text(self.width//2 ,self.height//2 - 60,
        text="Press 1 if first time playing this game or mode", font = 'Arial 20 bold',
            fill = "white")

        canvas.create_text(self.width//2 ,self.height//2 ,
        text="Press 2 to reload previous data values", font = 'Arial 20 bold',
            fill = "white")
        
        canvas.create_text(self.width//2 ,self.height//2 + 60,
        text="Click inside the circles below to choose the game mode", font = 'Arial 20 bold',
            fill = "white")
    
    #start screen of the game
    def startScreen(self,canvas):
        canvas.create_image(600, 400, image=ImageTk.PhotoImage(self.image1))
        
        canvas.create_text(self.width//2-188,self.height//4-100,
        text = "F", font = 'Arial 150 bold',fill = "purple")

        canvas.create_text(self.width//2-78,self.height//4-100,
        text = "R", font = 'Arial 150 bold',fill = "red")

        canvas.create_text(self.width//2 + 28,self.height//4-100,
        text = "U", font = 'Arial 150 bold',fill = "yellow")

        canvas.create_text(self.width//2+108,self.height//4-100,
        text = "I", font = 'Arial 150 bold',fill = "orange")

        canvas.create_text(self.width//2+188,self.height//4-100,
        text = "T", font = 'Arial 150 bold',fill = "green")

        canvas.create_text(self.width//2,self.height//4 + 30,
        text="NINJA", font = 'Arial 100 bold',fill = "white")

        Main.playedBefore(self,canvas)
        Main.classicMode(self,canvas)
        Main.arcadeMode(self,canvas)
        Main.zenMode(self,canvas)

    #classic Mode and difficulty includes all levels
    def classicModeLevel(self,canvas):
        Main.drawScreen(self,canvas)
        Main.drawScore(self,canvas)
        Main.drawLevel(self,canvas)
        Main.livesRemaining(self,canvas)
        Main.userAccuracy(self,canvas)
        Main.displayBombProbability(self,canvas)
        Main.mouseDrag(self,canvas)
        Main.menuButton(self,canvas)
        Main.saveButton(self,canvas)
    
    #arcade Mode and difficulty includes all levels
    def arcadeModeLevel(self,canvas):
        Main.drawScreen(self,canvas)
        Main.drawScore(self,canvas)
        Main.drawLevel(self,canvas)
        Main.timeLeft(self,canvas)
        Main.userAccuracy(self,canvas)
        Main.displayBombProbability(self,canvas)
        Main.mouseDrag(self,canvas)
        Main.menuButton(self,canvas)
        Main.saveButton(self,canvas)
 
    #zen Mode and difficulty includes all levels
    def zenModeLevel(self,canvas):
        Main.drawScreen(self,canvas)
        Main.drawScore(self,canvas)
        Main.drawLevel(self,canvas)
        Main.timeLeft(self,canvas)
        Main.userAccuracy(self,canvas)
        Main.displayBombProbability(self,canvas)
        Main.mouseDrag(self,canvas)
        Main.menuButton(self,canvas)
        Main.saveButton(self,canvas)

    #next level screen
    def nextLevel(self,canvas):
        #itializes game over state
        nextLevelCx = self.width//2 - 250
        nextLevelCy = self.height//2 - 100
        nextLevelCx2 = self.width//2 + 250
        nextLevelCy2 = self.height//2 + 100

        #splashscreen for level change
        if(self.timer == self.time and self.levelChange):
            canvas.create_rectangle(nextLevelCx,nextLevelCy,
                                    nextLevelCx2,nextLevelCy2,fill="Black")

            canvas.create_text(self.width//2,self.height//2 - 30,text="Next Level",
                                font = "Arial 50 bold",fill="white")
            
            canvas.create_text(self.width//2,self.height//2 + 30,text="Press any key to continue!",
                                font = "Arial 30 bold",fill="white")

    #Display all statistics of user after game is over
    def displayStatistics(self,canvas):
        statisticsCx = self.width//2 - 250
        statisticsCy = self.height//2
        statisticsCx2 = self.width//2 + 250
        statisticsCy2 = self.height - 60

        totalFruitsMissed = self.totalFruitsThrown - self.totalFruitsHit

        canvas.create_rectangle(statisticsCx,statisticsCy,
                                statisticsCx2,statisticsCy2,fill="Black")

        canvas.create_text(self.width//2,statisticsCy + 50,text="Statistics",
                            font = "Arial 30 bold",fill="white")

        canvas.create_text(self.width//2 ,statisticsCy + 90,
                text=f'Total Fruits Hit: {self.totalFruitsHit}',
                            font = "Arial 20 bold",fill="white")

        canvas.create_text(self.width//2 ,statisticsCy + 130,
                text=f'Total Fruits Missed: {totalFruitsMissed}',
                            font = "Arial 20 bold",fill="white")

        canvas.create_text(self.width//2 ,statisticsCy + 170,
                text=f'Total Bombs Hit: {self.totalBombsHit}',
                            font = "Arial 20 bold",fill="white")

        canvas.create_text(self.width//2 ,statisticsCy + 210,
                text=("Total Accuracy: %0.1f" % self.accuracy),
                            font = "Arial 20 bold",fill="white")

        canvas.create_text(self.width//2 ,statisticsCy + 250,
                text=f'Total Score: {self.counter}',
                            font = "Arial 20 bold",fill="white")

        canvas.create_text(self.width//2 ,statisticsCy + 290,
                text=f'Total Fruits Thrown: {self.totalFruitsThrown}',
                            font = "Arial 20 bold",fill="white")

    #displays game over once all levels are complete
    def gameOver(self,canvas):
        #itializes game over state
        gameOverCx = self.width//2 - 250
        gameOverCy = 100
        gameOverCx2 = self.width//2 + 250
        gameOverCy2 = 300

        #displays game over screen
        if(self.gameOver):
            canvas.create_rectangle(gameOverCx,gameOverCy,
                                    gameOverCx2,gameOverCy2,fill="Black")

            canvas.create_text(self.width//2,gameOverCy + 100,text="Game Over!",
                                font = "Arial 50 bold",fill="white")

            Main.displayStatistics(self,canvas)

    #function is responsible for drawing all the main parts of the game
    def redrawAll(self,canvas):
        if(self.gameMode == None):
            Main.startScreen(self,canvas)

        elif(((self.gameMode == "classic") and (self.waitingForMousePress == True)) 
                    and ((self.currentLevel == 1) or (self.currentLevel == 2) or
                            (self.currentLevel == 3) or (self.currentLevel == 4))):
            Main.classicModeLevel(self,canvas)
            if(self.nextLevelKey):
                Main.nextLevel(self,canvas)
            Main.gameOver(self,canvas)
        
        elif(((self.gameMode == "arcade") and (self.waitingForMousePress == True)) 
                    and ((self.currentLevel == 1) or (self.currentLevel == 2) or
                            (self.currentLevel == 3) or (self.currentLevel == 4))):
            Main.arcadeModeLevel(self,canvas)
            if(self.nextLevelKey):
                Main.nextLevel(self,canvas)
            Main.gameOver(self,canvas)
        
        elif(((self.gameMode == "zen") and (self.waitingForMousePress == True)) 
                    and ((self.currentLevel == 1) or (self.currentLevel == 2) or
                            (self.currentLevel == 3) or (self.currentLevel == 4))):
            Main.zenModeLevel(self,canvas)
            if(self.nextLevelKey):
                Main.nextLevel(self,canvas)
            Main.gameOver(self,canvas)
            
Main(width=1200,height=800)
    
