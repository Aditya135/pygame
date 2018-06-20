import pygame,random


HEIGHT = 500
WIDTH = 500

SNAKE_SPEED = 1

WHITE = (255,255,255)
BLUE = (0,0,255)
BLACK = (0,0,0)

pygame.init()
display = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("snake!")
clock = pygame.time.Clock()

class Board:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.pixelHeight = HEIGHT/height
        self.pixelWidth = WIDTH/width
        self.blit_pos = []
        self.generate_food()
    def add_blit(self,x,y,color):
        self.blit_pos.append((x,y,color))

    def generate_food(self):
        x, y = random.randint(1,self.width-1), random.randint(1,self.height-1)
        blit_list = [(i[0],i[1]) for i in self.blit_pos ]
        while (x,y) in blit_list:
             x, y = random.randint(1,self.width-1), random.randint(1,self.height-1)
        self.foodx = x
        self.foody = y

    def get_food_coord(self):
        return (self.foodx,self.foody)
    def get_grid_size(self):
        return (self.width,self.height)

    def blit_screen(self):
        self.blit_pos.append((self.foodx,self.foody,BLUE))
        for i in self.blit_pos:
            actx = i[0]*self.pixelWidth
            acty = i[1]*self.pixelHeight
            pygame.draw.rect(display,i[2],(actx+1,acty+1,self.pixelWidth-1,self.pixelHeight-1))
        pygame.display.update()
        self.blit_pos.clear()
brd = Board(50,50)


################################SNAKE##############################
class my_snake:
    def __init__(self):
        self.body = [[5,5]]
        self.total_size = 0
        self.xspeed = SNAKE_SPEED
        self.yspeed = 0
    
    def set_direction(self,keypress):
        if (keypress==pygame.K_DOWN):
            if(self.yspeed!=-SNAKE_SPEED):
                self.xspeed=0
                self.yspeed=SNAKE_SPEED
        elif (keypress==pygame.K_UP):
            if(self.yspeed!=SNAKE_SPEED):
                self.yspeed = -SNAKE_SPEED
                self.xspeed = 0
        elif (keypress==pygame.K_LEFT):
            if(self.xspeed!=SNAKE_SPEED):
                self.yspeed = 0
                self.xspeed = -SNAKE_SPEED
        elif (keypress==pygame.K_RIGHT):
            if(self.xspeed!=-SNAKE_SPEED):
                self.yspeed = 0
                self.xspeed = SNAKE_SPEED
    
    def update(self):

        non_head_body = [(i[0],i[1]) for i in self.body[1:]]
        if((self.body[0][0],self.body[0][1]) in non_head_body or self.body[0][0]>brd.width or self.body[0][1]>brd.height or self.body[0][0]<0 or self.body[0][1]<0):
            print("game over!")
            print("your total Score is: ",self.total_size)
            exit(0)
        

        food_coord = brd.get_food_coord()
        self.need_food=False
        if(self.body[0][0]==food_coord[0] and self.body[0][1]==food_coord[1]):
            self.body.append([1,1])
            self.total_size+=1
            self.need_food = True
        

        for i in range(self.total_size,0,-1):
                self.body[i][0] = self.body[i-1][0]
                self.body[i][1] = self.body[i-1][1]
        
        

        self.body[0][0] +=self.xspeed
        self.body[0][1] +=self.yspeed
        


    def blit(self):
        self.update()
        for x, y in self.body:
            brd.add_blit(int(x),int(y),WHITE)
        if self.need_food:
            brd.generate_food()

snake = my_snake()

running = True
need_food = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
        if event.type==pygame.KEYDOWN:
            snake.set_direction(event.key)
    display.fill(BLACK)
    snake.blit()
    brd.blit_screen()
    clock.tick(15)

pygame.quit()
quit()