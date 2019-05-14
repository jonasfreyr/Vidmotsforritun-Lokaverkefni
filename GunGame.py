import pygame, math, time, _thread
import RPi.GPIO as GPIO
import time
import serial
from pynput.keyboard import Key, Controller



wW = 1200
wH = 900

pygame.init()

ser=serial.Serial("/dev/ttyACM0", 115200)
ser.baudrate=115200

keyboard = Controller()


class game:
    def __init__(self, wW, wH):

        self.screen = pygame.display.set_mode((wW, wH))
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        self.wW = wW
        self.wH = wH

        telR = 0
        telL = 0

        color = (0, 0, 0)
        Scolor = (255, 255, 255)

        self.fontSize = 50
        self.font = pygame.font.SysFont("monospace", self.fontSize)

        self.speed = 5
        self.GunSpeed = 7

        self.GunWait = 50

        self.FPS = 120

        self.cheats = False

        self.gP = False

        self.win = 10

        _thread.start_new_thread(self.Wireless_input, ())
        
        game.restart(self, telR, telL, color, Scolor)

    def restart(self, telR, telL, color, Scolor):

        self.x = int((self.wW / 2) / 2)
        self.y = int((self.wH / 2))

        self.x2 = int((self.wW / 2) + self.wW / 4)
        self.y2 = int((self.wH / 2))

        if self.cheats == False:
            self.respos = False
            self.f3 = False
            self.f4 = False
            self.f5 = False
            self.f6 = False
            self.won = False

        self.size = 50
        self.shotSize = 10

        self.shotsL = []
        self.shotsR = []

        self.color = color
        self.Scolor = Scolor

        self.telR = telR
        self.telL = telL

    def shoot(self, x, y, dire):
        if dire == True:
            self.shotsR.append([x + self.size, y])
        elif dire == False:
            self.shotsL.append([x - self.size - self.shotSize * 2, y])

    def check(self):
        temp = self.shotsR
        for a in temp:
            x = a[0]
            y = a[1]

            vector1 = []
            vector1.append(self.x2 - x)
            vector1.append(self.y2 - y)

            vector2 = []
            vector2.append(self.x2 - x)
            vector2.append(self.y2 - (y + self.shotSize))

            vector3 = []
            vector3.append(self.x2 - (x + self.shotSize * 2))
            vector3.append(self.y2 - y)

            vector4 = []
            vector4.append(self.x2 - (x + self.shotSize * 2))
            vector4.append(self.y2 - (y + self.shotSize))

            if (self.size >= int(math.sqrt(math.pow(vector1[0], 2) + math.pow(vector1[1], 2)))) or (self.size >= int(math.sqrt(math.pow(vector2[0], 2) + math.pow(vector2[1], 2)))) or (self.size >= int(math.sqrt(math.pow(vector3[0], 2) + math.pow(vector3[1], 2)))) or (self.size >= int(math.sqrt(math.pow(vector4[0], 2) + math.pow(vector4[1], 2)))):
                if self.respos == False:
                    self.shotsR.remove(a)
                    self.telR += 1
                else:
                    game.restart(self, self.telR + 1, self.telL, self.color, self.Scolor)

        temp = self.shotsL
        for a in temp:
            x = a[0]
            y = a[1]

            vector1 = []
            vector1.append(self.x - x)
            vector1.append(self.y - y)

            vector2 = []
            vector2.append(self.x - x)
            vector2.append(self.y - (y + self.shotSize))

            vector3 = []
            vector3.append(self.x - (x + self.shotSize * 2))
            vector3.append(self.y - y)

            vector4 = []
            vector4.append(self.x - (x + self.shotSize * 2))
            vector4.append(self.y - (y + self.shotSize))

            if (self.size >= int(math.sqrt(math.pow(vector1[0], 2) + math.pow(vector1[1], 2)))) or (self.size >= int(math.sqrt(math.pow(vector2[0], 2) + math.pow(vector2[1], 2)))) or (self.size >= int(math.sqrt(math.pow(vector3[0], 2) + math.pow(vector3[1], 2)))) or (self.size >= int(math.sqrt(math.pow(vector4[0], 2) + math.pow(vector4[1], 2)))):
                if self.respos == False:
                    self.shotsL.remove(a)
                    self.telL += 1
                else:
                    game.restart(self, self.telR, self.telL + 1, self.color, self.Scolor)

    def shots(self):
        for a in range(len(self.shotsR)):
            x = self.shotsR[a][0]
            y = self.shotsR[a][1]

            pygame.draw.rect(self.screen, self.color ,pygame.Rect(x, y, self.shotSize * 2, self.shotSize ))

            self.shotsR[a].insert(0 ,x + self.GunSpeed)
            self.shotsR[a].remove(x)

        for a in range(len(self.shotsL)):
            x = self.shotsL[a][0]
            y = self.shotsL[a][1]

            pygame.draw.rect(self.screen, self.color ,pygame.Rect(x, y, self.shotSize * 2, self.shotSize ))

            self.shotsL[a].insert(0 ,x - self.GunSpeed)
            self.shotsL[a].remove(x)

        temp = self.shotsR
        for a in temp:
            if a[0] > self.wW:
                self.shotsR.remove(a)

        temp = self.shotsL
        for a in temp:
            if a[0] < 0:
                self.shotsL.remove(a)

    def colorChange(self):
        if self.color == (0, 0, 0):
            self.color = (255,255,255)
            self.Scolor = (0, 0, 0)
        elif self.color == (255, 255, 255):
            self.color = (0, 0, 0)
            self.Scolor = (255, 255, 255)

    def winner(self,vann):
        self.won = True
        label = self.font.render(vann + " won!", 1, self.color)
        self.screen.blit(label,(self.wW / 2 - self.fontSize * 3, self.wH / 2 - (self.fontSize / 2)))

    def Wireless_input(self):
        while True:
            read_ser = ser.readline()
            read_ser = read_ser[:len(read_ser)-2]
            self.read_ser = read_ser.split(b",")

            #print(self.read_ser)
            
            try:
                if self.read_ser[0] == b"1":
                    self.read_ser1 = self.read_ser

                elif self.read_ser[0] == b"2":
                    self.read_ser2 = self.read_ser
            except:
                pass
            
    def loop(self):
        tel1 = self.GunWait
        tel2 = self.GunWait
        while True:
            pressed = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_F1:
                        game.colorChange(self)
                    if event.key == pygame.K_F2:
                        # self.respos = not self.respos
                        pass
                    if event.key == pygame.K_F3:
                        self.f3 = not self.f3
                    if event.key == pygame.K_F4:
                        self.f4 = not self.f4
                    if event.key == pygame.K_F5:
                        self.f5 = not self.f5
                    if event.key == pygame.K_F6:
                        self.f6 = not self.f6
                    if event.key == pygame.K_ESCAPE:
                        quit()
            if self.gP == False and self.won == False:
                self.screen.fill(self.Scolor)

                if self.f3 or self.f4 or self.f5 or self.f6:
                    self.cheats = True

                if self.f3 == True:
                    self.GunSpeed = 20
                elif self.f3 == False:
                    self.GunSpeed = 7

                if self.f4 == True:
                    self.GunWait = 15
                elif self.f4 == False:
                    self.GunWait = 50

                if self.f5 == True:
                    self.FPS = 30
                elif self.f5 == False:
                    self.FPS = 120

                if self.f6 == True:
                    self.speed = 15
                elif self.f6 == False:
                    self.speed = 5

                try:
                    if self.y > 0 + self.size:
                        if int(self.read_ser1[2]) > 800: self.y -= self.speed
                    if self.y < self.wH - self.size:
                        if int(self.read_ser1[2]) < 200: self.y += self.speed
                    if self.x > 0 + self.size:
                        if int(self.read_ser1[1]) > 800: self.x -= self.speed
                    if self.x < int(self.wW /2) - self.size:
                        if int(self.read_ser1[1]) < 200: self.x += self.speed
                    if tel1 >= self.GunWait:
                        if int(self.read_ser1[3]) == 0:
                            game.shoot(self, self.x, self.y, True)
                            tel1 = 0
                except:
                    pass

                try:
                    if self.y2 > 0 + self.size:
                        if int(self.read_ser2[2]) > 800:  self.y2 -= self.speed
                    if self.y2 < self.wH - self.size:
                         if int(self.read_ser2[2]) < 200: self.y2 += self.speed
                    if self.x2 > int(self.wW / 2) + self.size:
                        if int(self.read_ser2[1]) > 800: self.x2 -= self.speed
                    if self.x2 < int(self.wW) - self.size:
                        if int(self.read_ser2[1]) < 200: self.x2 += self.speed
                    if tel2 >= self.GunWait:
                        if int(self.read_ser2[3]) == 0:
                            game.shoot(self, self.x2, self.y2, False)
                            tel2 = 0
                except:
                    pass

                tel1 += 1
                tel2 += 1

                game.check(self)

                pygame.draw.line(self.screen,self.color,[self.wW / 2, 0],[self.wW / 2, self.wH])

                pygame.draw.circle(self.screen, self.color,(self.x, self.y), self.size)
                pygame.draw.circle(self.screen, self.color, (self.x2, self.y2), self.size)

                game.shots(self)

                scoreR = self.font.render(str(self.telR), 1, self.color)
                scoreL = self.font.render(str(self.telL), 1, self.color)

                if self.telR < 10:
                    self.screen.blit(scoreR, ((self.wW / 2) - self.fontSize, 0))
                elif self.telR >= 10 and self.telR < 100:
                    self.screen.blit(scoreR, ((self.wW / 2) - self.fontSize - 15, 0))
                elif self.telR >= 100 and self.telR < 1000:
                    self.screen.blit(scoreR, ((self.wW / 2) - self.fontSize - 45, 0))
                elif self.telR >= 1000:
                    self.screen.blit(scoreR, ((self.wW / 2) - self.fontSize - 75, 0))
                self.screen.blit(scoreL, ((self.wW / 2) + 15, 0))

                if self.telR == self.win:
                    game.winner(self,"Left")
                elif self.telL == self.win:
                    game.winner(self,"Right")

            if pressed[pygame.K_r]:
                self.cheats = False
                game.restart(self, 0, 0, self.color, self.Scolor)
            pygame.display.flip()
            self.clock.tick(self.FPS)
H = game(wW, wH)
H.loop()
