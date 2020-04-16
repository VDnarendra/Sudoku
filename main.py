import pygame, sys
import time
from random import randint

class Game(object):
    """docstring for Game"""
    def __init__(self):
        super(Game, self).__init__()
        self.pygame = pygame
        self.pygame.init()
        self.pygame.font.init()
        self.display_width = 800
        self.display_height = 600
        self.font = self.pygame.font.SysFont('arial',25)
        self.gameDisplay = self.pygame.display.set_mode((self.display_width,self.display_height))
        self.pygame.display.set_caption('NumGun')
        self.clock = self.pygame.time.Clock()

    def displayBullets(self,bullets,color=(0,0,0)):
        w,h = 8,8
        for location in bullets:
            x,y = location[0],location[1]
            x = (x-1)*10 +1
            y = (y-1)*10 +1
            self.pygame.draw.rect(self.gameDisplay, color,(x,y,w,h))

    def displayTanker(self,tanker,color=(0,0,0)):
        w,h = 8,8
        for y1 in range(59,61):
            for x1 in range(tanker-1, tanker+2):
                y = (y1-1)*10 +1
                x = (x1-1)*10 +1
                self.pygame.draw.rect(self.gameDisplay, color,(x,y,w,h))
        y = (57)*10 +1
        x = (tanker-1)*10 +1
        self.pygame.draw.rect(self.gameDisplay, color,(x,y,w,h))

    def updateBullets(self,bullets, bullSpeed):
        NewBullets = []
        for x in range(len(bullets)):
            bullets[x] = [ bullets[x][0], bullets[x][1]-bullSpeed ]
            bull = bullets[x][1]
            if bull>0:
                NewBullets.append(bullets[x])
        return NewBullets

    def Display(self,a,start,clearWay):
        y = start%600

        i=0
        while(i<6):
            x = i*100
            x1 = (i+1)*100
            if(i not in clearWay):
                self.pygame.draw.line(self.gameDisplay,(0,250,0),(x,y),(x1,y),4)
                self.pygame.draw.line(self.gameDisplay,(0,250,0),(x,y+50),(x1,y+50),4)
                text = self.font.render(str(a[i]),True,(0,0,0))
                self.gameDisplay.blit(text,(x+30,y+5))
            self.pygame.draw.line(self.gameDisplay,(0,250,0),(x,y),(x,y+50),4)
            i+=1
        return a

    def updateArray(self,a,start,bullets,bombs):
        if(bullets !=[]):
            XLocation = (bullets[0][0]-1)*10
            YLocation = (bullets[0][1]-1)*10
            # index  = XLocation//100
            if(start+50>=YLocation):
                a[XLocation//100]-=1
                bullets = bullets[1:]

        if(bombs !=[]):
            XLocation = (bombs[0][0]-1)*10
            YLocation = (bombs[0][1]-1)*10
            if(start+50>=YLocation):
                a[XLocation//100]=0
                bombs = bombs[1:]

        clearWay = []
        for i in range(len(a)):
            if(a[i]<=0):
                clearWay.append(i)
        return a,clearWay,bullets,bombs

    def displayBombs(self,bombs,color=(0,0,0)):
        w,h = 8,8
        for location in bombs:
            x1,y1 = location[0]-1,location[1]-1
            x = (x1)*10 +1
            y = (y1)*10 +1
            self.pygame.draw.rect(self.gameDisplay, color,(x,y,w,h))
            x = (x1-1)*10 +1
            y = (y1)*10 +1
            self.pygame.draw.rect(self.gameDisplay, color,(x,y,w,h))
            x = (x1+1)*10 +1
            y = (y1)*10 +1
            self.pygame.draw.rect(self.gameDisplay, color,(x,y,w,h))
            x = (x1)*10 +1
            y = (y1-1)*10 +1
            self.pygame.draw.rect(self.gameDisplay, color,(x,y,w,h))
            x = (x1)*10 +1
            y = (y1+1)*10 +1
            self.pygame.draw.rect(self.gameDisplay, color,(x,y,w,h))

    def updateB(self,bullets, bullSpeed):
        NewBullets = []
        for x in range(len(bullets)):
            bullets[x] = [ bullets[x][0], bullets[x][1]-bullSpeed ]
            bull = bullets[x][1]
            if bull>0:
                NewBullets.append(bullets[x])
        return NewBullets

    def set_mode(self):
        font = self.pygame.font.SysFont("comicsansms",50)
        self.gameDisplay.fill((255,255,255))
        speed = 5
        self.gameDisplay.fill((255,255,255))
        text = font.render("Easy  Medium  Hard",True,(0,0,0))
        self.gameDisplay.blit(text,(150,150))
        self.pygame.display.update()
        while 1:
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.pygame.quit()
                    quit() 
                if event.type == self.pygame.MOUSEBUTTONDOWN:
                    x,y = self.pygame.mouse.get_pos()
                    if(x>150 and x<258 and y>160 and y<220):
                        speed = 5
                    elif(x>300 and x<460 and y>160 and y<220):
                        speed = 15
                    elif(x>495 and x<620 and y>160 and y<220):
                        speed = 30
                    return speed

    def game_intro(self):
        font = self.pygame.font.SysFont("comicsansms",60)
        self.gameDisplay.fill((255,255,255))
        text = font.render("NumGun v1.0",True,(0,0,0))
        self.gameDisplay.blit(text,(200,150))
        text = font.render("Play",True,(120,250,130))
        self.gameDisplay.blit(text,(190,350))
        text = font.render("Exit",True,(120,250,130))
        self.gameDisplay.blit(text,(510,350))
        self.pygame.display.update()
        while 1:
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    # self.pygame.quit()
                    self.__del__()
                    return
                    # quit()
                if event.type == self.pygame.MOUSEBUTTONDOWN:
                    x,y = self.pygame.mouse.get_pos()
                    if(x>185 and x<310 and y>360 and y<420):
                        speed = self.set_mode()
                        self.game_loop(speed)
                    elif(x>510 and x<630 and y>360 and y<420):
                        # self.pygame.quit()
                        # quit()
                        # sys.exit()
                        return

    def game_loop(self,speed):
        tanker = 30

        bombs = []
        bullets = []
        hit = False
        Vel_right = 1
        bomSpeed = 3
        bullSpeed = 2

        global highscore
        hit = False
        # array = [12,12,12,12,12,12,12]
        array = [randint(1,50) for i in range(7)]
        start = 0
        bombCount = 5
        usingBomb  =False
        self.gameDisplay.fill((255,255,255))
        
        count=0
        while not hit:
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    hit = True
                    # self.pygame.quit()
                    # quit()
                    # sys.exit()
                if event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_LEFT:
                        Vel_right = -2
                    elif event.key == self.pygame.K_RIGHT:
                        Vel_right = 1
                    elif event.key == self.pygame.K_b:
                        if(bombCount>0):
                            bombCount-=1
                            bombs.append([tanker,58])
                    if event.key == self.pygame.K_SPACE or event.key == self.pygame.K_UP:
                        bullets.append([tanker,58])
                        
            self.gameDisplay.fill((255,255,255))
            self.pygame.draw.line(self.gameDisplay,(0,0,0),(600,0),(600,600),2)
            tanker = (tanker+Vel_right)%60 +1
            bombs = self.updateB(bombs,bomSpeed)
            bullets = self.updateBullets(bullets,bullSpeed)
            self.displayBullets(bullets)
            self.displayBombs(bombs)
            self.displayTanker(tanker)
            array,clearWay,bullets,bombs = self.updateArray(array,start,bullets,bombs)
            self.Display(array,start,clearWay)
            text = self.font.render("NumGun v1.0",True,(0,0,0))
            self.gameDisplay.blit(text,(602,1))
            if(count>highscore):
                highscore = count
            text = self.font.render("High score: "+str(highscore),True,(0,0,0))
            self.gameDisplay.blit(text,(602,100))
            text = self.font.render("Your score: "+str(count),True,(0,0,0))
            self.gameDisplay.blit(text,(602,200))
            text = self.font.render("Bombs: "+str(bombCount),True,(0,0,0))
            self.gameDisplay.blit(text,(602,300))
            start+=5
            if(start%520==0):
                # print(clearWay[0]*100,tanker*10)
                hit = True
                for cw in clearWay:
                    if(cw>=0 and tanker>cw*10+3 and tanker<cw*10+10):
                        count+=1
                        if(count%5==0):
                            bombCount+=1
                        hit = False
                        break
                    else:
                        continue
                    
            if(start%600==0):
                start = 0
                array = [randint(1,20) for i in range(7)]

            self.pygame.display.update()
            self.clock.tick(speed)
            if(hit is True):
                self.game_intro()

        self.__del__()

    def __del__(self):
        
        self.pygame.quit()

if __name__ == '__main__':

    highscore = 0
    game = Game()
    try:
        game.game_intro()
        
    except Exception as e:
        game.pygame.quit()
        raise e

