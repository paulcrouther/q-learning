import pygame, math
import itertools
 
r_visual_range   = 100     #measured from robot center
r_visual_angle   = 30       #in degrees, must divide 90 exactly!
r_visual_granularity = 5    #must be < wall_thickness for walls to be detected correctly!
r_init_azi       = 0
r_step_theta     = 7.5
 
class Robot(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 2
    MAX_REVERSE_SPEED = -2
    ACCELERATION = 2
    TURN_SPEED = 2
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.rect           = self.src_image.get_rect()
        self.rect_original  = self.rect     #unchanging copy, for rotations
        self.x = self.position[0]
        self.y = self.position[1]
        self.speed = 0
        self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0
        self.azi            = r_init_azi
        self.visual_range   = r_visual_range
        self.visual_angle   = r_visual_angle
        self.nr_sensors     = 2*90/self.visual_angle+1
        self.retina         = list([self.visual_range]\
                                   for i in range(self.nr_sensors))   
        
                                        
    def setAction(self,speed,direction):
        self.speed=speed
        self.direction=direction
        return speed, direction
         
    def update(self, deltat):
        # SIMULATION
        self.speed += (self.k_up + self.k_down)
        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        if self.speed < self.MAX_REVERSE_SPEED:
            self.speed = self.MAX_REVERSE_SPEED
        self.direction += (self.k_right + self.k_left)
        rad = self.direction * math.pi / 180
         
        self.azi += (self.k_right + self.k_left)
        '''
        if self.azi >= 360:         #keep theta between -360..360
            self.azi = self.azi-360
        if self.azi <= -360:
            self.azi = self.azi+360        
        '''
        self.x += self.speed*math.sin(rad)
        self.y += self.speed*math.cos(rad)
        self.position = (self.x, self.y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
     
    def printRetina(self):
        """Prints the content of the retina list"""
        for s in self.retina:
            if (s[0] == self.visual_range): #this really means >=, since sense() func. caps distances
                                            #to visual_range
                print '>'+str(self.visual_range)
            else:       #obstacle detected
                print s
        print '\n'
 
    #this function's job is to place in self.retina the range sensed by each sensor
    def sense(self, list_rect_obstacles):
        n = (self.nr_sensors - 1)/2     #the "natural" sensor range is -n to +n
        granu = r_visual_granularity    #must be at least as large as the wall thickness!!
        for i in range(-n,n+1):         #sense with each of the 2n+1 range sensors
            ang = (self.azi - i*self.visual_angle)*math.pi/180
            for distance in range(granu, self.visual_range+granu, granu):
                x = self.rect.center[0]-distance*math.sin(ang)  #endpoint coordinates
                y = self.rect.center[1]-distance*math.cos(ang)
                nr_collisions = 0
                count = -1          #needed to coordinate the two lists, to extract color after loop
                 
                for ob in list_rect_obstacles:  #use the stripped-down list of rectangles for speed
                    count = count + 1
                    if ob.collidepoint(x,y):
                        nr_collisions = 1
                        break       #breaks out of wall loop
                if nr_collisions:   #non-zero collision
                    break           #breaks out of distance loop
                 
            #distance now has the min. between the visual range and the first collision
            self.retina[i+n][0] = distance
            
            '''
            if nr_collisions:       #nr_collisions is 1 if a collision has occurred
                self.retina[i+n][1] = list_obstacles[count].color #color comes form the larger list
            else:
                self.retina[i+n][1] = pygame.Color(color_of_nothing)
            '''
        #print 'sense -->retina is:\n', self.retina
#        self.printRetina()
        #print list_dist
        merged = list(itertools.chain.from_iterable(self.retina))
#        print merged
        return merged
         
    def draw_rays(self, target_surf):
        n = (self.nr_sensors - 1)/2 #the "natural" sensor range -n to +n
        for i in range(-n,n+1):     #draw the 2n+1 rays of the range sensors
            ang = (self.azi - i*self.visual_angle)*math.pi/180
            x = self.rect.center[0]-self.retina[i+n][0]*math.sin(ang)
            y = self.rect.center[1]-self.retina[i+n][0]*math.cos(ang)
            #use aaline for smoother (but slower) lines
            pygame.draw.line(target_surf, (0,0,0), self.rect.center, (x,y))