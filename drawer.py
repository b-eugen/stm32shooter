import serial
import threading
import time
from tkinter import *
import mouse
import random

def atoi(string):
    num = 0
    for elem in string:
        if (string[0] == '-'):
            if elem != '-':
                num = num * 10 - ord(elem) + ord('0')
        else:
            num = num * 10 + ord(elem) - ord('0')
    return num

global vel
global pos
global size
global click
click = 0

size = 1000

vel = [[0, 0]]
pos = [[0, 0]]
def reader():
    acceleration = []
    global vel
    global pos
    global click
    while (True):
        response = ser.readline()
        if len(response) > 0:
            strResp = response.decode("utf-8");
            strResp = strResp[5:-1]
            #print(strResp);
            strResp = strResp.split(', ')
            for i in range(len(strResp)):
                strResp[i] = atoi(strResp[i][4:])
            if (strResp[3] == 1):
                click = 1
                #    mouse.click('left')
            #    time.sleep(1e-4)
            acceleration.append([strResp[0], strResp[1]]);
            if len(acceleration) > 500:
                acceleration = acceleration[1:]
                vel = vel[1:]
                pos = pos[1:]
            #print(strResp)
            if len(acceleration) > 1:
                absX = abs(acceleration[-1][0] - acceleration[-2][0])
                absY = abs(acceleration[-1][1] - acceleration[-2][1])
                vel.append([(acceleration[-1][0] - acceleration[-2][0])* 0.01 + vel[-1][0], (acceleration[-1][1] - acceleration[-2][1]) * 0.01 + vel[-1][1]])
                pos.append([(vel[-1][0] - vel[-2][0])* 0.01 + pos[-1][0], (vel[-1][1] - vel[-2][1]) * 0.01 + pos[-1][1]])
                
                #print(pos[-1]) 
class rect: 
    def __init__(self):
        global size
        self.side = round(size/random.randint(20, 40)) 
        self.x = random.randint(0, size - self.side)
        self.y = random.randint(0, size - self.side)
    def isIn(self, X, Y):
        print(X, Y, self.x, self.y, self.side)
        if (self.x + self.side > X and self.x < X and self.y + self.side > Y and self.y < Y):
            return True
        return False


class Block:
    def __init__(self, master):
        global size
        #self.but = Button(master, text = "reset")
        self.score = 0
        self.lab = Label(master, width = 20, text = "Score = 0", font=("Calibri", 30, "bold"))
        self.c = Canvas(master, width = size, height = size, bg = 'white')
        self.lab.pack()
        self.c.pack()
        self.t2 = threading.Thread( target = self.receive)
        self.t2.start()
    def killrect(self, rect):
        rec_temp = rect
        self.c.itemconfigure(rec_temp,'red')
        time.sleep(0.2)
        self.c.delete(rec_temp)
    def receive(self):
        global size
        global pos
        global click 
        #rect = []
        self.c.create_line(0, 0, size, size, fill="red")
        self.c.create_line(0, size, size, 0, fill="blue")
        #self.c.create_oval(size/2 + size/20, size/2 - size/20, size/2 + size/20, size/2 - size/20, fill= "green")
        cross_x = self.c.create_line(size/2 - size/20, size/2, size/2 + size/20, size/2, fill="green")    
        cross_y = self.c.create_line(size/2, size/2 + size/20, size/2, size/2 - size/20, fill="green")    
        rectg = rect()
        rectgl =  self.c.create_rectangle(rectg.x, rectg.y, rectg.x + rectg.side, rectg.y + rectg.side, fill="pink")

        #ball.create_line(0, 0, size/20, size/20, fill="red")
        while(1):
            coordsX = self.c.coords(cross_y)[0] 
            coordsY = self.c.coords(cross_x)[1]
            vell = pos[-1]
            if (click == 1):
                print(click)
                if(rectg.isIn(coordsX, coordsY)):
                    #self.proc = threading.Thread(target = self.killrect, args=(rectgl))
                    #self.proc.start()
                    self.c.delete(rectgl)
                    rectg = rect()
                    rectgl =  self.c.create_rectangle(rectg.x, rectg.y, rectg.x + rectg.side, rectg.y + rectg.side, fill="pink")
                    self.score += 1
                    self.lab['text'] = ('Score =  %d' % self.score)

                click = 0   
            if coordsX + vell[0]  < size and coordsX + vell[0] > 0 and coordsY + vell[1] > 0 and coordsY + vell[1] < size:
                self.c.move(cross_x, vell[0], vell[1])
                self.c.move(cross_y, vell[0], vell[1])

ser = serial.Serial('/dev/ttyACM2', baudrate = 115200, timeout = 2)
print(ser.name)

t = threading.Thread(target=reader)
t.start()

root = Tk()
first = Block(root)
root.mainloop()

#while( True ):
 #   mouse.drag(0, 0, 2 * vel[-1][0], 2 * vel[-1][1], absolute=False, duration=0.01)
