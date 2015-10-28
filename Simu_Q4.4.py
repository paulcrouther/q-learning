#V4.4
#CHANGED SIMULATION ENVIRONMENT
import warnings
warnings.filterwarnings('ignore')
import learning, pygame, time, sys, SpriteV2
from math import exp, expm1, atan2, degrees, pi
from numpy import *
from numpy.random import *
 
sys.setrecursionlimit(15000)
 
pygame.init()
 
# DISPLAY CONSTANTS
fps             = 30
display_width   = 800
display_height  = 600
car_width       = 35
car_height      = 35
black           = (0,0,0)
white           = (255,255,255)
red             = (255,0,0)
blue            = (0,0,255)
green           = (0,255,0)

 
# DISPLAY SETTING IN PYGAME
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Car Simulator_Q')
clock = pygame.time.Clock()
 
#car = SpriteV2.Robot('car.png', (600,500))
 
# Q-LEARNING
class static:
    FLAG = (0,0)
    REWARD = 0
 
class Obstacle:      #for now just colored rectangles
    def __init__(self, x, y, width, height, color):
        self.x          = x
        self.y          = y
        self.width      = width
        self.height     = height
        self.color      = color
 
list_obstacles = []
w01 = Obstacle(0,0,800,5,black)   #top wall
list_obstacles.append(w01)
w02 = Obstacle(795,0,5,600,black) #right wall
list_obstacles.append(w02)
w03 = Obstacle(0,595,800,5,black) #bottom wall
list_obstacles.append(w03)
w04 = Obstacle(0,0,5,600,black)   #left wall
list_obstacles.append(w04) 

w05 = Obstacle(150,150,500,5,black)   #top wall
list_obstacles.append(w05)
w06 = Obstacle(650,150,5,300,black) #right wall
list_obstacles.append(w06)
w07 = Obstacle(150,450,500,5,black) #bottom wall
list_obstacles.append(w07)
w08 = Obstacle(150,150,5,300,black)   #left wall
list_obstacles.append(w08)


list_target = []
w09=Obstacle(100,100,30,30,red) #target
list_target.append(w09) 
 
#QLearning SETTING
class agent:
    count = 0
    n_arr = 0
    rewards = 0
    epsilon = 0.2
    alpha = 0.3
    gamma = 0.99
    iteration = 5000
 
Q = []     
E = []
ACTIONLIST = [(-1,0),(1,0),(-1,-1),(-1,+1)]
lastState = ()
lastAction = ()
 
carAgent=learning.QLearning(ACTIONLIST, agent.epsilon, agent.alpha, agent.gamma, agent.iteration)
 
     
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
 
# REWARD FOR CRASH
def crash():
#    print('crash')
#    print car.sense(list_rect_obstacles)
    static.REWARD = -10
    update()
    agent.rewards += static.REWARD
    static.REWARD = 0
#    print agent.rewards
    game_loop()
#    message_display('You Crashed')

# REWARD FOR CRASH
def danger():
#    print('crash')
    static.REWARD = -5
    update()
    agent.rewards += static.REWARD
    static.REWARD = 0

    
def avoid():
#    print('crash')
    static.REWARD = +5
    update()
    agent.rewards += static.REWARD
    static.REWARD = 0

 
# REWARD FOR ARRIVAL
def arrive():
#    print('arrive')
    print car.sense(list_rect_obstacles)
    agent.n_arr += 1
    print "'#of success :%d" % agent.n_arr

    static.REWARD = +10
    agent.rewards += static.REWARD
    update()
#    print agent.rewards
    static.REWARD = 0
    game_loop()
#    message_display('You Arrived')
 
# REWARD FOR MOVE
def move():
    static.REWARD = -1
    update()
    agent.rewards += static.REWARD
    static.REWARD = 0
 
 
# GAME SIMULATION LOOP
def game_loop():
    pygame.init()    
     
    agent.count += 1
    print (agent.count)
     
#    print carAgent.epsilon, carAgent.alpha, carAgent.iterations
    #EPSILON, ALPHA DECREASING
