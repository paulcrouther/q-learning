#V3.5
'''
1. With eligibility trace
'''
# INTIALISATION
import warnings
warnings.filterwarnings('ignore')
import pylab, os, sys, getopt, pdb, learningET, pygame, random, math, time, Sprite
import matplotlib.pyplot as plt
from math import exp, expm1, atan2, degrees, pi
from numpy import *
from numpy.random import *

from tiles import CMAC

sys.setrecursionlimit(30000)

pygame.init()
arrivenum = 0
crashnum = 0

# DISPLAY CONSTANTS
display_width = 400
display_height = 600
car_width = 35
car_height = 35
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)

#OBSTACLE CONSTANTS 
thing_startx = 100
thing_startx1 = 300
thing_starty = 300
thing_starty1= 300    

# DISPLAY SETTING IN PYGAME
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Car Simulator_Q')
clock = pygame.time.Clock()

car = Sprite.Robot('car.png', (250,500), 100, 30)

# Q-LEARNING
class static:
    FLAG = (0,0)
    REWARD = 0

class Rect:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
    def render(self,collision):
        if (collision==True):
            pygame.draw.rect(gameDisplay,red,(self.x,self.y,self.width,self.height))
        else:
            pygame.draw.rect(gameDisplay,black,(self.x,self.y,self.width,self.height))
            
Sprite2=Rect(thing_startx,thing_starty,30,30)
Sprite3=Rect(thing_startx1,thing_starty1,30,30)

#QLearning SETTING
class agent:
    count = 0
    rewards = 0
    epsilon = 0.1
    alpha = 0.1
    gamma = 0.9
    lamda = 0.9
    iteration = 1000
    
Q = []      
E = []
ACTIONLIST = [(-1,0),(0,0),(-1,-1),(-1,+1)]
lastState = ()
lastAction = static.FLAG

# MESSAGE 
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
#    time.sleep(2)
    
    #Iterate simulation!
    game_loop()

# COLLISION DETECTION
def detectCollisions(x1,y1,w1,h1,x2,y2,w2,h2):
    if (x2+w2>=x1>=x2 and y2+h2>=y1>=y2):
        return True
    elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1>=y2):
        return True
    elif (x2+w2>=x1>=x2 and y2+h2>=y1+h1>=y2):
        return True
    elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1+h1>=y2):
        return True
    else:
        return False

def crashRate():
    crashnum += 1

def arriveRate():
    arrivenum += 1

def errorRate():
    arrivenum = 0
    if arrive() and not crash():
        arrivenum += 1
        print (arrivenum)
    elif crash() and not arrive():
        crashnum += 1
        print (crashnum)
    else:
        arrivenum = arrivenum
        crashnum = crashnum
    errorrate = int(arrivenum)/int(crashnum)
    print ('This is the error: %d', errorrate)
    


# REWARD FOR CRASH
def crash():
    print('crash')
    static.REWARD = -100
    agent.rewards += static.REWARD
    update()
#    static.REWARD = 0
    message_display('You Crashed')
    crashnum += 1
    
# REWARD FOR ARRIVAL
def arrive():
    print('arrive')
    static.REWARD = +100
    agent.rewards += static.REWARD
    update()
    message_display('You Arrived')
    arrivenum += 1

# REWARD FOR MOVE
def move():
    static.REWARD = -1
    update()
    agent.rewards += static.REWARD

# GAME SIMULATION LOOP
def game_loop():

    pygame.init()    
    
    global cmac
    cmac = CMAC(4,.04,.1) #n levels of network, default was 2, where n: (n, .01, .1)
    
    global car
    car = Sprite.Robot('car.png', (250,500), 100, 30) 
    car_group = pygame.sprite.RenderPlain(car)
#    car.draw_rays(gameDisplay)
    
    global carAgent
    if(agent.count<agent.iteration):
        agent.count += 1
        print (agent.count)
        agent.epsilon -= agent.epsilon/agent.iteration
#        agent.alpha -= agent.alpha/agent.iteration
        carAgent=learningET.QLearning(ACTIONLIST, agent.epsilon, agent.alpha, agent.gamma, agent.lamda)
    else:
        carAgent=learningET.QLearning(ACTIONLIST, 0, 0, agent.gamma, agent.lamda)    
    
    gameExit = False
    
    # IN GAME
    while not gameExit:
        # USER INPUT
        deltat = clock.tick(60)
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            down = event.type == pygame.KEYDOWN
            if event.key == pygame.K_ESCAPE:
                '''
                fig1 = pylab.figure(1)
                pylab.plot(errors)

                pylab.show()                
                '''

                sys.exit(0)
#        print static.FLAG
        if(static.FLAG == (-1,0)):
            car.k_up=-2
            move()   
        elif(static.FLAG == (0,0)):
            car.k_down = +2
