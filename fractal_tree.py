import pygame
import math

BEND_FACTOR = 20
LENGTH_REDUCE_FACTOR = 0.75
THICKNESS_REDUCTION_FACTOR=0

COLOR_FACTOR_R = 3
COLOR_FACTOR_G = -5
COLOR_FACTOR_B = 1



pygame.init()

display = pygame.display.set_mode((800,600))
pygame.display.set_caption("fractal tree")
clock = pygame.time.Clock()

crashed = False

BLACK = (0,0,0)
WHITE = (255,255,255)

def draw_line(base,R,G,B,length,angle,width):
    if(R<0):
        R = 0
    if(G<0):
        G = 0
    if(B<0):
        B = 0
    if(width<=0):
        width = 1
    final_point = (base[0]+length*math.sin(math.radians(angle)),base[1]-length*math.cos(math.radians(angle)))
    pygame.draw.line(display,(R,G,B),base,final_point,int(width))
    
    if(length>12):
        draw_line(final_point,R-COLOR_FACTOR_R,G-COLOR_FACTOR_G,B-COLOR_FACTOR_B,length*LENGTH_REDUCE_FACTOR,BEND_FACTOR+angle,width-THICKNESS_REDUCTION_FACTOR)
        draw_line(final_point,R-COLOR_FACTOR_R,G-COLOR_FACTOR_G,B-COLOR_FACTOR_B,length*LENGTH_REDUCE_FACTOR,-BEND_FACTOR+angle,width-THICKNESS_REDUCTION_FACTOR)
    

class slider:
    def __init__(self):
        self.x= 150
    def draw(self):
        if(self.x>350):
            self.x = 350
        elif(self.x<50):
            self.x = 50
        pygame.draw.rect(display,(255,0,0),(50,50,300,3))
        pygame.draw.circle(display,(0,0,255),(self.x,49),10)
    def get_val(self):
        return ((self.x-50)/300.0)*150

flag = False
sl_obj = slider()



while not crashed:

    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if( math.sqrt( (sl_obj.x-x)**2 + (50-y)**2 ) <12 ):
                flag = True
        elif event.type == pygame.MOUSEBUTTONUP:
            flag = False
        if flag:
                x, y = pygame.mouse.get_pos()
                sl_obj.x = x

        if event.type == pygame.QUIT:
            crashed = True
        


    display.fill(BLACK)
    
    draw_line((400,600),83,53,10,int(sl_obj.get_val()),0,2)
    sl_obj.draw()
    pygame.display.update()
    clock.tick(20)

pygame.quit()
quit()