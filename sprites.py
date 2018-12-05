import pygame as pg
from settings import *
vector2 = pg.math.Vector2
import random
from os import path


class Spritesheet:
    def __init__(self,filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self,x,y,width,height):
        image = pg.Surface((width,height),pg.SRCALPHA,32)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image,(55,52))
        return image

    def fill_animation_sprites(self):
        self.all_sprites = [0,0,0,0,0,0,0,0,0,0,0,0]
        m = 0 # 0 to 5 are walking left anims, 6 to 11 are walking right anims.
        for y in range(0,1678,559):
            for x in range(0,1061,530):
                self.all_sprites[m] = self.get_image(x,y,529,558)
                m += 1


class Player(pg.sprite.Sprite):
    def __init__(self,spritesheet,game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.spritesheet = spritesheet
        self.spritesheet.fill_animation_sprites()
        self.walking = False
        self.jumping = False
        self.standing_frame = 0
        self.current_frame = 0
        self.last_update = 0
        self.image = self.spritesheet.all_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH /2, HEIGHT /2)
        self.pos = vector2(WIDTH /2, HEIGHT/2)
        self.vel = vector2(0, 0)
        self.acc = vector2(0, 0)
        self.now = 0

    def jump(self):
        self.vel.y -= PLAYER_JUMP_SPEED

    def update(self):
        self.acc = vector2(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        self.animate()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACCELERATION
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACCELERATION
        '''if keys[pg.K_UP] or keys[pg.K_w]:
            self.acc.y = -PLAYER_ACCELERATION
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.acc.y = PLAYER_ACCELERATION'''

        self.acc.x += self.vel.x * PLAYER_FRICTION # F = k . N notice we dont use the mass of player here.Because we don't want too much reality
        self.vel += self.acc # v = at
        self.pos += self.vel + 0.5 * self.acc # x = vt + 1/2att

        if self.pos.x - self.rect.width/2 > WIDTH:
            self.pos.x = 0 - self.rect.width/2
        if self.pos.x + self.rect.width < 0:
            self.pos.x = WIDTH + self.rect.width/2

        self.rect.midbottom = self.pos

    def animate(self):
        self.now = pg.time.get_ticks()

        if abs(self.vel.x) < 0.5:
            self.vel.x = 0
            self.walking = False
        if self.vel.x != 0:
            self.walking = True

        if self.walking:
            if self.now - self.last_update > 120:
                self.last_update = self.now
                self.current_frame = (self.current_frame + 1) % 6
                if self.vel.x > 0:
                    # walking right
                    self.standing_frame = 6
                    self.image = self.spritesheet.all_sprites[self.current_frame + 6]
                else:
                    # walking left
                    self.standing_frame = 0
                    self.image = self.spritesheet.all_sprites[self.current_frame]
        if not self.jumping and not self.walking:
            self.image = self.spritesheet.all_sprites[self.standing_frame]


class Platform(pg.sprite.Sprite):
    def __init__(self, game,x, y, filename1,filename2,time):
        self.groups = game.all_sprites, game.all_platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        print("Time: " + str(time))
        self.game = game
        self.platforms_images = [pg.image.load(filename1).convert_alpha(),pg.image.load(filename2).convert_alpha()]
        self.image = self.platforms_images[random.randint(0, 1)]
        self.xList = [75,100,125,150]
        self.yList = [40,45,50]
        self.image = pg.transform.scale(self.image, (self.xList[random.randint(0, 3)], self.yList[random.randint(0, 2)]))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if random.randrange(100) < 10:
            self.powerup = PowerUp(self.game,self)


class PowerUp(pg.sprite.Sprite):
    def __init__(self,game,platform):
        self.groups = game.all_sprites, game.all_powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.platform = platform
        self.type = "boost"
        self.image = pg.transform.scale(pg.image.load(path.join(self.game.img_dir,"powerup.png")),(40,40))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.platform.rect.centerx
        self.rect.bottom = self.platform.rect.top - 5

    def update(self):
        self.rect.bottom = self.platform.rect.top - 5
        if not self.game.all_platforms.has(self.platform):
            self.kill()

