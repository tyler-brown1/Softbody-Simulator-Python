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
r = 0.00005 # constant for time change
start = time.time()

m = 1
k = 20 # spring constant  = stretch

def add(A,B):
    return (A[0]+B[0],A[1]+B[1])

def sub(A,B):
    return (A[0]-B[0],A[1]-B[1])

def mult(A,a):
    return (A[0]*a,A[1]*a)

def shift(A):
    return (scale*A[0]+WIDTH/2,-scale*A[1]+HEIGHT/2)

def rotate(A,a):
    return (A[0]*cos(a)-A[1]*sin(a),A[0]*sin(a)+A[1]*cos(a))

class Vector():

    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def __add__(self,V): 
        return Vector(self.x+V.x,self.y+V.y)

    def __sub__(self,V):
        return Vector(self.x-V.x,self.y-V.y)

    def norm(self):
        return sqrt(self.x*self.x + self.y*self.y)
    
    def __mul__(self,v):
        return Vector(self.x*v,self.y*v)

    def __truediv__(self,v):
        return Vector(self.x/v,self.y/v)

    def dist(self,other):
        return (self-other).norm()

    def shift(self):
        return (scale*self.x+WIDTH/2,-scale*self.y+HEIGHT/2)
    
    def __repr__(self):
        return f"Vector({self.x},{self.y})"

class SoftBody():

    def __init__(self):
        self.nodes = {}
        self.connections = {}
    
    def add(self,nodes):
        for node in nodes:
            self.nodes[node.id] = node

    def connect(self,x,y,k = k):
        self.connections[(x,y)] = (self.nodes[x].dist(self.nodes[y]),k)

    def update(self):
        accel = {id: Vector(0,-g) for id in self.nodes}
        for conn in self.connections:
            conndata = self.connections[conn]
            X,Y = self.nodes[conn[0]], self.nodes[conn[1]]
            x,y = conn[0], conn[1]
            D,d,k = X.dist(Y), conndata[0], conndata[1]
            dcon = 1-d/D # constant used

            acc = (X-Y) * (k * dcon)

            accel[x] -= acc/X.m
            accel[y] += acc/Y.m
        
        for id in self.nodes:
            node = self.nodes[id]
            node.update(accel[id])

    def draw(self):

        for id in self.nodes:                
            self.nodes[id].draw()

        for conn in self.connections: #change to lines with only some visible at some point
            pygame.draw.line(WIN,black,self.nodes[conn[0]].p.shift(),self.nodes[conn[1]].p.shift(),1)


class Node():

    def __init__(self,id:int,p,static=False,v=(0,0),m=m,vis=True):
        self.id = id
        self.p0 = Vector(p[0],p[1])
        self.p = Vector(p[0],p[1])
        self.v = Vector(v[0],v[1])
        self.m = m
        self.vis = vis
        self.static = static
    
    def __str__(self):
        return f"Node {self.id}"
    
    def draw(self):
        if self.vis:
            pygame.draw.circle(WIN,black,self.p.shift(),2)
    
    def update(self,a):
        if not self.static:
            self.p,self.v = self.p+self.v*r, self.v + a*(r*damp)
    
    def shift(self):
        return self.p.shift()

    def dist(self,other):
        return self.p.dist(other.p)

    def __sub__(self,other):
        return self.p-other.p

def erase_window():
    WIN.fill(white)

def draw_window():
    pygame.display.update()

sb = SoftBody()
def initialize():
    nodes = []
    n = 4
    m = 5
    a=.25
    for i in range(m):
        for j in range(n):
            nodes.append(Node(n*i+j,(i*1.5,j*1.5),v=(0,0)))
            #nodes.append(Node(n*i+j,rotate((i*1,j*1),a),v=(0,0)))

    sb.add(nodes)
    sb.add([Node(-1,(0,10),1)])

    for i in range(m):
        for j in range(n-1):
            sb.connect(n*i+j,n*i+j+1,1000)

    for i in range(m-1):
        for j in range(n):
            sb.connect(n*i+j,n*i+j+n,1000)
    
    for i in range(m-1):
        for j in range(n-1):
            sb.connect(n*i+j,n*i+j+1+n,1000)
            sb.connect(n*i+j+n,n*i+j+1,1000)

            

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