#Platformer Game
#@author F.Talha Altınel
import pygame as pg
import random
import os
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.player = Player(30,GREEN) #experimenting giving game class to player
        self.all_sprites.add(self.player)
        
        for platform in PLATFORM_LIST:
            p = Platform(platform[0],platform[1],platform[2],platform[3], platform[4])
            self.all_sprites.add(p)
            self.all_platforms.add(p)

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pass

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing == True:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                hits = pg.sprite.spritecollide(self.player,self.all_platforms,False)
                if event.key == pg.K_SPACE and hits:
                    self.player.jump()

    def update(self):
        self.all_sprites.update()
        #check if player hits a Platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0

    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        pass

    def show_start_screen(self):
        #start start
        pass

    def show_go_screen(self):
        #game over
        pass

game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()

pg.quit()
