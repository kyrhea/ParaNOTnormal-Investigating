import pygame, sys

from sprites import *
from config import *

from pygame.locals import *


class Game:
    def __init__(self):
        pygame.init()
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.screen = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)

        self.fullscreen = False
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('slkscr.ttf', 32)
        self.running = True

        self.intro_background = pygame.image.load('./img/phas.png')
        self.intro_background = pygame.transform.scale(self.intro_background, (win_width, win_height))

    def newGame(self):
        #new game starts
        self.playing = True #if player dies or quits

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.ghost = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.player = Player(self, 1, 2)

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
        self.running = False

    def gameOver(self):
        pass
    
    def startScreen(self):
        intro = True

        title = self.font.render('ParaNOTnormal Investigating', True, white)
        title_rect = title.get_rect(x=10,y=10)

        play_button = Button(10, 50, 100, 50, white, black, 'PLAY', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(fps)
            pygame.display.update()

g = Game()
g.startScreen()
g.newGame()
while g.running:
    g.main()
    g.gameOver()

pygame.quit()
sys.exit()

