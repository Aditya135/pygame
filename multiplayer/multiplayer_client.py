import pygame,json
from networking import communicate
from threading import Thread

PLAYER1_IP = '127.0.0.1'
NAME = 'XYZ'



HEIGHT = 500
WIDTH = 500
WHITE = (255,255,255)
BLUE = (0,0,255)



class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.height = 70
        self.width = 10
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH-self.width
        self.rect.y = 100
        self.is_alive = True
    def update(self):
        x, y = pygame.mouse.get_pos()
        self.rect.y = y

class Ball(pygame.sprite.Sprite):
    def __init__(self,WIDTH,HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        super().__init__()
        self.image = pygame.Surface([10,10])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/2
        self.rect.y = HEIGHT/2


player2 = Player2() 
ball = Ball(WIDTH,HEIGHT)

class Player1(pygame.sprite.Sprite):
    def __init__(self,ip_address,name):
        self.ip_address = ip_address
        self.com = communicate((ip_address,12345),name,12346)
        super().__init__()
        self.height=70
        self.width = 10
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 100
        self.is_alive = True
        self.data = dict()

        self.com.createConnection()
        if self.com.is_connected:
            print("connected to player 1",self.com.get_connection_status()[0])
        else:
            self.com.closeconnection()
            print("unable to connect")
    def handle_client(self):
        running = True

        while running:
            if not self.com.is_connected:
                print("out of network thread")
                running = False
            if self.com.is_connected:

                json_string = self.com.get_data()
                self.data = json.loads(json_string)
                self.rect.y = self.data['y']
                ball.rect.x,ball.rect.y = self.data['ball']
                self.is_alive = self.data['p1_alive']
                player2.is_alive = self.data['p2_alive']
                
                self.data = dict()
                self.data['y'] = player2.rect.y
                json_string = json.dumps(self.data)
                self.com.send_data(json_string)
            
    def start_network_thread(self):
        thread = Thread(target=self.handle_client)
        print("starting network thread")
        thread.start()

player1 = Player1(PLAYER1_IP,NAME)
BLACK = (0,0,0)

pygame.init()
display = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("ping pong client!")
clock = pygame.time.Clock()






all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(ball)

running =True
player1.start_network_thread()
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False        

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

player1.com.closeconnection()
pygame.quit()
quit()