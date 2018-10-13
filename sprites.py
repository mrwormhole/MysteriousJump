import pygame as pg
from settings import *
vec = pg.math.Vector2 #for additional movement

class Player(pg.sprite.Sprite):
    def __init__(self,size,color):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pg.Surface((self.size,self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH /2 , HEIGHT /2)
        #self.velocityX = 0 #for additional movement
        #self.velocityY = 0 #for additional movement
        self.pos = vec(WIDTH /2, HEIGHT/2) #for additional movement
        self.vel = vec(0,0) #for additional movement
        self.acc = vec(0,0) #for additional movement

    def jump(self):
        self.vel.y = PLAYER_JUMP_SPEED

    def update(self):
        #self.velocityX = 0 #for additional movement
        #self.velocityY = 0 #for additional movement
        self.acc = vec(0,PLAYER_GRAVITY) #for additional movement
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            #self.velocityX = -5 #for additional movement
            self.acc.x = -PLAYER_ACCELERATION #for additional movement
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            #self.velocityX = 5 #for additional movement
            self.acc.x = PLAYER_ACCELERATION #for additional movement
        if keys[pg.K_UP] or keys[pg.K_w]:
            #self.velocityY = -5 #for additional movement
            self.acc.y = -PLAYER_ACCELERATION #for additional movement
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            #self.velocityY = 5 #for additional movement
            self.acc.y = PLAYER_ACCELERATION #for additional movement

        #self.rect.x += self.velocityX #for additional movement
        #self.rect.y += self.velocityY #for additional movement
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc #for additional movement. Notice that it is missing time from physics
        self.pos += self.vel + 0.5 * self.acc #for additional movement Notice that it is missing time from physics

        if self.pos.x - self.size/2 > WIDTH:
            self.pos.x = 0 - self.size/2
        if self.pos.x + self.size < 0:
            self.pos.x = WIDTH + self.size/2

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width,height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
