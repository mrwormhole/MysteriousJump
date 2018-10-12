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
        self.player = Player(GREEN)
        self.all_sprites.add(self.player)
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

    def update(self):
        self.all_sprites.update()

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
