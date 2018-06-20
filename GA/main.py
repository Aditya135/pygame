import pygame

pygame.init()
display_size = (800,700)
display = pygame.display.set_mode(display_size)
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)

GRAVITY = 0.1

floor_height = 50

class Floor:
    def __init__(self,height):
        self.height = height
        self.color = RED
        self.x = 0
        self.y = display_size[1]-self.height
        self.width = display_size[0]
    def blit(self):
        pygame.draw.rect(display,self.color,(self.x,self.y,self.width,self.height))

floor = Floor(100)

class Body(pygame.sprite.Sprite):
        def __init__(self,color,width,height):
            pygame.sprite.Sprite.__init__(self)  

            self.image = pygame.Surface([width,height])
            self.image.fill(color)
            self.vx = 0
            self.vy = 0
            self.ax = 0
            self.ay = GRAVITY
            self.rect = self.image.get_rect()
        def update(self):
            self.vx += self.ax
            self.vy += self.ay
            if self.vx>10:
                self.vx = 10
            if self.vy>10:
                self.vy = 10
            if self.vx<-10:
                self.vx = -10
            if self.vy<-10:
                self.vy = -10
            if self.rect.y+self.rect.height>display_size[1]-floor.height:
                if self.vy>0:
                    self.vy=0
            self.rect.x += self.vx
            self.rect.y += self.vy

obj = Body(BLUE,100,100)
obj.rect.x = 0
obj.rect.y = 0
obj.ax = 0

all_sprites = pygame.sprite.Group()

all_sprites.add(obj)

gameloop = True

while gameloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameloop = False
    display.fill(WHITE)

    all_sprites.update()
    all_sprites.draw(display)
    floor.blit()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
exit(0)