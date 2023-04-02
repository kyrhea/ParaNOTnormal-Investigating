import pygame, sys

from sprites import *
from config import *

from pygame.locals import *


class Game:
    def __init__(self):
        pygame.init()
        self.state = 'intro'
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.screen = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)

        self.fullscreen = False
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('./img/pixel_font.ttf', 32)
        self.running = True

        self.intro_background = pygame.image.load('./img/start_para.png')
        self.intro_background = pygame.transform.scale(self.intro_background, (win_width, win_height))


    def fade(self, width, height): 
        fade = pygame.Surface((width, height))
        fade.fill((0,0,0))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            self.draw()
            self.screen.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(5)






    def createTilemap(self):
        #loop through tilemap
        #enumerate gets position and content of item
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "D":
                    Door(self, j, i)
                if column == "C":
                    Cat(self,j,i)
                    
    def createTilemap2(self):
        #loop through tilemap
        #enumerate gets position and content of item
        for i, row in enumerate(tilemap2):
            for j, column in enumerate(row):
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "D":
                    Door(self, j, i)
            
    



    def newGame(self):
        #new game starts
        self.playing = True #if player dies or quits

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.ghost = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.door = pygame.sprite.LayeredUpdates()
        self.mainDoor = pygame.sprite.LayeredUpdates()
        self.cat = pygame.sprite.LayeredUpdates()

        self.createTilemap()




    def newGame2(self):
        #new game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.ghost = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.door = pygame.sprite.LayeredUpdates()

        self.createTilemap2()

    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == VIDEORESIZE:
                if not self.fullscreen:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == KEYDOWN:
                if event.key == K_f:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()), pygame.RESIZABLE)
                            
    def update(self):
        #game loop updates
        self.all_sprites.update()
    
    def draw(self):
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        self.clock.tick(fps)
        pygame.display.update()
        
                


    def main(self):
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
##            mouse_pos = pygame.mouse.get_pos()
##            mouse_pressed = pygame.mouse.get_pressed()
##            if mainDoor.is_pressed(mouse_pos, mouse_pressed):
##                self.fade(1000,800)
##                self.state = 'main2'
##            for event in pygame.event.get():
##                if event.type == pygame.MOUSEBUTTONDOWN and pygame.sprite.spritecollide(self.player, self.mainDoor, False):
##                    self.fade()
##                    self.state = 'main2'
      


            
                   
            pygame.display.update()
            
        self.running = False

    def gameOver(self):
        pass
    
    def main2(self):
        newGame2(self)
        
        while self.playing:
            self.events()
            self.update()
            self.draw()
            
            
        self.running = False
        
 
        
    
    def startScreen(self):
        intro = True

        #title = self.font.render('ParaNOTnormal Investigating', True, white)
        #title_rect = title.get_rect(x=10,y=10)

        play_button = Button(280, 310, 150, 80, white, dark_blue, 'PLAY', 50)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.state = 'main'

            self.screen.blit(self.intro_background, (0,0))
            #self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(fps)
            pygame.display.update()
            
    def state_manager(self):
        if self.state == 'intro':
            self.startScreen()
        if self.state == 'main':
            self.main()
        if self.state == 'main2':
            self.main2()
        

g = Game()
g.startScreen()
g.newGame()
while g.running:
    g.state_manager()
    g.gameOver()

pygame.quit()
sys.exit()
