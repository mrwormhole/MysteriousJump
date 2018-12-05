# Platformer Game
# @author F.Talha Altınel
import pygame as pg
import random
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)
        self.running = True
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir , 'img' )
        self.sound_dir = path.join(self.dir, 'sound')
        with open(path.join(self.dir, HIGHSCORE_FILE), 'r+') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
                print("console error")
            # f.close()
        self.spritesheet = Spritesheet(path.join(self.img_dir,SPRITESHEET))
        self.jump_sound = pg.mixer.Sound(path.join(self.sound_dir,JUMP_SOUND))

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.player = Player(self.spritesheet,self)
        self.score = 0


        for platform in PLATFORM_LIST:
            Platform(self,platform[0],platform[1], path.join(self.img_dir,GRASS_TILE),path.join(self.img_dir,STONE_TILE),self.player.now)

        pg.mixer.music.load(path.join(self.sound_dir, THEME_MUSIC))
        self.run()

    def run(self):
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.stop()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing == True:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                hits = pg.sprite.spritecollide(self.player,self.all_platforms,False)
                if hits:
                    self.player.walking = True
                    self.player.jumping = False
                if event.key == pg.K_SPACE and hits:
                    self.player.jump()
                    self.jump_sound.play()
                    self.player.walking = False
                    self.player.jumping = True




    def update(self):
        self.all_sprites.update()

        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top + 1
                        self.player.vel.y = 0

        # check if player reaches top 1/4 of the screen
        if self.player.rect.top <= HEIGHT/4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for plat in self.all_platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += random.randrange(10, 20)

        #if player picks a power up
        powerup_hits = pg.sprite.spritecollide(self.player,self.all_powerups, True)
        for powerup_hit in powerup_hits:
            if powerup_hit.type == "boost":
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

        # game over for falling
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y,10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.all_platforms) == 0:
            self.playing = False

        # spawning new platforms
        while len(self.all_platforms) < 7:
            Platform(self,random.randrange(0, WIDTH-random.randrange(50,100)),
                         random.randrange(-75, -30),
                        path.join(self.img_dir,GRASS_TILE),path.join(self.img_dir,STONE_TILE),self.player.now)

    def draw(self):
        self.screen.fill(GREY)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image,self.player.rect)
        self.draw_text(str(self.score), WIDTH/2, 5, 30, YELLOW)
        pg.display.flip()

    def draw_text(self, text, x, y, size, color):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_any_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.sound_dir, MENU_MUSIC))
        pg.mixer.music.play(loops =-1)
        self.screen.fill(GREY)
        self.draw_text(TITLE, WIDTH/2, HEIGHT/4, 48, WHITE)
        self.draw_text("A and D to move, Space to jump", WIDTH/2, HEIGHT/2, 22, WHITE)
        self.draw_text("Press any key to play", WIDTH / 2, HEIGHT * 3 / 4, 22, WHITE)
        self.draw_text("Highscore: " + str(self.highscore), WIDTH / 2, 15, 22, BLACK)
        pg.display.flip()
        self.wait_for_any_key()

    def show_game_over_screen(self):
        if not self.running:
            return # bug fix for closing game
        self.screen.fill(GREY)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGHSCORE!", WIDTH/2, HEIGHT/2 + 40, 22, BLACK)
            with open(path.join(self.dir, HIGHSCORE_FILE), 'r+') as f:
                f.write(str(self.highscore))
        else:
            self.draw_text("Highscore: " + str(self.highscore), WIDTH / 2, HEIGHT/2 + 40, 22, BLACK)
        self.draw_text("GAME OVER", WIDTH / 2, HEIGHT / 4, 48, WHITE)
        self.draw_text("Score: " + str(self.score), WIDTH / 2, HEIGHT / 2, 22, WHITE)
        self.draw_text("Press any key to play again", WIDTH / 2, HEIGHT * 3 / 4, 22, WHITE)
        pg.display.flip()
        self.wait_for_any_key()


game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_game_over_screen()

pg.quit()
