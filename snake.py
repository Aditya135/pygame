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
        while (x,y) in [(i[0],i[1]) for i in self.blit_pos ]:
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

class my_snake:
    def __init__(self):
        #self.body = [[random.randint(1,brd.get_grid_size()[0]),random.randint(1,brd.get_grid_size()[1])]]
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

        if(((self.body[0][0]-brd.get_food_coord()[0])**2+(self.body[0][1]-brd.get_food_coord()[1])**2)**(0.5)<1):
            self.body.append([self.body[0][0],self.body[0][1]])
            self.total_size+=1
            brd.generate_food()

        for i in range(self.total_size,0,-1):
                self.body[i][0] = self.body[i-1][0]
                self.body[i][1] = self.body[i-1][1]
            
        self.body[0][0] +=self.xspeed
        self.body[0][1] +=self.yspeed
        


    def blit(self):
        self.update()
        # brd.add_blit(self.headx,self.heady,WHITE)
        for x, y in self.body:
            brd.add_blit(int(x),int(y),WHITE)
snake = my_snake()

running = True

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