import pygame as pg
from settings import *
vector2 = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self,size,color):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pg.Surface((self.size,self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH /2 , HEIGHT /2)
        self.pos = vector2(WIDTH /2, HEIGHT/2)
        self.vel = vector2(0,0)
        self.acc = vector2(0,0)

    def jump(self):
        #observed a minor bug about jumping it is mostly related with collision detection.
        #set jump speed to 15 and acceleration to 0.25 to see that bug on first platform
        self.vel.y -= PLAYER_JUMP_SPEED

    def update(self):
        print(self.pos)
        self.acc = vector2(0,PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACCELERATION
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACCELERATION
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.acc.y = -PLAYER_ACCELERATION
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.acc.y = PLAYER_ACCELERATION

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