#            move()  
        elif(static.FLAG == (-1,-1)):
            car.k_down = 0
            car.k_left = 2
            car.k_right = 0
            move()  
        elif(static.FLAG == (-1,+1)):
            car.k_down = 0
            car.k_left = 0
            car.k_right = -2
            move()

        gameDisplay.fill(white)
               
        # COLLISION DETECTION
        # DARK OBSTACLES
        global collisions, collisions1
        collisions=detectCollisions(car.x,car.y,car_width,car_height,Sprite2.x,Sprite2.y,Sprite2.width,Sprite2.height)
        collisions1=detectCollisions(car.x,car.y,car_width,car_height,Sprite3.x,Sprite3.y,Sprite3.width,Sprite3.height)
    
        # MEASURE DISTANCE, POSITION, and SPEED OF CAR
        global dist, dist1, car_position, car_speed
        dist = math.hypot(car.x - thing_startx, car.y - thing_starty)
        dist1 = math.hypot(car.x - thing_startx1, car.y - thing_starty1)

        car_x = car.x
        car_y = car.y
        car_position = (car.x, car.y)
        car_speed = car.speed

        # MEASURE ANGLE
        dx,dy = thing_startx-car.x,thing_starty-car.y
        dx1,dy1 = thing_startx1-car.x,thing_starty1-car.y

        global rads,degs,rads1,degs1
        rads = (math.atan2(dx,dy))
        degs = math.degrees(rads)
        rads1 = (math.atan2(dx1,dy1))
        degs1 = math.degrees(rads1)
        
        dist = round(dist/10)
        dist1 = round(dist1/10)      

        degs = round(degs)
        degs1 = round(degs1)        
        
        #Quantized inputs
        '''
        global q_d, q_d1, q_deg, q_deg1
        q_d = cmac.quantize(dist)
        q_d1 = cmac.quantize(dist1)
        q_deg = cmac.quantize(degs)
        q_deg1 = cmac.quantize(degs)
        '''
        global predicted, predicted1, predicted2, predicted3, predicted4, predicted5
        points = uniform(low=0,high=2*car.x,size=10)
        points1 = uniform(low=0,high=2*car.y,size=10)
        points2 = uniform(low=0,high=2*dist1,size=10)
        points3 = uniform(low=0,high=2*degs1,size=10)
        points4 = uniform(low=0,high=2*dist,size=10)
        points5 = uniform(low=0,high=2*degs,size=10)
        response = sin(points)
        response1 = sin(points1)
        response2 = sin(points2)
        response3 = sin(points3)
        response4 = sin(points4)
        response5 = sin(points5)
        
        
        global errors, errors1, errors2, errors3, errors4, errors5
        errors = []
        errors1 = []
        errors2 = [] 
        errors3 = [] 
        errors4 = [] 
        errors5 = []
        
        for (point,response) in zip(points,response):
            predicted = cmac.response(array([point]),response)
            errors.append(abs(response - predicted))
        for (point,response1) in zip(points1,response1):
            predicted1 = cmac.response(array([point]),response1)
            errors1.append(abs(response1 - predicted1))
        for (point,response2) in zip(points2,response2):
            predicted2 = cmac.response(array([point]),response2)
            errors2.append(abs(response2 - predicted2))
        for (point,response3) in zip(points3,response3):
            predicted3 = cmac.response(array([point]),response3)
            errors3.append(abs(response3 - predicted3))
        for (point,response4) in zip(points4,response4):
            predicted4 = cmac.response(array([point]),response4)
            errors4.append(abs(response4 - predicted4))
        for (point,response5) in zip(points5,response5):
            predicted5 = cmac.response(array([point]),response5)
            errors5.append(abs(response5 - predicted5))

            
        '''
        points = uniform(low=0, high=dist, size=100)
        actual = []
        for point in points:
            actual.append(cmac.eval(array([point])))
        '''
        # BOUNDARY
        global decision_boundary
        if ((car.x > display_width - car_width or car.x < 10) or (car.y > display_height - car_height or car.y < 10)):
            decision_boundary = 1 #DANGEROUS
        else:
            decision_boundary = 0 #SAFE
            
        #ARRIVAL
        if (collisions1 == True):
#            static.REWARD = (exp(1/dist1))
            arrive()
            
        #SAFE
#        if ((collisions == False) and (decision_boundary == 0)):   
#            update()
  
        #NONSAFE  
        if ((collisions == True) or (decision_boundary == 1)):
            crash()
        else:
            update()
    
        # RENDERING
#        Sprite1.render(False)
        Sprite2.render(collisions)
        Sprite3.render(collisions1)            
        car_group.update(deltat)
        car_group.draw(gameDisplay)
        gameDisplay.blit(car.image, car.rect)
        pygame.display.flip()
        
# Q LEARNING UPDATE 
def update():
    temp = []
    state = temp  
       
    # STATE DEFINITION   
    temp.append([car.speed, predicted2, predicted3, predicted4, predicted5])     
    #temp.append([dist,dist1,degs,degs1])     

    # since distance [] is of no use
    if temp != []:
        state = temp[0]
        state = tuple(state)
        action = static.FLAG
        Q.append([state, action])
        E.append([state, action])        
        lastState = Q[len(Q)-2][0]
        lastAction = Q[len(Q)-2][1]

    carAgent.learn(lastState, lastAction, static.REWARD, state)
    static.FLAG = carAgent.chooseAction(state)

#    print static.REWARD

game_loop()

pygame.quit()



quit()

