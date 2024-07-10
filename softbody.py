import pygame
from math import *
import time

WIDTH,HEIGHT = 800,600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Softbody")

black = (0,0,0)
blue = (50,50,255)
white = (255,255,255)
grey = (30,30,30)

linew = 2
scale = 25

FPS = 1500

g = 2
floorheight = -6
damp = .997 #
size = 10
ct = 0
r = 0.00002 # constant for time change
start = time.time()

m = 1
k = 20 # spring constant  = stretch

def add(A,B):
    return (A[0]+B[0],A[1]+B[1])

def sub(A,B):
    return (A[0]-B[0],A[1]-B[1])

def mult(A,a):
    return (A[0]*a,A[1]*a)

def norm(A):
    return sqrt(A[0]**2+A[1]**2) 

def shift(A):
    return (scale*A[0]+WIDTH/2,-scale*A[1]+HEIGHT/2)

def dist(A,B):
    return sqrt(norm(sub(A,B)))

def rotate(A,a):
    return (A[0]*cos(a)-A[1]*sin(a),A[0]*sin(a)+A[1]*cos(a))


class SoftBody():

    def __init__(self):
        self.nodes = {}
        self.connections = {}
    
    def add(self,nodes):
        for node in nodes:
            self.nodes[node.id] = node

    def connect(self,x,y,k = k):
        self.connections[(x,y)] = (dist(self.nodes[x].p0,self.nodes[y].p0),k)

    def update(self):
        accel = {id:[0,-g] for id in self.nodes}
        for conn in self.connections:
            conndata = self.connections[conn]
            X,Y = self.nodes[conn[0]],self.nodes[conn[1]]
            x,y = conn[0],conn[1]
            D,d,k = dist(X.p,Y.p),conndata[0],conndata[1]
            dcon = 1-d/D # constant used

            xacc = k * dcon * (X.p[0]-Y.p[0])
            accel[x][0] += -xacc/X.m
            accel[y][0] += xacc/Y.m

            yacc = k * dcon * (X.p[1]-Y.p[1])
            accel[x][1] += -yacc/X.m 
            accel[y][1] += yacc/Y.m
        
        for id in self.nodes:
            node = self.nodes[id]
            node.update(accel[id])

    def draw(self):

        for id in self.nodes:                
            self.nodes[id].draw()

        for conn in self.connections: #change to lines with only some visible at some point
            pygame.draw.line(WIN,black,shift(self.nodes[conn[0]].p),shift(self.nodes[conn[1]].p),1)


class Node():

    def __init__(self,id:int,p,static=False,v=(0,0),m=m,vis=True):
        self.id = id
        self.p0 = p
        self.p = p
        self.v = v
        self.m = m
        self.vis = vis
        self.static = static
    
    def __str__(self):
        return f"Node {self.id}"
    
    def draw(self):
        if self.vis:
            pygame.draw.circle(WIN,black,shift(self.p),4 if self.static else 2)
    
    def update(self,a):
        if not self.static:
            self.p,self.v = add(self.p,mult(self.v,r*damp)),add(self.v,mult(a,r*damp))

def erase_window():
    WIN.fill(white)

def draw_window():
    pygame.display.update()


sb = SoftBody()
def initialize():
    nodes = []
    n = 3
    m = 3
    a=.25
    for i in range(m):
        for j in range(n):
            nodes.append(Node(n*i+j,(i*4-2,j*4),v=(2,0)))

    sb.add(nodes)
    sb.add([Node(-1,(-6,7),1)])
    sb.add([Node(-2,(9,6.5),1)])
    sb.add([Node(-3,(-2,-2),m=3)])
    sb.add([Node(-4,(1.5*m+2,-2),m=3)])


    for i in range(m):
        for j in range(n-1):
            sb.connect(n*i+j,n*i+j+1,2200)

    for i in range(m-1):
        for j in range(n):
            sb.connect(n*i+j,n*i+j+n,2200)
    
    for i in range(m-1):
        for j in range(n-1):
            sb.connect(n*i+j,n*i+j+1+n,450)
            sb.connect(n*i+j+n,n*i+j+1,450)      

    sb.connect(-1,n-1)
    sb.connect(-2,n*m-1)      
    sb.connect(-3,0,10)
    sb.connect(-4,n*m-n,10)


def main():
    
    initialize()
    run = True
    ct=0
    while run:
        ct+=1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        erase_window()
        sb.update()
        sb.draw()
        if ct%20==0:
            draw_window()
        if ct==10000:
            print(time.time()-start)

    pygame.quit()
    

if __name__ == "__main__":
    main()