#    carAgent.deacreasing_parameter()
     
    global car, car_group
    car = SpriteV2.Robot('car.png', (700,500))
    car_group = pygame.sprite.RenderPlain(car)
     
    gameExit = False
     
    # IN GAME
    while not gameExit:
        # USER INPUT
        deltat = clock.tick(fps)
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            down = event.type == pygame.KEYDOWN
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
        if(static.FLAG == (-1,0)):
            car.k_up=-2
            move()   
        elif(static.FLAG == (0,0)):
            car.speed     = 0
            car.direction = 0
          
        elif(static.FLAG == (-1,-1)):
            car.k_up=0
            car.k_down  = 0
            car.k_left  = 2
            car.k_right = 0
            move()  
        elif(static.FLAG == (-1,+1)):
            car.k_up=0
            car.k_down  = 0
            car.k_left  = 0
            car.k_right = -2
            move()
 
        gameDisplay.fill(white)

        '''               
        # MEASURE DISTANCE with TARGET, position of car, and speed of car 
        global dist, dist1, car_position, car_speed
        dist = math.hypot(car.x - thing_startx, car.y - thing_starty)
        car_position = (car.x, car.y)
        car_speed = car.speed
 
        dx = thing_startx-car.x
        dy = thing_starty-car.y
 
        global rads,degs,rads1,degs1
        rads = (math.atan2(dx,dy))
        degs = math.degrees(rads)        
        dist = round(dist/20)
        degs = round(degs/20)
         
        # MEASURE DISSTANCE WITH OBSTACLES
        global list_dist_rads
        list_dist_rads=[]
        for ob in list_obstacles:
            dis = round(math.hypot(car.x-ob.x, car.y-ob.y))
            dx = car.x-ob.x
            dy = car.y-ob.y   
            rad = (math.atan2(dx,dy)) 
            degs = math.degrees(rads) 
            degs = round(degs)
            list_dist_rads.append(degs)
             
        #DEFINITION FOR STATES
        global list_states
        list_states = list_dist_rads
        list_states.append(car_speed)
        list_states.append(dist)
        list_states.append(degs)
        '''
        # BOUNDARY
        global decision_boundary
        if ((car.x > display_width - car_width or car.x < 10) or (car.y > display_height - car_height or car.y < 10)):
            decision_boundary = 1 #DANGEROUS
        else:
            decision_boundary = 0 #SAFE
         
        # RENDERING
        global list_rect_obstacles, list_rect_target
        list_rect_obstacles = []
        for ob in list_obstacles:
            list_rect_obstacles.append(pygame.draw.rect(gameDisplay,black,(ob.x,ob.y,ob.width,ob.height)))
        list_rect_target = []
        for tar in list_target:
            list_rect_target.append(pygame.draw.rect(gameDisplay,red,(tar.x,tar.y,tar.width,tar.height)))   
                
        car_group.update(deltat)
        car_group.draw(gameDisplay)
        car.draw_rays(gameDisplay) 
        gameDisplay.blit(car.image, car.rect)
        pygame.display.update()
  
  
        s = car.sense(list_rect_obstacles)
        #DANGER          
        if (s[0] or s[1] or s[2] or s[3] or s[4] or s[5] <= 40 ):
            danger()
        else:
            avoid()
        
        #ARRIVAL
        if car.rect.collidelist(list_rect_target) != -1: #if car arrives
            arrive()

        #COLLISION
        if (car.rect.collidelist(list_rect_obstacles) != -1):
            crash()

 
# Q LEARNING UPDATE 
def update():
    temp = []
    state = temp  
 
    # STATE DEFINITION
    list_temp = car.sense(list_rect_obstacles)
    for i in range(0,7):
        if(list_temp[i]<=40):
            list_temp[i] = 0
        else:
            list_temp[i] = 1
    
    #temp = car.sense(list_rect_obstacles)
    temp = list_temp     
     
    # since distance [] is of no use
    if temp != []:
        state = temp
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