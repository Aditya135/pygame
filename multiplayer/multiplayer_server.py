import pygame,random,json,time
from networking import communicate
from threading import Thread

PLAYER2_IP = '127.0.0.1'
NAME = "Aditya"



HEIGHT = 500
WIDTH = 500
WHITE = (255,255,255)
BLUE = (0,0,255)

class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.height = 70
        self.width = 10
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.is_alive = True
    def update(self):
        x, y = pygame.mouse.get_pos()
        self.rect.y = y

class Ball(pygame.sprite.Sprite):
    def __init__(self,WIDTH,HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        super().__init__()
        self.vx = random.randint(5,10)
        self.vy = random.randint(3,6)
        self.image = pygame.Surface([10,10])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/2
        self.rect.y = HEIGHT/2
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.y>self.HEIGHT or self.rect.y<0:
            self.vy = -self.vy


player1 = Player1() 
ball = Ball(WIDTH,HEIGHT)

class Player2(pygame.sprite.Sprite):
    def __init__(self,ip_address,name):
        self.ip_address = ip_address
        self.com = communicate((ip_address,12346),name,12345)
        super().__init__()
        self.height=70
        self.width = 10
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH-self.width
        self.rect.y = 100
        self.is_alive = True
        self.data=dict()

        #initialize network
        if self.com.wait_connection():
            print("connected to palyer 2",self.com.get_connection_status()[0])
        else :
            self.com.closeconnection()
            print("unable to connect")


    def handle_server(self):
        running = True
        while running:
            if not self.com.is_connected:
                running = False
                print("out of network thread")
            if self.com.is_connected:

                self.data['y'] = player1.rect.y
                self.data['ball'] = (ball.rect.x,ball.rect.y)
                self.data['p1_alive']=player1.is_alive
                self.data['p2_alive']=self.is_alive
                json_string = json.dumps(self.data)
                self.com.send_data(json_string)


                self.data = self.com.get_data()
                if not self.data=='terminate':
                    self.data = json.loads(self.data)
                    self.rect.y = self.data['y']
            

    def start_network_thread(self):
        thread = Thread(target=self.handle_server)
        thread.start()
        print("started network thread")


player2 = Player2(PLAYER2_IP,NAME)

BLACK = (0,0,0)

pygame.init()
display = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("ping pong server!")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(ball)

running =True
time.sleep(4)
player2.start_network_thread()

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
        
    if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(player2.rect):
        ball.vx=  - ball.vx
    if ball.rect.x<0:
        player1.is_alive = False
    if ball.rect.x>WIDTH:
        player2.is_alive = False
        

    display.fill(BLACK)    
    all_sprites.update()
    
    all_sprites.draw(display)
    pygame.display.flip()
    clock.tick(30)

    if not player1.is_alive:
        print("player 1 looses the game")
        running = False
    elif not player2.is_alive:
        print("player 2 looses the game")
        running = False

player2.com.closeconnection()
pygame.quit()
quit()